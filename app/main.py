
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import items

# создание экземпляра FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    description="Микросервис для управления товарами с REST API",
    version="1.0.0",
    docs_url="/docs", 
)

# корсы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключение роутеров
app.include_router(items.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "FastAPI Microservice is running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    
    return {"status": "healthy"}