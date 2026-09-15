"""Chargement du jeu de données Titanic."""

from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_PATH = DATA_DIR / "titanic.csv"


def load_data() -> pd.DataFrame:
    """Retourne le dataset Titanic sous forme de DataFrame.

    Télécharge le CSV depuis GitHub s'il n'est pas déjà présent en local.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        print(f"Téléchargement du dataset depuis {DATA_URL} ...")
        urlretrieve(DATA_URL, DATA_PATH)
        print(f"Dataset enregistré dans {DATA_PATH}")

    return pd.read_csv(DATA_PATH)
