from pathlib import Path
import os
from datetime import timedelta
from pathlib import Path

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'  # будет создана папка /media, в которой у нас будут храниться все файлы загруженные пользователем
MEDIA_ROOT = os.path.join(BASE_DIR,
                          'media/')  # путь в файловой системе по которому хранятся файлы. По умолчанию путь формируется из настроек BASE_DIR (корневая папка проекта) и MEDIA_ROOT

CART_ID = 'cart'

SECRET_KEY = 'django-insecure--vl3ox=h38opfu*4%l-%hyz1w*i-^c!gacx+8sp^d%kjkmiksq'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'captcha',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrderConfig',
    'crispy_forms',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'django_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.get_cart_total_price',
                'shop.context_processors.get_categories_from_shop',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'  # префикс который будет добавляться к url статических файлов
STATIC_ROOT = os.path.join(BASE_DIR,
                           'static')  # тут хранится путь к общей папке static, в кот будут собираться все статич файлы и использоваться на боевом веб сервере-хостинге
STATICFILES_DIRS = []  # список для нестандартных путей где искать ститичные файлы

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

''' используется только во время разработки и не подходит для продекшена,
записываетет все письма в файл на сервере.
EMAIL_FILE_PATH - указывать путь где будут храниться письма
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' - выводит сообщение
в консоль.
'''
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails/email-messages/'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
