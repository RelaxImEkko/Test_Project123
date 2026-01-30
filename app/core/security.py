from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key
