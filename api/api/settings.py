import os
import sys
import dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load env variables from file
dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
else:
    print('.env file not found')
    sys.exit(1)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    print('TELEGRAM_TOKEN not found in env')
    sys.exit(1)

JWT_KEY = os.getenv("JWT_KEY")
if JWT_KEY is None:
    print('JWT_KEY not found in env')
    sys.exit(1)

WSB_STOREID = os.getenv("WSB_STOREID")
if WSB_STOREID is None:
    print('WSB_STOREID not found in env')
    sys.exit(1)

WEBPAY_SECRET_KEY = os.getenv("WEBPAY_SECRET_KEY")
if WEBPAY_SECRET_KEY is None:
    print('WEBPAY_SECRET_KEY not found in env')
    sys.exit(1)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if SECRET_KEY is None:
    print('DJANGO_SECRET_KEY not found in env')
    sys.exit(1)

FIELD_ENCRYPTION_KEY = os.getenv("FIELD_ENCRYPTION_KEY").encode()
if FIELD_ENCRYPTION_KEY is None:
    print('FIELD_ENCRYPTION_KEY not found in env')
    sys.exit(1)

MYSQL_NAME = os.getenv("MYSQL_NAME")
if MYSQL_NAME is None:
    print('MYSQL_NAME not found in env')
    sys.exit(1)

MYSQL_USER = os.getenv("MYSQL_USER")
if MYSQL_USER is None:
    print('MYSQL_USER not found in env')
    sys.exit(1)

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
if MYSQL_PASSWORD is None:
    print('MYSQL_PASSWORD not found in env')
    sys.exit(1)

EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
if EXCHANGE_RATE_API_KEY is None:
    print('EXCHANGE_RATE_API_KEY not found in env')
    sys.exit(1)

if os.environ.get('DJANGO_DEBUG') in ('True', 'true', '1', True):
    DEBUG = True
else:
    DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'loans.apps.LoansConfig',
    # 'ezaim.apps.EzaimConfig',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'encrypted_model_fields',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_NAME,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
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

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = []
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_REPLACE_HTTPS_REFERER = True
