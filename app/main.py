from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from models.telegram_api import set_bot_config

from routes import router
from telegram_router import router as tlg_router

# --- Приложение FastAPI ---
app = FastAPI(
    title="Letter Generation API",
    description="API для формирования официальных документов (заявлений) в PDF.",
    version="1.0.0",
)

origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,             
    allow_methods=["*"],                
    allow_headers=["*"],                
)

@app.on_event("startup")
async def startup_event():
    await set_bot_config()

@app.get("/")
def read_root():
    """Корневой маршрут, возвращает приветственное сообщение."""
    return {"message": "Привет! API для управления картинами работает."}


# --- Подключение роутинга ---
# FastAPI подключит все маршруты, определенные в router,
# например, /letter/
app.include_router(
    router,
    prefix="", # Оставляем префикс пустым, чтобы маршрут был доступен как /letter/
    tags=["documents"] # Группируем маршруты в документации
)

app.include_router(
    tlg_router
)


# Теперь ваш эндпоинт POST /letter/ доступен!