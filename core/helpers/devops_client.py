import base64
import requests


class DevOpsClient:
    def __init__(self, organization, project, pat):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.auth = base64.b64encode(f":{pat}".encode()).decode()

    # ---------------------------
    # CREATE WORK ITEM
    # ---------------------------
    def create_work_item(self, w_type, fields, parent_id=None):
        """Cria um work item no Azure DevOps."""
        url = (
            f"https://dev.azure.com/{self.organization}/{self.project}"
            f"/_apis/wit/workitems/${w_type}?api-version=7.0"
        )

        ops = [
            {"op": "add", "path": f"/fields/{key}", "value": value}
            for key, value in fields.items()
        ]

        if parent_id:
            ops.append({
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitems/{parent_id}"
                }
            })

        response = requests.patch(
            url,
            json=ops,
            headers={
                "Content-Type": "application/json-patch+json",
                "Authorization": f"Basic {self.auth}",
            },
        )

        if response.status_code >= 400:
            print("❌ DevOps error:", response.text)

        response.raise_for_status()
        return response.json()

    # ------------------------------------
    # CREATE STRUCTURE FROM UI JSON
    # ------------------------------------
    def criar_estrutura_desde_json(self, data):
        area_path = f"{self.project}\\Digital Delivery Team"
        iteration_path = f"{self.project}\\{self.project}"

        # 🔒 Epic sempre automático
        epic_title = f"{data['demand']} - {data['name']}"
        epic = self.create_work_item(
            "Epic",
            {
                "System.Title": epic_title,
                "System.AreaPath": area_path,
                "System.IterationPath": iteration_path
            }
        )

        print(f"✅ Epic criada: #{epic['id']} - {epic_title}")

        created = {}  # nome -> id

        def create_item(step, parent_id):
            fields = {
                "System.Title": step["name"],
                "System.AreaPath": area_path,
                "System.IterationPath": iteration_path,
            }

            if step["type"] == "Task":
                fields["Microsoft.VSTS.Scheduling.OriginalEstimate"] = float(step.get("hours", 0))

            wi = self.create_work_item(step["type"], fields, parent_id)
            created[step["name"]] = wi["id"]

            print(f"✅ {step['type']} criada: #{wi['id']} - {step['name']}")

        # 1️⃣ FEATURES → EPIC
        for step in data["steps"]:
            if step["type"] == "Feature":
                create_item(step, epic["id"])

        # 2️⃣ USER STORIES → FEATURE
        for step in data["steps"]:
            if step["type"] == "User Story":
                parent_name = step.get("parent")
                parent_id = created.get(parent_name)

                if not parent_id:
                    raise ValueError(f"User Story '{step['name']}' sem Feature pai válida")

                create_item(step, parent_id)

        # 3️⃣ TASKS → USER STORY
        for step in data["steps"]:
            if step["type"] == "Task":
                parent_name = step.get("parent")
                parent_id = created.get(parent_name)

                if not parent_id:
                    raise ValueError(f"Task '{step['name']}' sem User Story pai válida")

                create_item(step, parent_id)

        return {
            "epic": epic["id"],
            "items": created
        }
