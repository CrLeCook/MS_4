from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from product.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request, 'cart/partials/menu_cart.html')

def cart(request):
    return render(request, 'cart/cart.html')

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)

    if action == 'increment':
        cart.add(product_id, 1, True)
    elif action == 'decrement':
        cart.add(product_id, -1, True)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

    quantity = cart.get_item(product_id)

    if quantity:
        quantity = quantity['quantity']
        total_price = (quantity * product.price) / 100

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image.url,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': total_price,
            'quantity': quantity,
        }
    else:
        item = None

    return JsonResponse({'item': item})

@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')
