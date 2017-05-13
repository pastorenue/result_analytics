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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(PROJECT_DIR,'..'))

FIXTURE_DIRS = (
    os.path.join(PROJECT_BASE, 'fixtures'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$o0j8rj*2wv(5_ia8gxz3w^2+q0uj+vqp@2um)wdfgt7#2*zxm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analyzer',
    'courses',
    'form_utils',
    'institutions',
    'students',
    'states',
    'staff',
    'sorl.thumbnail',
    'results',
    'notification',
    'crispy_forms',
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
        'DIRS': [os.path.join(PROJECT_BASE, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'staff.context_processors.home_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'result_analytics.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_in_pro', 'static_root')
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static_in_pro', 'my_static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static_in_pro', 'uploads')
MEDIA_URL ='/media/'

AUTH_PROFILE_MODULE = 'users.UserProfile'

LOGIN_URL = 'result_login'
LOGOUT_URL = 'result_logout'
LOGIN_REDIRECT_URL = 'staff_index'
