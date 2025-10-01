import json
from datetime import datetime

def format_date(date):
    """Format datetime object to readable string"""
    if date:
        return date.strftime('%B %d, %Y at %I:%M %p')
    return 'Unknown'

def get_accessibility_preferences(user):
    """Parse user accessibility preferences from JSON"""
    if user.accessibility_preferences:
        try:
            return json.loads(user.accessibility_preferences)
        except json.JSONDecodeError:
            return {}
    return {}

def save_accessibility_preferences(user, preferences):
    """Save user accessibility preferences as JSON"""
    user.accessibility_preferences = json.dumps(preferences)

def get_disability_display_name(disability_type):
    """Get display name for disability type"""
    disability_names = {
        'visual': 'Visual Disability',
        'auditory': 'Auditory Disability',
        'motor': 'Motor Disability',
        'speech': 'Speech Disability',
        'cognitive': 'Cognitive Disability'
    }
    return disability_names.get(disability_type, 'Not specified')

def truncate_text(text, length=150):
    """Truncate text to specified length"""
    if len(text) <= length:
        return text
    return text[:length] + '...'

def get_application_status_color(status):
    """Get Bootstrap color class for application status"""
    status_colors = {
        'pending': 'warning',
        'reviewed': 'info',
        'accepted': 'success',
        'rejected': 'danger'
    }
    return status_colors.get(status, 'secondary')
