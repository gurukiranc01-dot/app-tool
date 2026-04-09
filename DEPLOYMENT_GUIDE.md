# 🚀 BikeVault Deployment Guide for Bosch Server

## Phase 1: Preparation & IT Coordination (Week 1)

### Request from IT/DBA
Contact your IT department with this information:

```
Subject: Database Setup Request for BikeVault Application

Requirements:
- Application: BikeVault (Vehicle Testing Management)
- Database: MySQL 8.0+ (preferred) or PostgreSQL 12+ or SQL Server 2019+
- Size: < 1GB initially
- Backup: Daily automated backups recommended
- Users: Need 1 application user account with full DB privileges

Requested Details:
- Database server hostname/IP: _______________
- Database port: _______________
- Application user account: _______________
- Application password: _______________
- Database name: bikevault_production
- Network access: Confirm firewall rules for app server → DB server
```

### What You'll Receive from IT
- ✅ Database server hostname/IP
- ✅ Port number (usually 3306 for MySQL)
- ✅ Username for application user
- ✅ Password for application user
- ✅ Database name created and ready
- ✅ Network access confirmed

---

## Phase 2: Local Setup & Testing (Your Machine - Week 2)

### Step 1: Install Database Driver
```bash
cd c:\Users\balaj\OneDrive\Desktop\bikevault-python
.\.venv\Scripts\pip install -r requirements.txt
```

### Step 2: Create Environment Configuration
```bash
# Copy the template file
copy .env.template .env

# Edit .env with your database credentials (provided by IT)
# Use your text editor to update:
```

**Edit .env file:**
```
FLASK_ENV=production
MYSQL_USER=bikevault_user          # From IT
MYSQL_PASSWORD=your_password       # From IT
MYSQL_HOST=192.168.1.50            # From IT (Bosch server IP)
MYSQL_PORT=3306                    # From IT (usually 3306)
MYSQL_DB=bikevault_production      # From IT
```

### Step 3: Test Database Connection
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Initialize the database
python init_db.py
```

**Expected output:**
```
============================================================
BikeVault Database Initialization
Environment: PRODUCTION
Database URI: mysql+pymysql://bikevault_user:****@192.168.1.50:3306/bikevault_db
============================================================

📊 Creating database tables...
✓ Tables created successfully!

👤 Creating default users...
   ✓ Created user: admin (Role: Admin)
   ✓ Created user: user (Role: User)
   ✓ Created user: eng (Role: Engineer)

✅ Database initialization completed successfully!
```

### Step 4: Test Application with Server Database
```bash
python app.py
```

Then test in browser:
- Open: http://localhost:5000
- Login as admin / admin123
- Try adding a vehicle
- Check if data persists after restart

---

## Phase 3: Deployment to Bosch Server (Week 3)

### Step 1: Prepare Application Files

Create deployment package:
```
bikevault-deployment/
├── app.py
├── models.py
├── routes.py
├── config.py
├── requirements.txt
├── init_db.py
├── templates/
├── static/
├── .env (← Keep this with production credentials)
└── README_DEPLOYMENT.txt
```

### Step 2: Transfer to Bosch Server

**Option A: Using Git (Recommended)**
```bash
# On your machine
git init
git add .
git commit -m "Initial commit"

# Push to corporate Git server
# Then clone on Bosch server
```

**Option B: Direct File Transfer**
- Copy files via SFTP/SCP to `/opt/bikevault/` (Linux) or `C:\Applications\bikevault\` (Windows)
- Ensure file permissions are correct

### Step 3: Server Setup

**On the Bosch Server:**

```bash
# Install Python 3.10+
# Create virtual environment
python -m venv .venv

# Activate venv
# Linux:
source .venv/bin/activate
# Windows:
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run application
python app.py
```

### Step 4: Configure Web Server (Production)

**Option A: Using Gunicorn (Linux/Mac)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option B: Using IIS (Windows Server)**
- Install Python Hosting for IIS
- Configure app pool and application
- Set environment variables in IIS

**Option C: Using Windows Service**
- Use NSSM to run as Windows service
- Auto-start on server reboot

### Step 5: Configure Nginx/Apache Reverse Proxy

**Nginx configuration example:**
```nginx
server {
    listen 80;
    server_name bikevault.bosch.local;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /opt/bikevault/static/;
        expires 7d;
    }
}
```

---

## Phase 4: Post-Deployment Checklist

### Security Hardening

- [ ] Change all default passwords in database
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure firewall rules
- [ ] Set up database user with minimal required permissions
- [ ] Enable database backups
- [ ] Set up log rotation
- [ ] Configure automated daily backups

### Testing

- [ ] Login with all user roles
- [ ] Add/Edit/Delete vehicle
- [ ] Upload files (RC card, insurance)
- [ ] Generate Excel export
- [ ] Test search functionality
- [ ] Verify data persists after application restart

### Monitoring

- [ ] Set up error logging
- [ ] Monitor CPU/Memory usage
- [ ] Monitor database size
- [ ] Set up alerts for critical errors
- [ ] Document any issues

---

## Troubleshooting

### Connection Timeout
```
Error: Unable to connect to database
Solution:
1. Verify MYSQL_HOST is correct
2. Check if database server is running: ping <host>
3. Confirm firewall allows port 3306
4. Test connection: telnet <host> 3306
```

### Authentication Failed
```
Error: Access denied for user
Solution:
1. Verify MYSQL_USER and MYSQL_PASSWORD in .env
2. Confirm IT provided correct credentials
3. Ensure user has permissions on database
```

### Table Creation Failed
```
Error: Cannot create tables
Solution:
1. Verify application user has CREATE, ALTER permissions
2. Check if database already exists
3. Ensure charset is utf8mb4
```

### File Upload Issues
```
Solution:
1. Verify 'static/uploads' directory exists and is writable
2. Check file permissions: chmod 755 static/uploads
3. Verify disk space available
```

---

## Backup and Recovery

### Automated Daily Backup (Linux)
```bash
# Create backup script: /opt/bikevault/backup.sh
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mysqldump -u bikevault_user -p$MYSQL_PASSWORD bikevault_production > \
  /backups/bikevault_$TIMESTAMP.sql

# Add to crontab (runs daily at 2 AM)
crontab -e
# Add line: 0 2 * * * /opt/bikevault/backup.sh
```

### Restore from Backup
```bash
mysql -u bikevault_user -p bikevault_production < /backups/bikevault_20260325.sql
```

---

## Performance Optimization

### Database Indexes (Often Done by DBA)
```sql
CREATE INDEX idx_vehicle_rc ON vehicle(rc);
CREATE INDEX idx_vehicle_status ON vehicle(status);
CREATE INDEX idx_activity_vehicle_id ON activity(vehicle_id);
```

### Connection Pooling
```python
# Already configured in SQLAlchemy with optimal settings
# Max pool size: 10
# Pool recycle: 3600 seconds
```

---

## Support & Next Steps

1. **During Testing**: Document any issues and share with development team
2. **Go-Live**: Notify all users of new URL and credentials
3. **Training**: Conduct user training session on new features
4. **Monitoring**: Check logs daily for first week
5. **Feedback**: Collect user feedback and plan improvements

---

## Related Files

- `.env.template` - Environment configuration template
- `config.py` - Database configuration management
- `init_db.py` - Database initialization script
- `requirements.txt` - Python package dependencies

---

**Last Updated**: March 25, 2026
**Environment**: Production ready
**Status**: Ready for Bosch deployment
