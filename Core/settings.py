# Core/settings.py

# python
from datetime import timedelta
from pathlib  import Path

# 3rd Party
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environments variables from .env file
DEBUG      = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party apps
    'rest_framework',
    'rest_framework_simplejwt',

    # local apps
    'account_app',
    'social_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Core.urls'

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

WSGI_APPLICATION = 'Core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# No strict slashes in url
APPEND_SLASH = False

# Using custom user model i.e. Account for managing application accounts
AUTH_USER_MODEL = 'account_app.Account'

# ALLOW CUSTOM AUTHENTICATE SYSTEM FOR USER AUTHENTICAION INSTEAD DEFAULT
AUTHENTICATION_BACKENDS = [
    'Core.utilities.authentication.CustomModelBackend'
]


###########################
# REST FRAMEWORK SETTINGS #
###########################

REST_FRAMEWORK = {

    # Use JWT token for authentication
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # User atleast need to be authenticated to access any endpoint
    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated'
    ],

    # GLOBAL PAGINATION
    'DEFAULT_PAGINATION_CLASS' : 'Core.utilities.utils.CustomPageNumberPagination',
}


######################
# JWT TOKEN SETTINGS #
######################

# Custom Life Span Of Token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME'  : timedelta(days=60),      # for testing purposes only
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=120),
}
