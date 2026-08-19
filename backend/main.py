from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import RECOMMENDATION_RATE_LIMIT
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.recommend import router as recommend_router            
from app.api.quotes import router as quotes_router
from app.rate_limit import limiter

app = FastAPI(
    title="Tadashii API",
    description="Backend API for the Tadashii application",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Tadashii API!",
        "status": "healthy",
        "version": "0.1.0"
    }

app.include_router(recommend_router, prefix="/api")
app.include_router(quotes_router, prefix="/api")


@app.get("/health")
@limiter.limit(RECOMMENDATION_RATE_LIMIT)
async def health_check(request: Request):
    return {
        "status": "ok",
        "details": "All systems operational"
    }



# cd backend
# venv\Scripts\activate
# uvicorn main:app --reload
