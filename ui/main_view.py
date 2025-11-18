import flet as ft
from core.project_manager import ProjectManager
from core.helpers.dialog_utils import auto_close_dialog
from core.helpers.template_utils import load_templates, save_templates


def main_view(page: ft.Page, manager: ProjectManager):
    page.title = "Project Estimator"
    page.scroll = None  # Remove scroll da página
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 10

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
                    add_step(s.get("name", ""), s.get("description", ""), s.get("hours", ""))
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

    def add_step(name="", description="", hours=""):
        name_field = ft.TextField(value=name, hint_text="Step", expand=True, color=ft.Colors.BLACK, border_color=ft.Colors.GREY_400)
        description_field = ft.TextField(value=description, hint_text="Description (optional)", expand=True, color=ft.Colors.BLACK, border_color=ft.Colors.GREY_400, multiline=True, min_lines=2)
        hours_field = ft.TextField(value=hours, hint_text="Hours", width=100, color=ft.Colors.BLACK, border_color=ft.Colors.GREY_400)

        def remove_step(e):
            steps.remove(step)
            steps_column.controls.remove(step_container)
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

        step_container = ft.Column(
            [
                step_row,
                description_field,
            ],
            spacing=4
        )

        step = {"name": name_field, "description": description_field, "hours": hours_field}
        steps.append(step)
        steps_column.controls.append(step_container)
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
                add_step(temp["name"], temp.get("description", ""), temp["hours"])

                success_add_dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Added", color=ft.Colors.GREEN_700),
                    content=ft.Text(f"Template '{temp['name']}' added to steps!"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: page.close(success_add_dlg)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(success_add_dlg)  # Primeiro abre
                page.update()  # Atualiza a página



            add_steps_btn = ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE,
                icon_color=ft.Colors.GREEN_600,
                tooltip="Add to steps",
                on_click=lambda e, temp=t: on_add_steps(e, temp)
            )

            # Edit button
            def on_edit_template(e, temp=t):
                name_input = ft.TextField(label="Template name", value=temp["name"], color=ft.Colors.WHITE)
                description_input = ft.TextField(label="Description (optional)", value=temp.get("description", ""), color=ft.Colors.WHITE, multiline=True, min_lines=2)
                hours_input = ft.TextField(label="Hours", value=temp["hours"], color=ft.Colors.WHITE)

                def save_edit(ev):
                    temp["name"] = name_input.value
                    temp["description"] = description_input.value
                    temp["hours"] = hours_input.value
                    save_templates(templates)
                    refresh_templates()
                    page.close(edit_dlg)

                    success_edit_dlg = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Success", color=ft.Colors.GREEN_700),
                        content=ft.Text("Template updated successfully!"),
                        actions=[
                            ft.TextButton("OK", on_click=lambda e: page.close(success_edit_dlg)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    page.run_task(auto_close_dialog, page, success_edit_dlg, 0.5)
                    page.open(success_edit_dlg)


                edit_dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Edit Template"),
                    content=ft.Column([name_input, description_input, hours_input], tight=True, spacing=10),
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
                    page.update()
                    page.run_task(auto_close_dialog, page, success_delete_dlg, 0.5)

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
        name_input = ft.TextField(label="Template name", color=ft.Colors.WHITE)
        description_input = ft.TextField(label="Description (optional)", color=ft.Colors.WHITE, multiline=True, min_lines=2)
        hours_input = ft.TextField(label="Hours", value="0", color=ft.Colors.WHITE)

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
            new_tpl = {"name": name, "description": description_input.value.strip(), "hours": hours_input.value.strip() or "0"}
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
            page.update()
            page.run_task(auto_close_dialog, page, success_create_dlg, 0.5)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("New Template"),
            content=ft.Column([name_input, description_input, hours_input], tight=True, spacing=10),
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
            "steps": [{"name": s["name"].value, "description": s["description"].value, "hours": s["hours"].value} for s in steps],
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

    # FilePicker para salvar PDF
    def on_save_pdf_result(e: ft.FilePickerResultEvent):
        if not e.path:
            # Usuário cancelou
            return

        try:
            # Importar o gerador de PDF
            from core.pdf_generator import generate_pdf as pdf_gen
            from datetime import datetime

            # Calcular total de horas
            total = 0.0
            for s in steps:
                try:
                    h = float(s["hours"].value or 0)
                except Exception:
                    h = 0.0
                total += h

            # Preparar os dados do projeto
            project_data = {
                "name": project_name.value,
                "developer": architect.value or "N/A",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "steps": [{"name": s["name"].value, "description": s["description"].value, "hours": float(s["hours"].value or 0)} for s in steps],
                "total": total,
            }

            # Gerar o PDF no caminho escolhido
            pdf_path = pdf_gen(project_data, e.path)

            # Mostrar diálogo de sucesso
            success_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Success", color=ft.Colors.GREEN_700),
                content=ft.Text(f"PDF generated successfully!\n\nSaved at:\n{pdf_path}"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(success_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(success_dlg)

        except Exception as ex:
            # Mostrar diálogo de erro
            error_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text(f"Failed to generate PDF:\n\n{str(ex)}"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(error_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(error_dlg)

    save_pdf_dialog = ft.FilePicker(on_result=on_save_pdf_result)
    page.overlay.append(save_pdf_dialog)

    def generate_pdf(e):
        # Validar se há um projeto para gerar
        if not project_name.value:
            error_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text("Please enter a project name before generating PDF!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(error_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(error_dlg)
            return

        if not steps:
            error_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text("Please add at least one step before generating PDF!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(error_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(error_dlg)
            return

        # Abrir diálogo para salvar arquivo
        pdf_filename = f"{project_name.value.replace(' ', '_')}_estimate.pdf"
        save_pdf_dialog.save_file(
            file_name=pdf_filename,
            allowed_extensions=["pdf"],
            dialog_title="Save PDF As"
        )

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
                        padding=6,
                        border_radius=6,
                        bgcolor=ft.Colors.BLUE_600,
                    ),
                    ft.Text("Project Estimator", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                ], spacing=8),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Image(src="BallLogo.png", width=62, height=40, fit=ft.ImageFit.CONTAIN),
                    padding=ft.padding.symmetric(horizontal=16, vertical=6),
                    border_radius=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

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
