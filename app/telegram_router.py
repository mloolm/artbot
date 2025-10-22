# telegram_router.py
from fastapi import APIRouter, Request, HTTPException
import os
import json
from typing import Optional
from models.telegram_api import  send_text_message
from fastapi import Header
from models.telegram_api import send_menu_keyboard, get_httpx_client
router = APIRouter(prefix="/telegram")

# Получаем токен из окружения (для проверки вебхука)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TEST_TOKEN_PLACEHOLDER")
# Ваш секретный токен, который НЕ ТОКЕН БОТА!
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Директория для HTML-шаблонов
TEMPLATE_DIR = '/app/tlg_templates'


def load_template(command: str) -> Optional[str]:
    """Загружает HTML-шаблон по имени команды (например, /start -> start.html)."""
    filename = os.path.join(TEMPLATE_DIR, f"{command}.html")

    print(filename)
    if os.path.exists(filename):
        print ("OK")
    else:
        # Проверка, куда смотрит os.getcwd()
        print (f"path_checked: {filename}, exists: False, cwd: {os.getcwd()}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:

        return None


@router.post("/webhook/")
async def telegram_webhook(
        request: Request,
        x_telegram_bot_api_secret_token: str = Header(None)  # Получаем заголовок
):

    print(x_telegram_bot_api_secret_token, request)

    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Неверный секретный заголовок.")

    try:
        update = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неверный формат JSON.")

    # Если это не сообщение, игнорируем
    if "message" not in update:
        return {"status": "ok"}

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    command_dict = {
        'об использовании персональных данных': 'personal_data',
        'инструкция':'instructions'
    }

    command = text.lower().lstrip("/")

    if command:
        # Обрабатываем команду

        template_content = load_template(command)
        if not template_content:
            if command in command_dict:
                template_content = load_template(command_dict[command])

        if template_content:
            await send_text_message(chat_id, template_content)
        elif text == '/start':
            await send_menu_keyboard(chat_id, get_httpx_client(), 10)
        else:
            await send_text_message(
                chat_id,
                f"Неизвестная команда '{text}'. Используйте меню внизу экрана",
                parse_mode="html"
            )

    return {"status": "ok"}