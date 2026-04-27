"""
Attendance History Screen
Shows student's attendance records in a simple list
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem
from kivy.metrics import dp
from kivy.clock import Clock

from utils.api_client import api_client


class AttendanceHistoryScreen(Screen):
    """Screen showing student's attendance history"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attendance_data = []
        self.build_ui()
    
    def build_ui(self):
        """Build the history UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top App Bar
        app_bar = MDTopAppBar(
            title="Attendance History",
            elevation=4,
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ]
        )
        main_layout.add_widget(app_bar)
        
        # Summary Card
        self.summary_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            elevation=2,
            padding=dp(15),
            spacing=dp(10)
        )
        
        summary_title = MDLabel(
            text="Attendance Summary",
            font_style='H6',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(30)
        )
        self.summary_card.add_widget(summary_title)
        
        self.summary_label = MDLabel(
            text="Loading...",
            font_style='Body1',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(40)
        )
        self.summary_card.add_widget(self.summary_label)
        
        main_layout.add_widget(self.summary_card)
        
        # History title
        history_title = MDLabel(
            text="Recent Records",
            font_style='H6',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40),
            padding=[dp(20), dp(10)]
        )
        main_layout.add_widget(history_title)
        
        # Scrollable list
        scroll_view = MDScrollView()
        
        self.history_list = MDList(
            padding=[dp(10), dp(5)]
        )
        scroll_view.add_widget(self.history_list)
        
        main_layout.add_widget(scroll_view)
        
        # Loading label
        self.loading_label = MDLabel(
            text="Loading attendance history...",
            halign='center',
            font_style='Body1',
            theme_text_color='Secondary'
        )
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_attendance_history()
    
    def load_attendance_history(self):
        """Load attendance history from API"""
        # Clear existing items
        self.history_list.clear_widgets()
        self.history_list.add_widget(self.loading_label)
        
        def fetch_data(dt):
            try:
                if api_client.current_user:
                    # Get student ID from current user
                    # For now, we'll need to get student info first
                    # This is a simplified version
                    
                    # In a real app, you'd have the student ID stored
                    # For demo, we'll show sample data
                    self.show_sample_data()
                else:
                    self.show_error("Not logged in")
                    
            except Exception as e:
                self.show_error(f"Error: {str(e)}")
        
        Clock.schedule_once(fetch_data, 0.1)
    
    def show_sample_data(self):
        """Show sample attendance data (for demo)"""
        self.history_list.clear_widgets()
        
        # Sample data
        sample_records = [
            {"date": "2026-04-27", "time": "08:30:15", "status": "PRESENT"},
            {"date": "2026-04-26", "time": "08:35:22", "status": "PRESENT"},
            {"date": "2026-04-25", "time": "08:28:45", "status": "PRESENT"},
            {"date": "2026-04-24", "time": "09:15:30", "status": "LATE"},
            {"date": "2026-04-23", "time": "08:32:10", "status": "PRESENT"},
            {"date": "2026-04-22", "time": "08:29:55", "status": "PRESENT"},
        ]
        
        # Update summary
        present_count = sum(1 for r in sample_records if r["status"] == "PRESENT")
        total_count = len(sample_records)
        
        self.summary_label.text = f"Total: {total_count} days | Present: {present_count} | Rate: {(present_count/total_count*100):.0f}%"
        
        # Add records to list
        for record in sample_records:
            # Color based on status
            if record["status"] == "PRESENT":
                icon_color = (0.2, 0.8, 0.2, 1)  # Green
                icon = "check-circle"
            elif record["status"] == "LATE":
                icon_color = (1, 0.6, 0.2, 1)  # Orange
                icon = "clock-alert"
            else:
                icon_color = (0.8, 0.2, 0.2, 1)  # Red
                icon = "close-circle"
            
            item = TwoLineAvatarIconListItem(
                text=f"{record['date']} - {record['status']}",
                secondary_text=f"Time: {record['time']}",
                theme_text_color='Custom',
                text_color=icon_color
            )
            
            # Add icon
            from kivymd.uix.list import IconLeftWidget
            item.add_widget(IconLeftWidget(icon=icon, theme_text_color='Custom', text_color=icon_color))
            
            self.history_list.add_widget(item)
    
    def show_error(self, message: str):
        """Show error message"""
        self.history_list.clear_widgets()
        
        error_label = MDLabel(
            text=message,
            halign='center',
            theme_text_color='Error'
        )
        self.history_list.add_widget(error_label)
    
    def go_back(self):
        """Go back to home screen"""
        self.manager.current = 'student_home'
