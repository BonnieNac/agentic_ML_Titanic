"""Routes système de l'API : santé et version."""

from fastapi import APIRouter, Request

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    """Retourne l'état de santé de l'API."""
    return {"status": "ok"}


@router.get("/version")
def version(request: Request) -> dict[str, str]:
    """Retourne la version courante de l'application."""
    return {"version": request.app.version}
