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

