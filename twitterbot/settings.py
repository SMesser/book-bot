from dotenv import load_dotenv
from os import environ
from os.path import abspath, dirname, join
from random import choice
from string import printable

BASE_DIR = dirname(dirname(abspath(__file__)))
load_dotenv(abspath(join(BASE_DIR, '.env')))
DEBUG = bool(int(environ.get('DEBUG', '0')))
if DEBUG:
	SECRET_KEY = environ.get('SECRET_KEY')
else:
	SECRET_KEY = ''.join(choice(printable) for _ in range(30))

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
	'story',

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'twitterbot.urls'

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

WSGI_APPLICATION = 'twitterbot.wsgi.application'


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': join(BASE_DIR, 'db.sqlite3'),
	}
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
RESOURCES = abspath(join(BASE_DIR, 'resources'))
STATIC_ROOT = abspath(join(RESOURCES, 'collected_static_files'))
