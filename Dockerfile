FROM python:3.9

# Создаем директорию /todo внутри образа
RUN mkdir /todo

# Устанавливаем рабочую директорию
WORKDIR /todo

# Копируем файл requirements.txt в директорию /todo внутри образа
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы и директории в /todo внутри образа
COPY . .

# Выдаём права
RUN chmod a+x /todo/app.sh

# Команда, которая будет выполняться при запуске контейнера
CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]


