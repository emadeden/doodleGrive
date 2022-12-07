"""
Django settings for geeks_site project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%p0(all9wjbr6y8+#u5%f#)ei#9*=^o95*1s9p7%8q2x8zawa_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'myApp',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # mohammed AUTHENTICATION_REQUIRED_MIDDLEWARE
    'geeks_site.middleware.LoginRequiredMiddleware.LoginRequiredMiddleware',
    'geeks_site.middleware.AuthoritiesMiddleware.checkAuthorization'
]

ROOT_URLCONF = 'geeks_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'geeks_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# emad added    
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
AUTH_USER_MODEL = 'accounts.CustomUser'
# mohammed added
LOGIN_URL= "/login/"
AUTHENTICATION_REQUIRED_URLS = (
    r'^.*./upload.*',
    r'^.*./update.*',
    r'^.*./delete.*',
    r'^.*./createGroup.*',
    r'^.*./getGroupDetail.*',
    r'^.*./showMyGroup.*',
    r'^.*./editContent.*',
    r'^.*./editGroup.*',
    r'^.*./blockFile.*',
    r'^.*./unblockFile.*',
    r'^.*./home.*',
    r'^.*./getFileDetail.*',
    r'^.*./displayContent.*',
)
FILE_GROUP_MEMBERSHIP_REQUIRED_URLS = (
    r'^.*./update.*',
    r'^.*.upload.*',
    r'^.*./editContent.*',
    r'^.*./getFileDetail.*',
    r'^.*./displayContent.*',
)
GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS = (
    r'^.*./getGroupDetail.*',
)
FILE_OWNER_REQUIRED_URLS =(
    r'^.*./delete.*',
)
GROUP_OWNER_REQUIRED_URLS = (
    r'^.*./deleteGroup.*',
    r'^.*./editGroup.*',
)
LOG_LEVEL = 3
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myApp/templates/static'),
]