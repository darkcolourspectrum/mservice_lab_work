# Dockerfile
# Multi-stage сборка

# Stage 1: Builder - установка зависимостей
FROM python:3.11-slim as builder

# Установка необходимых системных пакетов для компиляции
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv

# Активация виртуального окружения
ENV PATH="/opt/venv/bin:$PATH"

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime - финальный образ
FROM python:3.11-slim

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование виртуального окружения из builder stage
COPY --from=builder /opt/venv /opt/venv

# Установка рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY . .

# Активация виртуального окружения
ENV PATH="/opt/venv/bin:$PATH"

# Создание непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose порт приложения
EXPOSE 8000

# Команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]