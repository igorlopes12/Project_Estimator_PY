from core.config import PROJECTS_PATH
from core.project_manager import ProjectManager

_project_manager = ProjectManager(str(PROJECTS_PATH))


def get_project_manager() -> ProjectManager:
    """Retorna a instância do gerenciador de projects."""
    return _project_manager


def set_project_manager(manager: ProjectManager) -> None:
    """Define uma nova instância do gerenciador de projects."""
    global _project_manager
    _project_manager = manager


def _ensure_manager(manager: ProjectManager | None) -> ProjectManager:
    """Garante que um gerenciador é retornado."""
    return manager or _project_manager


def load_projects(manager: ProjectManager | None = None):
    """Carrega todos os projects do armazenamento."""
    mgr = _ensure_manager(manager)
    try:
        return mgr.load_projects()
    except Exception as e:
        print(f"Erro ao carregar projects: {e}")
        return []


def save_projects(projects, manager: ProjectManager | None = None):
    """Salva os projects no armazenamento."""
    mgr = _ensure_manager(manager)
    try:
        mgr.save_projects(projects)
    except Exception as exc:
        print(f"Erro ao salvar projects: {exc}")

