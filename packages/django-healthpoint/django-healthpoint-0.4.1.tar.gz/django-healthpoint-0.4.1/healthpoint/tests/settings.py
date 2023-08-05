DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',

    'healthpoint',
    'healthpoint.tests'
]

ROOT_URLCONF = 'healthpoint.tests.urls'

USE_TZ = True

SECRET_KEY = 'psst'
