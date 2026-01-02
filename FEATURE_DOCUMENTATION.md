"""PROJECT ESTIMATOR - FEATURE DOCUMENTATION

This document outlines all the features and capabilities of the Project Estimator application.

========================================
1. PROJECT MANAGEMENT
========================================

Projects consist of:
- Name: Project identifier
- Solution Architect: Person responsible for the project
- Area: Department or area (e.g., IT, IBP)
- Demand Number: Requirement/demand ID for tracking
- Purpose: Detailed description of the project goals
- Date: Creation/modification date
- Steps: List of tasks with hours estimation
- Total: Sum of hours across all steps

Projects are stored in projects.json on the network path (or local fallback).


========================================
2. STEP MANAGEMENT
========================================

Steps (work items) support:
- Name: Task/feature name (required)
- Description: Optional detailed description of what the step entails
- Hours: Estimated hours for completion (required)
- Type: Classification as Feature, User Story, or Task
- Parent: Hierarchical relationship to other steps

KEY FEATURE: Each step can have an optional description that is displayed
in the 3-column report (Task, Description, Hours) in PDF exports.

Steps are automatically saved as reusable templates when modified.


========================================
3. TEMPLATES SYSTEM
========================================

Templates are reusable step configurations stored in templates.json.

Each template includes:
- Name: Template identifier
- Description: Optional details about the step
- Hours: Default estimated hours

Operations:
- Create: Define new templates via the "New Template" dialog
- Add: Apply any template to current project steps
- Edit: Modify template name, description, or hours
- Delete: Remove templates from the system
- Search: Filter templates by name in real-time

Templates automatically appear when creating/modifying steps with matching names,
and descriptions are preserved when templates are applied.


========================================
4. PDF REPORT GENERATION
========================================

The PDF report includes:

**Header Section:**
- Application logo
- Project title and subtitle

**Project Information:**
- Demand ID
- Area/Department
- Solution Architect
- Purpose/Goals

**Project Breakdown (3-Column Table):**
- Column 1: Task (step name)
- Column 2: Description (optional description from step)
- Column 3: Hours (estimated hours for completion)

**Summary:**
- Total Estimated Hours (sum of all steps)

**Footer:**
- Disclaimer about estimation accuracy
- Page numbers


========================================
5. AZURE DEVOPS INTEGRATION
========================================

The "Upload to DevOps" feature creates a hierarchical work item structure:

Structure:
Epic (top-level)
  ├─ Features (created from Feature type steps)
  │   └─ User Stories (created from User Story type steps)
  │       └─ Tasks (created from Task type steps)

Process:
1. Validates project has name and at least one step
2. Creates Epic with demand ID and project name
3. Creates Features and links them to Epic
4. Creates User Stories and links them to parent Features
5. Creates Tasks and links them to parent User Stories
6. Sets task hours in "Original Estimate" field

Requirements:
- .env file with DevOps configuration:
  DEVOPS_ORG: Organization name
  DEVOPS_PROJECT: Project name
  DEVOPS_PAT: Personal Access Token


========================================
6. DATA STORAGE
========================================

Two JSON files store application data:

**projects.json:**
- List of all projects
- Each project contains all steps with names, descriptions, and hours
- Location: Network path or local fallback
- Auto-created if missing

**templates.json:**
- List of reusable step templates
- Each template includes name, description, and default hours
- Location: Network path or local fallback
- Auto-created if missing

Network Configuration:
- Primary: \\Nadc1rpaorcfs01\DEV\ProjectEstimatorApp
- Fallback: Local data directory if network is unavailable


========================================
7. KEY FIXES AND IMPROVEMENTS
========================================

✅ Save Functionality:
- Fixed: Projects now correctly save to JSON files
- Fixed: load_projects() always returns a list (handles dict edge case)
- Ensures compatibility with both network and local storage

✅ Full English Documentation:
- All code documented in English
- Method names in English (with Portuguese aliases for backwards compatibility)
- Clear docstrings and inline comments

✅ Description Support:
- Steps support optional descriptions
- Templates support optional descriptions
- Descriptions appear in PDF reports (3-column format)
- Descriptions persist when templates are reused

✅ Report Generation:
- 3-column format: Task | Description | Hours
- Automatic total hours calculation
- Professional PDF styling with logo
- Proper error handling


========================================
8. USER INTERFACE
========================================

Main Sections:
1. Project Details Card
   - Existing projects dropdown
   - Project name field
   - Solution Architect field
   - Area field
   - Demand number field
   - Purpose/goals field

2. Steps Card
   - Add step button
   - List of current steps
   - Each step shows: Name | Type | Parent | Hours | Delete button
   - Description field for each step
   - Total hours display

3. Templates Card
   - Search templates by name
   - Add template button
   - Template list showing: Name | Hours | Actions (Add, Edit, Delete)
   - New Template dialog

4. Action Buttons
   - Save: Persist project to storage
   - Generate PDF: Create estimate report
   - Upload to DevOps: Create work items in Azure DevOps


========================================
9. ERROR HANDLING
========================================

The application includes comprehensive error handling for:
- Missing project names
- Missing steps
- Invalid hours input
- Network path unavailability
- DevOps API errors
- File I/O errors
- Invalid parent-child relationships in DevOps upload


========================================
10. BACKWARDS COMPATIBILITY
========================================

Portuguese Method Alias:
- criar_estrutura_desde_json() → create_structure_from_json()
  Old Portuguese method still works for backwards compatibility


========================================
FILE STRUCTURE
========================================

Project_Estimator_PY/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── BallLogo.png                     # Application logo
├── data/
│   ├── projects.json               # Stored projects
│   └── templates.json              # Stored templates
├── core/
│   ├── config.py                   # Configuration and paths
│   ├── project_manager.py          # Project persistence logic
│   ├── pdf_generator.py            # PDF report generation
│   └── helpers/
│       ├── project_utils.py        # Project load/save helpers
│       ├── template_utils.py       # Template load/save helpers
│       ├── devops_client.py        # Azure DevOps integration
│       ├── dialog_utils.py         # Dialog helpers
│       ├── ui_utils.py             # UI utility functions
└── ui/
    └── main_view.py                # Main application UI


========================================
DEPENDENCIES
========================================

Key Libraries:
- flet: UI framework
- fpdf: PDF generation
- requests: HTTP client for DevOps API
- python-dotenv: Environment variable management


========================================
ENVIRONMENT VARIABLES (.env)
========================================

DEVOPS_ORG=BallCorporation
DEVOPS_PROJECT=Automation and Digital Adoption
DEVOPS_PAT=<your_personal_access_token>

"""

