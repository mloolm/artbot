#!/bin/bash

# ----------------------------------------------------------------------
# Скрипт для эмуляции команды /instructions от Telegram Webhook
# Использует безопасный паттерн с секретным токеном в заголовке
# ----------------------------------------------------------------------

# 🔥 1. ЗАМЕНИТЕ ЭТО ВАШИМ СЕКРЕТНЫМ ТОКЕНОМ
# Это должен быть тот же токен, что и в переменной окружения WEBHOOK_SECRET
SECRET_TOKEN="SOME_SAFE_DEFAULT_SECRET"

# 2. Базовый URL вашего FastAPI-приложения
API_URL="http://localhost:8000"

# 3. ID чата и текст сообщения (команда /instructions)
CHAT_ID=41416491  # Произвольный ID для отладки
MESSAGE_TEXT="/start"

# Структура JSON, которую Telegram отправляет на ваш вебхук
JSON_PAYLOAD=$(cat <<EOF
{
  "update_id": 10000,
  "message": {
    "message_id": 1234,
    "date": $(date +%s),
    "chat": {
      "id": ${CHAT_ID},
      "type": "private"
    },
    "text": "${MESSAGE_TEXT}",
    "from": {
      "id": ${CHAT_ID},
      "first_name": "Debug",
      "is_bot": false
    }
  }
}
EOF
)

# Выполняем POST-запрос с помощью curl
echo "Отправка команды ${MESSAGE_TEXT} на ${API_URL}/telegram/webhook/"
echo "Использование SECRET_TOKEN в заголовке..."
echo "---"

curl -X POST \
     -H "Content-Type: application/json" \
     -H "X-Telegram-Bot-Api-Secret-Token: ${SECRET_TOKEN}" \
     -d "${JSON_PAYLOAD}" \
     "${API_URL}/telegram/webhook/"

echo
echo "---"
echo "Запрос отправлен."