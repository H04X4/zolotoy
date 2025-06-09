from django.shortcuts import render, redirect
from .models import Product, UserProfile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.db.models import Max

@login_required
def order_list(request):
    sort_by = request.GET.get('sort', 'article')
    if sort_by not in ['article', 'stock', 'cost_price', 'order_quantity']:
        sort_by = 'article'

    if request.user.is_superuser:
        products = Product.objects.all()  
    else:
        try:
            user_unique_number = request.user.profile.unique_number
            products = Product.objects.filter(unique_number=user_unique_number)
        except UserProfile.DoesNotExist:
            products = Product.objects.none()  
    products = products.order_by(sort_by)
    print(f"DEBUG: Found {products.count()} products")
    total_sum = sum(p.order_quantity * p.cost_price for p in products)
    return render(request, 'orders/order_list.html', {
        'products': products,
        'total_sum': total_sum,
        'sort_by': sort_by
    })

@require_POST
@login_required
def update_order(request):
    product_id = request.POST.get('product_id')
    order_quantity = request.POST.get('order_quantity')
    comment = request.POST.get('comment')
    try:
        product = Product.objects.get(id=product_id)
        # Проверка, что пользователь имеет доступ к продукту
        if not request.user.is_superuser:
            user_unique_number = request.user.profile.unique_number
            if product.unique_number != user_unique_number:
                return JsonResponse({'error': 'Нет доступа к этому продукту'}, status=403)
        product.order_quantity = int(order_quantity)
        product.comment = comment
        product.save()
        line_total = product.order_quantity * product.cost_price
        if request.user.is_superuser:
            total_sum = sum(p.order_quantity * p.cost_price for p in Product.objects.all())
        else:
            total_sum = sum(p.order_quantity * p.cost_price for p in Product.objects.filter(unique_number=user_unique_number))
        return JsonResponse({'line_total': float(line_total), 'total_sum': float(total_sum)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            max_number = UserProfile.objects.aggregate(Max('unique_number'))['unique_number__max']
            new_number = (max_number or 999) + 1
            UserProfile.objects.create(user=user, unique_number=new_number)
            login(request, user)
            messages.success(request, f"Регистрация успешна! Ваш уникальный номер: {new_number}")
            return redirect('order_list')
        else:
            messages.error(request, "Ошибка регистрации. Проверьте введённые данные.")
    else:
        form = RegisterForm()
    return render(request, 'orders/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вход выполнен успешно!")
            return redirect('order_list')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()
    return render(request, 'orders/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect('login')