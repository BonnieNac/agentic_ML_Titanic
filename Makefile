# Makefile pour le projet Titanic ML

.PHONY: help install dev-install format lint typecheck test test-fast all check run run_api clean up down digest bump release

.DEFAULT_GOAL := help

###################################################################
# SETUP
###################################################################

install: ## Installe les dépendances via uv (prod + dev)
	uv sync

dev-install: install ## Installe les dépendances et les hooks pre-commit
	uv run pre-commit install

###################################################################
# RUN
###################################################################

run: ## Lance l'application web locale (Streamlit)
	uv run streamlit run app/streamlit_app.py

run_api: ## Lance l'API
	uv run titanic_ml-api

train: ## Lance le pipeline d'entraînement du modèle Titanic
	uv run python scripts/train_pipeline.py

up: ## Démarre l'API et Streamlit ensemble
	docker-compose up -d

down: ## Arrête l'API et Streamlit
	docker-compose down

docker-build: ## Construit les images Docker avec les labels OCI
	BUILD_VERSION=$$(cat VERSION) \
	BUILD_REVISION=$$(git rev-parse HEAD 2>/dev/null || echo "unknown") \
	BUILD_DATE=$$(date -u +%Y-%m-%dT%H:%M:%SZ) \
	docker-compose build

###################################################################
# QUALITÉ DE CODE
###################################################################

all: lint typecheck test ## Lance lint, typecheck et tests dans l'ordre

check: all ## Alias de 'all' (CI locale)

format: ## Formate le code avec ruff
	uv run ruff check --fix src/ tests/ app/
	uv run ruff format src/ tests/ app/

lint: ## Vérifie la propreté du code avec ruff (check + format)
	uv run ruff check src/ tests/ app/
	uv run ruff format --check src/ tests/ app/

typecheck: ## Vérifie strictement les types avec mypy
	uv run mypy --explicit-package-bases src/ app/

test: ## Lance les tests unitaires avec couverture complète
	uv run pytest tests/ -v

test-fast: ## Lance les tests et s'arrête à la première erreur
	uv run pytest tests/ -x

###################################################################
# DEV
###################################################################

clean: ## Supprime les fichiers temporaires et les caches
	rm -rf .venv
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage coverage.xml report.xml dist/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Caches et .venv nettoyés"

bump: ## Incrémente la version du projet (via commitizen)
	uv run cz bump

release: ## Pousse les derniers commits et tags vers origin main
	git push origin main --follow-tags
	git push --tags

###################################################################
# AIDE
###################################################################

help: ## Affiche cette aide
	@echo "Usage: make [target]"
	@echo ""
	@echo "Cibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
