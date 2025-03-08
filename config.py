import os
from datetime import timedelta

class Config:
    """Basis-Konfigurationsklasse"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'progressive-ladies-club-munich-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail-Konfiguration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'buchneresther08@gmail.com'
    
    # Admin-Konfiguration
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'buchneresther08@gmail.com'
    
    # Cache-Konfiguration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 Minuten
    
    # Uploads-Konfiguration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # Debug-Toolbar
    DEBUG_TB_ENABLED = False

class DevelopmentConfig(Config):
    """Entwicklungskonfiguration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev.db')
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class TestingConfig(Config):
    """Testkonfiguration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Produktionskonfiguration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prod.db')
    
    # Sicherheitseinstellungen für Produktion
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Cache-Konfiguration für Produktion
    CACHE_TYPE = 'FileSystemCache'
    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    CACHE_DEFAULT_TIMEOUT = 600  # 10 Minuten
    
    # SSL/HTTPS-Einstellung
    SSL_REDIRECT = os.environ.get('SSL_REDIRECT', 'True').lower() in ['true', 'on', '1']

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 