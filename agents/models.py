from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Agent(models.Model):
    AGENT_STATUS = [
        ('active', 'Активный'),
        ('inactive', 'Неактивный'),
        ('suspended', 'Приостановлен'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=10.00,
        verbose_name='Процент комиссии'
    )
    status = models.CharField(
        max_length=10, 
        choices=AGENT_STATUS, 
        default='active',
        verbose_name='Статус'
    )
    registration_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, verbose_name='Заметки')
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"
    
    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название оборудования')
    category = models.CharField(max_length=100, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

class Sale(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Оборудование')
    sale_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    commission = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Комиссия')
    client_name = models.CharField(max_length=200, verbose_name='Клиент')
    client_contact = models.CharField(max_length=200, verbose_name='Контакты клиента')
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.product.price * self.quantity
        if not self.commission:
            self.commission = self.total_amount * (self.agent.commission_rate / 100)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Продажа {self.product.name} - {self.agent.user.username}"
    
    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

class Presentation(models.Model):
    PRESENTATION_TYPES = [
        ('html', 'HTML презентация'),
        ('link', 'Внешняя ссылка'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название презентации')
    description = models.TextField(verbose_name='Описание', blank=True)
    presentation_type = models.CharField(
        max_length=10, 
        choices=PRESENTATION_TYPES, 
        default='html',
        verbose_name='Тип презентации'
    )
    html_content = models.TextField(verbose_name='HTML контент', blank=True)
    external_url = models.URLField(verbose_name='Внешняя ссылка', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_content(self):
        if self.presentation_type == 'html' and self.html_content:
            return self.html_content
        elif self.external_url:
            return f'<p><a href="{self.external_url}" class="btn" target="_blank">🌐 Открыть внешний ресурс</a></p>'
        else:
            return '<p>Контент пока не доступен</p>'
        
    def get_content(self):
        """Возвращает HTML контент презентации"""
        if self.html_content:
            return self.html_content
        elif self.file and self.file.name.endswith('.html'):
            # Если нужно читать из файла
            try:
                return self.file.read().decode('utf-8')
            except:
                return "<p>Контент недоступен</p>"
        else:
            return "<p>Презентация в процессе подготовки</p>"
    
    class Meta:
        verbose_name = 'Презентация'
        verbose_name_plural = 'Презентации'

class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Отправлен'),
        ('approved', 'Подтвержден'),
        ('completed', 'Выполнен'),
    ]
    
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price