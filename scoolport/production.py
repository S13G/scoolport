from .settings import *

DEBUG = True

ALLOWED_HOSTS = ["scoolport.up.railway.app"]

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

INSTALLED_APPS.remove("debug_toolbar")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CSP_DEFAULT_SRC = ("self",)

CSP_STYLE_SRC = ("self",)

CSP_SCRIPT_SRC = ("self",)

CSP_IMG_SRC = ("self",)

CSP_FONT_SRC = ("self",)

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
