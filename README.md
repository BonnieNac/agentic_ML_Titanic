# Titanic ML

Projet d'apprentissage supervisé : prédire la survie des passagers du Titanic.

## Structure

```
titanic_ml/
├── data/               # dataset (téléchargé automatiquement)
├── models/             # modèle entraîné + matrice de confusion
├── src/
│   ├── data.py         # chargement du dataset
│   ├── preprocess.py   # sélection des features + pipeline de préprocessing
│   ├── train.py        # entraînement (RandomForest) + validation croisée
│   └── evaluate.py      # métriques + matrice de confusion
└── main.py             # script principal
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l'entraînement

```bash
python main.py
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
