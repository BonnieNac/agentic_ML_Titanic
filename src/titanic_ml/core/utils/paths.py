"""Gestion centralisée des chemins pour éviter l'enfer des chemins relatifs."""

from pathlib import Path


def _find_project_root() -> Path:
    """Trouve dynamiquement la racine du projet en cherchant pyproject.toml.

    Remonte depuis le dossier du fichier courant jusqu'à trouver un pyproject.toml.
    Retombe sur une profondeur fixe si non trouvé.

    Returns:
        Path: le chemin absolu vers la racine du projet.

    """
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    # Repli sur la structure par défaut si non trouvé
    return Path(__file__).resolve().parents[4]


PROJECT_ROOT: Path = _find_project_root()

# Répertoires de données
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
INTERIM_DATA_DIR: Path = DATA_DIR / "interim"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EXTERNAL_DATA_DIR: Path = DATA_DIR / "external"

# Répertoire des modèles
MODELS_DIR: Path = PROJECT_ROOT / "models"

# Répertoire des notebooks
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"

# Répertoire des logs
LOGS_DIR: Path = PROJECT_ROOT / "logs"

# Répertoires de documentation / figures générées
DOCS_DIR: Path = PROJECT_ROOT / "docs"
FIGURES_DIR: Path = DOCS_DIR / "figures"


def ensure_dirs_exist() -> None:
    """Crée les répertoires standards du projet s'ils n'existent pas déjà.

    Garantit la présence des sous-répertoires data/, models/, logs/ et docs/figures/.
    """
    for dir_path in [
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXTERNAL_DATA_DIR,
        MODELS_DIR,
        LOGS_DIR,
        FIGURES_DIR,
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)
