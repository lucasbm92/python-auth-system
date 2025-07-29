import os
# Load environment variables from .env file
env_path = BASE_DIR / '.env'
load_dotenv(env_path, override=True)

# Debug: Print detailed .env loading information
print(f"🔍 Loading .env from: {env_path}")
print(f"🔍 .env file exists: {env_path.exists()}")

# Try reading the file directly
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:3]  # First 3 lines
        print(f"🔍 .env preview: {[line.strip() for line in lines if line.strip()]}")
except Exception as e:
    print(f"❌ Error reading .env: {e}")

# Check environment variables
debug_val = os.getenv('DEBUG')
email_user = os.getenv('EMAIL_HOST_USER')
secret_key = os.getenv('SECRET_KEY')
print(f"🔍 DEBUG: '{debug_val}'")
print(f"🔍 EMAIL_HOST_USER: '{email_user}'")
print(f"🔍 SECRET_KEY loaded: {bool(secret_key)}")

if debug_val and email_user:
    print("✅ Environment variables loaded!")
else:
    print("❌ Environment variables missing!")ort Path
from dotenv import load_dotenv
import pymysql

# Configure PyMySQL to work with Django
pymysql.install_as_MySQLdb()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

# Debug: Print if .env file is loaded
debug_value = os.getenv('DEBUG')
email_user = os.getenv('EMAIL_HOST_USER')
print(f"🔍 Loading .env from: {env_path}")
print(f"🔍 .env file exists: {env_path.exists()}")
print(f"🔍 DEBUG value: '{debug_value}' (type: {type(debug_value)})")
print(f"� EMAIL_HOST_USER: '{email_user}'")

if debug_value and debug_value.lower() == 'true':
    print(f"✅ .env file loaded successfully")
else:
    print("❌ .env file not loaded properly or DEBUG not true")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'authentication',
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME', 'auth_system_db'),
        'USER': os.getenv('DATABASE_USER', 'lucasbm92'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'lbm291292'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
EMAIL_TIMEOUT = 30  # Add timeout for Gmail SMTP

# Custom user model
AUTH_USER_MODEL = 'authentication.User'
