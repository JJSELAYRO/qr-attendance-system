"""
QR Attendance System - KivyMD Android App
Main application entry point
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.config import Config

# Window settings (for desktop testing)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.screen import MDScreen

from screens import (
    LoginScreen,
    StudentHomeScreen,
    QRScannerScreen,
    AttendanceSuccessScreen,
    AttendanceHistoryScreen,
    TeacherDashboardScreen,
    AdminPanelScreen
)


class QRAttendanceApp(MDApp):
    """
    Main QR Attendance Application
    
    A simple and modern attendance system with:
    - QR code scanning
    - GPS location tracking
    - Manual SMS notifications
    - Clean, student-friendly UI
    """
    
    def build(self):
        """Build the application"""
        # Configure theme
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Light'
        
        # Create screen manager
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Add all screens
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(StudentHomeScreen(name='student_home'))
        self.screen_manager.add_widget(QRScannerScreen(name='qr_scanner'))
        self.screen_manager.add_widget(AttendanceSuccessScreen(name='attendance_success'))
        self.screen_manager.add_widget(AttendanceHistoryScreen(name='attendance_history'))
        self.screen_manager.add_widget(TeacherDashboardScreen(name='teacher_dashboard'))
        self.screen_manager.add_widget(AdminPanelScreen(name='admin_panel'))
        
        # Start with login screen
        self.screen_manager.current = 'login'
        
        return self.screen_manager
    
    def on_start(self):
        """Called when app starts"""
        print("QR Attendance App Started")
        print("Version: 1.0.0")
        
        # Request Android permissions
        self.request_permissions()
    
    def request_permissions(self):
        """Request necessary Android permissions"""
        from kivy.utils import platform
        
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                
                permissions = [
                    Permission.CAMERA,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.SEND_SMS,
                    Permission.INTERNET
                ]
                
                request_permissions(permissions)
                print("Permissions requested")
                
            except Exception as e:
                print(f"Error requesting permissions: {e}")
    
    def on_pause(self):
        """Called when app is paused (backgrounded)"""
        return True
    
    def on_resume(self):
        """Called when app resumes from background"""
        pass


if __name__ == '__main__':
    QRAttendanceApp().run()
