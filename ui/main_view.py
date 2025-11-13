import flet as ft
from core.project_manager import ProjectManager
import os

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates.json")


def main_view(page: ft.Page, manager: ProjectManager):
    page.title = "Project Estimator"
    page.scroll = None  # Remove scroll da página
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 10

    template_manager = ProjectManager(TEMPLATES_PATH)

    # ---------- Helpers ----------
    def show_snack(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def load_templates():
        try:
            return template_manager.load_projects()
        except Exception:
            return []

    def save_templates(tpls):
        try:
            template_manager.save_projects(tpls)
        except Exception as e:
            show_snack(f"Error saving templates: {e}")

    def load_projects():
        try:
            return manager.load_projects()
        except Exception:
            return []

    def save_projects(projs):
        manager.save_projects(projs)

    projects = load_projects()
    templates = load_templates()
    steps = []

    # ---------- Project fields ----------
    existing_projects_dropdown = ft.Dropdown(
        label="Existing Projects",
        options=[ft.dropdown.Option("Create New Project")] +
                [ft.dropdown.Option(p["name"]) for p in projects],
        expand=True,
        color=ft.Colors.BLACK,
    )

    project_name = ft.TextField(label="Project", expand=True, color=ft.Colors.BLACK)
    architect = ft.TextField(label="Solution Architect", expand=True, color=ft.Colors.BLACK)
    area = ft.TextField(label="Area", expand=True, color=ft.Colors.BLACK)
    demand = ft.TextField(label="Demand Number", expand=True, color=ft.Colors.BLACK)
    purpose = ft.TextField(label="Purpose", multiline=True, min_lines=2, expand=True, color=ft.Colors.BLACK)

    def on_select_project(e):
        sel = existing_projects_dropdown.value
        if not sel or sel == "Create New Project":
            project_name.value = ""
            architect.value = ""
            area.value = ""
            demand.value = ""
            purpose.value = ""
            steps.clear()
            steps_column.controls.clear()
            update_total_hours()
            page.update()
            return

        for p in projects:
            if p.get("name") == sel:
                project_name.value = p.get("name", "")
                architect.value = p.get("architect", "")
                area.value = p.get("area", "")
                demand.value = p.get("demand", "")
                purpose.value = p.get("purpose", "")
                steps.clear()
                steps_column.controls.clear()
                for s in p.get("steps", []):
                    add_step(s.get("name", ""), s.get("hours", ""))
                update_total_hours()
                page.update()
                break

    existing_projects_dropdown.on_change = on_select_project

    # ---------- Steps ----------
    steps_column = ft.Column(spacing=8)

    total_hours_text = ft.Text("0.0 h", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)

    def update_total_hours():
        total = 0.0
        for s in steps:
            try:
                h = float(s["hours"].value or 0)
            except Exception:
                h = 0.0
            total += h
        total_hours_text.value = f"{total:.1f} h"
        page.update()

    def add_step(name="", hours=""):
        name_field = ft.TextField(value=name, hint_text="Step", expand=True, color=ft.Colors.BLACK, border_color=ft.Colors.GREY_400)
        hours_field = ft.TextField(value=hours, hint_text="Hours", width=100, color=ft.Colors.BLACK, border_color=ft.Colors.GREY_400)

        def remove_step(e):
            steps.remove(step)
            steps_column.controls.remove(step_row)
            update_total_hours()
            page.update()

        remove_btn = ft.IconButton(
            ft.Icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            tooltip="Remove step",
            on_click=remove_step
        )

        step_row = ft.Row(
            [name_field, hours_field, remove_btn],
            spacing=8,
            alignment=ft.MainAxisAlignment.START
        )

        step = {"name": name_field, "hours": hours_field}
        steps.append(step)
        steps_column.controls.append(step_row)
        hours_field.on_change = lambda e: update_total_hours()
        update_total_hours()

    def on_add_step(e):
        add_step()
        page.update()

    # ---------- Templates ----------
    templates_column = ft.Column(spacing=8)

    def refresh_templates():
        templates_column.controls.clear()
        for t in templates:
            name_text = ft.Text(
                t.get('name', ''),
                size=14,
                color=ft.Colors.BLACK,
                expand=True
            )

            hours_text = ft.Text(
                f"{t.get('hours', '0')}h",
                size=14,
                color=ft.Colors.GREY_700,
                weight=ft.FontWeight.BOLD
            )

            # Add steps button
            def on_add_steps(e, temp=t):
                add_step(temp["name"], temp["hours"])

            add_steps_btn = ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE,
                icon_color=ft.Colors.GREEN_600,
                tooltip="Add to steps",
                on_click=lambda e, temp=t: on_add_steps(e, temp)
            )

            # Edit button
            def on_edit_template(e, temp=t):
                name_input = ft.TextField(label="Template name", value=temp["name"], color=ft.Colors.BLACK)
                hours_input = ft.TextField(label="Hours", value=temp["hours"], color=ft.Colors.BLACK)

                def save_edit(ev):
                    temp["name"] = name_input.value
                    temp["hours"] = hours_input.value
                    save_templates(templates)
                    refresh_templates()
                    page.close(edit_dlg)

                    # Show success dialog
                    success_edit_dlg = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Success", color=ft.Colors.GREEN_700),
                        content=ft.Text("Template updated successfully!"),
                        actions=[
                            ft.TextButton("OK", on_click=lambda e: page.close(success_edit_dlg)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    page.open(success_edit_dlg)

                edit_dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Edit Template"),
                    content=ft.Column([name_input, hours_input], tight=True, spacing=10),
                    actions=[
                        ft.TextButton("Save", on_click=save_edit),
                        ft.TextButton("Cancel", on_click=lambda _: page.close(edit_dlg)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(edit_dlg)

            edit_btn = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=ft.Colors.ORANGE_400,
                tooltip="Edit template",
                on_click=lambda e, temp=t: on_edit_template(e, temp)
            )

            # Delete button
            def on_delete_template(e, temp=t):
                def confirm_delete(ev):
                    templates.remove(temp)
                    save_templates(templates)
                    refresh_templates()
                    page.close(delete_dlg)

                    # Show success dialog
                    success_delete_dlg = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Deleted", color=ft.Colors.GREEN_700),
                        content=ft.Text("Template deleted successfully!"),
                        actions=[
                            ft.TextButton("OK", on_click=lambda e: page.close(success_delete_dlg)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    page.open(success_delete_dlg)

                delete_dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirm Deletion"),
                    content=ft.Text(f"Delete template '{temp['name']}'?"),
                    actions=[
                        ft.TextButton("Delete", on_click=confirm_delete),
                        ft.TextButton("Cancel", on_click=lambda _: page.close(delete_dlg)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(delete_dlg)

            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                tooltip="Delete template",
                on_click=lambda e, temp=t: on_delete_template(e, temp)
            )

            row = ft.Container(
                content=ft.Row(
                    [
                        name_text,
                        hours_text,
                        ft.Row([add_steps_btn, edit_btn, delete_btn], spacing=0)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=8,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=6,
                bgcolor=ft.Colors.GREY_50,
            )
            templates_column.controls.append(row)
        page.update()

    def add_template_dialog(e):
        name_input = ft.TextField(label="Template name", color=ft.Colors.BLACK)
        hours_input = ft.TextField(label="Hours", value="0", color=ft.Colors.BLACK)

        def save_template(ev):
            name = name_input.value.strip()
            if not name:
                error_dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Error"),
                    content=ft.Text("Template name cannot be empty!"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: page.close(error_dlg)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(error_dlg)
                return
            new_tpl = {"name": name, "hours": hours_input.value.strip() or "0"}
            templates.append(new_tpl)
            save_templates(templates)
            refresh_templates()
            page.close(dlg)

            # Show success dialog
            success_create_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Success", color=ft.Colors.GREEN_700),
                content=ft.Text(f"Template '{name}' created successfully!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(success_create_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(success_create_dlg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("New Template"),
            content=ft.Column([name_input, hours_input], tight=True, spacing=10),
            actions=[
                ft.TextButton("Save", on_click=save_template),
                ft.TextButton("Cancel", on_click=lambda _: page.close(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)

    refresh_templates()

    # ---------- Save & PDF ----------
    def save_project(e):
        if not project_name.value:
            error_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text("Please enter a project name!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(error_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(error_dlg)
            return

        project_data = {
            "name": project_name.value,
            "architect": architect.value,
            "area": area.value,
            "demand": demand.value,
            "purpose": purpose.value,
            "steps": [{"name": s["name"].value, "hours": s["hours"].value} for s in steps],
        }

        existing = next((p for p in projects if p["name"] == project_data["name"]), None)
        if existing:
            projects.remove(existing)
        projects.append(project_data)

        save_projects(projects)
        existing_projects_dropdown.options = [ft.dropdown.Option("Create New Project")] + \
                                             [ft.dropdown.Option(p["name"]) for p in projects]
        page.update()

        # Show success dialog
        success_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Success", color=ft.Colors.GREEN_700),
            content=ft.Text(f"Project '{project_name.value}' saved successfully!"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(success_dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(success_dlg)

    def generate_pdf(e):
        # Show info dialog for PDF generation
        pdf_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("PDF Generation"),
            content=ft.Text("PDF generation feature is not implemented yet."),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(pdf_dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(pdf_dlg)

    save_btn = ft.ElevatedButton(
        "Save",
        icon=ft.Icons.SAVE,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=save_project
    )

    pdf_btn = ft.ElevatedButton(
        "Generate PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=generate_pdf
    )

    # ---------- Layout ----------

    # Header with logo
    header = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Container(
                        ft.Icon(ft.Icons.BUILD_CIRCLE_ROUNDED, color=ft.Colors.WHITE, size=24),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=6,
                        border_radius=6,
                    ),
                    ft.Text("Project Estimator", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], spacing=8),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text("Ball", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    padding=ft.padding.symmetric(horizontal=16, vertical=6),
                    bgcolor=ft.Colors.BLUE_800,
                    border_radius=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=ft.Colors.BLUE_700,
        padding=12,
        border_radius=ft.border_radius.only(top_left=8, top_right=8),
    )

    # Project Details Section
    project_details_card = ft.Container(
        content=ft.Column([
            ft.Text("Project Details", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            existing_projects_dropdown,
            project_name,
            ft.ResponsiveRow([
                ft.Container(architect, col={"sm": 12, "md": 4}),
                ft.Container(area, col={"sm": 12, "md": 4}),
                ft.Container(demand, col={"sm": 12, "md": 4}),
            ]),
            purpose,
        ], spacing=8),
        padding=12,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
    )

    # Steps Section
    steps_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Steps", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_600,
                    icon_size=24,
                    tooltip="Add step",
                    on_click=on_add_step,
                ),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Container(
                content=ft.Column([steps_column], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=8,
            ),
        ], spacing=8, expand=True),
        padding=12,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        expand=True,
    )

    # Templates Section
    templates_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Templates", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_600,
                    icon_size=24,
                    tooltip="Add template",
                    on_click=add_template_dialog,
                ),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Container(
                content=ft.Column([templates_column], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=8,
            ),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Row([
                ft.Text("Total:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                total_hours_text,
            ], spacing=8),
        ], spacing=8, expand=True),
        padding=12,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        expand=True,
    )

    # Footer with buttons
    footer = ft.Container(
        content=ft.Row([
            save_btn,
            pdf_btn,
        ], spacing=12, alignment=ft.MainAxisAlignment.END),
        padding=12,
        bgcolor=ft.Colors.GREY_50,
        border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
    )

    # Main container
    main_container = ft.Container(
        content=ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    project_details_card,
                    ft.Container(
                        content=ft.ResponsiveRow([
                            ft.Container(steps_card, col={"sm": 12, "md": 12, "lg": 8}),
                            ft.Container(templates_card, col={"sm": 12, "md": 12, "lg": 4}),
                        ]),
                        expand=True,
                    ),
                    footer,
                ], spacing=12, expand=True),
                padding=12,
                bgcolor=ft.Colors.GREY_50,
                expand=True,
            ),
        ], spacing=0, expand=True),
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        border=ft.border.all(2, ft.Colors.GREY_400),
        expand=True,
    )

    page.add(main_container)
    page.update()

