#!/usr/bin/env python
"""
Database Initialization Script for BikeVault
Run this script to set up the database and create initial tables
"""

import os
import sys
from flask import Flask
from models import db, User, Vehicle, Instrumentation, Activity
from config import config

def init_database():
    """Initialize the database with all tables and default data"""
    
    env = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config[env])
    
    print(f"\n{'='*60}")
    print(f"BikeVault Database Initialization")
    print(f"Environment: {env.upper()}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
    print(f"{'='*60}\n")
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✓ Tables created successfully!")
            
            # Create default users if they don't exist
            if not User.query.first():
                print("\n👤 Creating default users...")
                
                users = [
                    User(username="admin", password="admin123", role="Admin"),
                    User(username="user", password="user123", role="User"),
                    User(username="eng", password="eng123", role="Engineer")
                ]
                
                for user in users:
                    db.session.add(user)
                    print(f"   ✓ Created user: {user.username} (Role: {user.role})")
                
                db.session.commit()
            else:
                print("\n✓ Users already exist, skipping user creation")
            
            # Create sample vehicle if database is empty
            if not Vehicle.query.first():
                print("\n🚗 Creating sample vehicles...")
                
                sample_vehicles = [
                    Vehicle(
                        name="Pulsar NS200",
                        rc="KA-01-AB-1234",
                        chassis="MBLHA10EJ8M123456",
                        engine="MA8M123456",
                        owner="Bajaj Auto",
                        received_on="2026-02-26",
                        bike="Pulsar NS200",
                        number_plate="KA-01-AB-1234",
                        insurance="Bajaj Allianz - Policy: BA/2026/001",
                        cc="200",
                        gears="6",
                        fuel="Petrol",
                        status="In Testing"
                    ),
                    Vehicle(
                        name="Classic 350",
                        rc="MH-12-CD-5678",
                        chassis="MBLHA10EJ8M789012",
                        engine="MA8M789012",
                        owner="Royal Enfield",
                        received_on="2026-01-15",
                        bike="Classic 350",
                        number_plate="MH-12-CD-5678",
                        insurance="Royal Enfield Insurance - Policy: RE/2026/002",
                        cc="350",
                        gears="5",
                        fuel="Petrol",
                        status="Returned"
                    )
                ]
                
                for vehicle in sample_vehicles:
                    db.session.add(vehicle)
                    print(f"   ✓ Created vehicle: {vehicle.name}")
                
                db.session.commit()
            else:
                print("\n✓ Vehicles already exist, skipping sample data creation")
            
            print(f"\n{'='*60}")
            print("✅ Database initialization completed successfully!")
            print(f"{'='*60}\n")
            
            # Print connection info
            print("📍 Connection Details:")
            print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI'][:80]}")
            print(f"\n🔐 Default Credentials (CHANGE THESE IN PRODUCTION):")
            print(f"   Admin:     admin / admin123")
            print(f"   User:      user / user123")
            print(f"   Engineer:  eng / eng123")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during database initialization:")
            print(f"   {str(e)}")
            print(f"\nTroubleshooting:")
            print(f"   1. Check database connection settings in .env file")
            print(f"   2. Verify database server is running")
            print(f"   3. Verify user has permissions to create tables")
            print(f"   4. Check firewall/network access to database server")
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
