import base64
import requests

class DevOpsClient:
    def __init__(self, organization, project, pat):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.auth = base64.b64encode(f":{pat}".encode()).decode()

    # ---------------------------
    # METODO QUE CHAMA A API REAL
    # ---------------------------
    def create_work_item(self, w_type, fields, parent_id=None):
        url = (
            f"https://dev.azure.com/{self.organization}/{self.project}"
            f"/_apis/wit/workitems/${w_type}?api-version=7.0"
        )

        ops = [
            {"op": "add", "path": f"/fields/{key}", "value": value}
            for key, value in fields.items()
        ]

        # Add parent relationship if provided
        if parent_id:
            ops.append({
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitems/{parent_id}"
                }
            })

        print("\n🔗 Chamando API:", url)
        print("📦 Payload:", ops)

        response = requests.patch(
            url,
            json=ops,
            headers={
                "Content-Type": "application/json-patch+json",
                "Authorization": f"Basic {self.auth}",
            },
        )

        if response.status_code >= 400:
            print("❌ Erro DevOps:", response.text)

        response.raise_for_status()

        return response.json()

    # ------------------------------------
    # METODO QUE CRIA TUDO A PARTIR DO JSON
    # ------------------------------------
    def criar_estrutura_desde_json(self, data):
        # Epic = demand + name
        epic_title = f"{data['demand']} - {data['name']}"
        area = data.get('area', '')

        # 1️⃣ Criar Epic with Area Path and Iteration
        # Area Path: Use the exact path from DevOps (Project Name\Team Name)
        area_path = f"{self.project}\\Digital Delivery Team"
        
        # Iteration Path format: "Project Name\Project Name"
        iteration_path = f"{self.project}\\{self.project}"
        
        epic_fields = {
            "System.Title": epic_title,
            "System.AreaPath": area_path,
            "System.IterationPath": iteration_path
        }
        
        epic = self.create_work_item("Epic", epic_fields, parent_id=None)
        print(f"✅ Epic criada: #{epic['id']} - {epic_title}")
        print(f"   Area Path: {area_path}")
        print(f"   Iteration Path: {iteration_path}")

        # 2️⃣ Criar Feature under Epic
        feature_fields = {
            "System.Title": data['name'],
            "System.AreaPath": area_path,
            "System.IterationPath": iteration_path
        }

        feature = self.create_work_item("Feature", feature_fields, parent_id=epic["id"])
        print(f"✅ Feature criada: #{feature['id']} - {data['name']} (parent: #{epic['id']})")

        # 3️⃣ Criar User Story "Development" under Feature
        story_fields = {
            "System.Title": "Development",
            "System.AreaPath": area_path,
            "System.IterationPath": iteration_path
        }
        
        story = self.create_work_item("User Story", story_fields, parent_id=feature["id"])
        print(f"✅ User Story criada: #{story['id']} - Development (parent: #{feature['id']})")

        # 4️⃣ Criar Tasks a partir dos steps
        task_ids = []
        for step in data["steps"]:
            task_title = f"{step['name']} ({step['hours']}h)"
            hours = float(step.get('hours', 0))

            task_fields = {
                "System.Title": task_title,
                "System.AreaPath": area_path,
                "System.IterationPath": iteration_path,
                "Microsoft.VSTS.Scheduling.OriginalEstimate": hours
            }

            task = self.create_work_item("Task", task_fields, parent_id=story["id"])
            task_ids.append(task["id"])
            print(f"✅ Task criada: #{task['id']} - {task_title} ({hours}h) (parent: #{story['id']})")

        return {
            "epic": epic["id"],
            "feature": feature["id"],
            "story": story["id"],
            "tasks": task_ids
        }
