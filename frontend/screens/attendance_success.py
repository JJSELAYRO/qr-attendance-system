"""
Attendance Success Screen
Shows success animation and opens SMS app
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, ObjectProperty

from utils.sms_helper import sms_helper


class AttendanceSuccessScreen(Screen):
    """Screen shown after successful attendance recording"""
    
    # Properties for dynamic data
    student_name = StringProperty("")
    time_text = StringProperty("")
    location_text = StringProperty("")
    status_text = StringProperty("")
    sms_message = StringProperty("")
    parent_contact = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_data = None
        self.build_ui()
    
    def build_ui(self):
        """Build the success UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20),
            md_bg_color=self.theme_cls.bg_normal
        )
        
        # Spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        # Success Card
        self.success_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(400),
            elevation=4,
            padding=dp(25),
            spacing=dp(15),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            md_bg_color=(0.9, 1, 0.9, 1)  # Light green
        )
        
        # Success Icon (using label with large text)
        self.success_icon = MDLabel(
            text="✓",
            halign='center',
            font_style='H2',
            theme_text_color='Custom',
            text_color=(0.2, 0.8, 0.2, 1),  # Green
            size_hint_y=None,
            height=dp(60)
        )
        self.success_card.add_widget(self.success_icon)
        
        # Success title
        self.title_label = MDLabel(
            text="Attendance Recorded!",
            halign='center',
            font_style='H5',
            theme_text_color='Custom',
            text_color=(0.2, 0.6, 0.2, 1),  # Dark green
            size_hint_y=None,
            height=dp(40)
        )
        self.success_card.add_widget(self.title_label)
        
        # Student name
        self.name_label = MDLabel(
            text="",
            halign='center',
            font_style='H6',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(35)
        )
        self.success_card.add_widget(self.name_label)
        
        # Time
        self.time_label = MDLabel(
            text="",
            halign='center',
            font_style='Body1',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        self.success_card.add_widget(self.time_label)
        
        # Location chip
        location_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(50), 0]
        )
        
        self.location_chip = MDChip(
            label="Location: Getting...",
            icon="map-marker",
            pos_hint={'center_x': 0.5},
            size_hint_x=None
        )
        location_layout.add_widget(self.location_chip)
        self.success_card.add_widget(location_layout)
        
        # Status chip
        status_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(50), 0]
        )
        
        self.status_chip = MDChip(
            label="PRESENT",
            icon="check-circle",
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.2, 0.8, 0.2, 1),  # Green
            text_color=(1, 1, 1, 1),
            size_hint_x=None
        )
        status_layout.add_widget(self.status_chip)
        self.success_card.add_widget(status_layout)
        
        main_layout.add_widget(self.success_card)
        
        # Spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        # SMS Button (Big and prominent)
        self.sms_button = MDRaisedButton(
            text="SEND SMS TO PARENT",
            size_hint=(None, None),
            size=(dp(300), dp(60)),
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.2, 0.5, 0.9, 1),  # Blue
            font_style='H6',
            icon="message-text"
        )
        self.sms_button.bind(on_press=self.on_send_sms)
        main_layout.add_widget(self.sms_button)
        
        # SMS note
        sms_note = MDLabel(
            text="SMS app will open. Please press SEND manually.",
            halign='center',
            font_style='Caption',
            theme_text_color='Hint',
            size_hint_y=None,
            height=dp(25)
        )
        main_layout.add_widget(sms_note)
        
        # Spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        # Done button
        done_button = MDFlatButton(
            text="DONE",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5},
            font_style='Button'
        )
        done_button.bind(on_press=self.on_done)
        main_layout.add_widget(done_button)
        
        # Bottom spacer
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        self.add_widget(main_layout)
    
    def set_data(self, data: dict):
        """Set the scan result data"""
        self.scan_data = data
        
        # Extract data
        attendance = data.get('attendance', {})
        
        self.student_name = data.get('student_name', 'Student')
        self.time_text = f"Time: {attendance.get('time', 'Unknown')}"
        
        lat = attendance.get('latitude')
        lon = attendance.get('longitude')
        if lat and lon:
            self.location_text = f"{lat:.6f}, {lon:.6f}"
        else:
            self.location_text = "Location not available"
        
        self.status_text = attendance.get('status', 'PRESENT')
        self.sms_message = data.get('sms_message', '')
        self.parent_contact = data.get('parent_contact', '')
    
    def on_enter(self):
        """Called when screen is entered"""
        # Update UI with data
        self.name_label.text = self.student_name
        self.time_label.text = self.time_text
        self.location_chip.label = f"Location: {self.location_text}"
        self.status_chip.label = self.status_text
        
        # Animate success icon
        anim = Animation(scale=1.2, duration=0.3) + Animation(scale=1.0, duration=0.3)
        anim.start(self.success_icon)
        
        # Animate card
        anim2 = Animation(opacity=0.5, duration=0.2) + Animation(opacity=1, duration=0.5)
        anim2.start(self.success_card)
    
    def on_send_sms(self, instance):
        """Handle SMS button press"""
        if self.parent_contact and self.sms_message:
            # Open SMS app with pre-filled message
            success = sms_helper.send_sms(self.parent_contact, self.sms_message)
            
            if success:
                # Show confirmation
                self.sms_button.text = "SMS App Opened"
                self.sms_button.md_bg_color = (0.4, 0.7, 0.4, 1)  # Light green
            else:
                self.sms_button.text = "Could not open SMS"
                self.sms_button.md_bg_color = (0.8, 0.4, 0.4, 1)  # Red
    
    def on_done(self, instance):
        """Handle done button - return to home"""
        # Reset SMS button
        self.sms_button.text = "SEND SMS TO PARENT"
        self.sms_button.md_bg_color = (0.2, 0.5, 0.9, 1)
        
        # Go back to home
        self.manager.current = 'student_home'
