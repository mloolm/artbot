from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from .models.schemas import ApplicationData  # ApplicationData и ItemData теперь здесь
from .models.letter import generate_application_pdf

router = APIRouter()

# --- ФИКСИРОВАННЫЕ ТЕСТОВЫЕ ДАННЫЕ ДЛЯ GET-ЗАПРОСА ОТЛАДКИ ---
# ВНИМАНИЕ: Все ключи и структура должны соответствовать моделям ApplicationData и ItemData

TEST_PAYLOAD = {
    "first_name": "PAVEL",
    "last_name": "PETROV",
    "email": "ggg@gmail.com",
    "citizenship": "ამერიკული სამოას",
    "country_to": "ანდორასკენ",
    "items": [
        {
            "name": "PAINTING NAME",
            "size": "44x55",
            "dimension": "სმ",
            "reason": "მე ვარ ამ ნამუშევრის ავტორი.",
            "item_type": "ნახატი",
            "item_type_rod": "ნახატის",
            "medium": "ზეთი",
            "medium_base": "ტილო"
        }
    ],
    "is_twa": False,
    "telegram_user_id": 0
}


@router.get(
    "/letter/",
    summary="[DEBUG] Сформировать тестовое заявление PDF",
    response_description="Тестовый PDF-документ (application/pdf)"
)
def letter_get():
    """
    Маршрут для отладки. Генерирует PDF, используя фиксированные тестовые данные.
    """

    try:
        # 1. Валидируем тестовые данные через Pydantic
        data = ApplicationData(**TEST_PAYLOAD)
        data_dict = data.model_dump()

        # 2. Генерируем PDF-содержимое
        pdf_content = generate_application_pdf(data_dict)

        # 3. Возвращаем PDF в браузер (или клиент)
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "inline; filename=test_application.pdf"
            }
        )
    except Exception as e:
        print(f"Ошибка генерации тестового PDF: {e}")
        # Возвращаем просто текст в случае ошибки для удобства отладки в браузере
        return {"error": "Не удалось создать тестовый PDF", "details": str(e)}


@router.post(
    "/letter/",
    summary="Сформировать заявление на вывоз предмета искусства в формате PDF",
    response_description="Сформированный PDF-документ (application/pdf) в виде байтов"
)
def create_application_letter(data: ApplicationData):
    """
    Принимает необходимые данные и генерирует готовое заявление в формате PDF.
    Возвращает бинарное содержимое.
    """

    data_dict = data.model_dump()

    try:
        # 1. Генерируем PDF-содержимое (bytes)
        pdf_content = generate_application_pdf(data_dict)

        # 2. Возвращаем HTTP-ответ с бинарным содержимым
        return Response(
            content=pdf_content,
            media_type="application/pdf"
        )

    except Exception as e:
        print(f"Ошибка генерации PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Не удалось создать PDF-документ: {e}")
