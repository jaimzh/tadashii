from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.recommend import router as recommend_router            
from app.api.quotes import router as quotes_router

app = FastAPI(
    title="Tadashii API",
    description="Backend API for the Tadashii application",
    version="0.1.0",
)

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
async def health_check():
    return {
        "status": "ok",
        "details": "All systems operational"
    }



# cd backend
# venv\Scripts\activate
# cd app
# uvicorn app.main:app --reload
