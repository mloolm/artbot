from pydantic import BaseModel, Field
from typing import List


# --- Модель для одного предмета (картины) ---
class ItemData(BaseModel):
    """Модель для описания одного предмета искусства."""
    reason: str = Field(..., description="Заявление о происхождении (груз.).")
    item_type: str = Field(..., description="Тип предмета (именительный падеж, груз.).")
    item_type_rod: str = Field(..., description="Тип предмета (родительный падеж, груз.).")
    name: str = Field(..., description="Название предмета.")
    size: str = Field(..., description="Размеры (напр., '44x33').")
    dimension: str = Field(..., description="Единица измерения (напр., 'cm').")
    medium: str = Field(..., description="Техника/Материал (груз.).")
    medium_base: str = Field(..., description="База - холст, доска, картон (груз.).")


# --- Модель для всего запроса ---
class ApplicationData(BaseModel):
    """Основная модель для данных заявления на вывоз."""
    first_name: str
    last_name: str
    citizenship: str = Field(..., description="Гражданство в грузинском именительном падеже.")
    country_to: str = Field(..., description="Страна назначения в направительном падеже (напр., 'უზბეკეთისკენ').")
    email: str
    telegram_user_id:int
    is_twa:bool


    # НОВОЕ ПОЛЕ: Список предметов
    items: List[ItemData] = Field(..., description="Список предметов для вывоза.")

    class Config:
        json_schema_extra = {
            "example": {
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
                        "medium": "ზეთი",
                        "medium_base": "ტილო"
                    },
                    {
                        "reason": "მე ვარ ამ ნამუშევრის ავტორი.",
                        "item_type": "ნახატი",
                        "item_type_rod": "ნახატის",
                        "name": "Item name 2",
                        "size": "66x43",
                        "dimension": "cm",
                        "medium": "ზეთი",
                        "medium_base": "ტილო"
                    }
                ]
            }
        }