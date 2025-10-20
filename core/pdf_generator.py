"""
Module: pdf_generator
Function: Generates a simple project estimate PDF using the FPDF library.

Expected structure of the `project` dictionary (English keys only):
{
    'name': str,
    'client': str,
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


def generate_pdf(project: Dict[str, Any], destination: str = "estimate.pdf") -> str:
    """Generate a PDF containing project estimate data using English keys only.

    Returns the absolute path of the generated file.
    """
    # Initialize FPDF and add a page
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Read required fields (English keys only)
    project_name = project.get('name', 'No name')
    client = project.get('client', 'N/A')
    date = project.get('date', 'N/A')

    # Header
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt=f"Estimate - {project_name}", ln=1, align="C")

    # Project info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=f"Client: {client}", ln=1)
    pdf.cell(0, 8, txt=f"Date: {date}", ln=1)

    pdf.ln(6)

    # Steps listing (expects 'steps' list with English keys)
    steps = project.get('steps', []) or []
    pdf.set_font("Arial", size=11)
    if not steps:
        pdf.cell(0, 8, txt="No steps recorded.", ln=1)
    else:
        for step in steps:
            step_name = step.get('name', 'Unnamed step')
            hours = step.get('hours', 0)
            pdf.cell(0, 8, txt=f"{step_name} - {hours}h", ln=1)

    # Total
    total = project.get('total')
    if total is None:
        try:
            total = sum((s.get('hours', 0) for s in steps))
        except Exception:
            total = 0

    pdf.ln(4)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=f"Total: {total}h", ln=1)

    # Save
    try:
        pdf.output(destination)
    except Exception as e:
        raise RuntimeError(f"Failed to generate PDF: {e}")

    return os.path.abspath(destination)
