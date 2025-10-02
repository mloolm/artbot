# telegram_helpers.py
import httpx
import os
from typing import Optional
from typing import List, Dict, Any

# 🔥 Получение токена бота из переменных окружения
# ВАЖНО: Установите TELEGRAM_BOT_TOKEN в вашем .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    # Заглушка, если токен не найден, но в продакшене это вызовет ошибку
    print("ВНИМАНИЕ: Переменная TELEGRAM_BOT_TOKEN не найдена.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
client = httpx.AsyncClient(base_url=TELEGRAM_API_URL)
TEMPLATE_DIR = '/app/tlg_templates'


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


async def set_twa_menu_button(twa_url: str, button_text: str, chat_id: Optional[int] = None):
    """
    Устанавливает кнопку 'Меню' слева внизу для запуска TWA.
    Если chat_id не указан, устанавливается для всех пользователей.
    """
    url = "setChatMenuButton"

    menu_button_data = {
        "type": "web_app",
        "text": button_text,
        "web_app": {
            "url": twa_url
        }
    }

    payload = {
        "menu_button": menu_button_data
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        if result.get("ok"):
            print(f"✅ Menu Button TWA успешно установлен ({button_text}).")
        else:
            print(f"❌ Ошибка установки Menu Button: {result.get('description')}")

        return result

    except httpx.HTTPStatusError as e:
        print(f"🔥 Ошибка HTTP при установке Menu Button: {e.response.text}")
        return None


async def set_bot_commands_from_templates():
    """
    Сканирует /app/tlg_templates, формирует команды (/имя_файла),
    и отправляет их в Telegram через API setMyCommands.

    Внимание: API требует, чтобы имя команды было без начального слеша.
    """
    commands_list: List[Dict[str, str]] = []

    descr = {
        "instructions":"Инструкция",
        "personal_data":"Об использовании персональных данных",

    }

    if not os.path.exists(TEMPLATE_DIR):
        print(f"❌ Директория шаблонов не найдена: {TEMPLATE_DIR}")
        return False

    # 1. Сканирование директории и формирование списка команд
    try:
        for filename in os.listdir(TEMPLATE_DIR):
            if filename.endswith(".html"):
                # Удаляем расширение .html
                command_name = filename[:-5]

                # Пропускаем служебные шаблоны (если они есть)
                if command_name.lower() in ("base", "start"):
                    continue

                description = ''
                if command_name in descr:
                    description = descr[command_name]
                commands_list.append({
                    # API ожидает команду БЕЗ слеша
                    "command": command_name,
                    # Простой текст описания
                    "description": description
                })

        if not commands_list:
            print("⚠️ HTML-шаблоны не найдены для создания команд.")
            return False

    except Exception as e:
        print(f"❌ Ошибка сканирования файлов: {e}")
        return False

    # 2. Вызов Telegram API (setMyCommands)
    url = "setMyCommands"
    payload = {
        "commands": commands_list
    }

    print(f"🤖 Отправка {len(commands_list)} команд в Telegram API...")

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("ok"):
            print("✅ Команды бота успешно обновлены.")
            return True
        else:
            print(f"❌ Ошибка API при setMyCommands: {response_data.get('description')}")
            return False

    except Exception as e:
        print(f"🔥 Не удалось установить команды: {e}")
        return False