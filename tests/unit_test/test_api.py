"""Tests unitaires des endpoints de l'application FastAPI."""

from pathlib import Path

from fastapi.testclient import TestClient

from titanic_ml.api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Teste que /health répond avec un statut 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_version() -> None:
    """Teste que /version retourne la version attendue."""
    response = client.get("/version")
    assert response.status_code == 200

    expected_version = (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip()
    assert response.json() == {"version": expected_version}


def test_api_home() -> None:
    """Teste la route racine de l'API."""
    response = client.get("/base/")
    assert response.status_code == 200
    assert "Bienvenue sur l'API Titanic ML !" in response.json()["message"]


def test_api_hello() -> None:
    """Teste la route /hello définie dans greetings.py."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_api_bonjour() -> None:
    """Teste la route /bonjour définie dans greetings.py."""
    response = client.get("/bonjour")
    assert response.status_code == 200
    assert response.json() == {"message": "Bonjour le monde !"}


def test_app_metadata() -> None:
    """Vérifie que les paramètres d'initialisation de FastAPI sont corrects."""
    assert app.title == "titanic_ml"
    assert app.description == "API du projet Titanic ML"
    expected_version = (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip()
    assert app.version == expected_version
