# QR Attendance System

A simple, modern, and user-friendly QR Code Attendance System built with Python.

![QR Attendance](assets/screenshots/placeholder.png)

## ✨ Features

### For Students
- **Simple UI**: Big QR scan button, clean design
- **Fast Scanning**: Camera-based QR code detection
- **GPS Tracking**: Automatic location capture
- **SMS Notification**: Manual SMS to parents via intent
- **History**: View attendance records

### For Teachers
- **Dashboard**: View daily attendance
- **Search**: Find students by name or ID
- **Statistics**: Present/absent summary

### For Admin
- **Student Management**: Add/edit students
- **Class Management**: Organize by classes
- **Reports**: View system statistics

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Python (Kivy + KivyMD) |
| Backend | FastAPI |
| Database | SQLite (upgradeable to MySQL) |
| Build | Buildozer (Android APK) |
| QR Scan | Camera + ZBar |
| GPS | Plyer GPS |
| SMS | Android SMS Intent |

## 🚀 Quick Start

### 1. Setup Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python seed_data.py
python main.py
```

Backend runs at: http://localhost:8000

### 2. Run Frontend (Desktop Test)

```bash
cd frontend
pip install -r ../requirements.txt
python main.py
```

### 3. Build Android APK

```bash
cd scripts
# Windows
build_apk.bat
# Linux/Mac
./build_apk.sh
```

Or manually:
```bash
cd frontend
buildozer android debug
```

## 📱 Screens

| Screen | Description |
|--------|-------------|
| Login | Clean login form |
| Student Home | Big QR scan button |
| QR Scanner | Camera preview with scan |
| Success | Attendance recorded + SMS |
| History | Past attendance records |
| Teacher Dashboard | Daily attendance table |
| Admin Panel | Student management |

## 🔐 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | teacher1 | teacher123 |
| Student | student1 | student123 |

## 📁 Project Structure

```
qr_attendance_system/
├── backend/           # FastAPI + SQLite
├── frontend/          # KivyMD Android App
├── scripts/           # Build + utility scripts
├── docs/              # Documentation
└── assets/            # Images and resources
```

## 📖 Documentation

- [Complete Setup Guide](docs/SETUP_GUIDE.md)
- API Docs: http://localhost:8000/docs (when backend running)

## 🔧 Configuration

### Backend URL

Edit `frontend/utils/api_client.py`:

```python
# For local testing
API_BASE_URL = "http://localhost:8000"

# For network testing
API_BASE_URL = "http://192.168.1.100:8000"
```

### Android Permissions

The following permissions are included in `buildozer.spec`:
- CAMERA
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION
- SEND_SMS
- INTERNET

## 📡 Network Setup

1. Find your computer's IP:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`

2. Update API_BASE_URL in frontend

3. Run backend with host:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. Ensure phone and computer are on same WiFi

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to backend | Check IP address and firewall |
| Camera not working | Check CAMERA permission |
| GPS not working | Check location permission, use real device |
| Build fails | Clean with `buildozer android clean` |
| SMS not opening | Check SEND_SMS permission |

## 📝 API Endpoints

```
POST   /login              # User login
POST   /register           # Register user (admin)
POST   /scan               # Process QR scan
POST   /attendance         # Record attendance
GET    /attendance/today   # Today's records
GET    /attendance/{id}    # Student records
GET    /students           # List students
POST   /students           # Add student
GET    /dashboard/summary  # Statistics
```

## 🎯 Flow

1. **Student** opens app
2. Clicks **"Scan QR Code"**
3. **QR Code** is scanned
4. **GPS** location captured
5. **Attendance** saved to database
6. **Success** screen shown
7. **SMS** app opens with message
8. Student **presses SEND** manually

## 🤝 Contributing

This is a student-friendly project. Contributions welcome!

## 📄 License

Open source for educational use.

---

**Made with ❤️ for Students and Teachers**

*Simple • Fast • User-Friendly*
