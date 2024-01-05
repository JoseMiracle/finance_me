from .dev import *
import dj_database_url

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

ALLOWED_HOSTS = ['*']
