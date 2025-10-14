# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для WeasyPrint (Cairo, Pango, GLib, Fonts)
# 1. build-essential, libffi-dev: Для компиляции python-пакетов
# 2. libcairo2, libglib2.0-0: Core WeasyPrint dependencies
# 3. libpango-1.0-0, libpangoft2-1.0-0: КЛЮЧЕВОЙ пакет для рендеринга шрифтов Pango/FreeType (ИСПРАВЛЕНИЕ)
# 4. libharfbuzz0b, libfreetype6: Дополнительные зависимости для работы со шрифтами
# 5. fontconfig, fonts-dejavu-core, fonts-noto: Шрифты и утилита для их кеширования
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libcairo2 \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfreetype6 \
    fontconfig \
    fonts-dejavu-core \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*

# Обновляем кэш шрифтов для WeasyPrint
RUN fc-cache -f -v

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Экспонируем порт FastAPI
EXPOSE 8000