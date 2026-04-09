# 📦 BikeVault Deployment Package Checklist

## Files to Deploy to Bosch Server

### ✅ **Core Application Files** (Must Include)
```
✓ app.py                          # Main Flask application
✓ models.py                       # Database models
✓ routes.py                       # Application routes
✓ config.py                       # Configuration manager
```

### ✅ **Configuration Files** (Must Include)
```
✓ requirements.txt                # Python dependencies
✓ .env                           # Production credentials (from IT)
✓ .env.template                  # Environment template
```

### ✅ **Database Setup Tools** (Recommended)
```
✓ init_db.py                     # Database initialization
✓ test_db_connection.py          # Connection verification
```

### ✅ **Templates Folder** (Must Include)
```
✓ templates/
  ├── base.html                  # Base template
  ├── login.html                 # Login page
  ├── dashboard.html             # Dashboard
  ├── receive.html               # Add vehicle form
  ├── vehicle.html               # Vehicle details
  ├── edit_vehicle.html          # Edit vehicle form
  ├── admin.html                 # Admin panel
  ├── scan.html                  # QR scan
  └── forgot.html                # Password recovery
```

### ✅ **Static Files Folder** (Must Include)
```
✓ static/
  ├── style.css                  # Stylesheet
  ├── bosch.png                  # Logo
  └── uploads/                   # File upload directory (create if missing)
```

### ✅ **Documentation** (Reference Only)
```
  - SETUP_SUMMARY.md             # This summary
  - DEPLOYMENT_GUIDE.md          # Full deployment guide
  - QUICK_REFERENCE.md           # Quick command reference
  - README.md                    # Project readme (optional)
```

---

## 🚀 Pre-Deployment Checklist

### **Before Transferring to Server:**

- [ ] All files in correct folder structure
- [ ] No .env file with credentials (will create on server)
- [ ] .env.template present (for reference)
- [ ] .gitignore in place (if using Git)
- [ ] Python 3.10+ available on server
- [ ] Permission to install packages

### **Server Setup:**

- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file created with IT credentials
- [ ] init_db.py executed successfully
- [ ] test_db_connection.py passed

### **Post-Deployment:**

- [ ] App starts without errors
- [ ] Can access web interface
- [ ] Login works with credentials
- [ ] Can add/view/edit vehicles
- [ ] File uploads work
- [ ] Data persists after restart

---

## 📁 Complete Directory Structure

```
/opt/bikevault/                          (or C:\Applications\bikevault\ on Windows)
│
├── app.py                               # Main application
├── models.py                            # Database models
├── routes.py                            # Routes
├── config.py                            # Configuration
│
├── init_db.py                           # DB initialization script
├── test_db_connection.py                # Connection test script
│
├── requirements.txt                     # Dependencies
├── .env                                 # Production config (create on server)
├── .env.template                        # Template (for reference)
│
├── templates/                           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── receive.html
│   ├── vehicle.html
│   ├── edit_vehicle.html
│   ├── admin.html
│   ├── scan.html
│   └── forgot.html
│
├── static/                              # Static files
│   ├── style.css
│   ├── bosch.png
│   └── uploads/                         # File uploads (auto-created)
│
└── docs/                                # Documentation
    ├── SETUP_SUMMARY.md
    ├── DEPLOYMENT_GUIDE.md
    ├── QUICK_REFERENCE.md
    └── README.md
```

---

## 🔧 Server Installation Steps

### **1. Prepare Server**
```bash
# Create application directory
mkdir /opt/bikevault
cd /opt/bikevault

# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### **2. Transfer Files**
```bash
# Option A: Git clone
git clone <your-repo-url> .

# Option B: Direct file transfer (SCP/SFTP)
# Copy all files maintaining directory structure
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Database**
```bash
# Create .env from template
cp .env.template .env

# Edit .env with IT-provided credentials
nano .env  # or use your text editor
```

### **5. Initialize Database**
```bash
python init_db.py
```

### **6. Test Connection**
```bash
python test_db_connection.py
```

### **7. Start Application**
```bash
# Development mode
python app.py

# Production mode (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📊 File Size Estimates

| Component | Size |
|-----------|------|
| Core Python files | ~500 KB |
| Templates | ~200 KB |
| Static files | ~300 KB |
| Virtual environment | ~50 MB |
| Total (with venv) | ~51 MB |

---

## ⚙️ System Requirements for Server

### **Minimum:**
- Python 3.10+
- 1 GB RAM
- 500 MB disk space
- Network access to database server

### **Recommended:**
- Python 3.11+
- 2 GB RAM
- 1 GB disk space
- Dedicated database server
- HTTPS/SSL certificate
- Backup solution

---

## 🔐 Security Checklist

Before going live:

- [ ] .env file with credentials NOT in version control
- [ ] Production passwords changed from defaults
- [ ] HTTPS/SSL certificate installed
- [ ] Firewall configured (allow only required ports)
- [ ] Database backups configured
- [ ] Log rotation configured
- [ ] Monitoring/alerting configured
- [ ] Regular security updates planned

---

## 📋 Deployment Command Reference

### **Quick Reference**
```bash
# Test connection
python test_db_connection.py

# Initialize database (first run)
python init_db.py

# Start development mode
python app.py

# Start with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Backup database
mysqldump -u user -p database_name > backup.sql

# Restore from backup
mysql -u user -p database_name < backup.sql
```

---

## 🆘 Troubleshooting

### **Connection Issues**
```bash
# Test database connection
python test_db_connection.py

# Check network connectivity
ping <database-host>

# Check firewall
telnet <database-host> 3306
```

### **Package Issues**
```bash
# Reinstall all requirements
pip install --force-reinstall -r requirements.txt

# Check installed packages
pip list
```

### **Permission Issues**
```bash
# Fix file permissions (Linux)
chmod 755 app.py
chmod 755 init_db.py
chmod 755 templates
chmod 755 static

# Create uploads directory if missing
mkdir -p static/uploads
chmod 755 static/uploads
```

---

## 📞 Support Files

| File | Purpose |
|------|---------|
| SETUP_SUMMARY.md | Overview of setup (this file) |
| DEPLOYMENT_GUIDE.md | Detailed step-by-step guide |
| QUICK_REFERENCE.md | Quick command lookup |
| .env.template | Configuration template |

---

## ✅ Deployment Sign-Off

Before going live, verify:

- [ ] Files transferred correctly
- [ ] Permissions set properly
- [ ] Dependencies installed
- [ ] Database connection working
- [ ] Application starts
- [ ] Login works
- [ ] All features functional
- [ ] Backups configured
- [ ] Monitoring active

---

**Version:** 1.0  
**Date:** March 25, 2026  
**For:** Bosch Local Server Deployment  
**Status:** Ready for Production
