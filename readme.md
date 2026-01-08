# Project Estimator - Complete Guide

## Overview

**Project Estimator** is a desktop application for creating and managing project estimates with time tracking and DevOps integration. Built with Flet (Python UI framework), it provides an intuitive interface to define project steps, estimate hours, generate PDF reports, and upload projects directly to Azure DevOps.

---

## How It Works

### Architecture

The application follows a modular architecture:

```
main.py
├── ui/main_view.py              (Flet UI - forms, dialogs, layout)
├── core/
│   ├── project_manager.py       (Load/save projects as JSON)
│   ├── pdf_generator.py         (PDF report generation)
│   └── helpers/
│       ├── devops_client.py     (Azure DevOps API integration)
│       ├── template_utils.py    (Template CRUD operations)
│       ├── dialog_utils.py      (Dialog helpers)
│       ├── ui_utils.py          (UI utilities like snackbars)
│       └── project_utils.py     (Project initialization)
└── data/
    ├── projects.json            (Stored projects)
    └── templates.json           (Reusable step templates)
```

### Data Flow

1. **UI Layer** (main_view.py) - Renders forms and captures user input
2. **Business Logic** - ProjectManager, template management, PDF generation
3. **External Integration** - DevOps API client for work item creation
4. **Storage** - JSON files (projects.json, templates.json)

### Key Technologies

- **Flet 0.28.3** - Cross-platform desktop UI
- **FPDF2 2.8.4** - PDF generation
- **Requests** - HTTP client for Azure DevOps API
- **Python-dotenv** - Environment variable management
- **Azure DevOps REST API** - Work item integration

---

## How to Use

### Starting the Application

```bash
python main.py
```

The app opens with a window (1200x800 minimum 800x600) displaying three main sections: Project Details, Steps, and Templates.

---

### Creating a Project

#### Step 1: Enter Project Details

Fill in the following fields in the **Project Details** card:

| Field | Required | Notes |
|-------|----------|-------|
| Project | ✓ | Project name (identifier) |
| Solution Architect | - | Name of the solution architect |
| Area | - | Project area or department |
| Demand Number | - | Internal demand/request ID |
| Purpose | - | Project description (multiline) |

#### Step 2: Add Steps (Tasks/Features)

Click the **+** icon in the Steps section to add work items:

1. **Name** - Step/task name (auto-saved as template)
2. **Type** - Choose: Feature, User Story, or Task
3. **Parent** - Link to parent step (auto-populated based on hierarchy)
4. **Hours** - Estimated hours for completion
5. **Description** (optional) - Click the description icon to expand/edit details

**Hierarchy Rules:**
- User Stories can have Feature parents
- Tasks can have User Story parents
- Features are top-level items

#### Step 3: Save the Project

Click **Save** to store the project. Once saved:
- Project appears in the "Existing Projects" dropdown
- Data persists in `projects.json`
- Can be loaded later from the dropdown

---

### Working with Templates

Templates are reusable step configurations that auto-save when you edit a step.

#### Adding a Step from Template

1. Search templates by name in the template search box
2. Click the **+** button next to a template
3. Template auto-fills into a new step with name, description, and hours

#### Creating a New Template

Click the **+** icon in the Templates section:

1. Enter template name (required)
2. Add description (optional)
3. Set default hours
4. Click Save

The template is stored in `templates.json`.

#### Managing Templates

- **Edit** (pencil icon) - Modify name, description, or hours
- **Delete** (trash icon) - Remove template permanently
- **Search** - Filter templates by name in real-time

**Auto-Save Feature:**
When you edit a step's name, description, or hours, it's automatically saved as a template if one doesn't exist, or updates the existing template.

---

### Generating PDF Report

1. Fill in all project details and add at least one step
2. Click **Generate PDF**
3. Choose save location and filename
4. PDF is generated with:
   - Ball Corporation logo
   - Project name, architect, area, demand, purpose
   - Three-column table: Task | Description | Hours
   - Total hours summary
   - Page numbers and footer

---

### Uploading to Azure DevOps

#### Prerequisites

Create a `.env` file in the project root:

```env
DEVOPS_ORG=YourOrganizationName
DEVOPS_PROJECT=YourProjectName
DEVOPS_PAT=your_personal_access_token
```

**Get a PAT (Personal Access Token):**
1. Go to Azure DevOps organization settings
2. Personal access tokens → New Token
3. Scopes: Work Items (read & write), Code (read)
4. Copy the token and add to `.env`

#### Uploading

Click **Upload to DevOps** to:

1. Validate project name and steps exist
2. Create an Epic (main work item)
3. Create Features under the Epic
4. Create User Stories under Features
5. Create Tasks under User Stories

**Result:**
- Epic ID is displayed
- All work items linked hierarchically
- Hours transferred to Azure DevOps

---

## UI Components Reference

### Project Details Card
- Dropdown to load existing projects or create new
- Text fields for project metadata
- Multiline purpose field

### Steps Section
- List of added steps with inline editing
- Type selector (Feature/User Story/Task)
- Parent dropdown (auto-filtered by hierarchy)
- Hours input (auto-updates total)
- Description toggle button
- Remove button

### Templates Section
- Search box for filtering templates
- Template list with hours display
- Quick-add, edit, delete buttons
- Auto-save from steps when names are entered

### Footer
- **Save** - Save current project to storage
- **Generate PDF** - Create PDF report
- **Upload to DevOps** - Push to Azure DevOps

---

## File Structure

### Data Files

**projects.json** - List of saved projects
```json
[
  {
    "name": "Project Name",
    "architect": "Name",
    "area": "Area",
    "demand": "DEM-001",
    "purpose": "Description",
    "date": "2026-01-06",
    "total": 40.0,
    "steps": [
      {
        "name": "Step 1",
        "description": "Details",
        "hours": 8.0
      }
    ]
  }
]
```

**templates.json** - Reusable step templates
```json
[
  {
    "name": "Design",
    "description": "UI/UX design work",
    "hours": "16"
  }
]
```

### Configuration
- **main.spec** / **ProjectEstimator.spec** - PyInstaller specs for building exe

---

## Common Tasks

### Load a Previous Project
1. Click the "Existing Projects" dropdown
2. Select project name
3. All data auto-fills (steps, hours, metadata)

### Add Multiple Steps Quickly
1. Use templates - search and click **+**
2. Modify names/hours as needed
3. Auto-saves to templates for reuse

### Update Hours and See Total Instantly
- Type hours in any step
- Total updates automatically in real-time

### Hierarchy: Feature → User Story → Task
1. Create Feature (no parent)
2. Create User Story, select Feature as parent
3. Create Task, select User Story as parent
4. DevOps upload respects this structure

### Change Project Type Later
1. Click "Existing Projects" → select project
2. Edit fields and steps
3. Click Save (overwrites existing)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "DevOps PAT not configured" | Check `.env` file exists with DEVOPS_PAT value |
| PDF not generating | Ensure project name and at least 1 step exist |
| Templates not saving | Auto-save requires step name to be non-empty |
| DevOps upload fails | Verify organization, project, and PAT in `.env` |
| Projects won't load | Check `data/projects.json` exists and is valid JSON |
| Steps disappear on reload | Project must be saved via Save button first |

---

## Architecture Details

### ProjectManager
- Manages projects list persistence
- Thread-safe save operations
- Handles both list and dict JSON formats
- Auto-creates directories and files

### PDF Generator
- Custom FPDF subclass with header/footer
- Renders Ball logo, project metadata, step table
- Supports multiline descriptions
- Auto-page-break management

### DevOps Client
- Azure DevOps REST API wrapper
- Converts project hierarchy to work items
- Handles authentication with PAT
- Creates Epic → Feature → User Story → Task structure

### Template Utilities
- Load/save templates to JSON
- Case-insensitive template lookup
- Support for update or insert

---

## Environment Variables

| Variable | Example | Required |
|----------|---------|----------|
| DEVOPS_ORG | BallCorporation | Yes (for DevOps) |
| DEVOPS_PROJECT | Automation and Digital Adoption | Yes (for DevOps) |
| DEVOPS_PAT | xxxxxxxxxxx | Yes (for DevOps) |

---

## Development

### Adding a New Feature

1. **UI Changes** → Edit `ui/main_view.py`
2. **Data Handling** → Update `core/project_manager.py` or helpers
3. **PDF Changes** → Modify `core/pdf_generator.py`
4. **DevOps Changes** → Update `core/helpers/devops_client.py`

### Building Executable

**Option 1: Using PyInstaller Spec File**

```bash
pyinstaller ProjectEstimator.spec
```

Output: `build/ProjectEstimator/ProjectEstimator.exe`

**Option 2: Full Command with All Dependencies**

```bash
pyinstaller --name ProjectEstimator --onedir --windowed --hidden-import=flet --hidden-import=flet.app --hidden-import=flet_js --hidden-import=flet_web.fastapi --hidden-import=flet_cli --hidden-import=httpx --hidden-import=anyio --hidden-import=PIL --hidden-import=fontTools --hidden-import=numpy --collect-all flet --collect-all httpx --collect-all anyio --add-data "%VIRTUAL_ENV%\Lib\site-packages\flet_desktop\app\flet;flet_desktop\app\flet" main.py
```

**Notes:**
- `%VIRTUAL_ENV%` automatically points to your active virtual environment
- Replace with your venv path if using a different Python environment
- Command is OS-independent when using environment variables

**Command Flags:**
- `--onedir` - Creates single directory with all dependencies
- `--windowed` - No console window (desktop app)
- `--hidden-import` - Explicitly includes modules not detected automatically
- `--collect-all` - Collects all files from specified packages
- `--add-data` - Includes Flet desktop app resources

Output: `dist/ProjectEstimator/ProjectEstimator.exe`

---

## License & Credits

Built with Flet, FPDF2, and Python. Integrates with Azure DevOps.

For support, check `.env` configuration and validate JSON data files.

