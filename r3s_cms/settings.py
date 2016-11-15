# -*- coding: utf-8 -*-
import os
import socket
from django.core.urlresolvers import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'l6+kubs2ihl28-s8x(8n2lou984u7rlme0e-98ymlwwgu9zuz('
DEBUG = True
ALLOWED_HOSTS = ['*' , ]
STAGE_HOST = {
	'DEVELOPMENT' : [
					'MacBook-Pro-de-Ricardo.local' ,
					'development' ,
					'Development' ,
					'mac-ricardo-lan' ,
					'mac-ricardo-wireless' ,
					'Mac-Ricardo-Wireless' ,
					'mac-mini-ethernet' ,
					'development.local' ,					
					] ,
	'SANDBOX' : [
				'vps-1152651-20280.manage.myhosting.com' ,	
				's192-169-250-216.secureserver.net' ,
				] ,
	'PRODUCTION' : [
					'ip-172-31-22-183' ,
					] ,
}
ADMINS = (
    ('ricardo.tercero', 'ee-admin@r3s.com.mx'),
)
socket_hostname = socket.gethostname()
print "socket_hostname: %s" % socket_hostname
if socket_hostname in STAGE_HOST.get('DEVELOPMENT'):
	DEBUG = True
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'ricardo.tercero.solis@gmail.com'
	EMAIL_HOST_PASSWORD = 'SkipperMan8'
	CC_EMAIL_RECEPIENT = []
	BCC_EMAIL_RECEPIENT = []
	DATABASES = {
			    'default': {
							'ENGINE' : 'django.db.backends.postgresql_psycopg2',
							'NAME' : 'ee_cms_db',
							'USER' : 'ee_cms_db_user',
							'PASSWORD' : 'SkipperMan8' ,
							'HOST' : 'development' ,
			    		} ,
				}
elif socket_hostname in STAGE_HOST.get('SANDBOX'):
	DEBUG = False
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'ricardo.tercero.solis@gmail.com'
	EMAIL_HOST_PASSWORD = 'SkipperMan8'
	CC_EMAIL_RECEPIENT = []
	BCC_EMAIL_RECEPIENT = []
	DATABASES = {
			    'default': {
							'ENGINE' : 'django.db.backends.postgresql_psycopg2',
							'NAME' : 'ee_cms_db',
							'USER' : 'ee_cms_db_user',
							'PASSWORD' : 'SkipperMan8' ,
							'HOST' : '127.0.0.1' ,
			    		} ,
				}
elif socket_hostname in STAGE_HOST.get('PRODUCTION'):
	DEBUG = False
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'ricardo.tercero.solis@gmail.com'
	EMAIL_HOST_PASSWORD = 'SkipperMan8'
	CC_EMAIL_RECEPIENT = []
	BCC_EMAIL_RECEPIENT = []
	DATABASES = {
			    'default': {
							'ENGINE' : 'django.db.backends.postgresql_psycopg2',
							'NAME' : 'ee_cms_db',
							'USER' : 'ee_cms_db_user',
							'PASSWORD' : 'SkipperMan8' ,
							'HOST' : '127.0.0.1' ,
			    		} ,
				}
else:
	DEBUG = True
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'ricardo.tercero.solis@gmail.com'
	EMAIL_HOST_PASSWORD = 'SkipperMan8'
	CC_EMAIL_RECEPIENT = []
	BCC_EMAIL_RECEPIENT = []
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}
ANALYTICS_RECORD = not DEBUG
GOOGLE_ANALYTICS = ANALYTICS_RECORD
GOOGLE_GOOGLE_ANALYTICS_ID = 'UA-75268765-2'
INSTALLED_APPS = (
#    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'r3s_cms.apps.analytics' ,
	'r3s_cms.apps.system' ,
	'r3s_cms.apps.systemAuth' ,
	'r3s_cms.apps.imagery' ,
	'r3s_cms.apps.underConstruction' ,
	'r3s_cms.apps.content' ,
	'r3s_cms.apps.polls' ,
	'r3s_cms.apps.emailer' ,
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
ROOT_URLCONF = 'r3s_cms.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
				os.path.join(BASE_DIR, 'r3s_cms' , 'templates'),
				],
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
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'r3s_cms' , 'templates'),
)
WSGI_APPLICATION = 'r3s_cms.wsgi.application'
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Monterrey'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR,  'deployment/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
SYSTEM_DOMAIN = 'localhost'
SESSION_TAG = 'R3S_CMS_SESSION'
SLUG_SEPARATOR = "_"
#AUTH_USER_MODEL = "systemAuth.R3SUser"
BUSINESS_LABEL = "Efecto Estrategia"
LOGIN_URL = reverse('system_login')
LOGOUT_URL = reverse('system_logout')