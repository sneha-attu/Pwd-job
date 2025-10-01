# 🚀 PWD Job Portal - Accessible Employment Platform

An accessible job portal designed to connect Persons with Disabilities (PWD) with inclusive employers, providing assistive features that ensure equal access to job opportunities.

---

## ♿ Accessibility Features

- *Visual support*: Voice navigation, screen reader-friendly templates, high contrast UI  
- *Auditory support*: Speech-to-text and text-to-speech features (browser-based)  
- *Motor support*: Full keyboard navigation, large and simple UI controls  
- *Speech support*: Voice input for search and navigation  
- *Cognitive support*: Simplified navigation and content structure  

---

## 🛠 Technology Stack

- *Backend*: Python 3.12, Flask, Flask-SQLAlchemy  
- *Database*: SQLite (default) | PostgreSQL (via DATABASE_URL)  
- *Authentication*: Flask-Login (role-based: Jobseeker & Employer)  
- *Forms*: Flask-WTF + WTForms  
- *Frontend*: Jinja2 (templating), Bootstrap 5, HTML5, CSS3, JavaScript  
- *Accessibility Tools*: Web Speech API (browser-side voice input/output)  
- *Deployment*: Gunicorn (WSGI server)  

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/pwd-job-portal.git
cd pwd-job-portal

Create virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt 

Run database migrations
python migrate_db.py

Start the server
python run.py


App will be running at 👉 http://127.0.0.1:5000


👥 Demo Accounts
Jobseeker

Email: demo@jobseeker.com

Password: demo123

Employer

Email: demo@employer.com

Password: demo123

Project Structure

pwdjob/
│── app/
│   ├── _init_.py        # App factory
│   ├── models.py          # Database models
│   ├── routes.py          # Routes and views
│   ├── forms.py           # Flask-WTF forms
│   ├── templates/         # HTML (Jinja2) templates
│   ├── static/            # CSS, JS, images
│   └── matching_engine.py # Job matching logic
│
│── run.py                 # App entry point
│── migrate_db.py          # Database setup
│── cleanup.py             # Utility scripts
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
