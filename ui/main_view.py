"""
Refined Ball Corporation style Project Estimator UI.
Uniform spacing, aligned fields, consistent heights, and corporate color palette.
"""

import flet as ft
from datetime import date
from typing import List, Dict, Any
from core.project_manager import ProjectManager
from core.pdf_generator import generate_pdf

# --- Ball Corporation Official Brand Palette ---
BRAND_BLUE = "#1140FE"      # Primary Blue - CMYK: 93/75/0/0
BRAND_BLACK = "#000000"     # Black - CMYK: 0/0/0/100
BRAND_CHARCOAL = "#1A1A1A"  # Charcoal - CMYK: 0/0/0/90
BRAND_GREY = "#8C8E94"      # Grey - CMYK: 5/4/42
BRAND_WHITE = "#FFFFFF"     # White - CMYK: 0/0/0/0
BRAND_SUCCESS = "#4CAF50"   # Green accent for success messages

# UI Colors
BG_COLOR = "#F5F5F5"        # Light grey background
CARD_BG = BRAND_WHITE       # White cards
TEXT_PRIMARY = BRAND_CHARCOAL  # Dark text
BORDER_COLOR = "#E0E0E0"    # Light borders


def main_view(page: ft.Page, manager: ProjectManager):
    page.title = "Project Estimator"
    page.padding = 40
    page.bgcolor = BG_COLOR
    page.scroll = "adaptive"

    projects: List[Dict[str, Any]] = manager.load_projects() or []

    # File picker to save PDF
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.path:
            generate_pdf_with_path(e.path)
        else:
            show_notification("PDF generation cancelled", "#FF9800", "⚠️")

    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Notification area visible on screen
    notification_container = ft.Container(
        visible=False,
        bgcolor=ft.Colors.BLUE_100,
        border_radius=10,
        padding=20,
        margin=ft.margin.only(bottom=20),
    )

    def show_notification(message: str, color: str, icon: str = "✅"):
        """Show notification visible on screen"""
        notification_container.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.CHECK_CIRCLE if icon == "✅" else ft.Icons.WARNING if icon == "⚠️" else ft.Icons.ERROR,
                        color=color, size=30),
                ft.Text(message, size=16, weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=10,
        )
        notification_container.bgcolor = color + "20"
        notification_container.border = ft.border.all(2, color)
        notification_container.visible = True
        page.update()

    def hide_notification():
        """Hide notification"""
        notification_container.visible = False
        page.update()

    # --- UI elements ---
    def styled_textfield(label, **kwargs):
        return ft.TextField(
            label=label,
            color=TEXT_PRIMARY,
            border_color=BRAND_GREY,
            focused_border_color=BRAND_BLUE,
            bgcolor=BRAND_WHITE,
            filled=True,
            height=50,
            border_radius=8,
            text_size=14,
            **kwargs,
        )

    project_list = ft.Container(
        content=ft.Dropdown(
            label="Existing Projects",
            options=[ft.dropdown.Option(p.get("name", "")) for p in projects],
            color=TEXT_PRIMARY,
            border_color=BRAND_GREY,
            focused_border_color=BRAND_BLUE,
            bgcolor=BRAND_WHITE,
            filled=True,
            border_radius=8,
            text_size=14,
            expand=True,
            on_change=lambda e: load_project(e.control.value),
        ),
        height=50,
    )

    name_field = styled_textfield("Project Name", expand=True)
    dev_field = styled_textfield("Developer", expand=True)

    steps = ft.Column(spacing=12)
    total_label = ft.Text("Total: 0h", color=BRAND_BLUE, size=18, weight=ft.FontWeight.BOLD)

    # --- Logic functions ---
    def update_total():
        total = 0.0
        for row in steps.controls:
            try:
                total += float(row.controls[1].value or 0)
            except (ValueError, TypeError, AttributeError):
                pass
        total_label.value = f"Total: {total:.1f}h"
        page.update()

    def collect_project_data():
        """Collect current project data (used by save and generate_pdf_with_path)"""
        data = []
        total = 0.0
        for row in steps.controls:
            step_name = row.controls[0].value
            hours_raw = row.controls[1].value
            try:
                hours = float(hours_raw)
            except ValueError:
                hours = 0
            data.append({"name": step_name, "hours": hours})
            total += hours

        return {
            "name": name_field.value,
            "developer": dev_field.value if dev_field.value else "N/A",
            "date": date.today().isoformat(),
            "steps": data,
            "total": total,
        }

    def create_step_row(name: str = "", hours: Any = ""):
        step_field = styled_textfield("Step", value=name, width=350)
        hours_field = styled_textfield("Hours", value=str(hours), width=120, on_change=lambda _: update_total())

        def remove_step(_):
            steps.controls.remove(row)
            update_total()
            page.update()

        remove_btn = ft.IconButton(
            icon=ft.Icons.DELETE_FOREVER_ROUNDED,
            icon_color="#D32F2F",
            tooltip="Remove Step",
            on_click=remove_step,
        )
        row = ft.Row([step_field, hours_field, remove_btn], alignment=ft.MainAxisAlignment.START, spacing=15)
        return row

    def add_step(_):
        steps.controls.append(create_step_row())
        page.update()

    def load_project(selected_name):
        for p in projects:
            if p.get("name") == selected_name:
                name_field.value = p.get("name", "")
                dev_field.value = p.get("developer", "")
                steps.controls.clear()
                for st in p.get("steps", []):
                    steps.controls.append(create_step_row(st.get("name"), st.get("hours", 0)))
                total_label.value = f"Total: {p.get('total', 0)}h"
                page.update()
                break

    def save(_):
        project = collect_project_data()

        existing = next((p for p in projects if p["name"] == project["name"]), None)
        if existing:
            projects[projects.index(existing)] = project
        else:
            projects.append(project)

        manager.save_projects(projects)
        total_label.value = f"Total: {project['total']:.1f}h"
        show_notification(f"Project '{project['name']}' saved successfully!", BRAND_SUCCESS, "✅")

    def generate_pdf_click(_):
        hide_notification()

        # Validations
        if not name_field.value or not name_field.value.strip():
            show_notification("Please enter a project name before generating PDF!", "#FF9800", "⚠️")
            return

        if not steps.controls:
            show_notification("Please add at least one step before generating PDF!", "#FF9800", "⚠️")
            return

        # Suggest filename based on project
        suggested_filename = f"{name_field.value.replace(' ', '_')}_estimate.pdf"

        # Open file picker for user to choose where to save
        file_picker.save_file(
            dialog_title="Save PDF Estimate",
            file_name=suggested_filename,
            allowed_extensions=["pdf"],
        )

    def generate_pdf_with_path(save_path: str):
        """Generate PDF at the path selected by user"""
        current_project = collect_project_data()

        try:
            path = generate_pdf(current_project, save_path)
            show_notification(f"PDF generated successfully! Location: {path}", BRAND_SUCCESS, "✅")

        except Exception as ex:
            show_notification(f"Error generating PDF: {str(ex)}", "#D32F2F", "❌")

    # --- Header and Layout ---
    header = ft.Row(
        [
            ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, color=BRAND_BLUE, size=36),
            ft.Text("Project Estimator", size=28, weight=ft.FontWeight.BOLD, color=BRAND_BLUE),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    )

    divider = ft.Divider(height=1, color=BRAND_GREY)

    buttons = ft.Row(
        [
            ft.ElevatedButton(
                "Add Step",
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                bgcolor=BRAND_BLUE,
                color=BRAND_WHITE,
                height=45,
                on_click=add_step
            ),
            ft.ElevatedButton(
                "Save",
                icon=ft.Icons.SAVE_ROUNDED,
                bgcolor=BRAND_CHARCOAL,
                color=BRAND_WHITE,
                height=45,
                on_click=save
            ),
            ft.ElevatedButton(
                "Generate PDF",
                icon=ft.Icons.DESCRIPTION_ROUNDED,
                bgcolor=BRAND_SUCCESS,
                color=BRAND_WHITE,
                height=45,
                on_click=generate_pdf_click
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=20,
    )

    form_grid = ft.ResponsiveRow(
        [
            ft.Container(project_list, col={"xs": 12, "md": 4}),
            ft.Container(name_field, col={"xs": 12, "md": 4}),
            ft.Container(dev_field, col={"xs": 12, "md": 4}),
        ],
        spacing=20,
    )

    card = ft.Container(
        content=ft.Column(
            [
                notification_container,
                header,
                divider,
                form_grid,
                ft.Container(steps, padding=ft.padding.only(top=10)),
                ft.Container(total_label, alignment=ft.alignment.center_right, padding=10),
                buttons,
            ],
            spacing=25,
        ),
        padding=35,
        bgcolor=CARD_BG,
        border_radius=15,
        border=ft.border.all(2, BRAND_BLUE),
        shadow=ft.BoxShadow(blur_radius=20, color="#00000015", offset=ft.Offset(0, 4)),
        width=950,
    )

    page.add(ft.Container(content=card, alignment=ft.alignment.center, expand=True))
    page.update()
