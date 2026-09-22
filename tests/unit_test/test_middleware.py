"""Tests unitaires des middlewares FastAPI."""

import pytest
from fastapi.testclient import TestClient

from titanic_ml.api.main import app

client = TestClient(app)


def test_large_request_rejected() -> None:
    """Teste que les requêtes dépassant la limite de Content-Length sont rejetées avec un 413."""
    response = client.post("/health", headers={"content-length": "999999999"})

    assert response.status_code == 413
    assert "Requête trop volumineuse" in response.json()["detail"]


def test_normal_request_passes() -> None:
    """Teste que les requêtes normales sans charge excessive passent normalement."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_request_without_content_length_passes() -> None:
    """Teste que l'absence d'en-tête Content-Length ne bloque pas la requête."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_custom_max_upload_size(monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste que la limite de téléversement est bien chargée et appliquée depuis la variable d'environnement.

    On instancie une app de test locale car l'app globale a déjà évalué os.getenv
    lors de son import, rendant monkeypatch inefficace sur elle.
    """
    monkeypatch.setenv("API_MAX_UPLOAD_SIZE", "100")

    from fastapi import FastAPI

    from titanic_ml.api.middlewares import LimitUploadSizeMiddleware

    test_app = FastAPI()
    test_app.add_middleware(LimitUploadSizeMiddleware)

    @test_app.post("/test")
    def test_route() -> dict:
        return {"status": "ok"}

    local_client = TestClient(test_app)

    # 200 octets > limite de 100 octets
    response = local_client.post("/test", headers={"content-length": "200"})
    assert response.status_code == 413
