"""
Pydantic Schemas for API requests and responses
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ============== USER SCHEMAS ==============

class UserBase(BaseModel):
    username: str
    role: str  # student, teacher, admin
    full_name: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None


# ============== STUDENT SCHEMAS ==============

class StudentBase(BaseModel):
    student_id: str
    full_name: str
    class_name: str
    parent_contact: str


class StudentCreate(StudentBase):
    user_id: int


class StudentResponse(StudentBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True


class StudentWithUser(StudentResponse):
    user: UserResponse
    
    class Config:
        from_attributes = True


# ============== ATTENDANCE SCHEMAS ==============

class AttendanceBase(BaseModel):
    student_id: int
    status: str = "PRESENT"


class AttendanceCreate(AttendanceBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AttendanceResponse(AttendanceBase):
    id: int
    date: str
    time: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceWithStudent(AttendanceResponse):
    student: StudentResponse
    
    class Config:
        from_attributes = True


# ============== QR SCAN SCHEMAS ==============

class QRScanRequest(BaseModel):
    student_id: str  # QR code contains student ID
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class QRScanResponse(BaseModel):
    success: bool
    message: str
    attendance: Optional[AttendanceResponse] = None
    student_name: Optional[str] = None
    parent_contact: Optional[str] = None
    sms_message: Optional[str] = None


# ============== DASHBOARD SCHEMAS ==============

class AttendanceSummary(BaseModel):
    total_students: int
    present_today: int
    absent_today: int
    late_today: int


class DailyAttendance(BaseModel):
    date: str
    records: List[AttendanceWithStudent]
