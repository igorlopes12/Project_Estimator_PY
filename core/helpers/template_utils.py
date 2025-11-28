"""core/helpers/template_utils.py

Helpers to manage templates using the ProjectManager abstraction.
This module wraps a ProjectManager instance dedicated to templates and provides
simple load/save convenience functions.
"""

from core.config import TEMPLATES_PATH
from core.project_manager import ProjectManager

_template_manager = ProjectManager(str(TEMPLATES_PATH))


def get_template_manager() -> ProjectManager:
    """Return the template ProjectManager instance."""
    return _template_manager


def set_template_manager(manager: ProjectManager) -> None:
    """Replace the default template manager (used for tests or swapping storage)."""
    global _template_manager
    _template_manager = manager


def _ensure_manager(manager: ProjectManager | None) -> ProjectManager:
    return manager or _template_manager


def load_templates(manager: ProjectManager | None = None):
    """Load templates using the provided manager or the default one.

    Returns an empty list on error.
    """
    mgr = _ensure_manager(manager)
    try:
        return mgr.load_projects()
    except Exception:
        return []


def save_templates(tpls, manager: ProjectManager | None = None):
    """Save templates using the provided manager or the default one."""
    mgr = _ensure_manager(manager)
    try:
        mgr.save_projects(tpls)
    except Exception as exc:
        print(f"Error saving templates: {exc}")
