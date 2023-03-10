from django.shortcuts import render, redirect
from django.views import View
from .forms import CartAddProductForm
from .cart_services import Cart


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        cart_items = cart.get_cart_items_with_products()
        cart_total_price = cart.get_cart_total_price(cart_items)
        context = {
            'cart': cart_items,
            'cart_total_price': cart_total_price
        }
        return render(request, 'cart/detail.html', context)


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add_to_cart(product_id, cd['quantity'], request.POST.get('overwrite_qty'))
            return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        cart.remove_from_cart(product_id)
        return redirect('cart:cart_detail')


