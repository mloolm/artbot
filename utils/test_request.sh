#!/bin/bash

# Устанавливаем переменные для удобства
URL="http://localhost:8000/letter/"
OUTPUT_FILE="generated_application_test.pdf"

# Тестовые данные в формате JSON (ОШИБКИ ИСПРАВЛЕНЫ)
JSON_DATA='{
    "first_name": "Pavel",
    "last_name": "Petrov",
    "citizenship": "ამერიკის შეერთებული შტატების",
    "country_to": "უზბეკეთისკენ",
    "email": "pavel@google.com",
    "is_twa": true,
    "telegram_user_id": 41416491,
    "items": [
        {
            "reason": "ეს ნახატი შევიძინე ავტორისგან.",
            "item_type": "ნახატი",
            "item_type_rod": "ნახატის",
            "name": "Item name 1",
            "size": "44x33",
            "dimension": "cm",
            "medium": "ზეთი",
            "medium_base":"ტილოზე"
        },
        {
            "reason": "მე ვარ ამ ნამუშევრის ავტორი.",
            "item_type": "ნახატი",
            "item_type_rod": "ნახატის",
            "name": "Item name 2",
            "size": "66x43",
            "dimension": "cm",
            "medium": "ზეთი",
            "medium_base":"ტილოზე"
        }
    ]
}'

# 1. Отправляем POST-запрос с JSON-данными
echo "Отправка запроса на $URL..."
# Флаг -s скрывает прогресс-бар curl, но -w позволяет увидеть HTTP-код
HTTP_CODE=$(curl -X POST "$URL" \
     -H 'Content-Type: application/json' \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE" \
     -s -w "%{http_code}")

# Проверяем HTTP-код завершения и размер файла
if [ "$HTTP_CODE" -eq 200 ] && [ -s "$OUTPUT_FILE" ]; then
    echo ""
    echo "✅ Успех (HTTP $HTTP_CODE)! PDF-документ сохранен как '$OUTPUT_FILE'."
    echo "Проверьте содержимое файла."
else
    echo ""
    echo "❌ Ошибка! HTTP-код: $HTTP_CODE. Не удалось получить PDF. Проверьте логи Docker-контейнера."
fi