"""
Build script that reads build_config.json and runs PyInstaller with basic options.
Usage:
  python build.py

The script will:
- Read build_config.json
- Ensure PyInstaller is installed
- Build a PyInstaller command with --onefile and --windowed
- Include `data` and `assets` folders via --add-data (Windows syntax)
- Run the command and print the result

Note: adjust options as needed (additional files in --add-data, etc.).
"""

import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT, 'build_config.json')


def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_pyinstaller():
    try:
        import PyInstaller  # noqa: F401
        return True
    except Exception:
        return False


def build():
    if not os.path.exists(CONFIG_PATH):
        print('build_config.json not found. Create and configure it before running the build script.')
        sys.exit(1)

    cfg = load_config(CONFIG_PATH)
    name = cfg.get('app_name', 'app')
    icon = cfg.get('icon')

    # Base command
    cmd = [sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', '--name', name]

    # Icon if present
    if icon:
        icon_path = os.path.join(ROOT, icon)
        if os.path.exists(icon_path):
            cmd += ['--icon', icon_path]
        else:
            print(f"Warning: icon not found at {icon_path}, skipping icon option.")

    # Include data and assets folders next to the executable
    # Add-data syntax for Windows: "src;dest"
    data_dir = os.path.join(ROOT, 'data')
    assets_dir = os.path.join(ROOT, 'assets')
    if os.path.exists(data_dir):
        cmd += ['--add-data', f"{data_dir};data"]
    if os.path.exists(assets_dir):
        cmd += ['--add-data', f"{assets_dir};assets"]

    # Entry file
    entry = os.path.join(ROOT, 'main.py')
    if not os.path.exists(entry):
        print('main.py not found in the project root.')
        sys.exit(1)
    cmd.append(entry)

    # Ensure PyInstaller is installed
    if not ensure_pyinstaller():
        print('PyInstaller does not seem to be installed. Installing via pip...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

    # Execute the command
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print('Error running PyInstaller. Exit code:', res.returncode)
        sys.exit(res.returncode)

    print('Build finished. Check the dist/ folder for the executable.')


if __name__ == '__main__':
    build()
