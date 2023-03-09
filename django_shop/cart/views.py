from django.shortcuts import render, redirect
from django.views import View
from .forms import CartAddProductForm
from .services import get_cart, get_cart_items_with_products, get_cart_total_price, add_to_cart, remove_from_cart, \
    clear_cart


class CartDetailView(View):
    def get(self, request):
        cart = get_cart(request)
        cart_items = get_cart_items_with_products(cart)
        cart_total_price = get_cart_total_price(cart_items)
        context = {
            'cart': cart_items,
            'cart_total_price': cart_total_price
        }
        return render(request, 'cart/detail.html', context)


class CartAddView(View):
    def post(self, request, product_id):
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            add_to_cart(request, product_id, cd['quantity'], request.POST.get('overwrite_qty'))
            return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        remove_from_cart(request, product_id)
        return redirect('cart:cart_detail')


class CartClearView(View):
    def post(self, request):
        clear_cart(request)
        return redirect('cart:cart_detail')
