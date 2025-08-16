#!/bin/sh
set -e
until nc -z db 5432; do echo "Esperando postgres..."; sleep 1; done
if [ ! -f manage.py ]; then
  django-admin startproject config .
  awk '1' config/settings.py > config/_base.py && mv config/_base.py config/settings.py
  cat << 'PY' >> config/settings.py
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY","dev-insecure")
DEBUG = os.getenv("DJANGO_DEBUG","1") == "1"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","*").split(",")
INSTALLED_APPS += ["rest_framework"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST","db"),
        "PORT": os.getenv("POSTGRES_PORT","5432"),
    }
}
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL","redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND","redis://redis:6379/1")
PY
  # urls base con /api/
  sed -i "s/from django.urls import path/from django.urls import path, include/g" config/urls.py
  sed -i "s/urlpatterns = \[/urlpatterns = \[ path('api\/', include('api.urls')),\n/g" config/urls.py || true
  python manage.py startapp api
  mkdir -p api
  cat << 'PY' > api/urls.py
from django.urls import path
from .views import ping
urlpatterns = [ path("ping/", ping) ]
PY
  cat << 'PY' > api/views.py
from django.http import JsonResponse
def ping(request): return JsonResponse({"status":"ok"})
PY
  sed -i "s/INSTALLED_APPS = \[/INSTALLED_APPS = \['api',/g" config/settings.py
fi
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
