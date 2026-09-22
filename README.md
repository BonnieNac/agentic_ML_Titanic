# Titanic ML

Apprentissage supervisé sur le dataset Titanic, avec API FastAPI et dashboard Streamlit.

## 🚀 Fonctionnalités principales

- **Pipeline ML** : chargement, préprocessing, entraînement (`RandomForestClassifier`) et
  évaluation, orchestrés par [scripts/train_pipeline.py](scripts/train_pipeline.py).
- **API FastAPI** : squelette de routes (`/health`, `/version`, `/hello`, `/bonjour`) prêt à
  être enrichi d'un endpoint de prédiction.
- **Dashboard Streamlit** : exploration interactive de datasets via Pygwalker.
- **uv** : gestion des dépendances et de l'environnement Python.
- **Docker** : Dockerfile multi-stage + `docker-compose.yml` pour l'API et Streamlit.
- **CI/CD** : pipelines GitHub Actions et GitLab CI préconfigurés.
- **Qualité** : Ruff (lint + format), MyPy (strict), Pytest (couverture ≥ 80 %).

## 🏗️ Architecture

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour le détail des composants et du flux de données.

## 🛠️ Démarrage

### Prérequis
- [uv](https://github.com/astral-sh/uv)
- [Docker](https://www.docker.com/) & Docker Compose (optionnel, pour la conteneurisation)

### Installation

```bash
make dev-install
```

Ou directement :

```bash
uv sync
uv run pre-commit install
```

### Configuration

```bash
cp .env.example .env
```

## 📖 Utilisation

### Entraîner le modèle

```bash
make train
# équivalent à : uv run python scripts/train_pipeline.py
```

Télécharge le dataset dans `data/raw/titanic.csv`, entraîne le modèle et sauvegarde :
- le modèle dans `models/titanic_model.joblib`
- la matrice de confusion dans `docs/figures/confusion_matrix.png`

### Lancer en local

```bash
make run       # Streamlit sur http://localhost:8501
make run_api   # API sur http://localhost:8000
```

### Lancer avec Docker

```bash
make up
```
- Streamlit : http://localhost:8501
- Documentation FastAPI : http://localhost:8000/docs

```bash
make down
```

## 🧪 Qualité de code

```bash
make check       # lint + typecheck + tests
make format       # formate avec ruff
make test          # tests avec couverture
make test-fast    # tests, arrêt à la première erreur
```

## 📁 Structure du projet

```text
├── app/                    # Application Streamlit
├── dockerfiles/            # Dockerfile multi-stage
├── docs/                   # Figures, références, rapports générés
├── data/                   # raw / interim / processed / external (voir DVC ci-dessous)
├── notebooks/              # Notebooks d'exploration
├── scripts/                # Scripts d'orchestration (ex. train_pipeline.py)
├── src/titanic_ml/
│   ├── api/                # Implémentation FastAPI
│   └── core/
│       ├── data_io/        # Chargement des données
│       ├── features/       # Feature engineering / préprocessing
│       ├── models/         # Entraînement / évaluation
│       ├── utils/          # Chemins centralisés, version
│       └── visualization/  # Réservé aux évolutions futures
├── tests/                  # unit_test / integration / functional
├── .env.example            # Modèle de variables d'environnement
├── docker-compose.yml       # Orchestration API + Streamlit
├── Makefile                 # Raccourcis de développement
└── pyproject.toml           # Métadonnées et configuration des outils
```

## 💾 Gestion des données

`data/` contient des sous-dossiers par étape du pipeline :
- `raw/` : dumps originaux, immuables. Ne jamais modifier.
- `interim/` : données intermédiaires transformées.
- `processed/` : datasets finaux prêts pour la modélisation.
- `external/` : données de sources tierces.

Ces répertoires sont ignorés par Git. Pour des datasets volumineux, utilise
[DVC](https://dvc.org/) plutôt que de les committer directement.

## 🤝 Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licence

Aucune licence choisie pour l'instant.
