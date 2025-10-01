import sqlite3

# Connect to database
conn = sqlite3.connect('pwd_jobs.db')
cursor = conn.cursor()

# Add new columns to User table
try:
    cursor.execute("ALTER TABLE user ADD COLUMN skills TEXT")
    print("✅ Added skills column to User")
except:
    print("⚠️ skills column already exists")

try:
    cursor.execute("ALTER TABLE user ADD COLUMN experience_level VARCHAR(50)")
    print("✅ Added experience_level column to User")
except:
    print("⚠️ experience_level column already exists")

try:
    cursor.execute("ALTER TABLE user ADD COLUMN preferred_location VARCHAR(200)")
    print("✅ Added preferred_location column to User")
except:
    print("⚠️ preferred_location column already exists")

try:
    cursor.execute("ALTER TABLE user ADD COLUMN salary_expectation VARCHAR(100)")
    print("✅ Added salary_expectation column to User")
except:
    print("⚠️ salary_expectation column already exists")

try:
    cursor.execute("ALTER TABLE user ADD COLUMN accessibility_needs TEXT")
    print("✅ Added accessibility_needs column to User")
except:
    print("⚠️ accessibility_needs column already exists")

try:
    cursor.execute("ALTER TABLE user ADD COLUMN work_preferences TEXT")
    print("✅ Added work_preferences column to User")
except:
    print("⚠️ work_preferences column already exists")

# Add new columns to Job table
try:
    cursor.execute("ALTER TABLE job ADD COLUMN required_skills TEXT")
    print("✅ Added required_skills column to Job")
except:
    print("⚠️ required_skills column already exists")

try:
    cursor.execute("ALTER TABLE job ADD COLUMN experience_required VARCHAR(50)")
    print("✅ Added experience_required column to Job")
except:
    print("⚠️ experience_required column already exists")

try:
    cursor.execute("ALTER TABLE job ADD COLUMN work_type VARCHAR(50)")
    print("✅ Added work_type column to Job")
except:
    print("⚠️ work_type column already exists")

try:
    cursor.execute("ALTER TABLE job ADD COLUMN disability_friendly BOOLEAN DEFAULT 1")
    print("✅ Added disability_friendly column to Job")
except:
    print("⚠️ disability_friendly column already exists")

# Create JobMatch table
try:
    cursor.execute('''
        CREATE TABLE job_match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            match_score FLOAT NOT NULL,
            skills_match FLOAT DEFAULT 0.0,
            experience_match FLOAT DEFAULT 0.0,
            location_match FLOAT DEFAULT 0.0,
            accessibility_match FLOAT DEFAULT 0.0,
            salary_match FLOAT DEFAULT 0.0,
            match_details TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (job_id) REFERENCES job (id)
        )
    ''')
    print("✅ Created JobMatch table")
except:
    print("⚠️ JobMatch table already exists")

# Commit changes
conn.commit()
conn.close()

print("\n🎉 Database migration completed!")
print("You can now run: python run.py")
