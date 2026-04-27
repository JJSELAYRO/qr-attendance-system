"""
QR Scanner Screen
Camera-based QR code scanning
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
import requests

try:
    from zbarcam import ZBarCam
    from kivy_garden.xcamera import XCamera
    HAS_CAMERA = True
except ImportError:
    HAS_CAMERA = False
    print("Warning: Camera not available. Install zbarcam for QR scanning.")

from utils.api_client import api_client
from utils.gps_helper import gps_helper


class QRScannerScreen(Screen):
    """QR code scanner screen with camera preview"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_result = None
        self.is_processing = False
        self.build_ui()
    
    def build_ui(self):
        """Build the QR scanner UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top App Bar
        app_bar = MDTopAppBar(
            title="Scan QR Code",
            elevation=4,
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ]
        )
        main_layout.add_widget(app_bar)
        
        if HAS_CAMERA:
            # Camera preview with QR scanner
            self.camera_layout = MDBoxLayout(orientation='vertical')
            
            # ZBarCam for QR code scanning
            self.zbar_cam = ZBarCam(
                id='camera',
                resolution=(640, 480),
                play=False  # Don't start immediately
            )
            self.zbar_cam.bind(symbols=self.on_qr_detected)
            self.camera_layout.add_widget(self.zbar_cam)
            
            # Overlay with scan area
            with self.camera_layout.canvas.after:
                Color(1, 1, 1, 0.3)
                # Scan area corners
                self.scan_lines = []
            
            main_layout.add_widget(self.camera_layout)
            
        else:
            # Fallback for development (no camera)
            fallback_layout = MDBoxLayout(
                orientation='vertical',
                padding=dp(30),
                spacing=dp(20)
            )
            
            # Info card
            info_card = MDCard(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(10),
                elevation=2
            )
            
            info_label = MDLabel(
                text="Camera not available in development mode.\nEnter Student ID manually:",
                halign='center',
                font_style='Body1'
            )
            info_card.add_widget(info_label)
            
            from kivymd.uix.textfield import MDTextField
            self.manual_input = MDTextField(
                hint_text="Enter Student ID (e.g., STU001)",
                mode="rectangle"
            )
            info_card.add_widget(self.manual_input)
            
            scan_button = MDRaisedButton(
                text="Simulate Scan",
                pos_hint={'center_x': 0.5},
                on_press=self.on_manual_scan
            )
            info_card.add_widget(scan_button)
            
            fallback_layout.add_widget(info_card)
            fallback_layout.add_widget(MDBoxLayout())
            
            main_layout.add_widget(fallback_layout)
        
        # Bottom controls
        bottom_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Status label
        self.status_label = MDLabel(
            text="Point camera at QR code",
            halign='center',
            font_style='Body1'
        )
        bottom_layout.add_widget(self.status_label)
        
        main_layout.add_widget(bottom_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Called when screen is entered"""
        # Start camera
        if HAS_CAMERA and hasattr(self, 'zbar_cam'):
            self.zbar_cam.play = True
            self.is_processing = False
            self.status_label.text = "Point camera at QR code"
        
        # Start GPS
        gps_helper.enable()
        
        # Reset scan result
        self.scan_result = None
    
    def on_leave(self):
        """Called when screen is left"""
        # Stop camera
        if HAS_CAMERA and hasattr(self, 'zbar_cam'):
            self.zbar_cam.play = False
        
        # Stop GPS
        gps_helper.disable()
    
    def on_qr_detected(self, instance, symbols):
        """Handle QR code detection"""
        if self.is_processing:
            return
        
        if symbols:
            # Get first detected symbol
            symbol = symbols[0]
            data = symbol.data.decode('utf-8')
            
            print(f"QR Code detected: {data}")
            
            # Process scan
            self.process_scan(data)
    
    def on_manual_scan(self, instance):
        """Handle manual scan button (for development)"""
        student_id = self.manual_input.text.strip()
        if student_id:
            self.process_scan(student_id)
    
    def process_scan(self, student_id: str):
        """Process the scanned QR code"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.status_label.text = "Processing..."
        
        # Get location
        latitude, longitude = gps_helper.get_location()
        
        # Call API
        def do_scan(dt):
            try:
                result = api_client.scan_qr(student_id, latitude, longitude)
                
                if result.get('success'):
                    # Navigate to success screen with data
                    success_screen = self.manager.get_screen('attendance_success')
                    success_screen.set_data(result)
                    self.manager.current = 'attendance_success'
                else:
                    # Show error
                    self.status_label.text = result.get('message', 'Scan failed')
                    self.is_processing = False
                    
            except Exception as e:
                self.status_label.text = f"Error: {str(e)}"
                self.is_processing = False
        
        Clock.schedule_once(do_scan, 0.1)
    
    def go_back(self):
        """Go back to home screen"""
        self.manager.current = 'student_home'
