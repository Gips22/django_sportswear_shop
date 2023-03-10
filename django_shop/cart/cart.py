from decimal import Decimal
from django.conf import settings
from shop.models import Product


# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_ID)
#         if not cart:
#             cart = self.session[settings.CART_ID] = {}
#         self.cart = cart
#
#     def get_cart_total_price(self, cart_items: List[Dict[str, Union[str, int, Decimal]]]) -> Decimal:
#         """
#         Вычисляет общую стоимость всех товаров в корзине.
#         """
#         return sum(item['total_price'] for item in cart_items)
#
#     def get_cart_items_with_products(self, cart):
#         """
#         Возвращает список словарей, содержащий товары в корзине и их соответствующие объекты Product.
#         """
#         product_ids = cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#         cart_items = []
#
#         for product in products:
#             cart_item = cart[str(product.id)]
#             cart_item['product'] = product
#             cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
#             cart_item['update_quantity_form'] = CartAddProductForm(initial={'quantity': cart_item['quantity']})
#             cart_items.append(cart_item)
#
#         return cart_items
#
#     def add_to_cart(self, request, product_id: int, quantity: int, overwrite_qty: bool = False) -> None:
#         """
#         Добавляет товар в корзину или обновляет его количество, если товар уже в корзине.
#         """
#         cart = get_cart(request)
#         product = get_object_or_404(Product, id=product_id)
#         product_id = str(product_id)
#
#         if product_id not in cart:
#             cart[product_id] = {'quantity': 0, 'price': str(product.price)}
#
#         if overwrite_qty:
#             cart[product_id]['quantity'] = quantity
#         else:
#             cart[product_id]['quantity'] += quantity
#
#         request.session[settings.CART_ID] = cart
#         request.session.modified = True
#
#     def remove_from_cart(self, request, product_id: int) -> None:
#         """
#         Удаляет товар из корзины.
#         """
#         cart = get_cart(request)
#         product_id = str(product_id)
#
#         if product_id in cart:
#             del cart[product_id]
#             request.session[settings.CART_ID] = cart
#             request.session.modified = True
#
#     def clear_cart(self, request) -> None:
#         """
#         Очищает корзину.
#         """
#         request.session[settings.CART_ID] = {}
#         request.session.modified = True
#
#     def get_cart(self, request) -> Dict[str, Dict[str, Union[str, int]]]:
#         """
#         Возвращает корзину из сессии или пустой словарь, если ее нет.
#         """
#         return request.session.get(settings.CART_ID, {})

    # class Cart(object):
    #     def __init__(self, request):
    #         self.session = request.session
    #         cart = self.session.get(settings.CART_ID)
    #         if not cart:
    #             cart = self.session[settings.CART_ID] = {}
    #         self.cart = cart

    # def add(self, product, quantity=1, update_quantity=False):
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
    #     if update_quantity:
    #         self.cart[product_id]['quantity'] = quantity
    #     else:
    #         self.cart[product_id]['quantity'] += quantity
    #     self.save()

    # def save(self):
    #     self.session[settings.CART_ID] = self.cart
    #     self.session.modified = True

    # def remove(self, product):
    #     product_id = str(product.id)
    #     if product_id in self.cart:
    #         del self.cart[product_id]
    #         self.save()

    # def __iter__(self):
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     for product in products:
    #         self.cart[str(product.id)]['product'] = product
    #
    #     for item in self.cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item
    #
    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())

    # def get_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # def clear(self):
    #     del self.session[settings.CART_ID]
    #     self.session.modified = True
