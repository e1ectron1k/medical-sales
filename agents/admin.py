from django.contrib import admin
from .models import Agent, Product, Sale, Presentation

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'commission_rate', 'status', 'registration_date']
    list_filter = ['status', 'registration_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['agent', 'product', 'sale_date', 'total_amount', 'commission']
    list_filter = ['sale_date', 'agent']
    search_fields = ['agent__user__username', 'product__name', 'client_name']

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Автоматическая конвертация при сохранении в админке
        from .utils import process_presentation
        process_presentation(obj)