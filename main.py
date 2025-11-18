import flet as ft
from dotenv import load_dotenv
from core.helpers.project_utils import get_project_manager
from ui.main_view import main_view

load_dotenv()


def main(page: ft.Page):
    page.title = "Project Estimator"
    page.padding = 0
    page.spacing = 0
    page.scroll = None  # Remove scroll da página inteira
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800  # Define largura mínima
    page.window.min_height = 600

    # Obtém o gerenciador de projects configurado para usar a pasta de rede
    manager = get_project_manager()
    main_view(page, manager)


ft.app(target=main)
