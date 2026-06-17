from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from ..config import Config

app = FastAPI(
    title="TradeLens API",
    description="Professional Crypto Market Intelligence Dashboard",
    version="1.0.0",
    contact={"name": "crwz46"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
