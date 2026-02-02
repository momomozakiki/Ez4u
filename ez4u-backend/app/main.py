from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# Import routers
from app.routers import auth, users

# Create FastAPI app instance
app = FastAPI(
    title="Ez4u Backend API",
    description="FastAPI backend for Ez4u SaaS application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])

# Pydantic model for response
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        message="FastAPI backend is running successfully!"
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Ez4u Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }
