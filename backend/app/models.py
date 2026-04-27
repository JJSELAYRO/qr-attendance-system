"""
Database Models
Simple structure for students, attendance, and users
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """User accounts for students, teachers, and admin"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Hashed password
    role = Column(String)  # student, teacher, admin
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class Student(Base):
    """Student information"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(String, unique=True, index=True)  # Student ID number
    full_name = Column(String)
    class_name = Column(String)  # Class/Grade
    parent_contact = Column(String)  # Parent phone number for SMS
    
    # Relationship
    user = relationship("User", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")


class Attendance(Base):
    """Attendance records with GPS location"""
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(String)  # YYYY-MM-DD format
    time = Column(String)  # HH:MM:SS format
    status = Column(String, default="PRESENT")  # PRESENT, ABSENT, LATE
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship
    student = relationship("Student", back_populates="attendances")


# Set up relationships
User.student = relationship("Student", back_populates="user", uselist=False)
