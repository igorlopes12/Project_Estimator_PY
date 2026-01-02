"""core/helpers/devops_client.py

Azure DevOps integration client for creating work items and epics.
Provides functionality to upload project data as a structured hierarchy
(Epic -> Features -> User Stories -> Tasks) to Azure DevOps.
"""

import base64
import requests


class DevOpsClient:
    """Client for interacting with Azure DevOps REST API.

    Handles authentication, work item creation, and project structure
    management in Azure DevOps.
    """

    def __init__(self, organization: str, project: str, pat: str):
        """Initialize the DevOps client with organization and authentication details.

        Args:
            organization: Azure DevOps organization name.
            project: Azure DevOps project name.
            pat: Personal Access Token for authentication.
        """
        self.organization = organization
        self.project = project
        self.pat = pat
        self.auth = base64.b64encode(f":{pat}".encode()).decode()

    def create_work_item(self, w_type: str, fields: dict, parent_id: int = None) -> dict:
        """Create a work item in Azure DevOps.

        Args:
            w_type: Work item type (Epic, Feature, User Story, Task, Bug, etc.).
            fields: Dictionary of field names and values for the work item.
            parent_id: Optional ID of the parent work item for linking.

        Returns:
            Dictionary containing the created work item details including ID.

        Raises:
            HTTPError: If the DevOps API returns an error status code.
        """
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

    def create_structure_from_json(self, data: dict) -> dict:
        """Create a hierarchical work item structure in Azure DevOps from project data.

        Creates an Epic at the top level, then creates Features, User Stories, and Tasks
        based on the project steps, establishing proper parent-child relationships.

        Args:
            data: Project data dictionary containing:
                - demand: Demand/requirement ID
                - name: Project name
                - steps: List of step dictionaries with name, type, parent, and hours

        Returns:
            Dictionary containing:
                - epic: ID of the created Epic
                - items: Dictionary mapping step names to their work item IDs

        Raises:
            ValueError: If a User Story or Task references a non-existent parent item.
        """
        area_path = f"{self.project}\\Digital Delivery Team"
        iteration_path = f"{self.project}\\{self.project}"

        # Create Epic automatically
        epic_title = f"{data['demand']} - {data['name']}"
        epic = self.create_work_item(
            "Epic",
            {
                "System.Title": epic_title,
                "System.AreaPath": area_path,
                "System.IterationPath": iteration_path
            }
        )

        print(f"✅ Epic created: #{epic['id']} - {epic_title}")

        created = {}  # name -> id mapping

        def create_item(step, parent_id):
            """Helper to create a work item with the given parent."""
            fields = {
                "System.Title": step["name"],
                "System.AreaPath": area_path,
                "System.IterationPath": iteration_path,
            }

            if step["type"] == "Task":
                fields["Microsoft.VSTS.Scheduling.OriginalEstimate"] = float(step.get("hours", 0))

            wi = self.create_work_item(step["type"], fields, parent_id)
            created[step["name"]] = wi["id"]

            print(f"✅ {step['type']} created: #{wi['id']} - {step['name']}")

        # Step 1: Create Features under Epic
        for step in data["steps"]:
            if step["type"] == "Feature":
                create_item(step, epic["id"])

        # Step 2: Create User Stories under Features
        for step in data["steps"]:
            if step["type"] == "User Story":
                parent_name = step.get("parent")
                parent_id = created.get(parent_name)

                if not parent_id:
                    raise ValueError(f"User Story '{step['name']}' has no valid parent Feature")

                create_item(step, parent_id)

        # Step 3: Create Tasks under User Stories
        for step in data["steps"]:
            if step["type"] == "Task":
                parent_name = step.get("parent")
                parent_id = created.get(parent_name)

                if not parent_id:
                    raise ValueError(f"Task '{step['name']}' has no valid parent User Story")

                create_item(step, parent_id)

        return {
            "epic": epic["id"],
            "items": created
        }

    # Alias for backwards compatibility with Portuguese method name
    def criar_estrutura_desde_json(self, data: dict) -> dict:
        """Portuguese alias for create_structure_from_json for backwards compatibility."""
        return self.create_structure_from_json(data)
