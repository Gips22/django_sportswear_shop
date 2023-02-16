from django.urls import path
from .views import *


# используем namespacing для удобства. Теперь, к примеру, the product_list URL будет доступен, как shop:product_list в других частях Django проекта.
app_name = 'shop'

urlpatterns = [
    path('', ShopHome.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', ShopCategory.as_view(), name='product_list_by_category'),
    path('category/<slug:category_slug>/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('about/', about, name='about'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

]
