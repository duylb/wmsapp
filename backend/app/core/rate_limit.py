from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from redis import Redis

from app.core.config import settings


# ==========================================
# REDIS CLIENT
# ==========================================

redis_client = Redis.from_url(settings.REDIS_URL)


# ==========================================
# LIMITER INSTANCE
# ==========================================

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.REDIS_URL,
)


# ==========================================
# EXCEPTION HANDLER
# ==========================================

def rate_limit_exceeded_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
    )