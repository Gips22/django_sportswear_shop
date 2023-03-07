from cart.views import _get_cart
from decimal import Decimal


def cart(request):
    cart = _get_cart(request)
    cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
    return {
        'cart_total_price': cart_total_price
    }

