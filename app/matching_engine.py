import re
import json
from datetime import datetime
from app.models import User, Job, JobMatch
from app import db

class JobMatchingEngine:
    
    @staticmethod
    def calculate_skills_match(user_skills, job_skills):
        """Calculate skills compatibility (0-100)"""
        if not user_skills or not job_skills:
            return 0.0
            
        user_skills_list = [skill.strip().lower() for skill in user_skills.split(',') if skill.strip()]
        job_skills_list = [skill.strip().lower() for skill in job_skills.split(',') if skill.strip()]
        
        if not user_skills_list or not job_skills_list:
            return 0.0
            
        # Find matching skills
        matching_skills = set(user_skills_list) & set(job_skills_list)
        
        # Also check for partial matches (e.g., "python" matches "python programming")
        partial_matches = 0
        for user_skill in user_skills_list:
            for job_skill in job_skills_list:
                if user_skill in job_skill or job_skill in user_skill:
                    partial_matches += 0.5
                    break
        
        # Calculate match percentage
        total_required_skills = len(job_skills_list)
        match_score = ((len(matching_skills) + partial_matches) / total_required_skills) * 100
        
        return min(100.0, match_score)
    
    @staticmethod
    def calculate_experience_match(user_experience, job_experience):
        """Calculate experience level match (0-100)"""
        if not user_experience or not job_experience:
            return 50.0  # Neutral if not specified
            
        experience_levels = {
            '0-1': 1, '1-3': 2, '3-5': 3, '5-10': 4, '10+': 5
        }
        
        user_level = experience_levels.get(user_experience, 0)
        job_level = experience_levels.get(job_experience, 0)
        
        if user_level == 0 or job_level == 0:
            return 50.0
            
        # Exact match = 100%, 1 level difference = 80%, 2 levels = 60%, etc.
        difference = abs(user_level - job_level)
        if difference == 0:
            return 100.0
        elif difference == 1:
            return 80.0
        elif difference == 2:
            return 60.0
        else:
            return 40.0
    
    @staticmethod
    def calculate_location_match(user_location, job_location, work_type):
        """Calculate location compatibility (0-100)"""
        if not job_location:
            return 100.0  # No location requirement
            
        if work_type and 'remote' in work_type.lower():
            return 100.0  # Remote work = location doesn't matter
            
        if not user_location:
            return 50.0  # User hasn't specified location
            
        # Simple keyword matching for cities/states
        user_location_words = set(user_location.lower().split())
        job_location_words = set(job_location.lower().split())
        
        common_words = user_location_words & job_location_words
        if common_words:
            return 100.0
        else:
            return 20.0  # Different locations
    
    @staticmethod
    def calculate_accessibility_match(user_disability, user_needs, job_features):
        """Calculate accessibility compatibility (0-100)"""
        if not user_disability and not user_needs:
            return 100.0  # No accessibility requirements
            
        if not job_features:
            return 20.0  # Job doesn't specify accessibility features
            
        # Check if job features match user needs
        user_needs_lower = (user_needs or '').lower()
        job_features_lower = job_features.lower()
        
        # Keywords that indicate good accessibility matches
        accessibility_keywords = [
            'wheelchair', 'accessible', 'screen reader', 'braille', 'hearing',
            'visual', 'cognitive', 'mobility', 'remote', 'flexible', 'accommodation'
        ]
        
        matches = 0
        for keyword in accessibility_keywords:
            if keyword in user_needs_lower and keyword in job_features_lower:
                matches += 1
        
        # Base score for PWD-friendly jobs
        base_score = 60.0
        keyword_bonus = min(40.0, matches * 10)
        
        return base_score + keyword_bonus
    
    @staticmethod
    def calculate_salary_match(user_expectation, job_range):
        """Calculate salary compatibility (0-100)"""
        if not user_expectation or not job_range:
            return 75.0  # Neutral if not specified
            
        try:
            # Extract numbers from salary strings
            user_numbers = re.findall(r'\d+', user_expectation.replace(',', ''))
            job_numbers = re.findall(r'\d+', job_range.replace(',', ''))
            
            if not user_numbers or not job_numbers:
                return 75.0
                
            user_salary = int(user_numbers[0]) * (1000 if len(user_numbers[0]) <= 3 else 1)
            job_min = int(job_numbers[0]) * (1000 if len(job_numbers[0]) <= 3 else 1)
            job_max = int(job_numbers[-1]) * (1000 if len(job_numbers[-1]) <= 3 else 1)
            
            if job_min <= user_salary <= job_max:
                return 100.0  # Perfect match
            elif user_salary < job_min:
                # User expects less than offered
                return 90.0
            else:
                # User expects more than offered
                difference_percent = ((user_salary - job_max) / job_max) * 100
                return max(20.0, 80.0 - difference_percent)
                
        except (ValueError, IndexError):
            return 75.0
    
    @staticmethod
    def calculate_overall_match(user, job):
        """Calculate overall match score and details"""
        
        # Calculate individual match scores
        skills_match = JobMatchingEngine.calculate_skills_match(
            user.skills, job.required_skills
        )
        
        experience_match = JobMatchingEngine.calculate_experience_match(
            user.experience_level, job.experience_required
        )
        
        location_match = JobMatchingEngine.calculate_location_match(
            user.preferred_location, job.location, job.work_type
        )
        
        accessibility_match = JobMatchingEngine.calculate_accessibility_match(
            user.disability_type, user.accessibility_needs, job.accessibility_features
        )
        
        salary_match = JobMatchingEngine.calculate_salary_match(
            user.salary_expectation, job.salary_range
        )
        
        # Weighted overall score
        weights = {
            'skills': 0.35,
            'experience': 0.25,
            'accessibility': 0.20,
            'location': 0.10,
            'salary': 0.10
        }
        
        overall_score = (
            skills_match * weights['skills'] +
            experience_match * weights['experience'] +
            accessibility_match * weights['accessibility'] +
            location_match * weights['location'] +
            salary_match * weights['salary']
        )
        
        # Match details
        match_details = {
            'skills_match': round(skills_match, 1),
            'experience_match': round(experience_match, 1),
            'location_match': round(location_match, 1),
            'accessibility_match': round(accessibility_match, 1),
            'salary_match': round(salary_match, 1),
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        return round(overall_score, 1), match_details
    
    @staticmethod
    def generate_matches_for_user(user_id):
        """Generate job matches for a specific user"""
        user = User.query.get(user_id)
        if not user or user.user_type != 'job_seeker':
            return []
        
        # Get all available jobs
        jobs = Job.query.all()
        matches = []
        
        for job in jobs:
            # Skip if user already applied to this job
            existing_application = Application.query.filter_by(
                user_id=user.id, job_id=job.id
            ).first()
            if existing_application:
                continue
                
            # Skip if match already exists
            existing_match = JobMatch.query.filter_by(
                user_id=user.id, job_id=job.id
            ).first()
            if existing_match:
                continue
            
            # Calculate match
            overall_score, match_details = JobMatchingEngine.calculate_overall_match(user, job)
            
            # Only create matches above threshold (e.g., 30%)
            if overall_score >= 30.0:
                job_match = JobMatch(
                    user_id=user.id,
                    job_id=job.id,
                    match_score=overall_score,
                    skills_match=match_details['skills_match'],
                    experience_match=match_details['experience_match'],
                    location_match=match_details['location_match'],
                    accessibility_match=match_details['accessibility_match'],
                    salary_match=match_details['salary_match'],
                    match_details=json.dumps(match_details)
                )
                
                db.session.add(job_match)
                matches.append(job_match)
        
        db.session.commit()
        return matches
