from __future__ import absolute_import, unicode_literals

from os import getenv

import dj_database_url

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["*"]

# production settings are specified as environment variables
SECRET_KEY = getenv("VOTE_SECRET_KEY")
SU_API_KEY = getenv("VOTE_SU_API_KEY")
db_url = getenv("VOTE_DB_URL")

SOCIALACCOUNT_PROVIDERS = {
    'uwcs': {
        'APP': {
            'client_id': getenv("VOTE_CLIENT_ID"),
            'secret': getenv("VOTE_CLIENT_SECRET"),
            'key': ''
        }
    }
}

assert SECRET_KEY
assert SU_API_KEY
assert db_url

DATABASES = {"default": dj_database_url.parse(db_url)}
