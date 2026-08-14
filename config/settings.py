import os
from pathlib import Path
from datetime import timedelta
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY","unsafe-dev-key")
DEBUG=os.getenv("DEBUG","False").lower()=="true"
ALLOWED_HOSTS=[x for x in os.getenv("ALLOWED_HOSTS","*").split(",") if x]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","django.contrib.gis","rest_framework","django_filters","corsheaders","simple_history","accounts","incidents","dispatches","etc_claims","audit"]
MIDDLEWARE=["corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","simple_history.middleware.HistoryRequestMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":{"ENGINE":"django.contrib.gis.db.backends.postgis","NAME":os.getenv("POSTGRES_DB","jsemsas"),"USER":os.getenv("POSTGRES_USER","jsemsas"),"PASSWORD":os.getenv("POSTGRES_PASSWORD","change-me"),"HOST":os.getenv("POSTGRES_HOST","db"),"PORT":os.getenv("POSTGRES_PORT","5432")}}
AUTH_USER_MODEL="accounts.User"
LANGUAGE_CODE="en-us"; TIME_ZONE="Africa/Lagos"; USE_I18N=True; USE_TZ=True
STATIC_URL="/static/"; MEDIA_URL="/media/"; MEDIA_ROOT=BASE_DIR/"media"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=[x for x in os.getenv("CORS_ALLOWED_ORIGINS","").split(",") if x]
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),"DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticated",),"DEFAULT_FILTER_BACKENDS":("django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),"DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":50}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=15),"REFRESH_TOKEN_LIFETIME":timedelta(days=7),"ROTATE_REFRESH_TOKENS":True,"BLACKLIST_AFTER_ROTATION":True}
CELERY_BROKER_URL=os.getenv("REDIS_URL","redis://localhost:6379/0"); CELERY_RESULT_BACKEND=CELERY_BROKER_URL; CELERY_TIMEZONE=TIME_ZONE
QR_SIGNING_KEY=os.getenv("QR_SIGNING_KEY",SECRET_KEY)
GOOGLE_SHEETS_ID=os.getenv("GOOGLE_SHEETS_ID",""); GOOGLE_SHEETS_RANGE=os.getenv("GOOGLE_SHEETS_RANGE","Tariffs!A:E"); GOOGLE_SERVICE_ACCOUNT_JSON=os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON","")
