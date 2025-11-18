#!/bin/bash
echo "Установка системы медицинских продаж..."

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем только Django
pip install django==4.2.7

# Создаем структуру папок
mkdir -p agents/templates/agents
mkdir -p static/css static/js

# Выполняем миграции
python manage.py makemigrations
python manage.py migrate

# Создаем суперпользователя
echo "Создание суперпользователя..."
python manage.py createsuperuser

echo ""
echo "=== УСТАНОВКА ЗАВЕРШЕНА ==="
echo "Запуск сервера: python manage.py runserver"
echo "Адрес: http://127.0.0.1:8000"
echo "Админка: http://127.0.0.1:8000/admin"