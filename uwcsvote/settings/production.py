from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#l^2LjJpy^RtxLMv!Ky96V6&zFbWs2%4V^eEcOgp&!p@X!J59AsPDPuX11g@WL'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uwcs_vote',
        'USER': 'uwcs_vote',
        'PASSWORD': 'F3Vo4$y9HWwf0P4nJ*Gt@V',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/compsoc/sites/thebruce/lower-third/tempdebug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
"""
# Warwick SU API keys
UWCS_API_KEY = '71409874-3652-41f5-91bf-f9a4c0909a1e'

try:
    from .local import *
except ImportError:
    pass
