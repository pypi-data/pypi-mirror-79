from .dev import *

print("-> settings 'docker'")

DEBUG = int(os.environ.get("DEBUG", default=0))

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}


LOGGING = None
