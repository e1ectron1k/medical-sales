@echo off
echo Установка системы медицинских продаж...

echo Создание виртуального окружения...
python -m venv venv
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt

echo Применение миграций...
python manage.py makemigrations
python manage.py migrate

echo Создание суперпользователя...
python manage.py createsuperuser

echo Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Установка завершена!
echo ========================================
echo.
echo Для запуска сервера выполните:
echo venv\Scripts\activate.bat
echo python manage.py runserver
echo.
echo Затем откройте в браузере: http://127.0.0.1:8000
echo Админка: http://127.0.0.1:8000/admin
pause