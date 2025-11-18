#!/bin/bash
echo "Исправление установки системы..."

# Активация виртуального окружения
source venv/bin/activate

# Создаем правильную структуру папок
mkdir -p agents/templates/agents
mkdir -p static/css
mkdir -p static/js
mkdir -p media/presentations

# Применяем миграции
echo "Применение миграций..."
python manage.py makemigrations agents
python manage.py migrate

# Создаем суперпользователя
echo "Создание суперпользователя..."
python manage.py createsuperuser

echo ""
echo "=== ИСПРАВЛЕНИЕ ЗАВЕРШЕНО ==="
echo "Запуск сервера..."
python manage.py runserver