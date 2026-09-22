"""Routes de salutation, en plusieurs langues."""

from fastapi import APIRouter

router = APIRouter(tags=["greetings"])


@router.get("/hello")
def say_hello() -> dict[str, str]:
    """Retourne un message de salutation en anglais."""
    return {"message": "Hello world!"}


@router.get("/bonjour")
def say_bonjour() -> dict[str, str]:
    """Retourne un message de salutation en français."""
    return {"message": "Bonjour le monde !"}
