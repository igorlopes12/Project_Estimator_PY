import flet as ft
from core.project_manager import ProjectManager
from ui.main_view import main_view
from dotenv import load_dotenv
import os

load_dotenv()
PROJECTS_PATH = os.getenv("PROJECTS_PATH", "data/projects.json")

def main(page: ft.Page):
    manager = ProjectManager(PROJECTS_PATH)
    main_view(page, manager)

ft.app(target=main)
