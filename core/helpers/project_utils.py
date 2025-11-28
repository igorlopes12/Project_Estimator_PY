"""core/helpers/project_utils.py

Convenience wrappers around the global ProjectManager instance used by the app.
Provides getter/setter and load/save helper functions.
"""

from core.config import PROJECTS_PATH
from core.project_manager import ProjectManager

_project_manager = ProjectManager(str(PROJECTS_PATH))


def get_project_manager() -> ProjectManager:
    """Return the singleton ProjectManager instance used by the application."""
    return _project_manager


def set_project_manager(manager: ProjectManager) -> None:
    """Replace the global ProjectManager instance (useful for testing)."""
    global _project_manager
    _project_manager = manager


def _ensure_manager(manager: ProjectManager | None) -> ProjectManager:
    """Return the provided manager or the global default."""
    return manager or _project_manager


def load_projects(manager: ProjectManager | None = None):
    """Load all projects from storage via the manager.

    Returns an empty list on error.
    """
    mgr = _ensure_manager(manager)
    try:
        return mgr.load_projects()
    except Exception as e:
        print(f"Error loading projects: {e}")
        return []


def save_projects(projects, manager: ProjectManager | None = None):
    """Save the given projects list using the manager."""
    mgr = _ensure_manager(manager)
    try:
        mgr.save_projects(projects)
    except Exception as exc:
        print(f"Error saving projects: {exc}")
