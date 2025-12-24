import os
import sys
from django.core.wsgi import get_wsgi_application

# Try to import waitress
try:
    from waitress import serve
except ImportError:
    print("❌ Error: 'waitress' is not installed.")
    print("👉 Run: pip install waitress")
    sys.exit(1)

def find_project_name():
    """Auto-detect the Django project name based on manage.py location"""
    for item in os.listdir(os.getcwd()):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, 'settings.py')):
            return item
    return "food_marketplace" # Default fallback

if __name__ == "__main__":
    project_name = find_project_name()
    
    # Set the Django settings environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

    # Initialize Django Application
    try:
        application = get_wsgi_application()
    except Exception as e:
        print(f"❌ Could not load Django application: {e}")
        sys.exit(1)

    print(f"🚀 Starting Production Server for '{project_name}'...")
    print("🟢 Serving on http://localhost:8000")
    print("   (Press Ctrl+C to stop)")
    
    # Start the production server
    serve(application, host='0.0.0.0', port=8000)