INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'simulation',
]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ROOT_URLCONF = "core.urls"