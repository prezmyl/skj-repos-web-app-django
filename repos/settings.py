import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
#SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-OS-qVRwk4sBq4sf2--DZ23UurC7ef4_K5GaGWW__OSFSYQ3QBPRxCbw0NXibmDldqXw'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'repos_app',            # my app
]
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# to tell django where muj project-level urls.py zije
ROOT_URLCONF = 'repos.urls'

# WSGI/ASGI applikacni entry points
WSGI_APPLICATION = 'repos.wsgi.application'
ASGI_APPLICATION = 'repos.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Use BigAutoField (64-bit) as the default primary key type instead of AutoField (32-bit)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
