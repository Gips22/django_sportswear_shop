from decimal import Decimal

from cart.services import Cart


def get_cart_total_price(request):
    cart = Cart(request)
    cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.get_cart(request).values())
    return {
        'cart_total_price': cart_total_price
    }
