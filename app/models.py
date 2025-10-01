from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), default='job_seeker')
    disability_type = db.Column(db.String(50))
    accessibility_preferences = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # NEW: Added fields for job matching
    skills = db.Column(db.Text)
    experience_level = db.Column(db.String(50))
    preferred_location = db.Column(db.String(200))
    salary_expectation = db.Column(db.String(100))
    accessibility_needs = db.Column(db.Text)
    work_preferences = db.Column(db.Text)

    # Relationships
    applications = db.relationship('Application', backref='applicant', lazy=True)
    posted_jobs = db.relationship('Job', backref='employer', lazy=True)
    matches = db.relationship('JobMatch', backref='user', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    accessibility_features = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    location = db.Column(db.String(100))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # NEW: Added fields for job matching
    required_skills = db.Column(db.Text)
    experience_required = db.Column(db.String(50))
    work_type = db.Column(db.String(50))
    disability_friendly = db.Column(db.Boolean, default=True)

    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True)
    matches = db.relationship('JobMatch', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    accommodation_request = db.Column(db.Text)

# NEW: JobMatch model
class JobMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    skills_match = db.Column(db.Float, default=0.0)
    experience_match = db.Column(db.Float, default=0.0)
    location_match = db.Column(db.Float, default=0.0)
    accessibility_match = db.Column(db.Float, default=0.0)
    salary_match = db.Column(db.Float, default=0.0)
    match_details = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
