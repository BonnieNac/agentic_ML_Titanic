"""Composants middleware pour l'application FastAPI."""

import os
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    """Middleware limitant la taille des requêtes entrantes.

    Rejette les requêtes dont le Content-Length dépasse la limite fixée.
    """

    def __init__(self, app: ASGIApp, max_upload_size: int | None = None) -> None:
        super().__init__(app)
        # 50 Mo par défaut si non spécifié
        self.max_upload_size = max_upload_size or int(os.getenv("API_MAX_UPLOAD_SIZE", "52428800"))

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Traite la requête et la rejette si la charge dépasse la limite de taille."""
        content_length = request.headers.get("content-length")

        if content_length and int(content_length) > self.max_upload_size:
            logger.warning(f"Requête trop volumineuse : {content_length} octets (limite : {self.max_upload_size})")
            return JSONResponse(
                status_code=413,
                content={
                    "detail": f"Requête trop volumineuse. Taille maximale autorisée : {self.max_upload_size} octets."
                },
            )

        return await call_next(request)
