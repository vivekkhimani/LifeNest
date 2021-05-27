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
