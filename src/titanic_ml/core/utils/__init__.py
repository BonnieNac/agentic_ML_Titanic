"""Utilitaires partagés : chemins et version du projet."""

from .paths import (
    DATA_DIR,
    FIGURES_DIR,
    MODELS_DIR,
    PROJECT_ROOT,
    RAW_DATA_DIR,
    ensure_dirs_exist,
)
from .version import get_project_version

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "MODELS_DIR",
    "FIGURES_DIR",
    "ensure_dirs_exist",
    "get_project_version",
]
