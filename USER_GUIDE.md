# Project Estimator - User Guide

Welcome to **Project Estimator**! This application was designed to facilitate the creation and management of project estimates.

---

## Getting Started

### For Windows Users

1. **Locate the executable file** `ProjectEstimator.exe` on your computer
2. **Double-click** the file to launch the application
3. The application window will open automatically

⚠️ **Note:** No installation is necessary - the executable contains everything you need to run it!

---

## How It Works

The **Project Estimator** has three main sections:

### 1️⃣ Project Details

Here you define the general information of the project:

| Field | Required | What to Fill |
|-------|----------|--------------|
| **Project** | ✓ | Project name |
| **Solution Architect** | - | Name of the responsible person |
| **Area** | - | Department or involved area |
| **Request Number** | - | Internal request ID |
| **Objective** | - | Detailed project description |

**💡 Tip:** Use the "Existing Projects" dropdown to load a previously saved project.

---

### 2️⃣ Steps (Tasks/Features)

Add tasks or features to your project by clicking the **+** button:

**For each step, define:**
- **Name** - Brief task description
- **Type** - Feature, User Story, or Task
- **Parent** - If it's a subtask, select the parent task
- **Hours** - How many hours you estimate to complete it
- **Description** (optional) - Click the description icon for additional details

**Hierarchical Structure:**
```
Feature (main task)
├── User Story (subtask)
│   └── Task (sub-subtask)
```

---

### 3️⃣ Templates

Reuse common task configurations:

- **Search** a template by name
- **Click +** to add a template as a new step
- **Edit** (pencil icon) to modify an existing template
- **Delete** (trash icon) to remove a template

**🔄 Auto-Save:** When you edit a step, it is automatically saved as a template for future use!

---

## Step-by-Step: Creating a Project

### 1. Fill in Project Information

Open the application and fill in the data in the **Project Details** panel:

```
Project: My Automation Project
Architect: John Smith
Area: Digital Adoption
Request: REQ-2026-001
Objective: Automate sales process
```

### 2. Add Steps

Click the **+** in **Steps** and add your tasks:

**Example:**

| Step | Type | Hours |
|------|------|-------|
| Requirements Analysis | Feature | - |
| Gather data from stakeholders | User Story | 8 |
| Document requirements | Task | 16 |
| Development | Feature | - |
| Implement API | User Story | 40 |
| Unit testing | Task | 20 |

### 3. Save the Project

Click the **Save** button to save everything.

✅ **Done!** Your project is saved and can be loaded later from the dropdown.

---

## Generating PDF Report

After creating your project, you can generate a professional PDF report:

1. Click the **Generate PDF** button
2. Choose the folder where you want to save it
3. Type the file name
4. The PDF will be created with:
   - Company logo
   - All project information
   - Detailed table with tasks and hours
   - Automatic calculation of total hours

📄 Share this PDF with your team or client!

---

## Helpful Tips

✨ **Use Templates to Save Time**
- If you use similar tasks across multiple projects, create templates
- Next time you need them, just search and click **+**

⏱️ **View Total Hours**
- The total is calculated automatically as you add hours

🔄 **Modify an Existing Project**
- Load it from the "Existing Projects" dropdown
- Make the desired changes
- Click Save (it will overwrite the previous version)

🗑️ **Remove a Step**
- Click the trash icon next to the step

---

## Azure DevOps Integration

Click the **Upload to DevOps** button to:
- Automatically send your project to Azure DevOps
- Create a hierarchical task structure
- Share with the development team

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| The application won't open | Make sure you double-click on `ProjectEstimator.exe` |
| My project disappeared | Click Save after making changes to ensure it is saved |
| PDF was not generated | Check if you filled in the project name and added at least one step |
| I can't edit a field | Click on the field (or the pencil icon if it's a template) to edit |

---

## Contact and Support

If you have any questions or encounter any problems, contact the development team.

---

**Version:** 1.0  
**Last updated:** January 2026  
**Developed by:** Igor Lopes

Enjoy Project Estimator! 🚀

