"""
QR Attendance System - FastAPI Backend
Main application file
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import models, schemas, crud, auth
from app.database import engine, get_db, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="QR Attendance System API",
    description="Simple and fast attendance system with QR scanning and GPS",
    version="1.0.0"
)

# CORS configuration for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== HEALTH CHECK ==============

@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "message": "QR Attendance System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ============== AUTHENTICATION ENDPOINTS ==============

@app.post("/login", response_model=schemas.LoginResponse)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """User login endpoint"""
    user = crud.authenticate_user(db, user_login.username, user_login.password)
    
    if not user:
        return schemas.LoginResponse(
            success=False,
            message="Invalid username or password"
        )
    
    token = auth.generate_token(user.username)
    
    return schemas.LoginResponse(
        success=True,
        message="Login successful",
        user=schemas.UserResponse.from_orm(user),
        token=token
    )


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user (for admin use)"""
    # Check if username already exists
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = crud.create_user(db, user)
    return new_user


# ============== STUDENT ENDPOINTS ==============

@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    # Check if student ID already exists
    existing = crud.get_student_by_id(db, student.student_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already exists"
        )
    
    new_student = crud.create_student(db, student)
    return new_student


@app.get("/students", response_model=List[schemas.StudentWithUser])
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all students"""
    students = crud.get_all_students(db, skip=skip, limit=limit)
    return students


@app.get("/students/{student_id}", response_model=schemas.StudentWithUser)
def get_student(student_id: str, db: Session = Depends(get_db)):
    """Get student by student ID"""
    student = crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@app.get("/students/search/{query}", response_model=List[schemas.StudentWithUser])
def search_students(query: str, db: Session = Depends(get_db)):
    """Search students by name or ID"""
    students = crud.search_students(db, query)
    return students


# ============== ATTENDANCE ENDPOINTS ==============

@app.post("/attendance", response_model=schemas.AttendanceResponse)
def create_attendance(
    attendance: schemas.AttendanceCreate, 
    db: Session = Depends(get_db)
):
    """Create a new attendance record"""
    # Check if student exists
    student = crud.get_student_by_id(db, str(attendance.student_id))
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if already checked in today
    if crud.check_already_checked_in(db, student.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already checked in today"
        )
    
    new_attendance = crud.create_attendance(
        db, 
        student_id=student.id,
        latitude=attendance.latitude,
        longitude=attendance.longitude
    )
    
    return new_attendance


@app.get("/attendance/student/{student_id}", response_model=List[schemas.AttendanceResponse])
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    """Get attendance records for a specific student"""
    attendances = crud.get_attendance_by_student(db, student_id)
    return attendances


@app.get("/attendance/today", response_model=List[schemas.AttendanceWithStudent])
def get_today_attendance(db: Session = Depends(get_db)):
    """Get all attendance records for today"""
    attendances = crud.get_today_attendance(db)
    return attendances


@app.get("/attendance/date/{date}", response_model=List[schemas.AttendanceWithStudent])
def get_attendance_by_date(date: str, db: Session = Depends(get_db)):
    """Get attendance records for a specific date (YYYY-MM-DD)"""
    attendances = crud.get_attendance_by_date(db, date)
    return attendances


# ============== QR SCANNING ENDPOINTS ==============

@app.post("/scan", response_model=schemas.QRScanResponse)
def scan_qr(scan_data: schemas.QRScanRequest, db: Session = Depends(get_db)):
    """Process QR code scan - Main attendance endpoint"""
    
    # Find student by student ID from QR code
    student = crud.get_student_by_id(db, scan_data.student_id)
    
    if not student:
        return schemas.QRScanResponse(
            success=False,
            message="Invalid QR code. Student not found."
        )
    
    # Check if already checked in today
    if crud.check_already_checked_in(db, student.id):
        return schemas.QRScanResponse(
            success=False,
            message="You have already checked in today!"
        )
    
    # Create attendance record
    attendance = crud.create_attendance(
        db,
        student_id=student.id,
        latitude=scan_data.latitude,
        longitude=scan_data.longitude
    )
    
    # Generate SMS message
    sms_message = auth.create_sms_message(
        student_name=student.full_name,
        time=attendance.time,
        latitude=attendance.latitude,
        longitude=attendance.longitude,
        status=attendance.status
    )
    
    return schemas.QRScanResponse(
        success=True,
        message="Attendance recorded successfully!",
        attendance=attendance,
        student_name=student.full_name,
        parent_contact=student.parent_contact,
        sms_message=sms_message
    )


# ============== DASHBOARD ENDPOINTS ==============

@app.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary statistics"""
    summary = crud.get_attendance_summary(db)
    return summary


@app.get("/dashboard/daily/{date}", response_model=schemas.DailyAttendance)
def get_daily_attendance(date: str, db: Session = Depends(get_db)):
    """Get daily attendance records with student info"""
    records = crud.get_attendance_by_date(db, date)
    return schemas.DailyAttendance(date=date, records=records)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
