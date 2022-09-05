from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', ShopHome.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', ShopCategory.as_view(), name='product_list_by_category'),
    path('category/<slug:category_slug>/<slug:slug>', product_detail, name='product_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    # path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

]
