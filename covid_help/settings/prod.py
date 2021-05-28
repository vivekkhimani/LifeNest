"""
Use the default and few overrides for PROD.
"""
from .default import *
import re

DEBUG = False

# production email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'lifenestio@gmail.com'
EMAIL_HOST_PASSWORD = 'otzbedarcpnbzjjr'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'admin@lifenest.io'

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

SERVER_EMAIL = 'errors@lifenest.io'

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
SECRET_KEY = "1878hs^z_nw)y6&2k4t0&**7c*li6k6j#ux_=uhz2t!)qj0=gp"

