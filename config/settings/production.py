from . import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://bef70534761d4110adf2f5e8354dc631@o1293076.ingest.sentry.io/6727217",
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.5,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


SECRET_KEY = os.environ["DJANGO_KEY"]
DEBUG = False
ALLOWED_HOSTS = [
    "51.38.234.122",
    "gamezscan.gitgudat.com",
    "www.gamezscan.gitgudat.com",
]

# removing debug_toolbar of used apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gamezscan.accounts.apps.AccountsConfig",
    "gamezscan.barcode.apps.BarcodeConfig",
    "gamezscan.collection.apps.CollectionConfig",
    "gamezscan.datafetcher.apps.DatafetcherConfig",
    "gamezscan.home.apps.HomeConfig",
    "crispy_forms",
    "djmoney",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "gamezscan",  # Replace using the db name on server
        "USER": os.environ["DB_GZS_USER"],  # Replace using the db user name on server
        "PASSWORD": os.environ["DB_GZS_PWD"],  # Replace using the db user pwd on server
        "HOST": "localhost",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "GameZScan <root@vps-8351387e.vps.ovh.net>"

# Setting CSRF for SSL
CSRF_TRUSTED_ORIGINS = ["https://gamezscan.gitgudat.com"]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_DOMAIN = ".gitgudat.com"

# Help for resolving tests errors on POST test on some views
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
