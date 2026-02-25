# Snapclean

> A Python CLI for creating clean, client-safe project snapshots.

<!-- [![PyPI version](https://img.shields.io/pypi/v/snapclean.svg)](https://pypi.org/project/snapclean/) -->
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<!-- [![CI](https://github.com/yourusername/snapclean/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/snapclean/actions) -->

Snapclean strips development clutter from your project, respects `.gitignore`, generates a safe `.env.example`, and produces a clean zip archive ready for sharing with clients or collaborators — all in a single command.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [CLI Reference](#cli-reference)
- [Configuration](#configuration)
- [What Gets Removed](#what-gets-removed)
- [Example Output](#example-output)
- [License](#license)

---

## Features

- **Removes development clutter** — `.git`, `node_modules`, `venv`, `__pycache__`, and more
- **Respects `.gitignore`** — automatically excludes patterns from your ignore file
- **Safe `.env` handling** — excludes secrets and generates a clean `.env.example` template
- **Size summary** — shows original vs. snapshot size and reduction percentage
- **Dry-run mode** — preview what would be removed without touching anything
- **Project configuration** — persist your preferred options in `.snapclean.toml`
- **Clean CLI output** — readable, minimal terminal output

---

## Installation

**From PyPI (recommended):**

```bash
pip install snapclean
```

**From source:**

```bash
git clone https://github.com/yourusername/snapclean.git
cd snapclean
pip install -e .
```

**Requirements:** Python 3.8+

---

## Quick Start

```bash
# Navigate to your project and create a snapshot
cd my-project
snap run
```

That's it. A timestamped zip archive is saved to `dist/` by default.

---

## Usage

```bash
# Basic snapshot
snap run

# Preview what would be removed (no files created)
snap run --dry-run

# Run a build step before snapshotting
snap run --build

# Save the snapshot to a custom directory
snap run --output ./release

# Snapshot a different project directory
snap run --path ./path/to/project

# Check the installed version
snap version
```

---

## CLI Reference

| Option | Default | Description |
|--------|---------|-------------|
| `--path TEXT` | `.` (current directory) | Path to the project to snapshot |
| `--output TEXT` | `dist` | Directory where the zip archive will be saved |
| `--build / --no-build` | `false` | Run a build command before snapshotting |
| `--dry-run / --no-dry-run` | `false` | Preview removals without creating any files |
| `--help` | — | Show help and exit |

---

## Configuration

To avoid typing options every time, create a `.snapclean.toml` file in your project root:

```toml
build = false
output = "release"
```

With this in place, running `snap` (no arguments) will use your saved preferences.

**Supported config keys:**

| Key | Type | Description |
|-----|------|-------------|
| `build` | boolean | Whether to run a build command before snapshotting |
| `output` | string | Output directory for the zip archive |

---

## What Gets Removed

The following are always excluded from the snapshot:

| Path / Pattern | Reason |
|----------------|--------|
| `.git/` | Version control history |
| `node_modules/` | Reinstallable JS dependencies |
| `venv/`, `.venv/` | Reinstallable Python environments |
| `__pycache__/` | Python bytecode cache |
| `.env` | Contains secrets — replaced by `.env.example` |
| All `.gitignore` patterns | Project-specific ignores |

If a `.env` file is found, Snapclean generates a `.env.example` with all keys present but values redacted, so recipients know which variables to configure.

---

## Example Output

```
Removed items:
  - .git/
  - node_modules/
  - venv/
  - .env  →  .env.example generated

Snapshot created: dist/snapshot_20260225_153013.zip

Snapshot Summary
----------------
Original size:  24.2 MB
Snapshot size:  10.4 KB
Reduced by:     99.96%
```

---

## How It Works

1. Copies your project to a temporary directory
2. Removes development files and anything matched by `.gitignore`
3. Replaces `.env` with a generated `.env.example`
4. Creates a timestamped zip archive in the output directory
5. Prints a size reduction summary

---

## Contributing

Contributions are welcome! Here's how to get started:

```bash
# Clone the repo
git clone https://github.com/nijil71/SnapClean.git  
cd snapclean

# Create a virtual environment and install dev dependencies
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

---


## License

MIT License — see [LICENSE](LICENSE) for full details.