# Project Estimator (Project_Estimator_PY)

Simple tool to create and manage project estimates, with a Flet GUI, JSON persistence and PDF export.

---

## Main features

- Create and manage projects
- Add and remove steps dynamically
- Automatic total hours calculation
- Persistence in a JSON file (data/projects.json)
- Export estimates to PDF
- Support for generating a Windows executable (.exe)

---

## Folder structure (summary)

Ignore the `build/` folder (artifacts generated when building the .exe).

Project_Estimator_PY/

- main.py                 # Application entry point
- readme.md               # Documentation (this file)
- requirements.txt        # Python dependencies
- build_config.json       # Build configuration used by build script
- build.py                # Helper script to run PyInstaller using build_config.json
- core/                   # Core application logic
  - project_manager.py    # Manages reading/writing projects.json
  - pdf_generator.py      # Generates PDF using FPDF
- ui/                     # UI views and components (Flet)
  - main_view.py          # Main view
  - project_form.py       # (optional) form components
- data/                   # Persisted data
  - projects.json         # Stores created projects
- assets/                 # Icons and other resources

---

## Requirements

- Python 3.10+ (or as specified in requirements.txt)
- Install dependencies with pip:

    pip install -r requirements.txt

---

## Run (development)

1. Create and activate a virtual environment (venv).
2. Install dependencies:

    pip install -r requirements.txt

3. Run the app:

    python main.py

The Flet UI should open and allow creating projects, adding steps, saving and exporting PDFs.

---

## Build a Windows executable (.exe)

Use PyInstaller to create a single-file Windows executable. The repository includes a convenience script `build.py` which reads `build_config.json` and runs PyInstaller with basic options.

1. Install PyInstaller:

    pip install pyinstaller

2. Adjust `build_config.json` as needed (app name, icon, version, etc.). Example:

```json
{
  "app_name": "Project Estimator",
  "product_name": "Project Estimator",
  "version": "1.0.0",
  "description": "Internal tool for project time estimates",
  "organization": "Your Organization",
  "icon": "assets/icon.ico"
}
```

3. Run the build script (it will install PyInstaller if missing):

    python build.py

4. After a successful build, the executable will be in `dist/` (e.g. `dist/Project Estimator.exe`).

Notes:
- The `build.py` script adds `data/` and `assets/` using PyInstaller's `--add-data` option (Windows syntax). Adjust if you need different paths.
- For more advanced builds (version info, manifests, special data files), create a PyInstaller spec file and tweak options.

---

## build_config.json usage

`build_config.json` is a simple JSON file that centralizes build metadata. The `build.py` script uses it to form the PyInstaller command (name, icon, etc.). PyInstaller itself does not read this file directly.

Typical fields:
- app_name: short application name used in the binary name
- product_name: product string
- version: application version
- description: short description
- organization: author/organization
- icon: relative path to a .ico file

You can write a custom build script or CI pipeline step that reads this JSON and executes PyInstaller (or other packagers) with consistent options.

---

## Best practices when distributing

- Test the .exe on a clean Windows VM to ensure all dependencies and data files are available.
- Keep `data/` alongside the executable or embed required assets using `--add-data`.
- Pin dependency versions in `requirements.txt` for reproducible builds.

---

## Contributing

- Open issues for bugs and feature requests
- Send pull requests with improvements

---

## Contact

Author: Igor Lopes

Last updated: 2025-10-17
