import os

def find_project_root():
    current = os.getcwd()
    if os.path.exists(os.path.join(current, 'manage.py')): return current
    if os.path.exists(os.path.join(current, 'food_marketplace', 'manage.py')): return os.path.join(current, 'food_marketplace')
    return None

PROJECT_ROOT = find_project_root()

# --- RECREATION CONTENT (If files are missing) ---
DEFAULT_WSGI = """
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_marketplace.settings')

application = get_wsgi_application()
app = application
"""

DEFAULT_URLS = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

DEFAULT_SETTINGS = """
import os
from pathlib import Path
from datetime import timedelta
import dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS += ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'users',
    'restaurants',
    'menu',
    'orders',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'food_marketplace.urls'

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

WSGI_APPLICATION = 'food_marketplace.wsgi.application'

# Database
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
DB_NAME = os.getenv('DB_NAME', 'db.sqlite3')

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': BASE_DIR / DB_NAME if 'sqlite3' in DB_ENGINE else DB_NAME,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
"""

def find_config_dir():
    """Recursively search for the directory containing settings.py"""
    if not PROJECT_ROOT: return None
    
    print(f"🔍 Scanning for Django configuration in {PROJECT_ROOT}...")
    
    candidates = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if 'env' in dirs: dirs.remove('env')
        if 'venv' in dirs: dirs.remove('venv')
        if '.git' in dirs: dirs.remove('.git')
        
        if 'settings.py' in files:
            candidates.append(os.path.relpath(root, PROJECT_ROOT))
    
    if not candidates:
        return None
        
    # Prefer one with wsgi.py
    for c in candidates:
        full_p = os.path.join(PROJECT_ROOT, c) if c != "." else PROJECT_ROOT
        if os.path.exists(os.path.join(full_p, 'wsgi.py')):
            return c
            
    return candidates[0]

# Detect or Create Config
CONFIG_DIR = find_config_dir()
CREATED_CONFIG = False

if not CONFIG_DIR:
    print("⚠️  Warning: Configuration files missing. Recreating them...")
    CONFIG_DIR_NAME = "food_marketplace"
    CONFIG_FULL_PATH = os.path.join(PROJECT_ROOT, CONFIG_DIR_NAME)
    
    if not os.path.exists(CONFIG_FULL_PATH):
        os.makedirs(CONFIG_FULL_PATH)
        
    with open(os.path.join(CONFIG_FULL_PATH, "__init__.py"), "w") as f: f.write("")
    with open(os.path.join(CONFIG_FULL_PATH, "settings.py"), "w") as f: f.write(DEFAULT_SETTINGS.strip())
    with open(os.path.join(CONFIG_FULL_PATH, "urls.py"), "w") as f: f.write(DEFAULT_URLS.strip())
    with open(os.path.join(CONFIG_FULL_PATH, "wsgi.py"), "w") as f: f.write(DEFAULT_WSGI.strip())
    
    CONFIG_DIR = CONFIG_DIR_NAME
    CREATED_CONFIG = True
    print(f"✅ Created configuration in '{CONFIG_DIR_NAME}/'")

# Determine paths
WSGI_PATH = "wsgi.py" if CONFIG_DIR == "." else f"{CONFIG_DIR.replace(os.sep, '/')}/wsgi.py"
FULL_CONFIG_PATH = PROJECT_ROOT if CONFIG_DIR == "." else os.path.join(PROJECT_ROOT, CONFIG_DIR)

# --- 1. VERCEL.JSON ---
VERCEL_JSON = f"""{{
    "builds": [
        {{
            "src": "{WSGI_PATH}",
            "use": "@vercel/python",
            "config": {{ "maxLambdaSize": "15mb", "runtime": "python3.9" }}
        }}
    ],
    "routes": [
        {{
            "src": "/static/(.*)",
            "dest": "/static/$1"
        }},
        {{
            "src": "/(.*)",
            "dest": "{WSGI_PATH}"
        }}
    ]
}}"""

def prepare_for_vercel():
    if not PROJECT_ROOT:
        print("❌ Error: manage.py not found.")
        return

    print(f"🚀 Preparing project for Vercel Deployment...")
    print(f"📂 Config Dir: {CONFIG_DIR}")

    # 1. Update requirements.txt
    req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
    new_reqs = ["dj-database-url", "psycopg2-binary", "whitenoise", "gunicorn"]
    
    current_reqs = ""
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as f: current_reqs = f.read()
    
    with open(req_path, "a", encoding="utf-8") as f:
        for req in new_reqs:
            if req not in current_reqs: f.write(f"\n{req}")
    print("✅ Updated requirements.txt")

    # 2. Create vercel.json
    with open(os.path.join(PROJECT_ROOT, "vercel.json"), "w", encoding="utf-8") as f:
        f.write(VERCEL_JSON)
    print("✅ Created vercel.json")

    # 3. Modify/Create wsgi.py if missing in existing config dir
    wsgi_file = os.path.join(FULL_CONFIG_PATH, "wsgi.py")
    if not os.path.exists(wsgi_file):
        with open(wsgi_file, "w") as f: f.write(DEFAULT_WSGI.strip())
        print("✅ Created missing wsgi.py")
    else:
        # Ensure app alias exists
        with open(wsgi_file, "r") as f: c = f.read()
        if "app = application" not in c:
            with open(wsgi_file, "a") as f: f.write("\napp = application\n")
            print("✅ Updated wsgi.py for Vercel")

    print("\n🎉 Project is ready for Vercel!")
    print("👉 Next Steps:")
    print("1.  Run 'pip install -r requirements.txt'")
    print("2.  Git add, commit, and push these changes.")
    print("3.  Go to Vercel and import your repository.")

if __name__ == "__main__":
    prepare_for_vercel()