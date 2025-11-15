import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='insecure-secret')

DEBUG = False

ALLOWED_HOSTS = [
    "soundlab-store.up.railway.app",
    "localhost",
    "127.0.0.1",
]

# ------------------------------------------------------------------
# APPS
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "corsheaders",
    "rest_framework",

    'soundlab_store',
    'usuario',
    'soundlab_api',
    'orders',
]

# ------------------------------------------------------------------
# REST FRAMEWORK / JWT
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ------------------------------------------------------------------
# MIDDLEWARE (CORS SIEMPRE PRIMERO)
# ------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 👈 OBLIGATORIO PRIMERO
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'soundlab_backend.urls'

# ------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'soundlab_backend.wsgi.application'

# ------------------------------------------------------------------
# DATABASE (RAILWAY)
# ------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD': 'QsMudtIzMdpTWMoEFlLbylvgmIUGmJmG',
        'HOST': 'shinkansen.proxy.rlwy.net',
        'PORT': '19227',
    }
}

MYSQL_URL = config('MYSQL_URL', default=None)
if MYSQL_URL:
    DATABASES['default'] = dj_database_url.parse(MYSQL_URL, conn_max_age=600)

# ------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# TIME / LANGUAGE
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATIC & MEDIA
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usuario.Usuario'

# ------------------------------------------------------------------
# CORS CONFIG (Netlify → Railway)
# ------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "https://soundlabstore.netlify.app",
    "http://localhost:3000",  # 👈 FRONTEND PRODUCCIÓN
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CSRF_TRUSTED_ORIGINS = [
    "https://soundlabstore.netlify.app",
    "https://soundlab-store.up.railway.app",
]



