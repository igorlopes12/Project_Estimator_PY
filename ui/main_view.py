"""ui/main_view.py

User interface for the Project Estimator application built with Flet.
This module defines the main_view function which composes the UI and connects
it to the ProjectManager for loading/saving projects and templates.
"""
import os
from datetime import datetime
import flet as ft
from dotenv import load_dotenv
from core.project_manager import ProjectManager
from core.helpers.dialog_utils import auto_close_dialog
from core.helpers.template_utils import load_templates, save_templates
from core.helpers.devops_client import DevOpsClient
from core.helpers.ui_utils import show_snackbar

# Load environment variables from .env file
load_dotenv()

# ---------- Dialog theme helpers ----------

DIALOG_BG = ft.Colors.GREY_900
DIALOG_TEXT = ft.Colors.WHITE
DIALOG_BORDER = ft.Colors.GREY_400


def dialog_text(value, **kwargs):
    """Create dialog text with optional color override.

    Args:
        value: Text content
        **kwargs: Additional Text properties, including optional 'color'
    """
    # Set default color only if not provided in kwargs
    if 'color' not in kwargs:
        kwargs['color'] = DIALOG_TEXT

    return ft.Text(value, **kwargs)


def dialog_textfield(**kwargs):
    return ft.TextField(
        color=DIALOG_TEXT,
        border_color=DIALOG_BORDER,
        label_style=ft.TextStyle(color=DIALOG_TEXT),
        text_style=ft.TextStyle(color=DIALOG_TEXT),
        cursor_color=DIALOG_TEXT,
        **kwargs
    )


def dialog_button(label, on_click):
    return ft.TextButton(
        label,
        style=ft.ButtonStyle(color=DIALOG_TEXT),
        on_click=on_click
    )


def main_view(page: ft.Page, manager: ProjectManager):
    """Build and attach the main application UI to the given Flet page.

    Args:
        page: Flet Page instance to populate.
        manager: ProjectManager instance used to load and save projects.
    """
    page.title = "Project Estimator"
    page.scroll = None
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
                    # Ensure we pass strings for textfields; hours may be float or str
                    add_step(s.get("name", ""), s.get("description", ""), str(s.get("hours", "")))
                update_total_hours()
                page.update()
                break

    existing_projects_dropdown.on_change = on_select_project

    # ---------- Steps ----------
    steps_column = ft.Column(spacing=8)
    total_hours_text = ft.Text("0.0 h", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)

    def auto_save_step_as_template(name, description, hours):
        """Automatically save a step as a template when the user leaves a field.

        If a template with the same name exists, it updates the existing one.
        Otherwise, creates a new template.

        Args:
            name: Template/step name
            description: Optional description
            hours: Estimated hours as string
        """
        name = (name or "").strip()
        if not name:
            return

        description = (description or "").strip()
        hours = (hours or "0").strip() or "0"

        for tpl in templates:
            if tpl["name"].lower() == name.lower():
                tpl["description"] = description
                tpl["hours"] = hours
                save_templates(templates)
                refresh_templates()
                return

        templates.append({
            "name": name,
            "description": description,
            "hours": hours
        })

        save_templates(templates)
        refresh_templates()

    def update_total_hours():
        """Recalculate the total hours from the steps and update the UI."""
        total = 0.0
        for s in steps:
            try:
                # s["hours"] is a TextField
                h = float(s["hours"].value or 0)
            except Exception:
                h = 0.0
            total += h
        total_hours_text.value = f"{total:.1f} h"
        page.update()

    def add_step(name="", description="", hours="", step_type="Feature", parent=None):
        """Add a new step (task/feature/user story) to the project.

        Each step can have:
        - name: The task/feature name
        - description: Optional detailed description of the step
        - hours: Estimated hours for completion
        - step_type: Type of work item (Feature, User Story, Task)
        - parent: Parent task reference for hierarchical organization

        Steps are auto-saved as templates when the user leaves a field.
        Users can optionally add or edit the description by clicking the description button.
        """
        name_field = ft.TextField(
            value=name,
            hint_text="Step",
            expand=True,
            color=ft.Colors.BLACK,
            border_color=ft.Colors.GREY_400
        )

        description_field = ft.TextField(
            value=description,
            hint_text="Description (optional)",
            expand=True,
            color=ft.Colors.BLACK,
            border_color=ft.Colors.GREY_400,
            multiline=True,
            min_lines=2,
            visible=False  # Hidden by default; shown only if user clicks description button
        )

        hours_field = ft.TextField(
            value=str(hours),
            hint_text="Hours",
            width=90,
            color=ft.Colors.BLACK,
            border_color=ft.Colors.GREY_400
        )

        def on_step_blur(e):
            auto_save_step_as_template(
                name_field.value,
                description_field.value,
                hours_field.value
            )

        name_field.on_blur = on_step_blur
        description_field.on_blur = on_step_blur
        hours_field.on_blur = on_step_blur

        # Note: Epic type was removed from the UI
        type_dropdown = ft.Dropdown(
            width=140,
            value=step_type,
            options=[
                ft.dropdown.Option("Feature"),
                ft.dropdown.Option("User Story"),
                ft.dropdown.Option("Task"),
            ]
        )

        parent_dropdown = ft.Dropdown(
            width=200,
            hint_text="Parent"
        )

        step = {
            "name": name_field,
            "description": description_field,
            "hours": hours_field,
            "type": type_dropdown,
            "parent": parent_dropdown,
            "id": None
        }

        def refresh_parent_options():
            options = []

            for s in steps:
                if s is step:
                    continue

                stype = s["type"].value
                ctype = type_dropdown.value

                if ctype == "User Story" and stype == "Feature":
                    options.append(ft.dropdown.Option(s["name"].value))
                elif ctype == "Task" and stype == "User Story":
                    options.append(ft.dropdown.Option(s["name"].value))

            parent_dropdown.options = options
            parent_dropdown.value = None

        type_dropdown.on_change = lambda e: (refresh_parent_options(), page.update())

        def remove_step(e):
            steps.remove(step)
            steps_column.controls.remove(step_container)
            update_total_hours()
            page.update()

        def toggle_description(e):
            """Show/hide the description field"""
            description_field.visible = not description_field.visible
            page.update()

        remove_btn = ft.IconButton(
            ft.Icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            tooltip="Remove step",
            on_click=remove_step
        )

        # Button to toggle description visibility
        description_btn = ft.IconButton(
            ft.Icons.DESCRIPTION_OUTLINED,
            icon_color=ft.Colors.GREY_600,
            tooltip="Add/edit description",
            on_click=toggle_description
        )

        step_row = ft.Row(
            [
                name_field,
                type_dropdown,
                parent_dropdown,
                hours_field,
                description_btn,
                remove_btn
            ],
            spacing=8
        )

        step_container = ft.Column(
            [step_row, description_field],
            spacing=4
        )

        steps.append(step)
        steps_column.controls.append(step_container)

        hours_field.on_change = lambda e: update_total_hours()
        refresh_parent_options()
        update_total_hours()

    def on_add_step(e):
        add_step()
        page.update()

    # ---------- Templates ----------

    template_search = ft.TextField(
        hint_text="Search template...",
        prefix_icon=ft.Icons.SEARCH,
        color=ft.Colors.BLACK,
    )

    templates_column = ft.Column(spacing=8)

    def add_template_dialog(e):
        """Open dialog to create a new template.

        Templates allow users to save reusable step configurations with:
        - Name: Template identifier
        - Description: Optional details about what the step entails
        - Hours: Default estimated hours for this step type

        Once created, templates can be added to projects and edited.
        """
        name_input = dialog_textfield(label="Template name")
        description_input = dialog_textfield(
            label="Description (optional)",
            multiline=True,
            min_lines=2
        )
        hours_input = dialog_textfield(label="Hours", value="0")

        def save_template(ev, dlg=None):
            name = (name_input.value or "").strip()
            if not name:
                dlg = ft.AlertDialog(
                    modal=True,
                    bgcolor=DIALOG_BG,
                    title=dialog_text("Error"),
                    content=dialog_text("Template name cannot be empty."),
                    actions=[dialog_button("OK", lambda e: page.close(dlg))]
                )
                page.open(dlg)
                return

            templates.append({
                "name": name,
                "description": (description_input.value or "").strip(),
                "hours": (hours_input.value or "0").strip() or "0"
            })

            save_templates(templates)
            refresh_templates()
            page.close(dlg)

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=DIALOG_BG,
            title=dialog_text("New Template"),
            content=ft.Column(
                [name_input, description_input, hours_input],
                tight=True,
                spacing=10
            ),
            actions=[
                dialog_button("Save", save_template),
                dialog_button("Cancel", lambda e: page.close(dlg))
            ]
        )
        page.open(dlg)

    def refresh_templates():
        """Refresh the templates UI from the loaded templates list.

        Each template displays:
        - Name: Template title
        - Hours: Estimated hours (shown in bold)
        - Buttons: Add to steps, Edit, Delete

        Templates are filtered based on the search field.
        Each template stores an optional description that is applied
        when added to steps.
        """
        templates_column.controls.clear()
        search = (template_search.value or "").lower()

        for t in templates[:]:  # Safe copy to avoid iteration issues
            if search and search not in t.get("name", "").lower():
                continue

            name_text = ft.Text(
                t.get("name", ""),
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

            # ---------- ADD TO STEPS ----------
            def on_add_steps(e, temp=t):
                add_step(
                    temp["name"],
                    temp.get("description", ""),
                    temp.get("hours", "0")
                )

                dlg = ft.AlertDialog(
                    modal=True,
                    bgcolor=DIALOG_BG,
                    title=dialog_text("Added", color=ft.Colors.GREEN_400),
                    content=dialog_text(
                        f"Template '{temp['name']}' added to steps!"
                    ),
                    actions=[
                        dialog_button("OK", lambda e: page.close(dlg))
                    ],
                )
                page.open(dlg)
                page.run_task(auto_close_dialog, page, dlg, 0.5)

            add_steps_btn = ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE,
                icon_color=ft.Colors.GREEN_600,
                tooltip="Add to steps",
                on_click=on_add_steps
            )

            # ---------- EDIT ----------
            def on_edit_template(e, temp=t):
                name_input = dialog_textfield(
                    label="Template name",
                    value=temp["name"]
                )
                description_input = dialog_textfield(
                    label="Description (optional)",
                    value=temp.get("description", ""),
                    multiline=True,
                    min_lines=2
                )
                hours_input = dialog_textfield(
                    label="Hours",
                    value=str(temp.get("hours", "0"))
                )

                def save_edit(ev):
                    temp["name"] = (name_input.value or "").strip()
                    temp["description"] = (description_input.value or "").strip()
                    temp["hours"] = (hours_input.value or "0").strip() or "0"

                    save_templates(templates)
                    refresh_templates()
                    page.close(edit_dlg)

                edit_dlg = ft.AlertDialog(
                    modal=True,
                    bgcolor=DIALOG_BG,
                    title=dialog_text("Edit Template"),
                    content=ft.Column(
                        [name_input, description_input, hours_input],
                        tight=True,
                        spacing=10
                    ),
                    actions=[
                        dialog_button("Save", save_edit),
                        dialog_button(
                            "Cancel",
                            lambda _: page.close(edit_dlg)
                        )
                    ],
                )
                page.open(edit_dlg)

            edit_btn = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=ft.Colors.ORANGE_400,
                tooltip="Edit template",
                on_click=on_edit_template
            )

            # ---------- DELETE ----------
            def on_delete_template(e, temp=t):
                def confirm_delete(ev):
                    if temp in templates:  # Check if template exists before removing
                        templates.remove(temp)
                        save_templates(templates)
                        refresh_templates()

                    page.close(delete_dlg)

                delete_dlg = ft.AlertDialog(
                    modal=True,
                    bgcolor=DIALOG_BG,
                    title=dialog_text("Confirm Deletion"),
                    content=dialog_text(
                        f"Delete template '{temp['name']}'?"
                    ),
                    actions=[
                        dialog_button("Delete", confirm_delete),
                        dialog_button(
                            "Cancel",
                            lambda _: page.close(delete_dlg)
                        )
                    ],
                )
                page.open(delete_dlg)

            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                tooltip="Delete template",
                on_click=on_delete_template
            )

            row = ft.Container(
                content=ft.Row(
                    [
                        name_text,
                        hours_text,
                        ft.Row(
                            [add_steps_btn, edit_btn, delete_btn],
                            spacing=0
                        ),
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

    template_search.on_change = lambda e: refresh_templates()
    refresh_templates()

    # ---------- Save & PDF ----------

    def on_upload_devops(e):
        try:
            # Validate that we have a project to upload
            if not project_name.value:
                show_snackbar(page, "⚠ Please save a project first before uploading to DevOps!", ft.Colors.ORANGE, 3000)
                return

            if not steps:
                show_snackbar(page, "⚠ Please add at least one step before uploading to DevOps!", ft.Colors.ORANGE, 3000)
                return

            # Build the project data to upload
            total = 0.0
            for s in steps:
                try:
                    h = float(s["hours"].value or 0)
                except Exception:
                    h = 0.0
                total += h

            data = {
                "name": project_name.value,
                "architect": architect.value or "N/A",
                "area": area.value or "N/A",
                "demand": demand.value or "N/A",
                "purpose": purpose.value or "",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "steps": [
                    {
                        "name": s["name"].value,
                        "description": s["description"].value,
                        "hours": float(s["hours"].value or 0),
                        "type": s["type"].value,
                        "parent": s["parent"].value
                    }
                    for s in steps
                ],

                "total": total,
            }

            print(f"📤 Uploading to DevOps: {data['name']}")
            print(f"📋 Steps count: {len(data['steps'])}")

            # Create DevOps client with environment variables
            devops_org = os.getenv("DEVOPS_ORG", "BallCorporation")
            devops_project = os.getenv("DEVOPS_PROJECT", "Automation and Digital Adoption")
            devops_pat = os.getenv("DEVOPS_PAT")

            if not devops_pat:
                show_snackbar(page, "❌ DevOps PAT not configured. Check your .env file.", ft.Colors.RED, 5000)
                return

            devops = DevOpsClient(
                organization=devops_org,
                project=devops_project,
                pat=devops_pat
            )

            print("✅ DevOps client created successfully")

            result = devops.create_structure_from_json(data)

            print(f"✅ Upload successful! Epic #{result['epic']} created")
            print("📌 Work Items created:")
            for name, wid in result["items"].items():
                print(f"   {name}: #{wid}")

            show_snackbar(page, f"✔ Upload concluído! Epic #{result['epic']} criada.", ft.Colors.GREEN, 4000)

        except AttributeError as ex:
            error_msg = f"❌ Erro de atributo: {ex}"
            print(error_msg)
            print(f"   Verifique se o método export_project_to_json existe no ProjectManager")
            show_snackbar(page, error_msg, ft.Colors.RED, 5000)
        except ValueError as ex:
            error_msg = f"❌ Erro de validação: {ex}"
            print(error_msg)
            show_snackbar(page, error_msg, ft.Colors.RED, 5000)
        except Exception as ex:
            error_msg = f"❌ Erro inesperado: {ex}"
            print(f"❌ Exception during DevOps upload: {ex}")
            import traceback
            print(traceback.format_exc())
            show_snackbar(page, error_msg, ft.Colors.RED, 5000)

    upload_devops_btn = ft.ElevatedButton(
        "Upload to DevOps",
        icon=ft.Icons.CLOUD_UPLOAD,
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE,
        on_click=on_upload_devops,
    )

    def save_project(e):
        """Validate and save the current project data to storage."""
        if not project_name.value:
            error_dlg = ft.AlertDialog(modal=True, title=ft.Text("Error"), content=ft.Text("Please enter a project name!"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(error_dlg))], actions_alignment=ft.MainAxisAlignment.END)
            page.open(error_dlg)
            return

        # Calculate total before saving
        total = 0.0
        for s in steps:
            try:
                h = float(s["hours"].value or 0)
            except Exception:
                h = 0.0
            total += h

        project_data = {
            "name": project_name.value,
            "architect": architect.value or "N/A",
            "area": area.value or "N/A",
            "demand": demand.value or "N/A",
            "purpose": purpose.value or "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "steps": [
                {
                    "name": s["name"].value,
                    "description": s["description"].value,
                    "hours": float(s["hours"].value or 0)
                }
                for s in steps
            ],
            "total": total,
        }

        existing = next((p for p in projects if p["name"] == project_data["name"]), None)
        if existing:
            projects.remove(existing)
        projects.append(project_data)

        save_projects(projects)
        existing_projects_dropdown.options = [ft.dropdown.Option("Create New Project")] + [ft.dropdown.Option(p["name"]) for p in projects]
        page.update()

        success_dlg = ft.AlertDialog(modal=True, title=ft.Text("Success", color=ft.Colors.GREEN_700), content=ft.Text(f"Project '{project_name.value}' saved successfully!"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dlg))], actions_alignment=ft.MainAxisAlignment.END)
        page.open(success_dlg)

    # FilePicker to save PDF
    def on_save_pdf_result(e: ft.FilePickerResultEvent):
        if not e.path:
            return

        try:
            from core.pdf_generator import generate_pdf as pdf_gen

            # Calculate total just before PDF generation
            total = 0.0
            for s in steps:
                try:
                    h = float(s["hours"].value or 0)
                except Exception:
                    h = 0.0
                total += h

            project_data = {
                "name": project_name.value,
                "architect": architect.value or "N/A",
                "area": area.value or "N/A",
                "demand": demand.value or "N/A",
                "purpose": purpose.value or "",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "steps": [
                    {
                        "name": s["name"].value,
                        "description": s["description"].value,
                        "hours": float(s["hours"].value or 0)
                    }
                    for s in steps
                ],
                "total": total,
            }

            pdf_path = pdf_gen(project_data, e.path)

            success_dlg = ft.AlertDialog(modal=True, title=ft.Text("Success", color=ft.Colors.GREEN_700), content=ft.Text(f"PDF generated successfully!\n\nSaved at:\n{pdf_path}"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dlg))], actions_alignment=ft.MainAxisAlignment.END)
            page.open(success_dlg)

        except Exception as ex:
            error_dlg = ft.AlertDialog(modal=True, title=ft.Text("Error"), content=ft.Text(f"Failed to generate PDF:\n\n{str(ex)}"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(error_dlg))], actions_alignment=ft.MainAxisAlignment.END)
            page.open(error_dlg)

    save_pdf_dialog = ft.FilePicker(on_result=on_save_pdf_result)
    page.overlay.append(save_pdf_dialog)

    def generate_pdf(e):
        """Validate UI state and request the save dialog to generate the PDF."""
        if not project_name.value:
            error_dlg = ft.AlertDialog(modal=True, title=ft.Text("Error"), content=ft.Text("Please enter a project name before generating PDF!"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(error_dlg))], actions_alignment=ft.MainAxisAlignment.END)
            page.open(error_dlg)
            return

        if not steps:
            error_dlg = ft.AlertDialog(modal=True, title=ft.Text("Error"), content=ft.Text("Please add at least one step before generating PDF!"), actions=[ft.TextButton("OK", on_click=lambda e: page.close(error_dlg))], actions_alignment=ft.MainAxisAlignment.END)
            page.open(error_dlg)
            return

        pdf_filename = f"{project_name.value.replace(' ', '_')}_estimate.pdf"
        save_pdf_dialog.save_file(file_name=pdf_filename, allowed_extensions=["pdf"], dialog_title="Save PDF As")

    save_btn = ft.ElevatedButton("Save", icon=ft.Icons.SAVE, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, on_click=save_project)
    pdf_btn = ft.ElevatedButton("Generate PDF", icon=ft.Icons.PICTURE_AS_PDF, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, on_click=generate_pdf)
    devops_btn = ft.ElevatedButton(
        "Upload to DevOps",
        icon=ft.Icons.CLOUD_UPLOAD,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=on_upload_devops
    )

    # ---------- Layout ----------
    header = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Container(ft.Icon(ft.Icons.BUILD_CIRCLE_ROUNDED, color=ft.Colors.WHITE, size=24), padding=6, border_radius=6, bgcolor=ft.Colors.BLUE_600),
                    ft.Text("Project Estimator", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                ], spacing=8),
                ft.Container(expand=True),
                ft.Container(content=ft.Image(src="BallLogo.png", width=62, height=40, fit=ft.ImageFit.CONTAIN), padding=ft.padding.symmetric(horizontal=16, vertical=6), border_radius=6),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=12,
        border_radius=ft.border_radius.only(top_left=8, top_right=8),
    )

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

    steps_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Steps", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.BLUE_600, icon_size=24, tooltip="Add step", on_click=on_add_step),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Container(content=ft.Column([steps_column], scroll=ft.ScrollMode.AUTO), expand=True, padding=8),
        ], spacing=8, expand=True),
        padding=12,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        expand=True,
    )

    templates_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Templates", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.BLUE_600, icon_size=24, tooltip="Add template", on_click=add_template_dialog),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            template_search,
            ft.Container(content=ft.Column([templates_column], scroll=ft.ScrollMode.AUTO), expand=True, padding=8),
        ], spacing=8, expand=True),
        padding=12,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        expand=True,
    )

    footer = ft.Container(content=ft.Row([save_btn, pdf_btn, devops_btn], spacing=12, alignment=ft.MainAxisAlignment.END), padding=12, bgcolor=ft.Colors.GREY_50, border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8))

    main_container = ft.Container(
        content=ft.Column([
            header,
            ft.Container(content=ft.Column([project_details_card, ft.Container(content=ft.ResponsiveRow([ft.Container(steps_card, col={"sm": 12, "md": 12, "lg": 8}), ft.Container(templates_card, col={"sm": 12, "md": 12, "lg": 4})]), expand=True), footer], spacing=12, expand=True), padding=12, bgcolor=ft.Colors.GREY_50, expand=True),
        ], spacing=0, expand=True),
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        border=ft.border.all(2, ft.Colors.GREY_400),
        expand=True,
    )

    page.add(main_container)
    page.update()
