"""
CRUD Operations
Database helper functions
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, auth
from datetime import datetime
from typing import Optional, List


# ============== USER CRUD ==============

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = auth.hash_password(user.password)
    
    db_user = models.User(
        username=user.username,
        password=hashed_password,
        role=user.role,
        full_name=user.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if user and auth.verify_password(password, user.password):
        return user
    return None


# ============== STUDENT CRUD ==============

def get_student_by_id(db: Session, student_id: str) -> Optional[models.Student]:
    """Get student by student ID number"""
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()


def get_student_by_user_id(db: Session, user_id: int) -> Optional[models.Student]:
    """Get student by user ID"""
    return db.query(models.Student).filter(models.Student.user_id == user_id).first()


def get_all_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    """Get all students"""
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    """Create a new student"""
    db_student = models.Student(
        user_id=student.user_id,
        student_id=student.student_id,
        full_name=student.full_name,
        class_name=student.class_name,
        parent_contact=student.parent_contact
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def search_students(db: Session, query: str) -> List[models.Student]:
    """Search students by name or student ID"""
    return db.query(models.Student).filter(
        models.Student.full_name.contains(query) | 
        models.Student.student_id.contains(query)
    ).all()


# ============== ATTENDANCE CRUD ==============

def get_attendance_by_id(db: Session, attendance_id: int) -> Optional[models.Attendance]:
    """Get attendance by ID"""
    return db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()


def get_attendance_by_student(db: Session, student_id: int, date: Optional[str] = None) -> List[models.Attendance]:
    """Get attendance records for a student"""
    query = db.query(models.Attendance).filter(models.Attendance.student_id == student_id)
    
    if date:
        query = query.filter(models.Attendance.date == date)
    
    return query.order_by(models.Attendance.created_at.desc()).all()


def get_attendance_by_date(db: Session, date: str) -> List[models.Attendance]:
    """Get all attendance records for a specific date"""
    return db.query(models.Attendance).filter(
        models.Attendance.date == date
    ).order_by(models.Attendance.time.desc()).all()


def get_today_attendance(db: Session) -> List[models.Attendance]:
    """Get all attendance records for today"""
    today = datetime.now().strftime("%Y-%m-%d")
    return get_attendance_by_date(db, today)


def create_attendance(db: Session, student_id: int, latitude: Optional[float] = None, 
                     longitude: Optional[float] = None) -> models.Attendance:
    """Create a new attendance record"""
    now = datetime.now()
    
    db_attendance = models.Attendance(
        student_id=student_id,
        date=now.strftime("%Y-%m-%d"),
        time=now.strftime("%H:%M:%S"),
        status="PRESENT",
        latitude=latitude,
        longitude=longitude
    )
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def check_already_checked_in(db: Session, student_id: int) -> bool:
    """Check if student already checked in today"""
    today = datetime.now().strftime("%Y-%m-%d")
    existing = db.query(models.Attendance).filter(
        and_(
            models.Attendance.student_id == student_id,
            models.Attendance.date == today
        )
    ).first()
    return existing is not None


# ============== DASHBOARD ==============

def get_attendance_summary(db: Session) -> dict:
    """Get attendance summary for today"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    total_students = db.query(models.Student).count()
    today_attendance = get_attendance_by_date(db, today)
    
    present = sum(1 for a in today_attendance if a.status == "PRESENT")
    absent = sum(1 for a in today_attendance if a.status == "ABSENT")
    late = sum(1 for a in today_attendance if a.status == "LATE")
    
    # Calculate actual absent (students who haven't checked in)
    not_checked_in = total_students - len(today_attendance)
    absent += not_checked_in
    
    return {
        "total_students": total_students,
        "present_today": present,
        "absent_today": absent,
        "late_today": late
    }
