"""
Student Home Screen
Main screen for students with big QR scan button
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation

from utils.api_client import api_client


class StudentHomeScreen(Screen):
    """Student home screen with big QR scan button"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the student home UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=self.theme_cls.bg_normal
        )
        
        # Top App Bar
        app_bar = MDTopAppBar(
            title="Student Home",
            elevation=4,
            right_action_items=[
                ["account-circle", lambda x: self.on_profile()]
            ]
        )
        main_layout.add_widget(app_bar)
        
        # Welcome section
        welcome_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(120),
            elevation=2,
            padding=dp(20),
            radius=[0, 0, dp(20), dp(20)]
        )
        
        self.welcome_label = MDLabel(
            text="Welcome, Student!",
            font_style='H5',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40)
        )
        welcome_card.add_widget(self.welcome_label)
        
        self.date_label = MDLabel(
            text="Ready to check in",
            font_style='Body1',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        welcome_card.add_widget(self.date_label)
        
        main_layout.add_widget(welcome_card)
        
        # Center content
        center_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )
        
        # Spacer
        center_layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        # Big QR Scan Button Container
        scan_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(250), dp(250)),
            pos_hint={'center_x': 0.5}
        )
        
        # Animated background circle
        with scan_container.canvas.before:
            Color(0.2, 0.6, 1, 0.1)  # Light blue
            self.bg_circle = Ellipse(
                pos=(scan_container.center_x - dp(125), scan_container.center_y - dp(125)),
                size=(dp(250), dp(250))
            )
        
        # Bind to update circle position
        scan_container.bind(pos=self.update_circle, size=self.update_circle)
        
        # Big floating action button
        self.scan_button = MDFloatingActionButton(
            icon="qrcode-scan",
            size=(dp(200), dp(200)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=8,
            md_bg_color=self.theme_cls.primary_color
        )
        self.scan_button.bind(on_press=self.on_scan_press)
        scan_container.add_widget(self.scan_button)
        
        center_layout.add_widget(scan_container)
        
        # Scan label
        scan_label = MDLabel(
            text="Tap to Scan QR Code",
            halign='center',
            font_style='H6',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40)
        )
        center_layout.add_widget(scan_label)
        
        # Spacer
        center_layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        # History button
        history_button = MDRaisedButton(
            text="View Attendance History",
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.accent_color,
            icon="history"
        )
        history_button.bind(on_press=self.on_history)
        center_layout.add_widget(history_button)
        
        # Spacer
        center_layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        main_layout.add_widget(center_layout)
        
        self.add_widget(main_layout)
    
    def update_circle(self, instance, value):
        """Update background circle position"""
        if hasattr(self, 'bg_circle'):
            self.bg_circle.pos = (
                instance.x + dp(0),
                instance.y + dp(0)
            )
            self.bg_circle.size = instance.size
    
    def on_enter(self):
        """Called when screen is entered"""
        # Update welcome message with user name
        if api_client.current_user:
            name = api_client.current_user.get('full_name', 'Student')
            self.welcome_label.text = f"Welcome, {name}!"
        
        # Animate scan button
        anim = Animation(scale=1.1, duration=0.5) + Animation(scale=1.0, duration=0.5)
        anim.repeat = True
        anim.start(self.scan_button)
    
    def on_scan_press(self, instance):
        """Handle scan button press"""
        # Navigate to QR scanner screen
        self.manager.current = 'qr_scanner'
    
    def on_history(self, instance):
        """Handle history button press"""
        self.manager.current = 'attendance_history'
    
    def on_profile(self):
        """Handle profile icon press"""
        # Could show a menu with logout option
        # For now, just logout
        api_client.token = None
        api_client.current_user = None
        self.manager.current = 'login'
