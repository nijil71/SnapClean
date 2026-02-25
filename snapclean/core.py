import os
import shutil
import tempfile
import zipfile
from datetime import datetime
import subprocess

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".idea",
    ".vscode"
    "dist"
}

EXCLUDE_FILES = {
    ".env"
}

def should_exclude(name):
    return name in EXCLUDE_DIRS or name in EXCLUDE_FILES


def create_snapshot(project_path, output_dir, build=False):
    project_path = os.path.abspath(project_path)

    if build:
        print("Running build command...")
        subprocess.run(["npm", "run", "build"], cwd=project_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = os.path.join(temp_dir, "project_copy")
        removed_items = []

        def ignore_filter(dir, files):
            ignored = []
            for f in files:
                if f in EXCLUDE_DIRS or f in EXCLUDE_FILES:
                    ignored.append(f)
                    removed_items.append(os.path.join(dir, f))
            return ignored
        shutil.copytree(
            project_path,
            temp_project,
            ignore=ignore_filter
        )

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"snapshot_{timestamp}.zip"
        zip_path = os.path.join(output_dir, zip_name)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_project):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_project)
                    zipf.write(full_path, rel_path)
        print("\nRemoved items:")
        for item in removed_items:
            print(f"- {item}")
        print(f"Snapshot created: {zip_path}")