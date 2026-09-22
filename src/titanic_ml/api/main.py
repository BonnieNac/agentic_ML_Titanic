"""Point d'entrée principal de l'application FastAPI."""

from fastapi import FastAPI

from titanic_ml.api.middlewares import LimitUploadSizeMiddleware
from titanic_ml.api.routers import base, greetings, system
from titanic_ml.core.utils import ensure_dirs_exist, get_project_version

# Initialise les répertoires du projet au démarrage
ensure_dirs_exist()

app = FastAPI(
    title="titanic_ml",
    description="API du projet Titanic ML",
    version=get_project_version(),
)

# Middleware global de limitation de taille des requêtes
app.add_middleware(LimitUploadSizeMiddleware)


app.include_router(base.router)
app.include_router(system.router)
app.include_router(greetings.router)


def main() -> None:  # pragma: no cover
    """Lance l'application FastAPI avec uvicorn."""
    import uvicorn

    uvicorn.run("titanic_ml.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
