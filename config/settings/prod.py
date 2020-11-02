"""
Production settings:
- configure HSTS
- use WhiteNoise for serving static files
"""
from .base import *  # noqa

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

INSTALLED_APPS += [
    'gunicorn',
]

# This ensures that Django will be able to detect a secure connection properly
# on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security

# TODO: set this to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# WhiteNoise

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHITENOISE_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE

# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = env.int('MAILGUN_SMTP_PORT')
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 3