import json, os
from threading import Lock

lock = Lock()

class ProjectManager:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def load_projects(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_projects(self, projects):
        with lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(projects, f, indent=4, ensure_ascii=False)
