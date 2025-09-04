# Використовуємо офіційний Python-образ (slim для меншого розміру)
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо лише requirements.txt для використання кешу Docker
COPY ./requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли додатку
COPY . .

# Запускаємо FastAPI з Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
