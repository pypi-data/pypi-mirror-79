from .base import *

print("-> settings 'dev'", end="")

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "backmatch",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{asctime}]:{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


INSTALLED_APPS.append("django_extensions")

BASE_URL = "http://localhost:8000"
ALLOWED_HOSTS = ["localhost"]
CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
FORMATCH_BASE_URL = "http://localhost:3000/"
FORMATCH_PWD = "testtest"

# config MailDev ou Mailcatcher
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

# ANYMAIL = {
#     "SENDINBLUE_API_KEY": "xkeysib-bb5ed19bbf72eead9246741d0803eb10d7aa704a"
#                           "5d4305636444302f0a4ea7f6-WHsApGYLazXvQUR4",
# }
# EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

# config anymail
ANYMAIL = {
    "SENDINBLUE_API_KEY": "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",  # noqa
}
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
