"""
Module: pdf_generator
Function: Generates a professional project estimate PDF using the FPDF library.

Expected structure of the `project` dictionary:
{
    'name': str,
    'architect': str,
    'area': str,
    'demand': str,
    'purpose': str,
    'steps': [ {'name': str, 'hours': float}, ... ],
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

        # Add Ball logo in the top right corner
        try:
            # Get logo path relative to the project root
            logo_path = os.path.join(os.path.dirname(__file__), '..', 'BallLogo.png')
            if os.path.exists(logo_path):
                # Position: x=170 (top right), y=5, width=35mm, height will be auto
                self.image(logo_path, x=170, y=5, w=35)
        except Exception as e:
            # If logo fails to load, continue without it
            pass

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
    architect = project.get('architect', 'N/A')
    area = project.get('area', 'N/A')
    demand = project.get('demand', 'N/A')
    purpose = project.get('purpose', 'N/A')
    steps = project.get('steps', []) or []

    # Calculate total
    total = 0
    try:
        total = sum((float(s.get('hours', 0)) for s in steps))
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

    # PROJECT INFORMATION SECTION
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(17, 64, 254)
    pdf.cell(0, 8, 'PROJECT INFORMATION', 0, 1, 'L')
    pdf.ln(2)

    # Information boxes - Row 1
    current_y = pdf.get_y()
    pdf.add_info_box('Demand ID', demand, 10, current_y, 90)
    pdf.add_info_box('Area', area, 105, current_y, 95)
    pdf.ln(18)

    # Information boxes - Row 2
    current_y = pdf.get_y()
    pdf.add_info_box('Solution Architect', architect, 10, current_y, 200)
    pdf.ln(18)

    # Purpose section with full width
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(17, 64, 254)
    pdf.cell(0, 6, 'Purpose:', 0, 1, 'L')

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(26, 26, 26)

    # Purpose with light background
    pdf.set_fill_color(245, 245, 245)
    pdf.set_draw_color(17, 64, 254)
    pdf.set_line_width(0.5)

    # Calculate height needed for purpose text
    purpose_text = purpose if purpose and purpose != 'N/A' else 'No purpose specified'
    pdf.multi_cell(0, 5, purpose_text, 1, 'L', True)
    pdf.ln(3)

    # Steps Section Title in Ball Blue
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(17, 64, 254)
    pdf.cell(0, 10, 'PROJECT BREAKDOWN', 0, 1, 'L')
    pdf.ln(2)

    # Table Header with Ball Blue background
    pdf.set_fill_color(17, 64, 254)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 10)

    # Header row - 3 columns: Task, Description, Hours
    pdf.cell(50, 10, 'Task', 1, 0, 'L', True)
    pdf.cell(80, 10, 'Description', 1, 0, 'L', True)
    pdf.cell(40, 10, 'Hours', 1, 1, 'C', True)

    # Table Body with Charcoal text
    pdf.set_text_color(26, 26, 26)
    pdf.set_font('Arial', '', 9)

    if not steps:
        pdf.set_fill_color(250, 250, 250)
        pdf.cell(170, 10, 'No tasks recorded for this project.', 1, 1, 'C', True)
    else:
        # Alternating row colors for better readability
        fill = False
        for step in steps:
            step_name = step.get('name', 'Unnamed task')
            step_description = step.get('description', '')
            hours = float(step.get('hours', 0)) if step.get('hours') else 0

            if fill:
                pdf.set_fill_color(245, 245, 245)  # Light grey
            else:
                pdf.set_fill_color(255, 255, 255)  # White

            # Use a simple approach: single-line cells for now
            # If description is too long, truncate it
            max_desc_len = 35
            desc_display = step_description[:max_desc_len] if step_description else '-'

            pdf.cell(50, 8, step_name[:25], 1, 0, 'L', True)
            pdf.cell(80, 8, desc_display, 1, 0, 'L', True)
            pdf.cell(40, 8, f'{hours:.1f}h', 1, 1, 'C', True)
            fill = not fill

    # Total Section with Ball Blue background
    pdf.ln(5)
    pdf.set_fill_color(17, 64, 254)  # Ball Blue
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 13)

    pdf.cell(50, 12, '', 1, 0, 'R', True)  # Task column
    pdf.cell(80, 12, 'TOTAL ESTIMATED HOURS', 1, 0, 'R', True)  # Description column
    pdf.cell(40, 12, f'{total:.1f}h', 1, 1, 'C', True)  # Hours column

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
