import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["domain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "prod_db",
        "USER": "prod_user",
        "PASSWORD": "secure_password",
        "HOST": "prod-db-host",
        "PORT": "5432",
    }
}
