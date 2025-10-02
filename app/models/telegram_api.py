# telegram_helpers.py
import httpx
import os
from typing import Optional

# 🔥 Получение токена бота из переменных окружения
# ВАЖНО: Установите TELEGRAM_BOT_TOKEN в вашем .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    # Заглушка, если токен не найден, но в продакшене это вызовет ошибку
    print("ВНИМАНИЕ: Переменная TELEGRAM_BOT_TOKEN не найдена.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
client = httpx.AsyncClient(base_url=TELEGRAM_API_URL)


async def send_text_message(chat_id: int, text: str, parse_mode: str = "HTML") -> Optional[dict]:
    """Отправляет текстовое сообщение в Telegram-чат."""
    url = "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        response = await client.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Ошибка отправки сообщения: {e.response.text}")
        return None


async def send_document_to_chat(chat_id: int, document_content: bytes, filename: str, caption: str) -> Optional[dict]:
    """Отправляет файл (документ) с подписью в Telegram-чат."""
    url = "sendDocument"
    files = {
        # httpx использует кортежи для multipart/form-data: (filename, content, mime_type)
        "document": (filename, document_content, "application/pdf")
    }
    payload = {
        "chat_id": chat_id,
        "caption": caption
    }

    try:
        response = await client.post(url, data=payload, files=files)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Ошибка отправки документа: {e.response.text}")
        return None


async def set_webhook(url: str, secret_token: str) -> Optional[dict]:
    """
    Устанавливает Telegram Webhook на указанный URL с секретным токеном.

    :param url: Полный HTTPS URL, куда Telegram должен отправлять обновления (например, 'https://yourdomain.com/telegram/webhook/').
    :param secret_token: Секретный токен для заголовка X-Telegram-Bot-Api-Secret-Token.
    """
    endpoint = "setWebhook"
    payload = {
        "url": url,
        "secret_token": secret_token
    }

    try:
        response = await client.post(endpoint, data=payload)
        response.raise_for_status()
        result = response.json()

        if result.get("ok"):
            print(f"✅ Webhook успешно установлен на: {url}")
        else:
            print(f"❌ Ошибка установки Webhook: {result.get('description')}")

        return result

    except httpx.HTTPStatusError as e:
        print(f"🔥 Ошибка HTTP при установке Webhook: {e.response.text}")
        return None
    except Exception as e:
        print(f"🔥 Неизвестная ошибка при установке Webhook: {e}")
        return None