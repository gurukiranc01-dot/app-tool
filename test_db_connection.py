#!/usr/bin/env python
"""
Database Connection Test Script
Use this to verify your database configuration before deployment
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_mysql_connection():
    """Test MySQL connection"""
    try:
        import pymysql
        
        # Get credentials from environment
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = int(os.getenv('MYSQL_PORT', '3306'))
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DB')
        
        print("\n" + "="*60)
        print("🔍 MySQL Connection Test")
        print("="*60)
        print(f"Host:     {host}")
        print(f"Port:     {port}")
        print(f"User:     {user}")
        print(f"Database: {database}")
        print("-"*60)
        
        # Test connection
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"✅ Connection Successful!")
        print(f"   MySQL Version: {version[0]}")
        
        # Test database access
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📊 Database Tables ({len(tables)} tables):")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ All tests passed! Database is ready.")
        print("="*60 + "\n")
        return True
        
    except ImportError:
        print("❌ PyMySQL not installed. Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Connection Failed!")
        print(f"Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify .env file has correct credentials")
        print("   2. Check if database server is running")
        print("   3. Verify firewall allows connection")
        print("   4. Confirm database and user exist on server")
        print("   5. Test manually: mysql -h <host> -u <user> -p\n")
        return False

def test_sqlite_connection():
    """Test SQLite connection"""
    try:
        from flask import Flask
        from config import config
        
        print("\n" + "="*60)
        print("🔍 SQLite Connection Test (Development)")
        print("="*60)
        
        app = Flask(__name__)
        app.config.from_object(config['development'])
        
        print(f"Database: bikevault.db")
        print("-"*60)
        
        from models import db
        db.init_app(app)
        
        with app.app_context():
            from models import Vehicle
            count = Vehicle.query.count()
            print(f"✅ Connection Successful!")
            print(f"   Vehicles in database: {count}")
        
        print("\n" + "="*60)
        print("✅ SQLite test passed!")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}\n")
        return False

def main():
    """Main test function"""
    env = os.getenv('FLASK_ENV', 'development')
    
    print("\n" + "="*60)
    print("BikeVault Database Connection Tester")
    print(f"Environment: {env.upper()}")
    print("="*60)
    
    if env == 'production':
        return test_mysql_connection()
    else:
        return test_sqlite_connection()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
