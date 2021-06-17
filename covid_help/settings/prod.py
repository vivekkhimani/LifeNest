"""
Use the default and few overrides for PROD.
"""
from .default import *
import re
import json
from django.core.exceptions import ImproperlyConfigured

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secrets(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


DEBUG = False

# production email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '35.222.236.158'
EMAIL_HOST_USER = get_secrets('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secrets('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'noreply@lifenest.io'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT=20
# EMAIL_SSL_CERTFILE = os.path.join(BASE_DIR, 'fullchain.pem')
# EMAIL_SSL_KEYFILE = os.path.join(BASE_DIR, 'privkey.pem')

# admins for alerting
ADMINS = [
    ('Vivek', 'vivek@lifenest.io'),
    ('John', 'john@lifenest.io'),
    ('Admin', 'admin@lifenest.io'),
    ('Vivek GMail', 'vivekkhimani07@gmail.com'),
]

# managers for broken link alerting
MANAGERS = [
    ('Vivek', 'vivek@lifenest.io'),
    ('John', 'john@lifenest.io'),
    ('Admin', 'admin@lifenest.io'),
    ('Vivek GMail', 'vivekkhimani07@gmail.com'),
]

# ignorable 404 urls
IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

SERVER_EMAIL = 'noreply@lifenest.io'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# secret key
SECRET_KEY = get_secrets("SECRET_KEY")

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '35.222.236.158',
        'NAME': 'dbaeo71xp0tn73',
        'USER': get_secrets("DB_USER"),
        'PASSWORD': get_secrets("DB_PASSWORD"),
        'PORT': '5432',
    }
}
CONN_MAX_AGE = 7200

# static files
STATIC_ROOT = '/var/www/LifeNest/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/LifeNest/media/'
