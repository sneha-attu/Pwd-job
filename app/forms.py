from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=20)],
                          render_kw={'class': 'form-control form-control-lg'})
    
    email = StringField('Email Address', 
                       validators=[DataRequired(), Email()],
                       render_kw={'class': 'form-control form-control-lg'})
    
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)],
                            render_kw={'class': 'form-control form-control-lg'})
    
    user_type = SelectField('I am a', 
                           choices=[
                               ('job_seeker', 'Job Seeker'),
                               ('employer', 'Employer')
                           ], 
                           validators=[DataRequired()],
                           render_kw={'class': 'form-select form-select-lg'})
    
    disability_type = SelectField('Disability Type (Optional)', 
                                 choices=[
                                     ('', 'Prefer not to say'),
                                     ('visual', 'Visual Disability'),
                                     ('auditory', 'Auditory Disability'),
                                     ('motor', 'Motor Disability'),
                                     ('speech', 'Speech Disability'),
                                     ('cognitive', 'Cognitive Disability')
                                 ],
                                 validators=[Optional()],
                                 render_kw={'class': 'form-select form-select-lg'})
    
    submit = SubmitField('Create Account', render_kw={'class': 'btn btn-primary btn-lg'})

class LoginForm(FlaskForm):
    email = StringField('Email Address', 
                       validators=[DataRequired(), Email()],
                       render_kw={'class': 'form-control form-control-lg'})
    
    password = PasswordField('Password', 
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control form-control-lg'})
    
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary btn-lg'})

class JobForm(FlaskForm):
    title = StringField('Job Title', 
                       validators=[DataRequired()],
                       render_kw={'class': 'form-control form-control-lg'})
    
    company = StringField('Company Name', 
                         validators=[DataRequired()],
                         render_kw={'class': 'form-control form-control-lg'})
    
    description = TextAreaField('Job Description', 
                               validators=[DataRequired()],
                               render_kw={'class': 'form-control', 'rows': '5'})
    
    requirements = TextAreaField('Requirements',
                                render_kw={'class': 'form-control', 'rows': '4'})
    
    accessibility_features = TextAreaField('Accessibility Features',
                                         validators=[DataRequired()],
                                         render_kw={'class': 'form-control', 'rows': '4'})
    
    salary_range = StringField('Salary Range',
                              render_kw={'class': 'form-control form-control-lg'})
    
    location = StringField('Location',
                          render_kw={'class': 'form-control form-control-lg'})
    
    submit = SubmitField('Post Job', render_kw={'class': 'btn btn-success btn-lg'})

class ApplicationForm(FlaskForm):
    accommodation_request = TextAreaField('Accommodation Requests',
                                        render_kw={'class': 'form-control', 'rows': '5'})
    
    submit = SubmitField('Submit Application', render_kw={'class': 'btn btn-primary btn-lg'})
