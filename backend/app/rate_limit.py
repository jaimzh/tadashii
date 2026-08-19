

import os
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

def get_real_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return get_remote_address(request)



redis_url = os.getenv("REDIS_URL")

limiter = Limiter(
    key_func=get_real_client_ip,
    storage_uri=redis_url or "memory://",
    key_prefix="tadashii:"
)

