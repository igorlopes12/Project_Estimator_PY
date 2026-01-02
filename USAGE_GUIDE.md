# Project Estimator - Usage Guide & Code Examples

## Quick Start Guide

### 1. Running the Application

```bash
cd C:\Users\ilopes\PycharmProjects\Project_Estimator_PY
python main.py
```

The application will:
- Check network path availability
- Fall back to local storage if needed
- Load existing projects and templates
- Display the main UI

### 2. Creating Your First Project

**Step-by-step:**

1. **Enter Project Information**
   - Project Name: "Website Redesign"
   - Solution Architect: "John Smith"
   - Area: "Marketing"
   - Demand Number: "DMND-2025-001"
   - Purpose: "Complete redesign of company website for better user experience"

2. **Add Steps (Tasks)**
   - Click the "Add Step" button
   
   **Step 1:**
   - Task: "Requirements & Discovery"
   - Description: "Gather requirements from stakeholders and competitors"
   - Hours: 20
   
   **Step 2:**
   - Task: "Design Mockups"
   - Description: "Create wireframes and visual designs for all pages"
   - Hours: 32
   
   **Step 3:**
   - Task: "Front-end Development"
   - Description: "Build responsive HTML/CSS/JavaScript components"
   - Hours: 80
   
   **Step 4:**
   - Task: "Testing & QA"
   - Description: "Test across browsers, devices, and accessibility"
   - Hours: 24

3. **Save the Project**
   - Click "Save" button
   - See confirmation message
   - Project now available in dropdown for future editing

### 3. Working with Templates

**Create a Reusable Template:**

1. Click "Add Template"
2. Fill in details:
   - Template Name: "Code Review"
   - Description: "Review code for quality and standards compliance"
   - Hours: 4
3. Click "Save"

**Use Template in Project:**

1. In your project, click "Add Step"
2. Type "Code Review" in the task field
3. Notice template appears in sidebar
4. Click the green "Add" button on the template
5. Description and hours automatically apply
6. Step is added to project

---

## Code Examples

### Example 1: Loading Projects Programmatically

```python
from core.helpers.project_utils import load_projects

# Load all projects
projects = load_projects()

# Always returns a list (never dict)
print(f"Found {len(projects)} projects")

# Access project data
for project in projects:
    print(f"Project: {project['name']}")
    print(f"  Architect: {project['architect']}")
    print(f"  Total Hours: {project['total']}")
    print(f"  Steps: {len(project['steps'])}")
```

### Example 2: Saving a New Project

```python
from core.helpers.project_utils import load_projects, save_projects
from datetime import datetime

# Load existing projects
projects = load_projects()

# Create new project
new_project = {
    "name": "Mobile App Development",
    "architect": "Sarah Johnson",
    "area": "Engineering",
    "demand": "DMND-2025-045",
    "purpose": "Build iOS and Android mobile app for customer engagement",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "steps": [
        {
            "name": "App Design",
            "description": "Design UI/UX for iOS and Android platforms",
            "hours": 40.0
        },
        {
            "name": "API Development",
            "description": "Build REST API backend for mobile app",
            "hours": 60.0
        },
        {
            "name": "Mobile Development",
            "description": "Implement app features for both platforms",
            "hours": 100.0
        }
    ],
    "total": 200.0
}

# Add to projects
projects.append(new_project)

# Save back to storage
save_projects(projects)

print("Project saved successfully!")
```

### Example 3: Creating a Template with Description

```python
from core.helpers.template_utils import load_templates, save_templates

# Load templates
templates = load_templates()

# Create new template
new_template = {
    "name": "Security Audit",
    "description": "Complete security assessment and penetration testing",
    "hours": "16"
}

# Add to templates
templates.append(new_template)

# Save
save_templates(templates)

print(f"Template '{new_template['name']}' created successfully!")
```

### Example 4: Generating PDF Report

```python
from core.pdf_generator import generate_pdf

# Project data with steps that have descriptions
project = {
    "name": "Website Redesign",
    "architect": "John Smith",
    "area": "Marketing",
    "demand": "DMND-2025-001",
    "purpose": "Complete redesign with modern design and better UX",
    "steps": [
        {
            "name": "Discovery & Requirements",
            "description": "Analyze current site and gather requirements",
            "hours": 20.0
        },
        {
            "name": "Design",
            "description": "Create responsive design mockups",
            "hours": 32.0
        },
        {
            "name": "Development",
            "description": "Build HTML/CSS/JavaScript frontend",
            "hours": 80.0
        },
        {
            "name": "Testing",
            "description": "QA testing and bug fixes",
            "hours": 24.0
        }
    ],
    "total": 156.0
}

# Generate PDF
pdf_path = generate_pdf(project, "estimate.pdf")

print(f"PDF generated at: {pdf_path}")
# Output includes 3-column table:
# Discovery & Requirements │ Analyze current site... │ 20.0
# Design                    │ Create responsive...    │ 32.0
# Development               │ Build HTML/CSS...       │ 80.0
# Testing                   │ QA testing and bug...   │ 24.0
# ─────────────────────────────────────────────────────────
# Total Estimated Hours                              │ 156.0
```

### Example 5: Uploading to Azure DevOps

```python
from core.helpers.devops_client import DevOpsClient
import os

# Get credentials from environment
org = os.getenv("DEVOPS_ORG", "BallCorporation")
project = os.getenv("DEVOPS_PROJECT", "Automation and Digital Adoption")
pat = os.getenv("DEVOPS_PAT")

# Create client
devops = DevOpsClient(
    organization=org,
    project=project,
    pat=pat
)

# Project data with work item types
project_data = {
    "demand": "DMND-2025-001",
    "name": "Website Redesign",
    "steps": [
        {
            "name": "UX/UI Design",
            "description": "Create visual designs",
            "hours": 40,
            "type": "Feature",
            "parent": None
        },
        {
            "name": "Home Page Design",
            "description": "Design home page",
            "hours": 0,
            "type": "User Story",
            "parent": "UX/UI Design"
        },
        {
            "name": "Implement Home Page",
            "description": "Code home page",
            "hours": 16,
            "type": "Task",
            "parent": "Home Page Design"
        }
    ]
}

# Upload to DevOps
result = devops.create_structure_from_json(project_data)

print(f"✅ Epic created: #{result['epic']}")
print(f"✅ Work items created:")
for name, item_id in result['items'].items():
    print(f"   - {name}: #{item_id}")

# Output:
# ✅ Epic created: #12345
# ✅ Work items created:
#    - UX/UI Design: #12346
#    - Home Page Design: #12347
#    - Implement Home Page: #12348
```

---

## Data Structure Reference

### Project Object

```python
project = {
    "name": str,                           # Project identifier
    "architect": str,                      # Solution architect name
    "area": str,                           # Department (IT, IBP, etc.)
    "demand": str,                         # Demand ID
    "purpose": str,                        # Project goals/description
    "date": str,                           # Creation date (YYYY-MM-DD)
    "steps": [
        {
            "name": str,                   # Task name
            "description": str,            # Optional description
            "hours": float,                # Estimated hours
            "type": str,                   # Feature/User Story/Task (optional)
            "parent": str                  # Parent task name (optional)
        },
        # ... more steps
    ],
    "total": float                         # Sum of all step hours
}
```

### Template Object

```python
template = {
    "name": str,                           # Template identifier
    "description": str,                    # Optional description
    "hours": str                           # Default hours as string
}
```

---

## Environment Configuration

Create a `.env` file in the project root:

```
# Azure DevOps Configuration
DEVOPS_ORG=BallCorporation
DEVOPS_PROJECT=Automation and Digital Adoption
DEVOPS_PAT=your_personal_access_token_here

# Optional: Network path (default is set in config.py)
# NETWORK_PATH=\\server\path\to\data
```

---

## Common Tasks

### Task 1: Export Project as PDF

```python
from core.helpers.project_utils import load_projects
from core.pdf_generator import generate_pdf

# Find your project
projects = load_projects()
my_project = next(p for p in projects if p['name'] == 'Website Redesign')

# Generate PDF
pdf_path = generate_pdf(my_project, "output.pdf")
print(f"PDF saved to: {pdf_path}")
```

### Task 2: Update Project Hours

```python
from core.helpers.project_utils import load_projects, save_projects

# Load and find project
projects = load_projects()
project = next(p for p in projects if p['name'] == 'Website Redesign')

# Update step hours
for step in project['steps']:
    if step['name'] == 'Development':
        step['hours'] = 100.0  # Update from 80 to 100
        
# Recalculate total
project['total'] = sum(s['hours'] for s in project['steps'])

# Save
save_projects(projects)
```

### Task 3: Clone Project

```python
from core.helpers.project_utils import load_projects, save_projects
from datetime import datetime

# Load projects
projects = load_projects()

# Find source project
source = next(p for p in projects if p['name'] == 'Website Redesign')

# Create clone
cloned = source.copy()
cloned['name'] = 'Website Redesign v2'
cloned['date'] = datetime.now().strftime("%Y-%m-%d")

# Save
projects.append(cloned)
save_projects(projects)
```

### Task 4: Batch Create Projects from CSV

```python
import csv
from core.helpers.project_utils import load_projects, save_projects
from datetime import datetime

# Sample CSV file: projects.csv
# name,architect,area,demand,purpose
# Website,John Smith,Marketing,DMND-001,Redesign website
# API,Jane Doe,Engineering,DMND-002,Build REST API

projects = load_projects()

with open('projects.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        project = {
            "name": row['name'],
            "architect": row['architect'],
            "area": row['area'],
            "demand": row['demand'],
            "purpose": row['purpose'],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "steps": [],
            "total": 0.0
        }
        projects.append(project)

save_projects(projects)
```

---

## Troubleshooting

### Issue: "Please save a project first"

**Cause:** No project name entered
**Solution:** Fill in the "Project" field before saving

### Issue: "Network path not available"

**Cause:** Network drive is offline
**Solution:** Application will automatically fall back to local storage

### Issue: "DevOps PAT not configured"

**Cause:** Missing .env file or DEVOPS_PAT variable
**Solution:** Create .env file with DevOps credentials

### Issue: PDF not generating

**Cause:** FPDF library not installed
**Solution:** `pip install fpdf2`

---

## Performance Tips

1. **Loading Large Projects**
   - Descriptions don't affect performance
   - Filter templates by search to reduce UI load

2. **PDF Generation**
   - PDFs with 50+ steps process normally
   - File size depends on content, typically 5-10 KB

3. **Template Management**
   - Search filters in real-time
   - No performance penalty for 100+ templates

4. **DevOps Upload**
   - Features with 10+ User Stories work fine
   - User Stories with 20+ Tasks work fine
   - Large structures take a few seconds

---

## Best Practices

1. **Use Descriptions Effectively**
   - Clear, concise descriptions (1-2 lines)
   - Include acceptance criteria if relevant

2. **Template Organization**
   - Create templates for recurring tasks
   - Use consistent naming (Code Review, Testing, etc.)

3. **Project Structure**
   - Start with high-level features
   - Break into user stories
   - Create tasks for detailed work

4. **Hours Estimation**
   - Use consistent units (hours, not days)
   - Include buffer for risks
   - Track actual vs. estimated for improvement

---

## Support & Documentation

- **Feature Guide:** See `FEATURE_DOCUMENTATION.md`
- **Fixes Summary:** See `FIXES_AND_DOCUMENTATION.md`
- **Code Documentation:** All modules have docstrings in English
- **Issues:** Check logs for detailed error messages

---

**Last Updated:** 2025-01-02
**Version:** 1.0 (All features working)
**Status:** Production Ready ✅

