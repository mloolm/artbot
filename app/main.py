# /app/main.py (Или ваш основной файл приложения)

from typing import List, Optional
from fastapi import FastAPI

# Импортируем роутер, который мы определили
from .routes import router


# --- Приложение FastAPI ---
app = FastAPI(
    title="Letter Generation API",
    description="API для формирования официальных документов (заявлений) в PDF.",
    version="1.0.0",
)


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

# Теперь ваш эндпоинт POST /letter/ доступен!