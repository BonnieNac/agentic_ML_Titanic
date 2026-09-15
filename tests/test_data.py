import pandas as pd

import src.data as data_module


def test_load_data_downloads_when_missing(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_path = data_dir / "titanic.csv"
    monkeypatch.setattr(data_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(data_module, "DATA_PATH", data_path)

    calls = []

    def fake_urlretrieve(url, filename):
        calls.append((url, filename))
        pd.DataFrame({"Survived": [0, 1]}).to_csv(filename, index=False)

    monkeypatch.setattr(data_module, "urlretrieve", fake_urlretrieve)

    df = data_module.load_data()

    assert len(calls) == 1
    assert list(df["Survived"]) == [0, 1]


def test_load_data_skips_download_when_file_exists(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    data_path = data_dir / "titanic.csv"
    pd.DataFrame({"Survived": [1]}).to_csv(data_path, index=False)

    monkeypatch.setattr(data_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(data_module, "DATA_PATH", data_path)

    def fail_urlretrieve(*args, **kwargs):
        raise AssertionError("ne devrait pas être appelé si le fichier existe déjà")

    monkeypatch.setattr(data_module, "urlretrieve", fail_urlretrieve)

    df = data_module.load_data()

    assert list(df["Survived"]) == [1]
