"""Tests unitaires du pipeline de préprocessing des features."""

import numpy as np
import pandas as pd

from titanic_ml.core.features.preprocessing import (
    CATEGORICAL_FEATURES,
    FEATURES,
    NUMERIC_FEATURES,
    build_preprocessor,
    split_features_target,
)


def test_split_features_target_returns_expected_columns(titanic_df: pd.DataFrame) -> None:
    """Teste que split_features_target sépare correctement les colonnes attendues."""
    X, y = split_features_target(titanic_df)

    assert list(X.columns) == FEATURES
    assert y.name == "Survived"
    assert len(X) == len(y) == len(titanic_df)


def test_build_preprocessor_handles_missing_values(titanic_df: pd.DataFrame) -> None:
    """Teste que le préprocesseur impute correctement les valeurs manquantes."""
    X, _ = split_features_target(titanic_df)
    preprocessor = build_preprocessor()

    transformed = preprocessor.fit_transform(X)

    assert transformed.shape[0] == len(X)
    assert not np.isnan(transformed).any()


def test_build_preprocessor_output_width_matches_encoding(titanic_df: pd.DataFrame) -> None:
    """Teste que la largeur de sortie correspond au nombre de catégories encodées."""
    X, _ = split_features_target(titanic_df)
    preprocessor = build_preprocessor()

    transformed = preprocessor.fit_transform(X)

    n_categories = sum(X[col].nunique(dropna=True) for col in CATEGORICAL_FEATURES)
    expected_width = len(NUMERIC_FEATURES) + n_categories
    assert transformed.shape[1] == expected_width
