"""core/helpers/ui_utils.py

Utility functions for UI operations in Flet.
"""
import flet as ft


def show_snackbar(page: ft.Page, message: str, bg_color: str = ft.Colors.BLUE, duration_ms: int = 3000):
    """Show a snackbar notification.
    
    Args:
        page: Flet Page instance where the snackbar will be displayed
        message: The message to display
        bg_color: Background color (default: BLUE)
        duration_ms: Duration in milliseconds before auto-close (default: 3000ms)
    """
    snack = ft.SnackBar(
        content=ft.Text(message, color=ft.Colors.WHITE),
        bgcolor=bg_color,
        duration=duration_ms
    )
    page.overlay.append(snack)
    snack.open = True
    page.update()
