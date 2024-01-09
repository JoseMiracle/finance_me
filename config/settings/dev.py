from .base import *
from datetime import timedelta

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(int(os.environ.get('DEBUG',1)))

LOCAL_APPS = [
    'finance.accounts',
    'finance.loans'
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "cloudinary_storage",
    "cloudinary",
    "corsheaders"
]



INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS
AUTH_USER_MODEL = 'accounts.User'



# E-MAIL SETTINGS

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USE_TLS = bool(int(os.environ.get('EMAIL_USE_TLS',1)))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = 'admin@mail.com'




REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


PASSWORD_RESET_TIMEOUT = 1