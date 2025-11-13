import flet as ft
from core.project_manager import ProjectManager
from dotenv import load_dotenv
import os

load_dotenv()
PROJECTS_PATH = os.path.join(os.path.dirname(__file__), "data", "projects.json")

from ui.main_view import main_view


def main(page: ft.Page):
    page.title = "Project Estimator"
    page.padding = 0
    page.spacing = 0
    page.scroll = None  # Remove scroll da página inteira
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800  # Define largura mínima
    page.window.min_height = 600

    manager = ProjectManager(PROJECTS_PATH)
    main_view(page, manager)


ft.app(target=main)
