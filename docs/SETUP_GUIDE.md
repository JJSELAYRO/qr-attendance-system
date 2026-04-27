# QR Attendance System - Complete Setup Guide

A simple, modern, and user-friendly QR Code Attendance System built with Python.

---

## 📁 Project Structure

```
qr_attendance_system/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLite configuration
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── crud.py             # Database operations
│   │   └── auth.py             # Authentication utilities
│   ├── main.py                 # FastAPI entry point
│   ├── seed_data.py            # Sample data generator
│   └── requirements.txt
├── frontend/                   # KivyMD Android App
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── login_screen.py     # Login UI
│   │   ├── student_home.py     # Student home screen
│   │   ├── qr_scanner.py       # QR scanner
│   │   ├── attendance_success.py
│   │   ├── attendance_history.py
│   │   ├── teacher_dashboard.py
│   │   └── admin_panel.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_client.py       # Backend API client
│   │   ├── gps_helper.py       # GPS location
│   │   └── sms_helper.py       # SMS intent
│   ├── main.py                 # App entry point
│   ├── intent_filters.xml      # Android intents
│   └── buildozer.spec          # Build configuration
├── scripts/
│   ├── build_apk.sh            # Linux/Mac build script
│   ├── build_apk.bat           # Windows build script
│   └── upload_to_drive.py      # Optional: Upload to Drive
├── assets/                     # Images, icons, etc.
├── requirements.txt            # All dependencies
└── docs/
    └── SETUP_GUIDE.md          # This file
```

---

## 🛠️ Prerequisites

### Required Software

1. **Python 3.8+**
   - Download from https://python.org
   - Make sure to check "Add to PATH"

2. **Git** (for cloning)
   - Download from https://git-scm.com

3. **Java JDK 17** (for Android builds)
   - Download from https://adoptium.net
   - Set `JAVA_HOME` environment variable

4. **Android SDK** (for Android builds)
   - Download Android Studio or SDK tools
   - Set `ANDROIDSDK` environment variable

---

## 🚀 Quick Start

### Step 1: Clone and Navigate

```bash
cd qr_attendance_system
```

### Step 2: Setup Backend

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python seed_data.py

# Start the backend server
python main.py
```

The backend will run at `http://localhost:8000`

### Step 3: Test Backend API

Open browser and go to:
- http://localhost:8000/ - API info
- http://localhost:8000/docs - Interactive API documentation

**Sample Login Credentials:**
- **Admin:** admin / admin123
- **Teacher:** teacher1 / teacher123
- **Students:** student1-5 / student123

---

## 📱 Running the Frontend

### Desktop Testing (Development)

```bash
# In a new terminal, from project root
cd frontend

# Install dependencies
pip install -r ../requirements.txt

# Run the app
python main.py
```

### Configure Backend URL

Edit `frontend/utils/api_client.py` and update:

```python
# Change this to your backend IP address
# For local testing:
API_BASE_URL = "http://localhost:8000"

# For network testing (same WiFi):
# Find your computer's IP: ipconfig (Windows) or ifconfig (Linux/Mac)
API_BASE_URL = "http://192.168.1.100:8000"
```

---

## 📲 Building Android APK

### Option 1: Using Build Scripts

**Windows:**
```bash
cd scripts
build_apk.bat
```

**Linux/Mac:**
```bash
cd scripts
chmod +x build_apk.sh
./build_apk.sh
```

### Option 2: Manual Build

```bash
cd frontend

# Clean previous builds
buildozer android clean

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

The APK will be created in `frontend/bin/` directory.

### Install on Device

```bash
# Automatic deploy and run
buildozer android deploy run

# Or manually install:
adb install bin/qrattendance-1.0.0-arm64-v8a.apk
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/database.py` to change database:

```python
# SQLite (default - for development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./qr_attendance.db"

# MySQL (for production)
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/qr_attendance"
```

### Frontend Configuration

Edit `frontend/utils/api_client.py`:

```python
# Backend API URL
API_BASE_URL = "http://YOUR_SERVER_IP:8000"
```

---

## 📡 Network Setup

### Running on Local Network

1. **Find your computer's IP address:**
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`

2. **Update frontend API client:**
   ```python
   API_BASE_URL = "http://192.168.1.100:8000"
   ```

3. **Run backend with host:**
   ```bash
   # In backend directory
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Test from phone:**
   - Make sure phone and computer are on same WiFi
   - Open browser on phone, go to `http://YOUR_IP:8000`

---

## 🔐 Security Notes

### Default Credentials (Change in Production!)

| Role     | Username   | Password   |
|----------|------------|------------|
| Admin    | admin      | admin123   |
| Teacher  | teacher1   | teacher123 |
| Student  | student1   | student123 |

### Production Checklist

- [ ] Change all default passwords
- [ ] Use HTTPS for API
- [ ] Set up proper authentication (JWT)
- [ ] Migrate from SQLite to MySQL/PostgreSQL
- [ ] Add rate limiting
- [ ] Set up firewall rules
- [ ] Regular backups

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Module not found errors
```bash
# Solution: Make sure you're in the backend directory and venv is activated
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Problem:** Database locked
```bash
# Solution: Close any other processes using the database
# Restart the backend server
```

### Frontend Issues

**Problem:** Camera not working
```bash
# Solution: Camera requires Android. For desktop testing, use manual entry.
# On Android, make sure CAMERA permission is granted.
```

**Problem:** Cannot connect to backend
```bash
# Solution: Check:
# 1. Backend is running
# 2. Correct IP address in api_client.py
# 3. Firewall allows port 8000
# 4. Phone and computer on same network
```

### Build Issues

**Problem:** Buildozer fails
```bash
# Solution: Clean and rebuild
cd frontend
buildozer android clean
buildozer android debug
```

**Problem:** Java not found
```bash
# Solution: Install JDK 17 and set JAVA_HOME
# Windows: Set in System Environment Variables
# Linux: export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
```

---

## 📖 API Documentation

### Authentication

```bash
POST /login
Body: {"username": "student1", "password": "student123"}
```

### QR Scan

```bash
POST /scan
Body: {
    "student_id": "STU001",
    "latitude": 14.5995,
    "longitude": 120.9842
}
```

### Attendance

```bash
GET /attendance/today          # Get today's attendance
GET /attendance/student/{id}   # Get student attendance history
```

### Dashboard

```bash
GET /dashboard/summary         # Get summary statistics
```

Full API docs at: http://localhost:8000/docs

---

## 🔄 Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Test Frontend (Desktop):**
   ```bash
   cd frontend
   python main.py
   ```

3. **Build APK (When Ready):**
   ```bash
   cd scripts
   ./build_apk.sh  # or build_apk.bat
   ```

4. **Deploy:**
   ```bash
   # Copy APK to device or use:
   buildozer android deploy run
   ```

---

## 📝 Features Summary

### Student Features
- ✅ Clean login screen
- ✅ Big QR scan button
- ✅ Camera-based QR scanning
- ✅ Automatic GPS location
- ✅ Attendance success animation
- ✅ Manual SMS to parents
- ✅ Attendance history view

### Teacher Features
- ✅ Simple dashboard
- ✅ View today's attendance
- ✅ Search students
- ✅ Summary statistics

### Admin Features
- ✅ Add students
- ✅ Manage classes
- ✅ View all records
- ✅ System reports

### Technical Features
- ✅ FastAPI backend
- ✅ SQLite database
- ✅ KivyMD modern UI
- ✅ Android APK build
- ✅ GPS integration
- ✅ SMS intent
- ✅ QR scanning

---

## 🆘 Support

### Common Commands

```bash
# Backend
python main.py                  # Start server
python seed_data.py             # Reset database

# Frontend
cd frontend && python main.py   # Run desktop app

# Build
cd frontend && buildozer android debug    # Build APK
cd frontend && buildozer android clean    # Clean build
```

### Logs

```bash
# Backend logs
# Shown in terminal where you run python main.py

# Android logs
adb logcat -s python:D

# Buildozer logs
buildozer android debug 2>&1 | tee build.log
```

---

## 📄 License

This project is open source and available for educational use.

---

**Made with ❤️ for Students and Teachers**

*Simple, Fast, and User-Friendly*
