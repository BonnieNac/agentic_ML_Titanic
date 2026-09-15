"""Point d'entrée : charge les données, entraîne le modèle et l'évalue."""

from src.data import load_data
from src.evaluate import evaluate_model
from src.preprocess import split_features_target
from src.train import save_model, train_model


def main() -> None:
    df = load_data()
    print(f"Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes\n")

    X, y = split_features_target(df)
    model, X_test, y_test = train_model(X, y)

    evaluate_model(model, X_test, y_test)
    save_model(model)


if __name__ == "__main__":
    main()
