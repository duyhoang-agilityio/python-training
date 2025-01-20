from .base import *

DEBUG = False
ALLOWED_HOSTS = ["domain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}
