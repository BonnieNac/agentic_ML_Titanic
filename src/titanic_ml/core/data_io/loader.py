"""Chargement du jeu de données Titanic."""

from urllib.request import urlretrieve

import pandas as pd

from titanic_ml.core.utils.paths import RAW_DATA_DIR

DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
DATA_PATH = RAW_DATA_DIR / "titanic.csv"


def load_data() -> pd.DataFrame:
    """Retourne le dataset Titanic sous forme de DataFrame.

    Télécharge le CSV depuis GitHub s'il n'est pas déjà présent en local.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        print(f"Téléchargement du dataset depuis {DATA_URL} ...")
        urlretrieve(DATA_URL, DATA_PATH)
        print(f"Dataset enregistré dans {DATA_PATH}")

    return pd.read_csv(DATA_PATH)
