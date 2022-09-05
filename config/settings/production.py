from . import *

SECRET_KEY = os.environ.get(['DJANGO-KEY'])
DEBUG = False
ALLOWED_HOSTS = ['']

# removing debug_toolbar of used apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'barcode.apps.BarcodeConfig',
    'collection.apps.CollectionConfig',
    'datafetcher.apps.DatafetcherConfig',
    'crispy_forms',
    'djmoney',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': os.environ.get['DB-NAME'],  # Replace using the db name on server
        'USER': os.environ.get['DB-USER'],  # Replace using the db user name on server
        'PASSWORD': os.environ.get['DB-PWD'],  # Replace using the db user pwd on server
        'HOST': '',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'GameZScan <root@vps-8351387e.vps.ovh.net>'