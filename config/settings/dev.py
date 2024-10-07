from decouple import config

print("dev")

DEBUG = True

SECRET_KEY = "ABC"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "django_posts",
        "USER": "postgres",
        "PASSWORD": "2077",
        "HOST": "localhost",
        "PORT": "5432",

    }
}

STATIC_URL = 'static/'

SITE_URL = 'http://localhost:8000/'


CACHE_LOCATION = config('CACHE_LOCATION', default='redis://localhost:6379/0')
if CACHE_LOCATION is None:
    raise ValueError('CACHE_LOCATION not provided.')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mohamadreza619ps4@gmail.com'
EMAIL_HOST_PASSWORD = "ibxq ysdw gqmp tebv"
DEFAULT_FORM_USER = "mohamadreza619ps4@gmail.com"

CELERY_BROKER_URL = CACHE_LOCATION
CELERY_RESULT_BACKEND = CACHE_LOCATION