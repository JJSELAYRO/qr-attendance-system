"""
Authentication utilities
Simple password hashing and token generation
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(username: str) -> str:
    """Generate a simple token (not JWT for simplicity)"""
    timestamp = datetime.now().isoformat()
    random_string = secrets.token_hex(16)
    data = f"{username}:{timestamp}:{random_string}"
    return hashlib.sha256(data.encode()).hexdigest()


def create_sms_message(student_name: str, time: str, latitude: float, longitude: float, status: str) -> str:
    """Generate SMS message for parent notification"""
    location_text = f"{latitude:.6f}, {longitude:.6f}" if latitude and longitude else "Location not available"
    
    message = (
        f"{student_name} checked in at {time}.\n"
        f"Location: {location_text}\n"
        f"Status: {status}"
    )
    return message
