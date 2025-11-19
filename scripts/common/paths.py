"""Shared repository path helpers used across CLI scripts."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHITECTURE_DIR = REPO_ROOT / "architecture"
GENERATED_DIR = REPO_ROOT / "generated"
BUILD_DIR = REPO_ROOT / "build"
MODELS_DIR = REPO_ROOT / "models"
RESOURCES_DIR = REPO_ROOT / "resources"


def ensure_directory(path: Path) -> Path:
    """Create the directory (or its parent) if missing and return it for chaining."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent_dir(path: Path) -> Path:
    """Create the parent directory for a file path if needed and return the file path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
