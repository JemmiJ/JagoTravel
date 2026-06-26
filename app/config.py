import os
from dotenv import load_dotenv

load_dotenv()

# Use the process working directory as project root (Render sets cwd to repo src)
PROJECT_ROOT = os.getcwd()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jagotravel-jwt-secret-2024')
    DEBUG = False

    # Static folder under project_root/app/static
    STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static')
    # Uploads under static/uploads
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static', 'uploads')

    # Database
    _db_url = os.getenv('DATABASE_URL', 'sqlite:///jagotravel.db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Supabase credentials — available in .env if needed elsewhere
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

    # Weather API — used if weather feature is implemented
    OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', '')