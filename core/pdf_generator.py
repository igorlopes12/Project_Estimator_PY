"""
Module: pdf_generator
Function: Generates a professional project estimate PDF using the FPDF library.

Expected structure of the `project` dictionary (English keys only):
{
    'name': str,
    'developer': str,
    'date': str,
    'steps': [ {'name': str, 'hours': float}, ... ],
    'total': float
}

The function returns the absolute path of the generated file.
"""

# Required imports
from fpdf import FPDF
import os
from typing import Dict, Any


class ProfessionalPDF(FPDF):
    """Custom PDF class with Ball Corporation brand styling"""

    def header(self):
        """Professional header with Ball Corporation branding"""
        # Ball Blue header background (RGB: 17/64/254)
        self.set_fill_color(17, 64, 254)
        self.rect(0, 0, 210, 40, 'F')

        # Title in white
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 24)
        self.cell(0, 20, 'PROJECT ESTIMATE', 0, 1, 'C')

        # Subtitle
        self.set_font('Arial', '', 10)
        self.set_text_color(240, 240, 240)
        self.cell(0, 5, 'Professional Time & Cost Analysis', 0, 1, 'C')

        # Reset text color to Charcoal
        self.set_text_color(26, 26, 26)
        self.ln(15)

    def footer(self):
        """Professional footer with Ball Grey"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(140, 142, 148)  # Ball Grey
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_info_box(self, label: str, value: str, x: float, y: float, width: float = 85):
        """Add a styled information box with Ball brand colors"""
        # Light grey background
        self.set_fill_color(245, 245, 245)
        self.rect(x, y, width, 15, 'F')

        # Ball Blue border
        self.set_draw_color(17, 64, 254)
        self.set_line_width(0.5)
        self.rect(x, y, width, 15, 'D')

        # Label (bold) in Ball Blue
        self.set_xy(x + 3, y + 3)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(17, 64, 254)
        self.cell(0, 4, label, 0, 1)

        # Value in Charcoal
        self.set_xy(x + 3, y + 8)
        self.set_font('Arial', '', 11)
        self.set_text_color(26, 26, 26)
        self.cell(0, 4, value, 0, 1)

        # Reset line width
        self.set_line_width(0.2)


def generate_pdf(project: Dict[str, Any], destination: str = "estimate.pdf") -> str:
    """Generate a professional PDF with Ball Corporation brand colors.

    Returns the absolute path of the generated file.
    """
    # Initialize custom PDF
    pdf = ProfessionalPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Read required fields
    project_name = project.get('name', 'Untitled Project')
    developer = project.get('developer', 'N/A')
    date_str = project.get('date', 'N/A')
    steps = project.get('steps', []) or []

    # Calculate total
    total = project.get('total')
    if total is None:
        try:
            total = sum((s.get('hours', 0) for s in steps))
        except (TypeError, ValueError, KeyError):
            total = 0

    # Project Title Section in Ball Blue
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(17, 64, 254)  # Ball Blue
    pdf.cell(0, 10, project_name, 0, 1, 'L')

    # Divider line in Ball Blue
    pdf.set_draw_color(17, 64, 254)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Information boxes
    current_y = pdf.get_y()
    pdf.add_info_box('Developer', developer, 10, current_y, 90)
    pdf.add_info_box('Date', date_str, 105, current_y, 95)
    pdf.ln(20)

    # Steps Section Title in Ball Blue
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(17, 64, 254)
    pdf.cell(0, 10, 'PROJECT BREAKDOWN', 0, 1, 'L')
    pdf.ln(2)

    # Table Header with Ball Blue background
    pdf.set_fill_color(17, 64, 254)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 11)

    # Header row
    pdf.cell(150, 10, 'Task Description', 1, 0, 'L', True)
    pdf.cell(40, 10, 'Hours', 1, 1, 'C', True)

    # Table Body with Charcoal text
    pdf.set_text_color(26, 26, 26)
    pdf.set_font('Arial', '', 10)

    if not steps:
        pdf.set_fill_color(250, 250, 250)
        pdf.cell(190, 10, 'No tasks recorded for this project.', 1, 1, 'C', True)
    else:
        # Alternating row colors for better readability
        fill = False
        for step in steps:
            step_name = step.get('name', 'Unnamed task')
            hours = step.get('hours', 0)

            if fill:
                pdf.set_fill_color(245, 245, 245)  # Light grey
            else:
                pdf.set_fill_color(255, 255, 255)  # White

            pdf.cell(150, 8, step_name, 1, 0, 'L', True)
            pdf.cell(40, 8, f'{hours:.1f}h', 1, 1, 'C', True)
            fill = not fill

    # Total Section with Ball Blue background
    pdf.ln(5)
    pdf.set_fill_color(17, 64, 254)  # Ball Blue
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 13)

    pdf.cell(150, 12, 'TOTAL ESTIMATED HOURS', 1, 0, 'R', True)
    pdf.cell(40, 12, f'{total:.1f}h', 1, 1, 'C', True)

    # Summary box at bottom with Ball Grey text
    pdf.ln(10)
    pdf.set_text_color(140, 142, 148)  # Ball Grey
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5,
        'This estimate represents the projected time required to complete the tasks outlined above. '
        'Actual hours may vary based on project complexity and unforeseen requirements.',
        0, 'L')

    # Save PDF
    try:
        pdf.output(destination)
    except (IOError, OSError) as e:
        raise RuntimeError(f"Failed to generate PDF: {e}") from e

    return os.path.abspath(destination)
