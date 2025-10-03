from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from io import BytesIO  # Используем буфер в памяти
from datetime import datetime
from typing import List, Dict

# Указываем, где искать шаблон 
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
template_loader = FileSystemLoader(searchpath=TEMPLATE_DIR)
env = Environment(loader=template_loader)


def generate_application_pdf(data: dict) -> bytes:
    """
    Генерирует PDF-заявление из шаблона, используя данные.
    Возвращает содержимое PDF в виде байтов.
    """

    # 1. Загрузка шаблона
    template = env.get_template("application_template.html")

    # 2. Рендеринг шаблона с данными
    # Мы используем метод replace для подстановки ваших %плейсхолдеров%
    rendered_html = template.render()

    #множественное / единственное
    mn = "გთხოვთ მომცეთ ჩემს კუთვნილებაში არსებული ხელოვნების ნიმუშების ქვეყნიდან გატანის სანებართვო მოწმობა, %country_to%."
    ed = "გთხოვთ მომცეთ/მისცეთ ჩემს კუთვნილებაში არსებული %item_type_rod% ქვეყნიდან გატანის სანებართვო მოწმობა, %country_to%."

    items: List = data.get('items', [])
    item_count = len(items)
    #item_count = 1


    if item_count > 1:
        rendered_html = rendered_html.replace(f"%request%", mn)
    else:
        rendered_html = rendered_html.replace(f"%request%", ed)
        rendered_html = rendered_html.replace(f"%item_type_rod%", str(items[0]['item_type_rod']))


    for key, value in data.items():
        if not isinstance(value, (list, dict)):
            rendered_html = rendered_html.replace(f"%{key}%", str(value))

    #фОРМИРУЕМ СПИСОК РАБОТ
    list_html = ""

    for num, art_data in enumerate(items):
        medium = art_data['medium']
        if art_data['medium_base']:
            medium=f"{medium}, {art_data['medium_base']}"

        if item_count > 1:
            list_html += f"{num+1}) "
        list_html+=f"{art_data['item_type']}, \"{art_data['name']}\", {art_data['size']}{art_data['dimension']}, {medium}"
        if item_count>1:
            list_html+=f". {art_data['reason']}"
        list_html+='<br>'

    rendered_html = rendered_html.replace(f"%art_list%", list_html)
    rendered_html = rendered_html.replace(f"%date%", datetime.now().strftime("%d.%m.%Y"))

    # 3. Генерация PDF в буфер в памяти (BytesIO)
    pdf_buffer = BytesIO()

    # Используем HTML(string=...).write_pdf(target=...)
    HTML(
        string=rendered_html,
        encoding="UTF-8",
        base_url=TEMPLATE_DIR  # Полезно, если в шаблоне есть ссылки на CSS/изображения
    ).write_pdf(pdf_buffer)

    # Возвращаем содержимое буфера (PDF-файл)
    return pdf_buffer.getvalue()