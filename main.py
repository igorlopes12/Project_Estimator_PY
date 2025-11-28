"""main.py

Entry point for the Project Estimator Flet application.
This module sets up the main window and starts the Flet app.
"""

import flet as ft
from dotenv import load_dotenv
from core.helpers.project_utils import get_project_manager
from ui.main_view import main_view

load_dotenv()


def main(page: ft.Page):
    """Initialize the main application page and launch the UI.

    Args:
        page: Flet Page object provided by the Flet runtime.
    """
    page.title = "Project Estimator"
    page.padding = 0
    page.spacing = 0
    page.scroll = None  # Remove scroll for the entire page
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800  # Minimum window width
    page.window.min_height = 600

    # Obtain the project manager configured to use the network folder (or local fallback)
    manager = get_project_manager()
    main_view(page, manager)


if __name__ == "__main__":
    # Start the Flet application when run as a script
    ft.app(target=main)
