import httpx
import os
from typing import List, Dict, Optional, Any
import json

# 🔥 Получение токена бота из переменных окружения
# ВАЖНО: Установите TELEGRAM_BOT_TOKEN в вашем .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    # Заглушка, если токен не найден, но в продакшене это вызовет ошибку
    print("ВНИМАНИЕ: Переменная TELEGRAM_BOT_TOKEN не найдена.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
client = httpx.AsyncClient(base_url=TELEGRAM_API_URL)
TEMPLATE_DIR = '/app/tlg_templates'
COMMAND_DESCRIPTIONS = {
    "instructions": "Инструкция",
    "personal_data": "Об использовании персональных данных",
}

def get_api_url():
    return TELEGRAM_API_URL

def get_httpx_client():
    return httpx.AsyncClient(base_url=TELEGRAM_API_URL)

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

    url = url.strip()

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
            print(f"❌ Ошибка установки Webhook: {result.get('description')} {url} {secret_token}")

        return result

    except httpx.HTTPStatusError as e:
        print(f"🔥 Ошибка HTTP при установке Webhook: {e.response.text} {url}")
        return None
    except Exception as e:
        print(f"🔥 Неизвестная ошибка при установке Webhook: {e} {url}")
        return None


async def set_twa_menu_button_global(
        twa_url: str,
        button_text: str = "Открыть приложение"  # Текст кнопки по умолчанию
):
    """
    Устанавливает глобальную кнопку 'Меню' (Web App) для всех пользователей бота.
    """

    twa_url = twa_url.strip()
    url = TELEGRAM_API_URL + "setChatMenuButton"

    menu_button_data = {
        "type": "web_app",
        "text": button_text,
        "web_app": {
            "url": twa_url
        }
    }

    # В API Bot Telegram этот параметр 'menu_button' должен быть передан
    # в качестве поля 'data' при использовании requests (httpx)
    payload = {
        "menu_button": menu_button_data
    }

    # Можно использовать 'setChatMenuButton' без chat_id для установки глобальной кнопки.

    try:
        async with httpx.AsyncClient() as client:
            # Отправка данных как JSON
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            if result.get("ok"):
                print(f"✅ Menu Button TWA успешно установлен глобально ({button_text}).")
            else:
                # В случае ошибки API Telegram вернет 'ok: false'
                print(f"❌ Ошибка установки Menu Button: {result.get('description')}")

            return result

    except httpx.HTTPStatusError as e:
        print(f"🔥 Ошибка HTTP ({e.response.status_code}) при установке Menu Button: {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"🌍 Ошибка запроса (сеть/DNS) при установке Menu Button: {e}")
        return None


def _scan_template_commands() -> Optional[List[str]]:
    """
    Сканирует директорию шаблонов и возвращает список имен команд (без слеша).
    Возвращает None в случае ошибки или если директория не найдена.
    """
    if not os.path.exists(TEMPLATE_DIR):
        print(f"❌ Директория шаблонов не найдена: {TEMPLATE_DIR}")
        return None

    command_names: List[str] = []
    try:
        for filename in os.listdir(TEMPLATE_DIR):
            if filename.endswith(".html"):
                command_name = filename[:-5]
                # Пропускаем служебные шаблоны
                if command_name.lower() in ("base"):
                    continue
                command_names.append(command_name)

        return command_names

    except Exception as e:
        print(f"❌ Ошибка сканирования файлов: {e}")
        return None


# --- ОСНОВНЫЕ ФУНКЦИИ ---

async def set_bot_commands_from_templates(client: httpx.AsyncClient) -> bool:
    """
    Сканирует /app/tlg_templates, формирует команды (/имя_файла),
    и отправляет их в Telegram через API setMyCommands.
    """
    command_names = _scan_template_commands()
    if command_names is None:
        return False

    commands_list: List[Dict[str, str]] = []


    # Добавляем команды из шаблонов
    for command_name in command_names:
        # Пропускаем 'start', если он случайно оказался в шаблонах
        if command_name.lower() == "start":
            continue

        description = COMMAND_DESCRIPTIONS.get(command_name, "Служебная команда")
        commands_list.append({
            # API ожидает команду БЕЗ слеша
            "command": command_name,
            # Простой текст описания
            "description": description
        })

    if not commands_list:
        print("⚠️ HTML-шаблоны не найдены для создания команд.")
        return False

    # 2. Вызов Telegram API (setMyCommands)
    url = TELEGRAM_API_URL + "setMyCommands"
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


async def send_menu_keyboard(chat_id: int, client: httpx.AsyncClient, row_limit: int = 2) -> bool:
    """
    Сканирует команды, генерирует ReplyKeyboardMarkup и отправляет ее пользователю
    вместе с сообщением. Это делает клавиатуру "постоянной" в чате.
    """
    command_names = _scan_template_commands()
    if command_names is None:
        return False

    # --- Формируем список кнопок с понятным текстом (описанием) ---
    keyboard_buttons: List[str] = []

    for name in command_names:
        # Используем описание из словаря COMMAND_DESCRIPTIONS.
        # Если описания нет, используем команду со слешем как запасной вариант.
        description = COMMAND_DESCRIPTIONS.get(name, f"/{name}")
        keyboard_buttons.append(description)

    # --- Построение ReplyKeyboardMarkup ---
    keyboard_rows: List[List[str]] = []
    current_row: List[str] = []

    # 1. Добавляем кнопку /start (используем ее описание, например, "Главное меню")
    start_text = COMMAND_DESCRIPTIONS.get("start", "/start")


    # 2. Распределяем остальные команды по рядам
    for button_text in keyboard_buttons:
        # Пропускаем, если "/start" случайно попало сюда
        if button_text == start_text:
            continue

        if len(current_row) >= row_limit:
            keyboard_rows.append(current_row)
            current_row = []

        current_row.append(button_text)

    if current_row:
        keyboard_rows.append(current_row)

    reply_markup = {
        "keyboard": keyboard_rows,
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

    # --- Отправка сообщения с клавиатурой ---
    url = "sendMessage"
    response_payload = {
        "chat_id": chat_id,
        "text": "Здравствуйте! В этом боте вы найдете инструкции и генератор заявления на разрешение на вывоз художественных работ.\n\nПолная инструкция тут /instructions",
        "parse_mode": "Markdown",
        "reply_markup": reply_markup
    }

    try:
        response = await client.post(url, json=response_payload)
        response.raise_for_status()

        if response.json().get("ok"):
            print(f"✅ Клавиатура команд успешно отправлена в чат {chat_id}.")
            return True
        else:
            print(f"❌ Ошибка отправки клавиатуры: {response.json().get('description')}")
            return False

    except Exception as e:
        print(f"🔥 Не удалось отправить сообщение с клавиатурой: {e}")
        return False


async def set_bot_config():
    url = f"{os.getenv('BACK_URL')}/telegram/webhook/"
    await set_webhook(url, TELEGRAM_BOT_TOKEN)

    front_url = os.getenv('FRONT_URL')
    await set_twa_menu_button_global(front_url, 'Создать заявление')
    await set_bot_commands_from_templates(get_httpx_client())
