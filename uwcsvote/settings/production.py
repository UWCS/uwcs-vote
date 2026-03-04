from __future__ import absolute_import, unicode_literals

from os import getenv

import dj_database_url

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["*"]

# production settings are specified as environment variables
SECRET_KEY = getenv("VOTE_SECRET_KEY")
UWCS_API_KEY = getenv("VOTE_SU_API_KEY")
db_url = getenv("VOTE_DB_URL")

assert SECRET_KEY
assert UWCS_API_KEY
assert db_url

DATABASES = {"default": dj_database_url.parse(db_url)}
