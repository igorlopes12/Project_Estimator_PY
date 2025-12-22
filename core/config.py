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

# Prefer the network path only if it's usable (exists or can be created and is writable).
# Fallback to local data directory when the network path is not writable.
if NETWORK_PATH:
    network_dir = Path(NETWORK_PATH)
    try:
        # try to create the directory if it doesn't exist
        network_dir.mkdir(parents=True, exist_ok=True)
        # perform a small write test to ensure the directory is writable
        test_file = network_dir / ".write_test"
        with open(test_file, "w", encoding="utf-8") as tf:
            tf.write("ok")
        test_file.unlink()
        DATA_DIR = network_dir
    except Exception as e:
        # If any error occurs (permission, network unavailable), fallback to local data dir
        print(f"Warning: Network path {network_dir} not usable: {e}")
        DATA_DIR = PROJECT_ROOT / "data"
else:
    DATA_DIR = PROJECT_ROOT / "data"

# Ensure the data directory exists; if creation fails, fallback to local data dir
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
