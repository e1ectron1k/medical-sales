from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import Agent, Product, Sale, Presentation, Order, OrderItem
from .forms import PresentationForm, OrderForm, OrderItemForm
from .utils import create_sample_presentation

@login_required
def dashboard(request):
    try:
        agent = Agent.objects.get(user=request.user)
    except Agent.DoesNotExist:
        agent = None
    
    if agent:
        sales = Sale.objects.filter(agent=agent)
        total_sales = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_commission = sales.aggregate(Sum('commission'))['commission__sum'] or 0
        sales_count = sales.count()
        
        context = {
            'agent': agent,
            'total_sales': total_sales,
            'total_commission': total_commission,
            'sales_count': sales_count,
            'recent_sales': sales.order_by('-sale_date')[:5],
        }
    else:
        total_agents = Agent.objects.count()
        active_agents = Agent.objects.filter(status='active').count()
        total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_commission = Sale.objects.aggregate(Sum('commission'))['commission__sum'] or 0
        
        context = {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'total_sales': total_sales,
            'total_commission': total_commission,
            'recent_agents': Agent.objects.order_by('-registration_date')[:5],
        }
    
    return render(request, 'agents/dashboard.html', context)

@login_required
def agent_list(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    agents = Agent.objects.all()
    return render(request, 'agents/agent_list.html', {'agents': agents})

@login_required
def agent_detail(request, agent_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    agent = get_object_or_404(Agent, id=agent_id)
    sales = Sale.objects.filter(agent=agent)
    
    context = {
        'agent': agent,
        'sales': sales,
        'total_sales': sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_commission': sales.aggregate(Sum('commission'))['commission__sum'] or 0,
    }
    
    return render(request, 'agents/agent_detail.html', context)

@login_required
def presentation_list(request):
    presentations = Presentation.objects.filter(is_active=True)
    
    if not presentations.exists():
        demo_presentation = Presentation(
            title='Демо-презентация: Введение в систему',
            description='Обзор системы медицинских продаж и возможностей для агентов',
            presentation_type='html',
            html_content=create_sample_presentation()
        )
        demo_presentation.save()
        presentations = Presentation.objects.filter(is_active=True)
    
    context = {
        'presentations': presentations,
    }
    
    return render(request, 'agents/presentations.html', context)

@login_required
def presentation_detail(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, is_active=True)
    
    context = {
        'presentation': presentation,
    }
    
    return render(request, 'agents/presentation_detail.html', context)

@login_required
def upload_presentation(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('presentation_list')
    else:
        form = PresentationForm()
    
    return render(request, 'agents/upload_presentation.html', {'form': form})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.agent = request.user
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'agents/create_order.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(agent=request.user).order_by('-created_at')
    return render(request, 'agents/order_list.html', {'orders': orders})

@login_required
def product_category(request, presentation_id, category_slug):
    presentation = get_object_or_404(Presentation, id=presentation_id, is_active=True)
    
    # Данные для категорий (можно вынести в базу данных)
    CATEGORIES_DATA = {
        'immobilization': {
            'title': 'Средства иммобилизации',
            'products': [
                {
                    'name': 'Матрас иммобилизационный вакуумный МИВ-2',
                    'description': 'Для иммобилизации позвоночного отдела, костей таза и нижних конечностей',
                    'models': 'МИВ-2 (взрослый), МИВ-3 (детский)',
                    'price': '15,000 руб.'
                },
                # ... другие товары
            ]
        },
        # ... другие категории
    }
    
    category_data = CATEGORIES_DATA.get(category_slug)
    if not category_data:
        return redirect('presentation_detail', presentation_id=presentation_id)
    
    context = {
        'presentation': presentation,
        'category_title': category_data['title'],
        'products': category_data['products'],
        'category_slug': category_slug
    }
    
    return render(request, 'agents/product_category.html', context)