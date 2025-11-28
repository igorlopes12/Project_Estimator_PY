"""core/pdf_generator.py

Generate a minimal PDF estimate report from project data using FPDF.
The generated report contains project info and a three-column breakdown: Task,
Description and Hours (as requested by the user).
"""

from fpdf import FPDF
import os
from typing import Dict, Any


class BallMinimalPDF(FPDF):
    """Small helper subclass to render common header/footer elements."""
    def header(self):
        # --- LOGO ---
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "..", "BallLogo.png")
            if os.path.exists(logo_path):
                self.image(logo_path, x=170, y=10, w=25)
        except:
            pass

        # --- TITLE ---
        self.set_xy(10, 15)
        self.set_font("Arial", "B", 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, "Project Estimate", ln=1, align="L")

        # --- SUBTITLE ---
        self.set_font("Arial", "", 10)
        self.set_text_color(90, 90, 90)
        self.cell(0, 5, "Project Time & Cost Analysis", ln=1)

        # --- SEPARATOR LINE ---
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.2)
        self.line(10, 33, 200, 33)

        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def generate_pdf(project: Dict[str, Any], destination="estimate.pdf") -> str:
    """Generate a PDF file from a project dictionary.

    The report includes a three-column table (Task, Description, Hours) and a
    total hours line. The destination path is returned as an absolute path.

    Args:
        project: Dictionary containing project fields and a 'steps' list.
        destination: Output PDF file path.

    Returns:
        Absolute path to the saved PDF file.
    """
    pdf = BallMinimalPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Extract input
    name = project.get("name", "Untitled Project")
    architect = project.get("architect", "N/A")
    area = project.get("area", "N/A")
    demand = project.get("demand", "N/A")
    purpose = project.get("purpose", "No purpose specified")
    steps = project.get("steps", []) or []

    # --- PROJECT NAME ---
    pdf.set_font("Arial", "B", 15)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, name, ln=1)
    pdf.ln(4)

    # --- PROJECT INFO ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Project Information", ln=1)
    pdf.ln(1)

    pdf.set_font("Arial", "", 11)
    line_height = 6

    def info_row(label, value):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(45, line_height, f"{label}:", ln=0)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, line_height, value, ln=1)

    info_row("Demand ID", demand)
    info_row("Area", area)
    info_row("Solution Architect", architect)

    pdf.ln(6)

    # --- PURPOSE ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Purpose", ln=1)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, purpose)
    pdf.ln(4)

    # --- BREAKDOWN ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Project Breakdown", ln=1)
    pdf.ln(1)

    # Column widths (clean Ball style)
    w_task = 60
    w_desc = 80
    w_hours = 30

    # HEADER
    pdf.set_font("Arial", "B", 11)
    pdf.set_draw_color(160, 160, 160)
    pdf.set_line_width(0.25)

    pdf.cell(w_task, 8, "Task", border="B")
    pdf.cell(w_desc, 8, "Description", border="B")
    pdf.cell(w_hours, 8, "Hours", border="B", ln=1, align="R")

    # BODY
    pdf.set_font("Arial", "", 11)
    total_hours = 0

    for step in steps:
        task = step.get("name", "")
        desc = step.get("description", "") or "-"
        hours = float(step.get("hours") or 0)
        total_hours += hours

        pdf.cell(w_task, 7, task)
        pdf.cell(w_desc, 7, desc)
        pdf.cell(w_hours, 7, f"{hours:.1f}", ln=1, align="R")

    pdf.ln(4)

    # --- TOTAL ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(w_task + w_desc, 8, "Total Estimated Hours")
    pdf.cell(w_hours, 8, f"{total_hours:.1f}", ln=1, align="R")

    pdf.ln(10)

    # --- DISCLAIMER ---
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        5,
        "This estimate represents the projected hours for task execution. "
        "Actual requirements may vary depending on process complexity."
    )

    pdf.output(destination)
    return os.path.abspath(destination)
