from django.shortcuts import render, redirect
from .models import Product, UserProfile, CartItem
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
    
    search_query = request.GET.get('search', '').strip()
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    
    products = Product.objects.exclude(cartitem__isnull=False)
    
    if search_query:
        products = products.filter(article__icontains=search_query)
    if price_min:
        try:
            products = products.filter(cost_price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            products = products.filter(cost_price__lte=float(price_max))
        except ValueError:
            pass
    
    products = products.order_by(sort_by)
    total_sum = sum(p.order_quantity * p.cost_price for p in products)
    
    return render(request, 'orders/order_list.html', {
        'products': products,
        'total_sum': total_sum,
        'sort_by': sort_by,
        'search_query': search_query,
        'price_min': price_min,
        'price_max': price_max,
    })

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_sum = sum(item.quantity * item.product.cost_price for item in cart_items)
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
    })

@require_POST
@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', 1)
    comment = request.POST.get('comment', '')
    try:
        product = Product.objects.get(id=product_id)
        quantity = int(quantity)
        if quantity < 1:
            return JsonResponse({'error': 'Количество должно быть больше 0'}, status=400)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity, 'comment': comment}
        )
        if not created:
            cart_item.quantity = quantity
            cart_item.comment = comment
            cart_item.save()
        
        return JsonResponse({'success': 'Товар добавлен в корзину', 'cart_item_id': cart_item.id})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
@login_required
def remove_from_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        total_sum = sum(item.quantity * item.product.cost_price for item in CartItem.objects.filter(user=request.user))
        return JsonResponse({'success': 'Товар удалён из корзины', 'total_sum': float(total_sum)})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден в корзине'}, status=404)
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