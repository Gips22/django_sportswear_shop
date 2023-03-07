from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls')),
    path('captcha/', include('captcha.urls')),
    path('', include('shop.urls', namespace='shop')),  # копируем все urls из приложения shop

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    # в режиме отладки добавляем к нашим маршрутам еще один маршрут для статических данных, графических файлов
    # вторым аргументом тут идет папка, где будут идти файлы. На реальных серверах это не нужно, так как уже все настроено
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
