from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent_list, name='agent_list'),
    path('<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('presentations/', views.presentation_list, name='presentation_list'),
    path('presentations/<int:presentation_id>/', views.presentation_detail, name='presentation_detail'),
    path('presentations/upload/', views.upload_presentation, name='upload_presentation'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('presentation/<int:presentation_id>/category/<str:category_slug>/', 
         views.product_category, name='product_category'),
]