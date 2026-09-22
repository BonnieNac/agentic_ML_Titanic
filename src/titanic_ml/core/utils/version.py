"""Utilitaires de gestion de version du projet."""

import importlib.metadata

from .paths import PROJECT_ROOT


def get_project_version() -> str:
    """Récupère la version du projet depuis les métadonnées du package ou le fichier VERSION.

    Returns:
        str: la chaîne de version.

    """
    try:
        # Essaie d'abord de lire la version du package installé
        return importlib.metadata.version("titanic_ml")
    except importlib.metadata.PackageNotFoundError:
        # Repli sur le fichier VERSION à la racine du projet
        version_file = PROJECT_ROOT / "VERSION"
        try:
            return str(version_file.read_text().strip())
        except (FileNotFoundError, PermissionError):
            # Dernier repli sur une version par défaut
            return "0.1.0"
