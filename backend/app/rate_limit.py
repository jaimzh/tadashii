
import os
from urllib.parse import urlparse

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_real_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return get_remote_address(request)


def get_rate_limit_storage_uri() -> str:
    redis_url = (os.getenv("REDIS_URL") or "").strip().strip("\"'")

    if not redis_url:
        return "memory://"

    try:
        parsed_url = urlparse(redis_url)
        if parsed_url.scheme not in {"redis", "rediss", "redis+sentinel"}:
            return "memory://"
        # Accessing port forces urllib to validate it before SlowAPI imports.
        _ = parsed_url.port
    except ValueError:
        return "memory://"

    return redis_url


RATE_LIMIT_STORAGE_URI = get_rate_limit_storage_uri()

limiter = Limiter(
    key_func=get_real_client_ip,
    storage_uri=RATE_LIMIT_STORAGE_URI,
    key_prefix="tadashii:"
)

