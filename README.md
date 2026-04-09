# 🏍️ Smart BikeVault - Vehicle Testing & Inventory Management System

## 🌐 Live Application

**[🚀 Live Demo](https://web-production-02de4.up.railway.app/)** - Click to access the deployed application
- **Login Credentials**: Username: `admin` | Password: `admin123`
- **Status**: ✅ Production Ready & Deployed on Railway.app

## 📌 Project Overview

**Smart BikeVault** is a comprehensive web-based application designed for managing vehicle (bike) testing operations and inventory tracking. The system provides real-time monitoring, QR code-based vehicle tracking, role-based access control, and automated workflow management for testing facilities.

Built with modern web technologies, this project demonstrates full-stack development capabilities with focus on user experience, database optimization, and production-ready practices.

---

## ✨ Key Features

### 🎯 Core Features
- **Vehicle Management**: Complete lifecycle tracking from receipt to return
- **QR Code Integration**: Automated QR code generation and scanning for quick vehicle access
- **Real-time Status Tracking**: Monitor vehicle status across Testing, Completed, and Returned states
- **User Authentication**: Secure login system with role-based access control (Admin, User)
- **Dashboard Analytics**: Interactive dashboard with vehicle statistics and insights

### 📊 Advanced Features
- **Document Management**: Store and manage vehicle documentation (receipts, testing reports)
- **Email Notifications**: Automated email alerts for testing updates
- **Search & Filtering**: Advanced search capabilities for quick vehicle lookup
- **Responsive Design**: Fully responsive UI compatible with desktop and mobile devices
- **Data Validation**: Comprehensive input validation and error handling

### 🔐 Technical Features
- **Database Optimization**: Efficient SQL queries with proper indexing
- **Error Handling**: Robust error management and user-friendly error messages
- **Session Management**: Secure user session handling
- **File Upload**: Support for document and image uploads

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **Authentication**: Flask-Login with password hashing

### Frontend
- **Markup**: HTML5 with Jinja2 templating
- **Styling**: Tailwind CSS (modern utility-first CSS framework)
- **Interactivity**: Vanilla JavaScript

### Tools & Libraries
- **QR Code Generation**: python-qrcode
- **Email Service**: Flask-Mail with SMTP integration
- **Security**: Werkzeug for password hashing

---

## 📋 Project Structure

```
smart-bikevault/
├── app.py                 # Main Flask application
├── models.py              # Database models (ORM definitions)
├── routes.py              # Application routes/endpoints
├── config.py              # Configuration settings
├── email_service.py       # Email handling logic
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── instance/              # Instance-specific files (DB, uploads)
├── static/
│   ├── style.css          # Custom styling
│   └── uploads/           # User-uploaded files
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── dashboard.html     # Main dashboard
    ├── vehicle.html       # Vehicle detail view
    ├── edit_vehicle.html  # Vehicle editing
    ├── login.html         # Authentication
    ├── admin.html         # Admin panel
    └── receive.html       # Vehicle intake form
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/smart-bikevault.git
   cd smart-bikevault
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Configure Settings**
   - Update `config.py` with your settings
   - Configure email service credentials (if needed)

6. **Run Application**
   ```bash
   python app.py
   ```
   - Access at: `http://localhost:5000`

---

## � Deployment Guide

### Production Deployment on Railway.app

This application is configured for seamless deployment on Railway.app with zero-dependency QR code generation.

#### Key Production Features
- ✅ **Environment-based Configuration**: Automatically adapts to production/development environments
- ✅ **Dynamic Port Binding**: Reads PORT from environment variables (Railway standard)
- ✅ **Dependency-Free QR Generation**: Uses QR Server API - no Pillow or local image libraries needed
- ✅ **Lazy-Loaded OCR**: Heavy ML libraries only load when actually used
- ✅ **Database Flexibility**: Supports SQLite (dev), PostgreSQL, MySQL (production)

#### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Production Ready"
   git push origin main
   ```

2. **Connect to Railway**
   - Visit [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Procfile and runtime.txt

3. **Add Environment Variables** (if needed)
   - `FLASK_ENV=production`
   - `DATABASE_URL=postgresql://...` (for production DB)
   - Mail credentials for email notifications

4. **Auto-Deploy**
   - Railway automatically deploys on every GitHub push
   - View logs in Railway dashboard
   - Automatic HTTPS SSL certificate

#### Production Configuration Files

**Procfile** - Tells Railway how to run the app:
```
web: gunicorn app:app
```

**runtime.txt** - Specifies Python version:
```
python-3.11.7
```

#### Current Deployment Status
- **URL**: https://web-production-02de4.up.railway.app/
- **Server**: Railway.app
- **Status**: ✅ Live & Running
- **Auto-Deploy**: Enabled (GitHub webhook integration)

---

## �📖 Usage Guide

### User Roles

#### Regular User
- View assigned vehicles
- Update vehicle status
- Download QR codes
- View vehicle documentation

#### Admin
- Full vehicle management
- User management
- System configuration
- Email notification settings
- Access to all reports

### Main Workflows

1. **Vehicle Intake**
   - Receive new vehicle
   - Generate QR code
   - Assign to testing team

2. **Testing Cycle**
   - Update vehicle status
   - Add testing notes
   - Upload documentation

3. **Vehicle Return**
   - Mark as completed
   - Generate final report
   - Archive vehicle data

---

## 🎨 Key UI Components

- **Dashboard**: Real-time vehicle statistics and quick actions
- **Vehicle Table**: Sortable, searchable vehicle list
- **QR Modal**: Quick view and download QR codes
- **Status Indicators**: Color-coded status badges
- **Search Bar**: Global search across vehicle attributes

---

## 📝 Database Schema Highlights

### Vehicle Model
- Vehicle Name, RC Number, Chassis Number
- Owner Information
- Status Tracking
- Date Fields (Received, Tested, Returned)
- Document Storage

### User Model
- Authentication credentials
- Role-based permissions
- Created/Last Login timestamps

---

## 🔧 Configuration

Key configuration options in `config.py`:
- Database connection string
- Email service credentials
- Session timeout settings
- Upload file restrictions
- Debug mode settings

---

## 🐛 Error Handling & Validation

- Form validation on both client and server side
- Database integrity constraints
- Comprehensive error logging
- User-friendly error messages
- Graceful error recovery

---

## 📊 Performance Optimizations

- Database query optimization
- Efficient pagination for large datasets
- Static file caching
- Minimal database round-trips
- Image compression for uploads

---

## 🔐 Security Features

✅ Password hashing with Werkzeug
✅ CSRF protection
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Session management
✅ Input validation and sanitization
✅ Role-based access control

---

## 📦 Dependencies

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-Login==0.6.0
Flask-Mail==0.9.0
python-qrcode==7.4.0
Werkzeug==2.3.0
```

See `requirements.txt` for complete list.

---

## 📈 Future Enhancements

- [ ] Advanced analytics and reporting
- [ ] Integration with external APIs
- [ ] Mobile app development
- [ ] Real-time notifications with WebSockets
- [ ] Machine learning for predictive maintenance
- [ ] Multi-location support
- [ ] API documentation with Swagger

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 About the Developer

**Developed by**: [Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile]
- Email: your.email@example.com

---

## 📧 Support & Contact

For questions, issues, or suggestions:
- Open an Issue on GitHub
- Contact: your.email@example.com

---

## 🎯 Learning Outcomes

This project demonstrates proficiency in:
- **Backend Development**: Flask, RESTful routing, form handling
- **Database Design**: Schema design, ORM usage, data relationships
- **Frontend Development**: HTML5, CSS (Tailwind), Vanilla JavaScript
- **Security**: Authentication, authorization, input validation
- **Software Engineering**: Version control, documentation, code organization
- **Problem Solving**: Feature implementation, bug fixes, optimization

---

**⭐ If you find this useful, please consider giving it a star!**
