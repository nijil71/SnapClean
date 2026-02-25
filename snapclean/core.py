import os
import shutil
import tempfile
import zipfile
from datetime import datetime
import subprocess
import pathspec

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".idea",
    ".vscode",
    "dist"
}

EXCLUDE_FILES = {
    ".env"
}

def should_exclude(name):
    return name in EXCLUDE_DIRS or name in EXCLUDE_FILES

def get_directory_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                total += os.path.getsize(full_path)
    return total

def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{round(size_bytes, 2)} {unit}"
        size_bytes /= 1024
    return f"{round(size_bytes, 2)} TB"

def create_snapshot(project_path, output_dir, build=False, dry_run=False):
    project_path = os.path.abspath(project_path)
    original_size = get_directory_size(project_path)
    gitignore_path = os.path.join(project_path, ".gitignore")
    spec = None

    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    if build:
        print("Running build command...")
        subprocess.run(["npm", "run", "build"], cwd=project_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = os.path.join(temp_dir, "project_copy")
        removed_items = []

        def ignore_filter(directory, contents):
            ignored = []
            for item in contents:
                full_path = os.path.join(directory, item)
                rel_path = os.path.relpath(full_path, project_path)

                should_ignore = False

                if item in EXCLUDE_DIRS or item in EXCLUDE_FILES:
                    should_ignore = True

                if spec and spec.match_file(rel_path):
                    should_ignore = True

                if should_ignore:
                    ignored.append(item)
                    removed_items.append(full_path)

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

        if dry_run:
            print("\nDry run mode enabled.")
            if removed_items:
                print("The following items would be removed:")
                for item in removed_items:
                    print(f"- {item}")
            else:
                print("No items would be removed.")
            return
        
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
        snapshot_size = os.path.getsize(zip_path)

        reduction = 0
        if original_size > 0:
            reduction = 100 - ((snapshot_size / original_size) * 100)

        print("\nSize Summary:")
        print(f"Original size: {format_size(original_size)}")
        print(f"Snapshot size: {format_size(snapshot_size)}")
        print(f"Reduced by: {round(reduction, 2)}%")