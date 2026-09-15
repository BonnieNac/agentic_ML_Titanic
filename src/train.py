"""Entraînement du modèle de classification (survie au Titanic)."""

from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from .preprocess import build_preprocessor

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "titanic_model.joblib"


def build_model() -> Pipeline:
    """Construit le pipeline complet : préprocessing + classifieur."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", RandomForestClassifier(n_estimators=300, random_state=42)),
        ]
    )


def train_model(X, y, test_size: float = 0.2, random_state: int = 42):
    """Entraîne le modèle et retourne (pipeline entraîné, X_test, y_test)."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    model = build_model()

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    print(
        f"Accuracy en validation croisée (5 folds) : {cv_scores.mean():.3f} "
        f"(+/- {cv_scores.std():.3f})"
    )

    model.fit(X_train, y_train)
    return model, X_test, y_test


def save_model(model: Pipeline) -> None:
    """Sauvegarde le pipeline entraîné sur le disque."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modèle sauvegardé dans {MODEL_PATH}")
