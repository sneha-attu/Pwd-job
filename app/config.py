import os
from datetime import timedelta

class Config:
    """Configuration settings for PWD Job Portal"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pwd-job-portal-accessible-employment-2025'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pwd_jobs.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Management (Accessibility: No time limits for cognitive disabilities)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    WTF_CSRF_TIME_LIMIT = None  # Removed for accessibility compliance
    
    # File Upload Limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Email Configuration (for future notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Business Settings
    PLATFORM_NAME = 'PWD Job Portal'
    PLATFORM_TAGLINE = 'Making Employment Accessible for All'
    SUPPORT_EMAIL = 'support@pwdjobportal.com'
    
    # Accessibility Compliance
    WCAG_LEVEL = 'AA'  # WCAG 2.1 AA compliance target
    MIN_BUTTON_SIZE = 48  # Minimum 48px for motor disabilities
    HIGH_CONTRAST_MODE = True
    SCREEN_READER_SUPPORT = True
