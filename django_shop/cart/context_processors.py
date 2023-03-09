from decimal import Decimal

from cart.services import get_cart


def get_cart_total_price(request):
    cart = get_cart(request)
    cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
    return {
        'cart_total_price': cart_total_price
    }
