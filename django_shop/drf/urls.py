from django.contrib import admin
from django.urls import path, include, re_path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers
from shop.views import *


from drf.views import ProductViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('v1/drf-auth/', include('rest_framework.urls')),  # Аутентификация по session id (session-based authentication)
    path('v1/', include(router.urls)),

    # path('v1/product/', ProductAPIList.as_view()),
    # path('v1/product/<int:pk>/', ProductAPIUpdate.as_view()),
    # path('v1/productdelete/<int:pk>/', ProductAPIDestroy.as_view()),

    # path('api/v1/auth/', include('djoser.urls')),  # djoser
    # re_path(r'^auth/', include('djoser.urls.authtoken')),  # djoser. Строчка отвечает за авторизацию по токенам
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]