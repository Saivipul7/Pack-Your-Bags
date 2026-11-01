from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'roamwise-local-demo-key-change-for-production'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']
INSTALLED_APPS = ['django.contrib.contenttypes','django.contrib.auth','rest_framework','corsheaders','tourism']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = []
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {'DEFAULT_RENDERER_CLASSES':['rest_framework.renderers.JSONRenderer'], 'DEFAULT_PARSER_CLASSES':['rest_framework.parsers.JSONParser']}
