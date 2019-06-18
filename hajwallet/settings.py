"""
Django settings for hajwallet project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_vobe#t7ltpld5o+l%@+fy#m7#22@zf9vz)l5c0b!4a$3!(8l#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'accounts',
    'pilgrims',
    'vendors',
    'payments',
    'django_adminlte',
    'django_adminlte_theme',
    'django.contrib.admin',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'statistics_app'
]
SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hajwallettest'
EMAIL_HOST_PASSWORD = 'haj15987wallet'
EMAIL_PORT = 587

# EMAIL_HOST = 'smtp.mailtrap.io'
# EMAIL_HOST_USER = 'b709a983278255'
# EMAIL_HOST_PASSWORD = 'a6993de88f2a66'
# EMAIL_PORT = '2525'
# DEFAULT_FROM_EMAIL = 'My Site <noreply@mysite.com>'
# EMAIL_USE_TLS = False

REST_AUTH_SERIALIZERS = {
    # 'USER_DETAILS_SERIALIZER': 'vendors.api.serializers.customUserDetailsSerializer',
     'TOKEN_SERIALIZER': 'vendors.api.serializers.TokenSerializer' # import path to CustomTokenSerializer defined above.
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'pilgrims.api.serializers.custom_exception_handler',
                         'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),

  'EXCEPTION_HANDLER': 'pilgrims.api.serializers.custom_exception_handler',
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hajwallet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hajwallet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',

        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'env.cnf'),
        },
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.mysql',
#         'NAME': 'hajwallet',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '3306'
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.Account'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'
STATIC_URL = os.path.join(BASE_DIR, 'statics/')
STATICFILES_DIRS = [
    STATIC_URL,
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STRIPE_PUBLISHABLE_KEY= 'pk_test_fMnNg167rZQxzKjNJECU8G3a006lIiWlZV'
STRIPE_SECRET_KEY= 'sk_test_dK0QWZrL5rdmp8XuDHaT1uxk00Lx8CsVTw'
STRIPE_CONNECT_CLIENT_ID= 'ca_FAysl1qQ2HnPvhb3KPMsLZUYBYG2pi4C'
