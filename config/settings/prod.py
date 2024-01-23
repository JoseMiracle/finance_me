from .dev import *
import dj_database_url
import sentry_sdk


DATABASES = {
	"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY':  os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET')
}

if DEBUG == False:
    MEDIA_URL = '/media/'  # or any prefix you choose
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

ALLOWED_HOSTS = ['loan-me.onrender.com', 'localhost']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", 
    "https://finance-me-blond.vercel.app"
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

# E-MAIL SETTINGS

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USE_TLS = bool(int(os.environ.get('EMAIL_USE_TLS',1)))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = 'admin@mail.com'



sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

