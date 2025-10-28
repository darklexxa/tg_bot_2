# 1. Используем минимальный образ Python под ARM64 (совместим с M1/M2)
FROM python:3.11-slim

# 2. Задаём рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем ВСЕ файлы твоего проекта внутрь контейнера
COPY . .

# 4. Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Указываем, что запускать внутри контейнера
CMD ["python", "bot.py"]