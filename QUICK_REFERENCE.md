# 📝 BikeVault Deployment Quick Reference

## 🎯 3-Phase Deployment Process

### PHASE 1️⃣: REQUEST FROM IT (What to Ask)
```
Database Server Details Needed:
□ Server Hostname/IP: _______________
□ Port Number: _______________
□ Database Name: bikevault_production
□ Application Username: _______________
□ Application Password: _______________
□ Network Access: Confirmed ✓
```

---

### PHASE 2️⃣: LOCAL TESTING (Your Machine)

**Path:** `C:\Users\balaj\OneDrive\Desktop\bikevault-python\`

#### Step 1: Install Requirements
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

#### Step 2: Configure Environment
```powershell
# Copy template
copy .env.template .env

# Edit .env - Add IT-provided credentials
FLASK_ENV=production
MYSQL_HOST=192.168.x.x    # From IT
MYSQL_USER=bikevault_user # From IT
MYSQL_PASSWORD=****       # From IT
MYSQL_DB=bikevault_db     # From IT
```

#### Step 3: Test Connection
```powershell
python test_db_connection.py
```
✅ Should show: "All tests passed!"

#### Step 4: Initialize Database
```powershell
python init_db.py
```
✅ Should show: "Database initialization completed!"

#### Step 5: Test Application
```powershell
python app.py
# Then open: http://localhost:5000
# Login with: admin / admin123
```
✅ Can add/view vehicles? Success!

---

### PHASE 3️⃣: DEPLOY TO BOSCH SERVER

#### On Bosch Server:
```bash
# 1. Transfer files
# Copy bikevault-python folder to server

# 2. Setup Python
cd /opt/bikevault
python3 -m venv .venv
source .venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Configure database (.env file)
# Edit with server credentials

# 5. Initialize Database
python init_db.py

# 6. Run Application
python app.py
# Or with Gunicorn:
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📂 Key Files Explained

| File | Purpose |
|------|---------|
| `config.py` | Database configuration management |
| `.env` | Securely stores database credentials |
| `.env.template` | Template for .env configuration |
| `init_db.py` | Initialize database & tables |
| `test_db_connection.py` | Test database connection |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment instructions |
| `requirements.txt` | Python dependencies (updated with PyMySQL) |

---

## 🚀 Quick Deployment Commands

### Development (SQLite)
```bash
set FLASK_ENV=development
python app.py
```

### Production (MySQL Server)
```bash
set FLASK_ENV=production
python init_db.py        # First time only
python app.py
```

### With Gunicorn (Production)
```bash
set FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔧 Troubleshooting Checklist

### Connection Issues
- [ ] Database server is running?
- [ ] Firewall allows port 3306?
- [ ] Credentials in .env are correct?
- [ ] Database name exists on server?
- [ ] Application user has permissions?

**Test:** `python test_db_connection.py`

### First Run Issues
- [ ] Virtual environment activated?
- [ ] Requirements installed? `pip install -r requirements.txt`
- [ ] .env file created with credentials?
- [ ] FLASK_ENV set to 'production'?
- [ ] init_db.py ran successfully?

### Application Issues
- [ ] Check application logs
- [ ] Verify static/uploads folder exists
- [ ] Ensure disk space available
- [ ] Check file permissions

---

## 📊 Database Supported Versions

| Database | Supported Version | Status |
|----------|------------------|--------|
| MySQL | 8.0+ | ✅ Recommended |
| PostgreSQL | 12+ | ✅ Supported |
| SQL Server | 2019+ | ✅ Supported |
| SQLite | 3.x | ✅ Development Only |

---

## 🔐 Security Reminders

⚠️ **FOR PRODUCTION:**
- [ ] Change default passwords immediately
- [ ] Use HTTPS/SSL certificate
- [ ] Store .env file outside web root
- [ ] Restrict database user permissions
- [ ] Enable automated backups
- [ ] Configure firewall properly
- [ ] Set up monitoring & logging

---

## 📞 Support Resources

### Provided Scripts
- `init_db.py` - Database setup
- `test_db_connection.py` - Connection verification
- `config.py` - Configuration management

### Documentation
- `DEPLOYMENT_GUIDE.md` - Full deployment instructions
- `.env.template` - Configuration example

### Default Credentials (CHANGE IN PRODUCTION)
```
Admin:     admin / admin123
User:      user / user123
Engineer:  eng / eng123
```

---

## ✅ Pre-Deployment Checklist

- [ ] IT provided database credentials
- [ ] Created .env file with credentials
- [ ] test_db_connection.py shows success
- [ ] init_db.py completed without errors
- [ ] Application runs locally on production DB
- [ ] Can login with admin credentials
- [ ] Can add/edit/view vehicles
- [ ] File uploads work
- [ ] Data persists after restart
- [ ] All security requirements met

---

## 📅 Estimated Timeline

| Phase | Duration | Task |
|-------|----------|------|
| 1️⃣ IT Coordination | 3-5 days | Request & receive credentials |
| 2️⃣ Local Testing | 1-2 days | Configure & test locally |
| 3️⃣ Deployment | 1-2 days | Deploy to server |
| 4️⃣ Testing | 1 day | Final verification |

**Total: 1-2 weeks**

---

**Version:** 1.0  
**Updated:** March 25, 2026  
**Status:** Production Ready  
**For:** Bosch Local Server Deployment
