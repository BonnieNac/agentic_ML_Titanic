"""Tests unitaires du chargement du dataset Titanic."""

from pathlib import Path

import pandas as pd
import pytest

import titanic_ml.core.data_io.loader as loader_module


def test_load_data_downloads_when_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste que le CSV est téléchargé quand il est absent du cache local."""
    data_dir = tmp_path / "data" / "raw"
    data_path = data_dir / "titanic.csv"
    monkeypatch.setattr(loader_module, "RAW_DATA_DIR", data_dir)
    monkeypatch.setattr(loader_module, "DATA_PATH", data_path)

    calls: list[tuple[str, Path]] = []

    def fake_urlretrieve(url: str, filename: Path) -> None:
        calls.append((url, filename))
        pd.DataFrame({"Survived": [0, 1]}).to_csv(filename, index=False)

    monkeypatch.setattr(loader_module, "urlretrieve", fake_urlretrieve)

    df = loader_module.load_data()

    assert len(calls) == 1
    assert list(df["Survived"]) == [0, 1]


def test_load_data_skips_download_when_file_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste que le téléchargement est ignoré si le fichier est déjà en cache."""
    data_dir = tmp_path / "data" / "raw"
    data_dir.mkdir(parents=True)
    data_path = data_dir / "titanic.csv"
    pd.DataFrame({"Survived": [1]}).to_csv(data_path, index=False)

    monkeypatch.setattr(loader_module, "RAW_DATA_DIR", data_dir)
    monkeypatch.setattr(loader_module, "DATA_PATH", data_path)

    def fail_urlretrieve(*args: object, **kwargs: object) -> None:
        raise AssertionError("ne devrait pas être appelé si le fichier existe déjà")

    monkeypatch.setattr(loader_module, "urlretrieve", fail_urlretrieve)

    df = loader_module.load_data()

    assert list(df["Survived"]) == [1]
