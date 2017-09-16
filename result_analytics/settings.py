"""
Django settings for result_analytics project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$o0j8rj*2wv(5_ia8gxz3w^2+q0uj+vqp@2um)wdfgt7#2*zxm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

FILTER_PROFANE_WORDS = True
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analyzer',
    'assignments',
    'courses',
    'form_utils',
    'institutions',
    'students',
    'states',
    'staff',
    'sorl.thumbnail',
    'results',
    'projects',
    'river',
    'core',
    'forum',
    'friendship',
    'collaborations',
    'rest_framework',
    'django_social_share',
    'notifications'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'result_analytics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'staff.context_processors.home_context',
                'staff.context_processors.performances',
                'staff.context_processors.performance_recommendation',
                'staff.context_processors.course_recommendation',
            ],
        },
    },
]

WSGI_APPLICATION = 'result_analytics.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'acadlytics',
#         'USER': 'postgres',
#         'PASSWORD': 'treble89',
#     }
# }
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'acadlytics.sqlite3',
        'USER': '',
        'PASSWORD': '',
    }
}
LEVEL_CHOICES = (
    (100, 100),
    (200, 200),
    (300, 300),
    (400, 400),
    (500, 500),
    (600, 600),
)

(FIRST, SECOND) = range(1,3)
SEMESTER_CHOICES = (
    (FIRST, 'First Semester'),
    (SECOND, 'Second Semester'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

LOGIN_URL = '/login/' # Expensive to use a login view
LOGOUT_URL = 'result_logout'
LOGIN_REDIRECT_URL = 'dashboard'
