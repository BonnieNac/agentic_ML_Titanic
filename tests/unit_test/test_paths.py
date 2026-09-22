"""Tests unitaires des utilitaires de chemins du projet."""

from pathlib import Path

import pytest

from titanic_ml.core.utils import paths


def test_ensure_dirs_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste que ensure_dirs_exist crée physiquement les répertoires attendus.

    Utilise la fixture tmp_path de pytest pour ne pas polluer le vrai système de fichiers.
    """
    monkeypatch.setattr(paths, "RAW_DATA_DIR", tmp_path / "data" / "raw")
    monkeypatch.setattr(paths, "INTERIM_DATA_DIR", tmp_path / "data" / "interim")
    monkeypatch.setattr(paths, "PROCESSED_DATA_DIR", tmp_path / "data" / "processed")
    monkeypatch.setattr(paths, "EXTERNAL_DATA_DIR", tmp_path / "data" / "external")
    monkeypatch.setattr(paths, "MODELS_DIR", tmp_path / "models")
    monkeypatch.setattr(paths, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(paths, "FIGURES_DIR", tmp_path / "docs" / "figures")

    assert not (tmp_path / "data" / "raw").exists()
    assert not (tmp_path / "logs").exists()

    paths.ensure_dirs_exist()

    assert (tmp_path / "data" / "raw").exists()
    assert (tmp_path / "data" / "interim").exists()
    assert (tmp_path / "data" / "processed").exists()
    assert (tmp_path / "data" / "external").exists()
    assert (tmp_path / "models").exists()
    assert (tmp_path / "logs").exists()
    assert (tmp_path / "docs" / "figures").exists()

    try:
        paths.ensure_dirs_exist()
    except FileExistsError:
        pytest.fail("ensure_dirs_exist a levé FileExistsError alors que ce n'était pas attendu.")


def test_find_project_root_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste que _find_project_root retombe sur le repli quand aucun pyproject.toml n'est trouvé."""
    original_exists = Path.exists

    def fake_exists(self: Path) -> bool:
        if self.name == "pyproject.toml":
            return False
        return original_exists(self)

    monkeypatch.setattr(Path, "exists", fake_exists)

    result = paths._find_project_root()
    assert isinstance(result, Path)
