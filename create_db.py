#!/usr/bin/env python
"""Fresh database creation script"""
import os
import sys

# Remove old database if exists
if os.path.exists('bikevault.db'):
    os.remove('bikevault.db')
    print("Deleted old bikevault.db")

if os.path.exists('instance/bikevault.db'):
    try:
        os.remove('instance/bikevault.db')
        print("Deleted old instance/bikevault.db")
    except:
        pass

# Clear Flask cache
if os.path.exists('__pycache__'):
    import shutil
    shutil.rmtree('__pycache__')
    print("Cleared __pycache__")

# Now create the app and database
from app import app, db
from models import User, Vehicle

print("\n" + "="*60)
print("Creating Fresh Database")
print("="*60)

with app.app_context():
    # Create all tables
    db.create_all()
    print("✓ Database tables created!")
    
    # Create default users
    if not User.query.first():
        users = [
            User(username="admin", password="admin123", role="Admin"),
            User(username="user", password="user123", role="User"),
            User(username="eng", password="eng123", role="Engineer")
        ]
        for user in users:
            db.session.add(user)
            print(f"✓ Created user: {user.username}")
        db.session.commit()
    
    print("\n" + "="*60)
    print("✅ Database Created Successfully!")
    print("="*60)
    print("\nDefault Users:")
    print("  Admin:     admin / admin123")
    print("  User:      user / user123")
    print("  Engineer:  eng / eng123")
    print()
