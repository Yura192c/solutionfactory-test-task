from .base import *  # подгружаем настройки по умолчанию

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ff=au=!_1(zv8w5ch(7gj@+#svlmxhd4^^c@8#y8u&c5ww28^#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

API_SENDING_URL = 'https://probe.fbrq.cloud/v1/send/'
API_JWT_TOKEN = os.environ['API_JWT_TOKEN']