from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
# Предполагаем, что ApplicationData теперь импортируется корректно
from models.schemas import ApplicationData
from models.letter import generate_application_pdf
from models.telegram_api import send_document_to_chat

router = APIRouter()


@router.post(
    "/letter/",
    summary="Сформировать заявление на вывоз предмета искусства",
    response_description="PDF-документ (браузер) или JSON-статус (TWA)"
)
async def create_application_letter(data: ApplicationData):
    """
    Принимает данные, генерирует PDF и:
    1. Если TWA=true, отправляет файл в Telegram и возвращает JSON-статус.
    2. Иначе, возвращает бинарный PDF для скачивания в браузере.
    """

    data_dict = data.model_dump()
    pdf_content = None

    try:
        # 1. Генерируем PDF-содержимое (bytes)
        pdf_content = generate_application_pdf(data_dict)
    except Exception as e:
        print(f"Ошибка генерации PDF: {e}")
        # Возвращаем 500 ошибку, если не удалось создать PDF
        raise HTTPException(status_code=500, detail=f"Не удалось создать PDF-документ: {e}")

    # --- УСЛОВНАЯ ЛОГИКА ОТВЕТА ---


    if data.is_twa and data.telegram_user_id:
        # 🔥 РЕЖИМ 1: TWA (Telegram Web App)

        chat_id = data.telegram_user_id
        # Устанавливаем имя файла для Telegram (он сам его отобразит)
        filename = f"Application_{data.last_name}.pdf"
        caption = f"Ваше заявление на вывоз предмета искусства, {data.last_name}."

        print(chat_id, filename, caption)

        # Асинхронно отправляем файл в чат
        telegram_result = await send_document_to_chat(
            chat_id=chat_id,
            document_content=pdf_content,
            filename=filename,
            caption=caption
        )

        if telegram_result:
            # Возвращаем JSON-ответ, который ждет фронтенд TWA
            return {
                "status": "ok",
                "message": "Файл успешно отправлен в чат Telegram."
            }
        else:
            # Если Telegram API вернул ошибку
            raise HTTPException(status_code=500,
                                detail="Ошибка при отправке файла в Telegram. Проверьте токен и chat_id.")

    else:
        # 🔥 РЕЖИМ 2: Браузер (Standalone) - оставляем как есть

        # Устанавливаем имя файла для скачивания в браузере
        filename = f"Application_{data.last_name}.pdf"

        # Возвращаем HTTP-ответ с бинарным содержимым
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                # "attachment" - принуждает браузер к скачиванию
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )