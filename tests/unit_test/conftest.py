"""Fixtures pytest partagées par les tests unitaires."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def titanic_df() -> pd.DataFrame:
    """Petit jeu de données synthétique imitant la forme du dataset Titanic."""
    n = 60
    rng = np.random.default_rng(42)

    df = pd.DataFrame(
        {
            "PassengerId": range(1, n + 1),
            "Survived": [0, 1] * (n // 2),
            "Pclass": rng.choice([1, 2, 3], size=n),
            "Name": [f"Passenger {i}" for i in range(n)],
            "Sex": rng.choice(["male", "female"], size=n),
            "Age": rng.uniform(1, 80, size=n),
            "SibSp": rng.integers(0, 4, size=n),
            "Parch": rng.integers(0, 3, size=n),
            "Ticket": [f"T{i}" for i in range(n)],
            "Fare": rng.uniform(5, 300, size=n),
            "Cabin": [None] * n,
            "Embarked": rng.choice(["S", "C", "Q"], size=n),
        }
    )

    df.loc[0:3, "Age"] = np.nan
    df.loc[4:5, "Embarked"] = np.nan

    return df
