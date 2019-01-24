import os

# FIXME: Statement for enabling the development environment
DEBUG = True
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Threads for application.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Authorization stuff for jwt
JWT_SECRET_KEY = 'thisissecretfortesting123'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_PATH = '/'   #This way this is usable in /api and /webui
JWT_REFRESH_COOKIE_PATH = '/api/re-login'  #this shouldn't be needed in webui
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_SECURE = True   # Set this false for testing if true doesn't work
