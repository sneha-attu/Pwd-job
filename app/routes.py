from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Job, Application, JobMatch # Added JobMatch
from app.forms import RegistrationForm, LoginForm, JobForm, ApplicationForm
import re
import json

main = Blueprint('main', __name__)

def create_sample_data():
    """Create sample employer and jobs if none exist"""
    if Job.query.count() == 0:
        # Create sample employer
        employer = User.query.filter_by(email='employer@demo.com').first()
        if not employer:
            employer = User(
                username='TechCorp',
                email='employer@demo.com',
                user_type='employer',
                password_hash=generate_password_hash('demo123')
            )
            db.session.add(employer)
            db.session.commit()

        # Create sample jobs
        jobs_data = [
            {
                'title': 'Accessible Web Developer',
                'company': 'TechCorp Solutions',
                'description': 'We are seeking a passionate web developer to create accessible, inclusive digital experiences. You will work with modern frameworks like React, Vue.js, and implement WCAG 2.1 AA standards. This role offers excellent growth opportunities in accessibility technology.',
                'requirements': '• 2+ years experience with HTML, CSS, JavaScript\n• Knowledge of WCAG 2.1 accessibility standards\n• Experience with React or Vue.js\n• Understanding of screen readers and assistive technologies\n• Strong problem-solving skills\n• Excellent communication abilities',
                'accessibility_features': '• Height-adjustable desk and ergonomic chair\n• Screen reader compatible development environment\n• Flexible working hours (6am-10am or 9am-1pm start)\n• Full remote work option available\n• Noise-canceling headphones provided\n• Large monitor setup (27+ inches)\n• Voice recognition software available\n• Accessible parking spot reserved\n• Step-free building access with elevator',
                'salary_range': '$65,000 - $85,000 annually',
                'location': 'Remote / New York, NY',
                'required_skills': 'HTML, CSS, JavaScript, React, Vue.js, WCAG, Accessibility',
                'experience_required': '1-3',
                'work_type': 'remote'
            },
            {
                'title': 'Inclusive UX/UI Designer',
                'company': 'Design Innovations Inc',
                'description': 'Join our design team to create beautiful, accessible user interfaces. You will design for diverse users including those with disabilities, ensuring our products are usable by everyone. Work with design systems, conduct user research, and prototype accessible solutions.',
                'requirements': '• 3+ years UX/UI design experience\n• Proficiency in Figma, Sketch, or Adobe XD\n• Understanding of accessibility design principles\n• Experience with user research and testing\n• Knowledge of color contrast and typography\n• Portfolio showing accessible design work',
                'accessibility_features': '• Adjustable lighting and desk setup\n• Color blindness-friendly design tools\n• Flexible schedule for medical appointments\n• Quiet workspace environment\n• Magnification software available\n• Alternative input devices (trackball, speech-to-text)\n• Visual schedule and task management tools\n• Accessible meeting rooms with proper acoustics',
                'salary_range': '$70,000 - $95,000 annually',
                'location': 'Hybrid - San Francisco, CA',
                'required_skills': 'UX Design, UI Design, Figma, Sketch, Adobe XD, User Research, Accessibility',
                'experience_required': '3-5',
                'work_type': 'hybrid'
            },
            {
                'title': 'Customer Support Specialist',
                'company': 'HelpDesk Solutions',
                'description': 'Provide exceptional customer support through multiple channels including chat, email, and phone. Help customers with technical issues, account questions, and product guidance. We value empathy, patience, and problem-solving skills in creating positive customer experiences.',
                'requirements': '• 1+ years customer service experience\n• Excellent written and verbal communication\n• Patience and empathy when helping customers\n• Basic technical troubleshooting skills\n• Ability to work in team environment\n• High school diploma or equivalent',
                'accessibility_features': '• Text-based communication options (chat/email focus)\n• Adjustable volume headsets and amplifiers\n• Real-time captioning for team meetings\n• Visual alert systems for notifications\n• TTY/TDD phone support available\n• Sign language interpreter services\n• Flexible break schedule\n• Quiet workspace with minimal distractions',
                'salary_range': '$40,000 - $55,000 annually',
                'location': 'Remote / Chicago, IL',
                'required_skills': 'Customer Service, Communication, Problem Solving, Technical Support',
                'experience_required': '0-1',
                'work_type': 'remote'
            },
            {
                'title': 'Data Analyst - Accessibility Focus',
                'company': 'Analytics Pro',
                'description': 'Analyze user behavior data to improve accessibility features in our products. Create reports, identify usage patterns, and provide insights that help make our platform more inclusive. Work with SQL, Python, and visualization tools.',
                'requirements': '• 2+ years data analysis experience\n• Proficiency in SQL and Python\n• Experience with Tableau or Power BI\n• Statistical analysis knowledge\n• Understanding of accessibility metrics\n• Bachelor\'s degree in related field preferred',
                'accessibility_features': '• Large dual monitor setup included\n• High contrast display options\n• Voice-activated data query tools\n• Flexible work hours (core hours 10am-2pm)\n• Ergonomic keyboard and mouse\n• Standing desk option\n• Screen magnification software\n• Accessible data visualization tools',
                'salary_range': '$58,000 - $75,000 annually',
                'location': 'Hybrid - Austin, TX',
                'required_skills': 'SQL, Python, Data Analysis, Tableau, Power BI, Statistics',
                'experience_required': '1-3',
                'work_type': 'hybrid'
            }
        ]

        for job_data in jobs_data:
            job = Job(
                title=job_data['title'],
                company=job_data['company'],
                description=job_data['description'],
                requirements=job_data['requirements'],
                accessibility_features=job_data['accessibility_features'],
                salary_range=job_data['salary_range'],
                location=job_data['location'],
                posted_by=employer.id,
                required_skills=job_data['required_skills'],
                experience_required=job_data['experience_required'],
                work_type=job_data['work_type']
            )
            db.session.add(job)
        
        db.session.commit()
        print("✅ Created 4 sample jobs!")

@main.route('/')
def index():
    create_sample_data()
    jobs = Job.query.order_by(Job.created_at.desc()).limit(3).all()
    return render_template('index.html', jobs=jobs)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html', form=form)

        # Check if username already exists
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already taken. Please choose a different username.', 'error')
            return render_template('register.html', form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data,
            disability_type=form.disability_type.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()

        flash(f'Account created successfully! Please login with your credentials.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password. Please try again.', 'error')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # Create sample data if none exists
    create_sample_data()
    
    # Get user stats
    total_jobs = Job.query.count()
    if current_user.user_type == 'job_seeker':
        my_applications = Application.query.filter_by(user_id=current_user.id).count()
        my_matches = JobMatch.query.filter_by(user_id=current_user.id).count()
        my_jobs = 0
        
        # Get pending matches for quick access
        pending_matches = JobMatch.query.filter_by(
            user_id=current_user.id, 
            status='pending'
        ).limit(3).all()
        
        dashboard_data = {
            'show_matching_card': my_matches == 0 or pending_matches,
            'pending_matches': pending_matches,
            'my_matches': my_matches
        }
    else:
        my_applications = 0
        my_matches = 0
        my_jobs = Job.query.filter_by(posted_by=current_user.id).count()
        dashboard_data = {}

    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(3).all()

    return render_template('dashboard.html',
                         total_jobs=total_jobs,
                         my_applications=my_applications,
                         my_jobs=my_jobs,
                         recent_jobs=recent_jobs,
                         **dashboard_data)

@main.route('/jobs')
def jobs():
    # Create sample data if none exists
    create_sample_data()
    
    # Get search parameters
    search_query = request.args.get('search', '').strip()
    location_filter = request.args.get('location', '').strip()
    work_type_filter = request.args.get('work_type', '').strip()
    
    # Start with all jobs
    jobs_query = Job.query
    
    # Apply search filters
    if search_query:
        jobs_query = jobs_query.filter(
            db.or_(
                Job.title.contains(search_query),
                Job.company.contains(search_query),
                Job.description.contains(search_query),
                Job.required_skills.contains(search_query)
            )
        )
    
    if location_filter:
        jobs_query = jobs_query.filter(Job.location.contains(location_filter))
    
    if work_type_filter:
        jobs_query = jobs_query.filter(Job.work_type == work_type_filter)
    
    # Get filtered jobs
    all_jobs = jobs_query.order_by(Job.created_at.desc()).all()
    
    # Get unique locations and work types for filter dropdowns
    locations = db.session.query(Job.location).distinct().filter(Job.location != None).all()
    locations = [loc[0] for loc in locations if loc[0]]
    
    work_types = db.session.query(Job.work_type).distinct().filter(Job.work_type != None).all()
    work_types = [wt[0] for wt in work_types if wt[0]]

    return render_template('jobs.html',
                         jobs=all_jobs,
                         search=search_query,
                         location_filter=location_filter,
                         work_type_filter=work_type_filter,
                         locations=locations,
                         work_types=work_types)

@main.route('/job/<int:id>')
def job_detail(id):
    job = Job.query.get_or_404(id)
    
    # Check if current user already applied
    already_applied = False
    if current_user.is_authenticated and current_user.user_type == 'job_seeker':
        already_applied = Application.query.filter_by(
            user_id=current_user.id, job_id=id).first() is not None
    
    # Get similar jobs
    similar_jobs = Job.query.filter(
        Job.id != id,
        db.or_(
            Job.required_skills.contains(job.required_skills.split(',')[0] if job.required_skills else ''),
            Job.work_type == job.work_type
        )
    ).limit(3).all()

    return render_template('job_detail.html', 
                         job=job, 
                         already_applied=already_applied,
                         similar_jobs=similar_jobs)

@main.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    if current_user.user_type != 'job_seeker':
        flash('Only job seekers can apply for jobs.', 'error')
        return redirect(url_for('main.job_detail', id=job_id))

    job = Job.query.get_or_404(job_id)
    
    existing_application = Application.query.filter_by(
        user_id=current_user.id, job_id=job_id).first()
    
    if existing_application:
        flash('You have already applied for this job.', 'info')
        return redirect(url_for('main.job_detail', id=job_id))

    if request.method == 'POST':
        # Handle PWD certificate file upload
        pwd_certificate = request.files.get('pwd_certificate')
        certificate_filename = None
        
        if pwd_certificate and pwd_certificate.filename:
            # Validate file type
            if not pwd_certificate.filename.lower().endswith('.pdf'):
                flash('PWD certificate must be a PDF file.', 'error')
                return render_template('apply_form.html', job=job)
            
            # Create uploads directory if it doesn't exist
            import os
            upload_dir = 'uploads/certificates'
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file with secure filename
            from werkzeug.utils import secure_filename
            import uuid
            filename = secure_filename(pwd_certificate.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            certificate_path = os.path.join(upload_dir, unique_filename)
            pwd_certificate.save(certificate_path)
            certificate_filename = unique_filename
        
        # Create application record
        accommodation_text = f"Disabilities: {', '.join(request.form.getlist('disability_type'))}\nDetails: {request.form.get('accommodation_details')}\nCertificate: {certificate_filename}"
        
        application = Application(
            user_id=current_user.id,
            job_id=job_id,
            accommodation_request=accommodation_text
        )
        db.session.add(application)
        
        # Update match status if exists
        job_match = JobMatch.query.filter_by(user_id=current_user.id, job_id=job_id).first()
        if job_match:
            job_match.status = 'applied'
        
        db.session.commit()
        
        flash('Application with PWD certificate submitted successfully!', 'success')
        return redirect(url_for('main.my_applications'))

    return render_template('apply_form.html', job=job)

@main.route('/my-applications')
@login_required
def my_applications():
    """View all user applications"""
    if current_user.user_type != 'job_seeker':
        flash('Only job seekers can view applications.', 'error')
        return redirect(url_for('main.dashboard'))
    
    applications = Application.query.filter_by(user_id=current_user.id)\
                                  .order_by(Application.applied_at.desc()).all()
    
    return render_template('my_applications.html', applications=applications)

@main.route('/withdraw-application/<int:application_id>', methods=['POST'])
@login_required
def withdraw_application(application_id):
    """Allow users to withdraw their job applications"""
    if current_user.user_type != 'job_seeker':
        flash('Only job seekers can withdraw applications.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Find the application
    application = Application.query.get_or_404(application_id)
    
    # Check if the application belongs to current user
    if application.user_id != current_user.id:
        flash('You can only withdraw your own applications.', 'error')
        return redirect(url_for('main.my_applications'))
    
    # Check if application can be withdrawn (only pending applications)
    if application.status != 'pending':
        flash(f'Cannot withdraw application with status: {application.status}', 'error')
        return redirect(url_for('main.my_applications'))
    
    # Store job title for flash message
    job_title = application.job.title
    
    # Update match status back to 'liked' if exists
    job_match = JobMatch.query.filter_by(
        user_id=current_user.id, 
        job_id=application.job_id
    ).first()
    if job_match and job_match.status == 'applied':
        job_match.status = 'liked'
    
    # Delete the application
    db.session.delete(application)
    db.session.commit()
    
    flash(f'Successfully withdrew application for "{job_title}". You can apply again later.', 'success')
    return redirect(url_for('main.my_applications'))

@main.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.user_type != 'employer':
        flash('Only employers can post jobs.', 'error')
        return redirect(url_for('main.dashboard'))

    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            description=form.description.data,
            requirements=form.requirements.data,
            accessibility_features=form.accessibility_features.data,
            salary_range=form.salary_range.data,
            location=form.location.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully! It is now visible to job seekers.', 'success')
        return redirect(url_for('main.my_jobs'))

    return render_template('post_job.html', form=form)

@main.route('/my-jobs')
@login_required
def my_jobs():
    """View employer's posted jobs"""
    if current_user.user_type != 'employer':
        flash('Only employers can view posted jobs.', 'error')
        return redirect(url_for('main.dashboard'))
    
    jobs = Job.query.filter_by(posted_by=current_user.id)\
                   .order_by(Job.created_at.desc()).all()
    
    return render_template('my_jobs.html', jobs=jobs)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update profile information
        current_user.username = request.form.get('username', current_user.username)
        current_user.skills = request.form.get('skills', current_user.skills)
        current_user.experience_level = request.form.get('experience_level', current_user.experience_level)
        current_user.preferred_location = request.form.get('preferred_location', current_user.preferred_location)
        current_user.salary_expectation = request.form.get('salary_expectation', current_user.salary_expectation)
        current_user.accessibility_needs = request.form.get('accessibility_needs', current_user.accessibility_needs)
        current_user.work_preferences = request.form.get('work_preferences', current_user.work_preferences)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    # Get user stats for profile page
    if current_user.user_type == 'job_seeker':
        applications = Application.query.filter_by(user_id=current_user.id).all()
        matches = JobMatch.query.filter_by(user_id=current_user.id).all()
        jobs = []
    else:
        applications = []
        matches = []
        jobs = Job.query.filter_by(posted_by=current_user.id).all()

    return render_template('profile.html', 
                         applications=applications, 
                         jobs=jobs, 
                         matches=matches)

# Job Matching Game Routes
def calculate_match_score(user, job):
    """Enhanced matching algorithm"""
    score = 0.0
    
    # Skills match (40% weight)
    if user.skills and job.required_skills:
        user_skills = [s.strip().lower() for s in user.skills.split(',')]
        job_skills = [s.strip().lower() for s in job.required_skills.split(',')]
        matching_skills = set(user_skills) & set(job_skills)
        skills_score = (len(matching_skills) / len(job_skills)) * 40 if job_skills else 0
        score += skills_score
    else:
        score += 20  # Neutral score if no skills specified
    
    # Experience match (25% weight)
    if user.experience_level and job.experience_required:
        exp_levels = {'0-1': 1, '1-3': 2, '3-5': 3, '5-10': 4, '10+': 5}
        user_exp = exp_levels.get(user.experience_level, 0)
        job_exp = exp_levels.get(job.experience_required, 0)
        if user_exp and job_exp:
            exp_diff = abs(user_exp - job_exp)
            exp_score = max(0, 25 - (exp_diff * 5))
            score += exp_score
        else:
            score += 12.5
    else:
        score += 12.5
    
    # Location match (15% weight)
    if job.work_type == 'remote':
        score += 15
    elif user.preferred_location and job.location:
        if any(word in job.location.lower() for word in user.preferred_location.lower().split()):
            score += 15
        else:
            score += 5
    else:
        score += 10
    
    # Accessibility match (20% weight)
    if user.disability_type and job.accessibility_features:
        if user.disability_type.lower() in job.accessibility_features.lower():
            score += 20
        else:
            score += 10
    else:
        score += 15
    
    return min(100.0, score)

@main.route('/job-matching-game')
@login_required
def job_matching_game():
    """Main job matching game interface"""
    if current_user.user_type != 'job_seeker':
        flash('Job matching is only available for job seekers.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Check if user profile is complete
    if not current_user.skills:
        flash('Please complete your profile to get better job matches!', 'info')
        return redirect(url_for('main.complete_profile'))
    
    # Get or generate matches
    matches = JobMatch.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).order_by(JobMatch.match_score.desc()).limit(1).all()
    
    if not matches:
        # Generate new matches
        jobs = Job.query.all()
        for job in jobs:
            # Skip if already applied or matched
            if Application.query.filter_by(user_id=current_user.id, job_id=job.id).first():
                continue
            if JobMatch.query.filter_by(user_id=current_user.id, job_id=job.id).first():
                continue
            
            # Calculate match score
            match_score = calculate_match_score(current_user, job)
            if match_score >= 30:  # Only show matches above 30%
                job_match = JobMatch(
                    user_id=current_user.id,
                    job_id=job.id,
                    match_score=match_score,
                    skills_match=match_score * 0.4,
                    experience_match=match_score * 0.25,
                    location_match=match_score * 0.15,
                    accessibility_match=match_score * 0.2,
                    salary_match=75.0,
                    match_details=json.dumps({'generated': True})
                )
                db.session.add(job_match)
        
        db.session.commit()
        matches = JobMatch.query.filter_by(
            user_id=current_user.id,
            status='pending'
        ).order_by(JobMatch.match_score.desc()).limit(1).all()
    
    # Get current match for the game
    current_match = matches[0] if matches else None
    total_matches = JobMatch.query.filter_by(user_id=current_user.id).count()
    
    return render_template('job_matching_game.html', 
                         current_match=current_match,
                         total_matches=total_matches)

@main.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """Complete user profile for better matching"""
    if request.method == 'POST':
        current_user.skills = request.form.get('skills')
        current_user.experience_level = request.form.get('experience_level')
        current_user.preferred_location = request.form.get('preferred_location')
        current_user.salary_expectation = request.form.get('salary_expectation')
        current_user.accessibility_needs = request.form.get('accessibility_needs')
        current_user.work_preferences = request.form.get('work_preferences')
        
        db.session.commit()
        flash('Profile completed! Now let\'s find your perfect job matches.', 'success')
        return redirect(url_for('main.job_matching_game'))
    
    return render_template('complete_profile.html')

@main.route('/match-action/<int:match_id>/<action>')
@login_required
def match_action(match_id, action):
    """Handle match actions (like, pass, apply)"""
    match = JobMatch.query.get_or_404(match_id)
    
    if match.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('main.job_matching_game'))
    
    if action == 'like':
        match.status = 'liked'
        flash('Job saved to your favorites!', 'success')
    elif action == 'pass':
        match.status = 'passed'
        flash('Job passed. We\'ll find better matches for you!', 'info')
    elif action == 'apply':
        match.status = 'applied'
        db.session.commit()
        return redirect(url_for('main.apply_job', job_id=match.job_id))
    
    db.session.commit()
    return redirect(url_for('main.job_matching_game'))

@main.route('/my-matches')
@login_required
def my_matches():
    """View all user matches with filters - FIXED VERSION"""
    if current_user.user_type != 'job_seeker':
        flash('Only job seekers can view matches.', 'error')
        return redirect(url_for('main.dashboard'))
    
    status_filter = request.args.get('status', 'all')
    
    matches_query = JobMatch.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        matches_query = matches_query.filter_by(status=status_filter)
    
    matches = matches_query.order_by(JobMatch.match_score.desc()).all()
    
    # Add application status to each match - FIXED APPROACH
    for match in matches:
        # Check if user has an active application for this job
        match.has_active_application = Application.query.filter_by(
            user_id=current_user.id,
            job_id=match.job.id
        ).first() is not None
    
    return render_template('my_matches.html', matches=matches, status_filter=status_filter)

# Additional utility routes
@main.route('/search')
def search():
    """Enhanced search functionality"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('main.jobs'))
    
    # Search in jobs
    jobs = Job.query.filter(
        db.or_(
            Job.title.contains(query),
            Job.company.contains(query),
            Job.description.contains(query),
            Job.accessibility_features.contains(query),
            Job.required_skills.contains(query)
        )
    ).all()
    
    return render_template('jobs.html', jobs=jobs, search=query)

@main.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'Goodbye {username}! You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))

# Demo and API routes (keeping your existing ones)
@main.route('/create-demo')
def create_demo():
    """Create demo accounts for testing"""
    # Create demo job seeker
    demo_seeker = User.query.filter_by(email='demo@jobseeker.com').first()
    if not demo_seeker:
        demo_seeker = User(
            username='DemoJobSeeker',
            email='demo@jobseeker.com',
            user_type='job_seeker',
            disability_type='visual',
            password_hash=generate_password_hash('demo123')
        )
        db.session.add(demo_seeker)
    
    # Create demo employer
    demo_employer = User.query.filter_by(email='demo@employer.com').first()
    if not demo_employer:
        demo_employer = User(
            username='DemoEmployer',
            email='demo@employer.com',
            user_type='employer',
            password_hash=generate_password_hash('demo123')
        )
        db.session.add(demo_employer)
    
    db.session.commit()
    create_sample_data()
    
    return '''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2>✅ Demo Accounts Created!</h2>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h3>Demo Accounts:</h3>
            <p><strong>Job Seeker:</strong><br>
            Email: demo@jobseeker.com<br>
            Password: demo123</p>
            
            <p><strong>Employer:</strong><br>
            Email: demo@employer.com<br>
            Password: demo123</p>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <a href="/login" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🚀 Login Now</a>
            <a href="/" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">← Back to Homepage</a>
        </div>
        
        <div style="background: #e7f3ff; padding: 15px; border-radius: 5px;">
            <p><strong>Sample Jobs:</strong> 4 accessible jobs created automatically</p>
            <p><strong>Features:</strong> Complete PWD job portal with navigation, search, job matching game, and accessibility features</p>
        </div>
    </div>
    '''

@main.route('/api/jobs')
def api_jobs():
    """API endpoint for job data"""
    jobs = Job.query.all()
    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'accessibility_features': job.accessibility_features,
            'created_at': job.created_at.strftime('%Y-%m-%d')
        })
    return {'jobs': jobs_data, 'total': len(jobs_data)}
