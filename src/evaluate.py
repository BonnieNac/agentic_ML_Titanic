"""Évaluation du modèle entraîné."""

from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    roc_auc_score,
)

REPORTS_DIR = Path(__file__).resolve().parent.parent / "models"


def evaluate_model(model, X_test, y_test) -> None:
    """Affiche les métriques de performance et sauvegarde la matrice de confusion."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print(f"\nAccuracy sur le jeu de test : {accuracy:.3f}")
    print(f"ROC AUC : {auc:.3f}\n")
    print("Rapport de classification :")
    print(classification_report(y_test, y_pred, target_names=["Décédé", "Survivant"]))

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=["Décédé", "Survivant"], ax=ax, cmap="Blues"
    )
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "confusion_matrix.png")
    print(f"Matrice de confusion sauvegardée dans {REPORTS_DIR / 'confusion_matrix.png'}")
