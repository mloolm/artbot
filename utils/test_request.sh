#!/bin/bash

# Устанавливаем переменные для удобства
URL="http://localhost:8000/letter/"
OUTPUT_FILE="generated_application_test.pdf"

# Тестовые данные в формате JSON (обязательно используем двойные кавычки)
JSON_DATA='{
    "first_name": "Pavel",
    "last_name": "Petrov",
    "citizenship": "ამერიკის შეერთებული შტატების",
    "country_to": "უზბეკეთისკენ",
    "email": "pavel@google.com",
    "items": [
        {
            "reason": "ეს ნახატი შევიძინე ავტორისგან.",
            "item_type": "ნახატი",
            "item_type_rod": "ნახატის",
            "name": "Item name 1",
            "size": "44x33",
            "dimension": "cm",
            "medium": "ზეთი ტილოზე"
        },
        {
            "reason": "მე ვარ ამ ნამუშევრის ავტორი.",
            "item_type": "ნახატი",
            "item_type_rod": "ნახატის",
            "name": "Item name 2",
            "size": "66x43",
            "dimension": "cm",
            "medium": "ზეთი ტილოზე"
        }
    ]
}'

# 1. Отправляем POST-запрос с JSON-данными
echo "Отправка запроса на $URL..."
curl -X POST "$URL" \
     -H 'Content-Type: application/json' \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE"

# Проверяем код завершения и размер файла
if [ $? -eq 0 ] && [ -s "$OUTPUT_FILE" ]; then
    echo ""
    echo "✅ Успех! PDF-документ сохранен как '$OUTPUT_FILE'."
    echo "Проверьте содержимое файла."
else
    echo ""
    echo "❌ Ошибка! Не удалось получить PDF. Проверьте логи Docker-контейнера."
fi