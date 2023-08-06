# flake8: noqa
from .dev import *

print(" -> settings 'local'")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "backmatch",
#         "USER": "root",
#         "PASSWORD": "test",
#         "HOST": "127.0.0.1",
#         "PORT": "3307",
#         "ATOMIC_REQUESTS": True,
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "backmatch",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "dfm9f6uptt9sen",
#         "USER": "icjtiyavdjqknt",
#         "PASSWORD": "ed4f4c87b0ca2f5b67dc3b98cd584b95b5fd8e9fc36f8abfee9a4773c0c86d06",
#         "HOST": "ec2-54-166-107-5.compute-1.amazonaws.com",
#         "PORT": "5432",
#         "ATOMIC_REQUESTS": True,
#     }
# }

BASE_URL = "http://localhost:8000"

# pg_restore -d dfm9f6uptt9sen ./dump_backmatch.sql -c -U icjtiyavdjqknt -h ec2-54-166-107-5.compute-1.amazonaws.com
