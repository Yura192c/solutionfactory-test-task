from .base import *

print('production')
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = []

# API settings
API_SENDING_URL = 'https://probe.fbrq.cloud/v1/send/'
API_JWT_TOKEN = os.environ['API_JWT_TOKEN']

# Email settins
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# Адреса электронной почты
STATISTICS_EMAIL_RECIPIENTS = os.environ.get('STATISTICS_EMAIL_RECIPIENTS', '').split(
    ',')  # Укажите список получателей статистики
