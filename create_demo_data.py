import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_sales.settings')
django.setup()

from django.contrib.auth.models import User
from agents.models import Agent, Product, Presentation
from agents.utils import create_sample_presentation

def create_demo_data():
    print("Создание демо-данных...")
    
    # Создаем демо-агентов
    agent1, created = User.objects.get_or_create(
        username='agent1',
        defaults={
            'first_name': 'Иван',
            'last_name': 'Петров', 
            'email': 'agent1@example.com',
            'is_staff': False
        }
    )
    if created:
        agent1.set_password('agent123')
        agent1.save()
        Agent.objects.create(
            user=agent1,
            phone='+7 (999) 123-45-67',
            address='Москва, ул. Примерная, 1',
            commission_rate=10.00
        )
        print("Создан агент: agent1 / agent123")
    
    agent2, created = User.objects.get_or_create(
        username='agent2',
        defaults={
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'email': 'agent2@example.com', 
            'is_staff': False
        }
    )
    if created:
        agent2.set_password('agent123')
        agent2.save()
        Agent.objects.create(
            user=agent2,
            phone='+7 (999) 123-45-68',
            address='Санкт-Петербург, ул. Образцовая, 2',
            commission_rate=12.00
        )
        print("Создан агент: agent2 / agent123")
    
    # Создаем продукты
    products_data = [
        {'name': 'ЭКГ аппарат CARDIOMAX', 'category': 'Диагностика', 'price': 150000},
        {'name': 'УЗИ аппарат SonoScape', 'category': 'Диагностика', 'price': 450000},
        {'name': 'Инфузионная помпа', 'category': 'Терапия', 'price': 85000},
        {'name': 'Дефибриллятор', 'category': 'Реанимация', 'price': 120000},
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"Создан продукт: {product.name}")
    
    # Создаем демо-презентацию
    presentation, created = Presentation.objects.get_or_create(
        title='Введение в медицинскую технику',
        defaults={
            'description': 'Базовое обучение по основным видам медицинского оборудования',
            'presentation_type': 'html',
            'html_content': create_sample_presentation(),
            'is_active': True
        }
    )
    if created:
        print("Создана демо-презентация")
    
    print("\n=== ДЕМО-ДАННЫЕ СОЗДАНЫ ===")
    print("Логины для тестирования:")
    print("Администратор: ваш суперпользователь")
    print("Агент 1: agent1 / agent123")
    print("Агент 2: agent2 / agent123")
    print("\nДля входа откройте: http://127.0.0.1:8000/login")

if __name__ == '__main__':
    create_demo_data()