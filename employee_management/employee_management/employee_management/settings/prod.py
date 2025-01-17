import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["your-production-domain.com"]

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


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
