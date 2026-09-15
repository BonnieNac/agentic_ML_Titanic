# Titanic ML

Projet d'apprentissage supervisé : prédire la survie des passagers du Titanic.

## Structure

```
titanic_ml/
├── data/               # dataset (téléchargé automatiquement, ignoré par git)
├── models/             # modèle entraîné + matrice de confusion (ignoré par git)
├── src/
│   ├── data.py         # chargement du dataset
│   ├── preprocess.py   # sélection des features + pipeline de préprocessing
│   ├── train.py        # entraînement (RandomForest) + validation croisée
│   └── evaluate.py      # métriques + matrice de confusion
├── tests/              # tests unitaires pytest
├── main.py             # script principal
└── pyproject.toml      # dépendances (uv) + config ruff/pytest
```

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances
et de l'environnement Python (uv télécharge lui-même une version de Python adaptée
si besoin, pas besoin d'en installer une manuellement).

```bash
uv sync
```

## Lancer l'entraînement

```bash
uv run python main.py
```

Le script télécharge le dataset (si absent), entraîne un `RandomForestClassifier`
sur les colonnes `Age`, `Fare`, `SibSp`, `Parch`, `Pclass`, `Sex`, `Embarked`,
affiche les métriques (accuracy, ROC AUC, rapport de classification), sauvegarde
la matrice de confusion dans `models/confusion_matrix.png` et le modèle dans
`models/titanic_model.joblib`.

## Réutiliser le modèle entraîné

```python
import joblib
import pandas as pd

model = joblib.load("models/titanic_model.joblib")

passager = pd.DataFrame(
    [
        {
            "Age": 29,
            "Fare": 50,
            "SibSp": 0,
            "Parch": 0,
            "Pclass": 1,
            "Sex": "female",
            "Embarked": "S",
        }
    ]
)

print(model.predict(passager))  # 0 = décédé, 1 = survivant
print(model.predict_proba(passager))
```

## Qualité de code

Formatage et lint avec [ruff](https://docs.astral.sh/ruff/) :

```bash
uv run ruff format .
uv run ruff check .
```

## Tests

Tests unitaires avec [pytest](https://docs.pytest.org/) (aucun appel réseau,
tout est basé sur des données synthétiques et du mocking) :

```bash
uv run pytest
```
