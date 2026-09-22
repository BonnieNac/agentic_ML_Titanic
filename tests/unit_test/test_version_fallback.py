"""Tests unitaires du mécanisme de repli de la version du projet."""

from unittest.mock import patch

from titanic_ml.core.utils.version import get_project_version


def test_version_fallback() -> None:
    """Teste la logique de repli quand le package n'est pas installé et que VERSION est absent."""
    import importlib.metadata

    with patch("importlib.metadata.version") as mock_version:
        mock_version.side_effect = importlib.metadata.PackageNotFoundError

        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.side_effect = FileNotFoundError("Fichier VERSION introuvable")

            version = get_project_version()

            assert version == "0.1.0"
