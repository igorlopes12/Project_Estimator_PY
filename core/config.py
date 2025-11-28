"""core/config.py

Application configuration and data paths.
This module defines the project root, a network data folder (optional), and the
paths for templates and projects JSON files. If the network path cannot be
created, the module falls back to a local data directory.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Network path (set to a UNC path or None to use the local directory)
NETWORK_PATH = r"\\Nadc1rpaorcfs01\DEV\ProjectEstimatorApp"

# Define data directory depending on the configured network path
if NETWORK_PATH:
    DATA_DIR = Path(NETWORK_PATH)
else:
    DATA_DIR = PROJECT_ROOT / "data"

# Ensure the data directory exists; if creation fails, fall back to local data dir
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create directory {DATA_DIR}: {e}")
    # Fallback to local data directory if there is an error
    DATA_DIR = PROJECT_ROOT / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Paths for the JSON files
TEMPLATES_PATH = DATA_DIR / "templates.json"
PROJECTS_PATH = DATA_DIR / "projects.json"
