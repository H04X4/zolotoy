from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def order_list(request):
    sort_by = request.GET.get('sort', 'article')
    if sort_by not in ['article', 'stock', 'cost_price', 'order_quantity']:
        sort_by = 'article'
    products = Product.objects.all().order_by(sort_by)
    print(f"DEBUG: Found {products.count()} products")  
    total_sum = sum(p.order_quantity * p.cost_price for p in products)
    return render(request, 'orders/order_list.html', {
        'products': products,
        'total_sum': total_sum,
        'sort_by': sort_by
    })

@require_POST
def update_order(request):
    product_id = request.POST.get('product_id')
    order_quantity = request.POST.get('order_quantity')
    comment = request.POST.get('comment')
    try:
        product = Product.objects.get(id=product_id)
        product.order_quantity = int(order_quantity)
        product.comment = comment
        product.save()
        line_total = product.order_quantity * product.cost_price
        total_sum = sum(p.order_quantity * p.cost_price for p in Product.objects.all())
        return JsonResponse({'line_total': float(line_total), 'total_sum': float(total_sum)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)