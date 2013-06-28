DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'sorl.thumbnail',
    'newsletter',
)

ROOT_URLCONF = 'test_urls'

STATIC_URL = '/static/'

SITE_ID = 1

TEMPLATE_DIRS = ('test_templates', )

# Enable time-zone support for Django 1.4 (ignored in older versions)
USE_TZ = True

# Required for django-webtest to work
STATIC_URL = '/static/'
