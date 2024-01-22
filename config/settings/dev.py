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


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


PASSWORD_RESET_TIMEOUT = 1800