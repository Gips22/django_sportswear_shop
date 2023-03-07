from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.conf import settings
from shop.models import Product
from .forms import CartAddProductForm


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




###############
# class CartDetailView(View):
#     def get(self, request):
#         cart = _get_cart(request)
#         product_ids = cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#         temp_cart = cart.copy()
#
#         for product in products:
#             cart_item = temp_cart[str(product.id)]
#             cart_item['product'] = product
#             cart_item['total_price'] = (Decimal(cart_item['price']) * cart_item['quantity'])
#             cart_item['update_quantity_form'] = CartAddProductForm(initial={
#                 'quantity': cart_item['quantity']})
#
#         cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in temp_cart.values())
#         context = {
#             'cart': temp_cart.values(),
#             'cart_total_price': cart_total_price
#         }
#         return render(request, 'cart/detail.html', context)
#
#
# class CartAddView(View):
#     def post(self, request, product_id):
#         cart = _get_cart(request)
#         product = get_object_or_404(Product, id=product_id)
#         product_id = str(product_id)
#         form = CartAddProductForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#
#             if product_id not in cart:
#                 cart[product_id] = {
#                     'quantity': 0,
#                     'price': str(product.price)
#                 }
#             if request.POST.get('overwrite_qty'):
#                 cart[product_id]['quantity'] = cd['quantity']
#             else:
#                 cart[product_id]['quantity'] += cd['quantity']
#
#             request.session.modified = True
#         return redirect('cart:cart_detail')
#
#
# class CartRemoveView(View):
#     def post(self, request, product_id):
#         cart = self._get_cart(request)
#         product_id = str(product_id)
#         if product_id in cart:
#             del cart[product_id]
#             request.session.modified = True
#         return redirect('cart:cart_detail')
#
#     def _get_cart(self, request):
#         cart = request.session.get(settings.CART_ID)  # получает значение идентификатора корзины из сессии
#         if not cart:
#             cart = request.session[settings.CART_ID] = {}
#         return cart
#
#
# class CartClearView(View):
#     def post(self, request):
#         del request.session[settings.CART_ID]
#         return redirect('cart:cart_detail')
#
#
# def _get_cart(request):
#     cart = request.session.get(settings.CART_ID)  # получает значение идентификатора корзины из сессии
#     if not cart:
#         cart = request.session[settings.CART_ID] = {}
#     return cart

#########

# def cart_detail(request):
#     cart = _get_cart(request)
#     product_ids = cart.keys()
#     products = Product.objects.filter(id__in=product_ids)
#     temp_cart = cart.copy()
#
#     for product in products:
#         cart_item = temp_cart[str(product.id)]
#         cart_item['product'] = product
#         cart_item['total_price'] = (Decimal(cart_item['price']) * cart_item['quantity'])
#         cart_item['update_quantity_form'] = CartAddProductForm(initial={
#             'quantity': cart_item['quantity']})
#
#     cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in temp_cart.values())
#     return render(
#         request,
#         'cart/detail.html',
#         {
#             'cart': temp_cart.values(),
#             'cart_total_price': cart_total_price
#         })
#
#
# def cart_add(request, product_id):
#     cart = _get_cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     product_id = str(product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#
#         if product_id not in cart:
#             cart[product_id] = {
#                 'quantity': 0,
#                 'price': str(product.price)
#             }
#         if request.POST.get('overwrite_qty'):
#             cart[product_id]['quantity'] = cd['quantity']
#         else:
#             cart[product_id]['quantity'] += cd['quantity']
#
#         request.session.modified = True
#     return redirect('cart:cart_detail')
#
#
# def cart_remove(request, product_id):
#     cart = _get_cart(request)
#     product_id = str(product_id)
#     if product_id in cart:
#         del cart[product_id]
#         request.session.modified = True
#         return redirect('cart:cart_detail')
#
#
# def cart_clear(request):
#     del request.session[settings.CART_ID]
#
#
# def _get_cart(request):
#     cart = request.session.get(settings.CART_ID)  # получает значение идентификатора корзины из сессии
#     if not cart:
#         cart = request.session[settings.CART_ID] = {}
#     return cart
