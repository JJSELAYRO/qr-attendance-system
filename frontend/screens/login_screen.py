"""
Login Screen
Clean and simple login form
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from utils.api_client import api_client


class LoginScreen(Screen):
    """Clean and simple login screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the login UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            md_bg_color=self.theme_cls.bg_normal
        )
        
        # Spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        # Logo/Title Card
        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(320), dp(420)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=4,
            padding=dp(25),
            spacing=dp(15),
            radius=[dp(20), dp(20), dp(20), dp(20)]
        )
        
        # App Logo/Title
        title_label = MDLabel(
            text="QR Attendance",
            halign='center',
            font_style='H4',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(50)
        )
        card.add_widget(title_label)
        
        # Subtitle
        subtitle = MDLabel(
            text="Smart Attendance System",
            halign='center',
            font_style='Subtitle1',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(subtitle)
        
        # Spacer
        card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))
        
        # Username field
        self.username_field = MDTextField(
            hint_text="Username",
            icon_right="account",
            mode="round",
            size_hint_y=None,
            height=dp(50)
        )
        card.add_widget(self.username_field)
        
        # Password field
        self.password_field = MDTextField(
            hint_text="Password",
            icon_right="lock",
            password=True,
            mode="round",
            size_hint_y=None,
            height=dp(50)
        )
        card.add_widget(self.password_field)
        
        # Spacer
        card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))
        
        # Progress bar (hidden by default)
        self.progress_bar = MDProgressBar(
            size_hint_y=None,
            height=dp(4),
            opacity=0
        )
        card.add_widget(self.progress_bar)
        
        # Error label (hidden by default)
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30),
            opacity=0
        )
        card.add_widget(self.error_label)
        
        # Login button
        self.login_button = MDRaisedButton(
            text="LOGIN",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.primary_color,
            font_style='Button'
        )
        self.login_button.bind(on_press=self.on_login)
        card.add_widget(self.login_button)
        
        # Add card to main layout
        main_layout.add_widget(card)
        
        # Bottom spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        self.add_widget(main_layout)
    
    def on_login(self, instance):
        """Handle login button press"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter username and password")
            return
        
        # Show loading
        self.show_loading(True)
        self.error_label.opacity = 0
        
        # Perform login (in real app, this would be async)
        Clock.schedule_once(lambda dt: self.perform_login(username, password), 0.1)
    
    def perform_login(self, username: str, password: str):
        """Perform login API call"""
        try:
            result = api_client.login(username, password)
            
            if result.get('success'):
                # Login successful
                user = result.get('user', {})
                role = user.get('role', 'student')
                
                self.show_loading(False)
                
                # Navigate based on role
                if role == 'student':
                    self.manager.current = 'student_home'
                elif role == 'teacher':
                    self.manager.current = 'teacher_dashboard'
                elif role == 'admin':
                    self.manager.current = 'admin_panel'
                else:
                    self.manager.current = 'student_home'
                    
                # Clear fields
                self.username_field.text = ""
                self.password_field.text = ""
            else:
                # Login failed
                self.show_loading(False)
                self.show_error(result.get('message', 'Login failed'))
                
        except Exception as e:
            self.show_loading(False)
            self.show_error(f"Error: {str(e)}")
    
    def show_loading(self, show: bool):
        """Show or hide loading indicator"""
        self.progress_bar.opacity = 1 if show else 0
        self.login_button.disabled = show
        
        if show:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
    
    def show_error(self, message: str):
        """Show error message"""
        self.error_label.text = message
        self.error_label.opacity = 1
