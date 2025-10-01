import os
import glob

# Find all .db files
db_files = glob.glob('**/*.db', recursive=True)
for db_file in db_files:
    try:
        os.remove(db_file)
        print(f"Deleted: {db_file}")
    except:
        print(f"Couldn't delete: {db_file}")

print("Cleanup complete!")
