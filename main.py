from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from src.infrastructure.database import engine, Base
from src.api.routes import router as api_router
from src.api.routers import router as users_router
from src.api.order_routers import router as order_router
from src.api.auth_routers import router as auth_router
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    yield
    print("Shutting down...")


app = FastAPI(
    title="FastAPI CQRS Commercial Website API",
    description="A commercial website API built with FastAPI, CQRS pattern, and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])


@app.get("/")
async def root():
    return {"message": "FastAPI CQRS Commercial Website API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )