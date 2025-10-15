from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config.database import Database
from routes.user_routes import router as user_router
from middlewares.logging_middleware import log_requests_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    await Database.connect_db()
    yield
    await Database.close_db()

app = FastAPI(
    title="User Service API",
    description="API REST para gestión de usuarios con FastAPI y MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

app.middleware("http")(log_requests_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de verificación de salud"""
    return {
        "status": "ok",
        "message": "User Service API is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)