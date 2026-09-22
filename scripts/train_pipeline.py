"""Pipeline complet : charge les données, entraîne le modèle et l'évalue."""

from titanic_ml.core.data_io.loader import load_data
from titanic_ml.core.features.preprocessing import split_features_target
from titanic_ml.core.models.evaluate import evaluate_model
from titanic_ml.core.models.train import save_model, train_model


def main() -> None:
    """Exécute le pipeline d'entraînement de bout en bout."""
    df = load_data()
    print(f"Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes\n")

    X, y = split_features_target(df)
    model, X_test, y_test = train_model(X, y)

    evaluate_model(model, X_test, y_test)
    save_model(model)


if __name__ == "__main__":
    main()
