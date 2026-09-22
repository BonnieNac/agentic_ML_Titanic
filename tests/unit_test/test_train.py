"""Tests unitaires de la construction et de l'entraînement du modèle."""

import pandas as pd
from sklearn.pipeline import Pipeline

from titanic_ml.core.features.preprocessing import split_features_target
from titanic_ml.core.models.train import build_model, train_model


def test_build_model_is_a_two_step_pipeline() -> None:
    """Teste que build_model retourne un pipeline préprocesseur + classifieur."""
    model = build_model()

    assert isinstance(model, Pipeline)
    assert [name for name, _ in model.steps] == ["preprocessor", "classifier"]


def test_train_model_fits_and_splits_data(titanic_df: pd.DataFrame) -> None:
    """Teste que train_model entraîne le modèle et découpe correctement les données."""
    X, y = split_features_target(titanic_df)

    model, X_test, y_test = train_model(X, y, test_size=0.2)

    assert len(X_test) == len(y_test) == round(len(X) * 0.2)

    predictions = model.predict(X_test)
    assert len(predictions) == len(y_test)
    assert set(predictions).issubset({0, 1})
