from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l33th4x0rs'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uwcs_vote',
        'USER': 'uwcs_vote',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Warwick SU API keys
UWCS_API_KEY = 'UWCS_API_KEY'

try:
    from .local import *
except ImportError:
    pass
