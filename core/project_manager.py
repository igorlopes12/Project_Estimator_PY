"""core/project_manager.py

Simple JSON-backed project manager with file safety and logging.
Provides load and save operations for a list of projects stored as JSON.
"""

import json
import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)
lock = Lock()


class ProjectManager:
    """Project manager that persists a list of projects to a JSON file.

    The manager ensures the parent directory and file exist on initialization.
    Thread-safe save operations are guarded with a mutex.
    """

    def __init__(self, path):
        """
        Initialize the manager with a path to a JSON file.

        Args:
            path: Path to a JSON file used to store the projects (network or local).
        """
        self.path = Path(path)
        self._ensure_directory()
        self._ensure_file_exists()

    def _ensure_directory(self):
        """Ensure the parent directory of the JSON file exists."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating directory {self.path.parent}: {e}")
            raise

    def _ensure_file_exists(self):
        """Ensure the JSON file exists; create an empty list file if missing."""
        try:
            if not self.path.exists():
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False)
                logger.info(f"File created: {self.path}")
        except Exception as e:
            logger.error(f"Error creating file {self.path}: {e}")
            raise

    def load_projects(self):
        """
        Load projects from the JSON file.

        Returns:
            A list of project dictionaries. Returns an empty list on error.
            Handles the case where the file contains a dict instead of a list.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                projects = json.load(f)

                # Handle case where file contains a dict instead of a list
                if isinstance(projects, dict):
                    logger.warning(f"Projects file contains dict instead of list. Converting to list.")
                    # If it's a dict, try to extract 'projects' key or return empty list
                    if "projects" in projects:
                        projects = projects["projects"]
                    else:
                        projects = []

                logger.debug(f"Projects loaded from {self.path}: {len(projects)} items")
                return projects
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading projects from {self.path}: {e}")
            return []

    def save_projects(self, projects):
        """
        Save the projects list to the JSON file in a thread-safe manner.

        Args:
            projects: A list of project dictionaries to save.
        """
        with lock:
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(projects, f, indent=4, ensure_ascii=False)
                logger.debug(f"Projects saved to {self.path}: {len(projects)} items")
            except Exception as e:
                logger.error(f"Error saving projects to {self.path}: {e}")
                raise

    def export_project_to_json(self):
        """
        Export the currently loaded project to JSON format for external use (e.g., DevOps upload).
        This method returns the first project if multiple projects are loaded.

        Returns:
            A dictionary with project data suitable for DevOps export.
        """
        try:
            projects = self.load_projects()
            if not projects:
                raise ValueError("No projects found to export")
            
            # Return the first project (or you could modify this logic to pick a specific one)
            project = projects[0]
            
            logger.debug(f"Exporting project: {project.get('name', 'Unknown')}")
            return project
        except Exception as e:
            logger.error(f"Error exporting project to JSON: {e}")
            raise
