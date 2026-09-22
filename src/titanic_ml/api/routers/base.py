"""Route de base de l'API, incluant le message de bienvenue."""

from fastapi import APIRouter

router = APIRouter(prefix="/base", tags=["base"])


@router.get("/")
def home() -> dict[str, str]:
    """Retourne un message de bienvenue."""
    return {"message": "Bienvenue sur l'API Titanic ML !"}
