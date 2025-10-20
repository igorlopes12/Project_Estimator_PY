"""
Refined Ball Corporation style Project Estimator UI.
Uniform spacing, aligned fields, consistent heights, and corporate color palette.
"""

import flet as ft
from datetime import date
from typing import List, Dict, Any
from core.project_manager import ProjectManager
from core.pdf_generator import generate_pdf

# --- Ball Corporation inspired palette ---
BRAND_PRIMARY = "#003594"   # Deep blue
BRAND_ACCENT = "#0095D9"    # Cyan-blue
BRAND_SUCCESS = "#4CAF50"   # Green accent
BG_COLOR = "#F4F6F9"
CARD_BG = "#FFFFFF"
TEXT_PRIMARY = "#003594"
BORDER_COLOR = "#DDE4ED"


def main_view(page: ft.Page, manager: ProjectManager):
    page.title = "Project Estimator"
    page.padding = 40
    page.bgcolor = BG_COLOR
    page.scroll = "adaptive"

    projects: List[Dict[str, Any]] = manager.load_projects() or []

    # --- UI elements ---
    def styled_textfield(label, **kwargs):
        return ft.TextField(
            label=label,
            color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            bgcolor="#FAFBFC",
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
            border_color=BORDER_COLOR,
            bgcolor="#FAFBFC",
            filled=True,
            border_radius=8,
            text_size=14,
            expand=True,
            on_change=lambda e: load_project(e.control.value),
        ),
        height=50,  # Define a altura externa via container
    )

    name_field = styled_textfield("Project Name", expand=True)
    dev_field = styled_textfield("Developer", expand=True)

    steps = ft.Column(spacing=12)
    total_label = ft.Text("Total: 0h", color=TEXT_PRIMARY, size=18, weight=ft.FontWeight.BOLD)

    # --- Logic functions ---
    def update_total():
        total = 0.0
        for row in steps.controls:
            try:
                total += float(row.controls[1].value or 0)
            except Exception:
                pass
        total_label.value = f"Total: {total:.1f}h"
        page.update()

    def create_step_row(name: str = "", hours: Any = ""):
        step_field = styled_textfield("Step", value=name, width=350)
        hours_field = styled_textfield("Hours", value=str(hours), width=120, on_change=lambda e: update_total())

        def remove_step(e):
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

    def add_step(e):
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

    def save(e):
        data = []
        total = 0.0
        for row in steps.controls:
            name = row.controls[0].value
            hours_raw = row.controls[1].value
            try:
                hours = float(hours_raw)
            except ValueError:
                hours = 0
            data.append({"name": name, "hours": hours})
            total += hours

        project = {
            "name": name_field.value,
            "developer": dev_field.value,
            "date": date.today().isoformat(),
            "steps": data,
            "total": total,
        }

        existing = next((p for p in projects if p["name"] == project["name"]), None)
        if existing:
            projects[projects.index(existing)] = project
        else:
            projects.append(project)

        manager.save_projects(projects)
        total_label.value = f"Total: {total:.1f}h"
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Project '{project['name']}' saved successfully!"))
        page.snack_bar.open = True
        page.update()

    def generate_pdf_click(e):
        if not projects:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ No project to generate PDF."))
            page.snack_bar.open = True
            page.update()
            return
        try:
            path = generate_pdf(projects[-1])
            page.snack_bar = ft.SnackBar(ft.Text(f"📄 PDF generated successfully: {path}"))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error generating PDF: {ex}"))
        page.snack_bar.open = True
        page.update()

    # --- Header and Layout ---
    header = ft.Row(
        [
            ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, color=BRAND_ACCENT, size=36),
            ft.Text("Project Estimator", size=28, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    )

    divider = ft.Divider(height=1, color=BORDER_COLOR)

    buttons = ft.Row(
        [
            ft.ElevatedButton("Add Step", icon=ft.Icons.ADD_CIRCLE_OUTLINE, bgcolor=BRAND_ACCENT, color="white", height=45, on_click=add_step),
            ft.ElevatedButton("Save", icon=ft.Icons.SAVE_ROUNDED, bgcolor=BRAND_PRIMARY, color="white", height=45, on_click=save),
            ft.ElevatedButton("Generate PDF", icon=ft.Icons.DESCRIPTION_ROUNDED, bgcolor=BRAND_SUCCESS, color="white", height=45, on_click=generate_pdf_click),
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
        border=ft.border.all(1, BORDER_COLOR),
        shadow=ft.BoxShadow(blur_radius=20, color="#00000020", offset=ft.Offset(0, 4)),
        width=950,
    )

    page.add(ft.Container(content=card, alignment=ft.alignment.center, expand=True))
    page.update()
