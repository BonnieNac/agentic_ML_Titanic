"""Tests unitaires de l'évaluation du modèle."""

from pathlib import Path

import pandas as pd
import pytest

import titanic_ml.core.models.evaluate as evaluate_module
from titanic_ml.core.features.preprocessing import split_features_target
from titanic_ml.core.models.evaluate import evaluate_model
from titanic_ml.core.models.train import train_model


def test_evaluate_model_creates_confusion_matrix(
    titanic_df: pd.DataFrame,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Teste que evaluate_model affiche les métriques et sauvegarde la matrice de confusion."""
    monkeypatch.setattr(evaluate_module, "FIGURES_DIR", tmp_path)

    X, y = split_features_target(titanic_df)
    model, X_test, y_test = train_model(X, y)

    evaluate_model(model, X_test, y_test)

    assert (tmp_path / "confusion_matrix.png").exists()
    captured = capsys.readouterr()
    assert "Accuracy" in captured.out
