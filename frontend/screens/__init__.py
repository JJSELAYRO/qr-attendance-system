"""
Screen modules for the QR Attendance App
"""

from .login_screen import LoginScreen
from .student_home import StudentHomeScreen
from .qr_scanner import QRScannerScreen
from .attendance_success import AttendanceSuccessScreen
from .attendance_history import AttendanceHistoryScreen
from .teacher_dashboard import TeacherDashboardScreen
from .admin_panel import AdminPanelScreen

__all__ = [
    'LoginScreen',
    'StudentHomeScreen',
    'QRScannerScreen',
    'AttendanceSuccessScreen',
    'AttendanceHistoryScreen',
    'TeacherDashboardScreen',
    'AdminPanelScreen'
]
