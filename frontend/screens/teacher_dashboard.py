"""
Teacher Dashboard Screen
Simple table view of attendance records
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.clock import Clock

from utils.api_client import api_client


class TeacherDashboardScreen(Screen):
    """Simple teacher dashboard with attendance records"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the teacher dashboard UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top App Bar
        app_bar = MDTopAppBar(
            title="Teacher Dashboard",
            elevation=4,
            right_action_items=[
                ["logout", lambda x: self.logout()]
            ]
        )
        main_layout.add_widget(app_bar)
        
        # Summary Cards
        summary_layout = MDGridLayout(
            cols=3,
            size_hint_y=None,
            height=dp(120),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Total Students Card
        self.total_card = self._create_summary_card("Total Students", "0", (0.2, 0.4, 0.8, 1))
        summary_layout.add_widget(self.total_card)
        
        # Present Today Card
        self.present_card = self._create_summary_card("Present Today", "0", (0.2, 0.7, 0.2, 1))
        summary_layout.add_widget(self.present_card)
        
        # Absent Today Card
        self.absent_card = self._create_summary_card("Absent Today", "0", (0.8, 0.3, 0.3, 1))
        summary_layout.add_widget(self.absent_card)
        
        main_layout.add_widget(summary_layout)
        
        # Search bar
        search_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(10)
        )
        
        self.search_field = MDTextField(
            hint_text="Search by name or student ID",
            mode="rectangle",
            size_hint_x=0.8
        )
        search_layout.add_widget(self.search_field)
        
        search_button = MDRaisedButton(
            text="Search",
            size_hint_x=0.2,
            on_press=self.on_search
        )
        search_layout.add_widget(search_button)
        
        main_layout.add_widget(search_layout)
        
        # Refresh button
        refresh_button = MDFlatButton(
            text="Refresh Data",
            pos_hint={'center_x': 0.5},
            on_press=self.load_data
        )
        main_layout.add_widget(refresh_button)
        
        # Data Table
        self.data_table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("No.", dp(30)),
                ("Student ID", dp(80)),
                ("Name", dp(120)),
                ("Class", dp(60)),
                ("Time", dp(60)),
                ("Status", dp(60)),
            ]
        )
        
        main_layout.add_widget(self.data_table)
        
        self.add_widget(main_layout)
    
    def _create_summary_card(self, title: str, value: str, color) -> MDCard:
        """Create a summary stat card"""
        card = MDCard(
            orientation='vertical',
            elevation=2,
            padding=dp(10),
            radius=[dp(10), dp(10), dp(10), dp(10)]
        )
        
        title_label = MDLabel(
            text=title,
            halign='center',
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(title_label)
        
        value_label = MDLabel(
            text=value,
            halign='center',
            font_style='H4',
            theme_text_color='Custom',
            text_color=color,
            size_hint_y=None,
            height=dp(50)
        )
        card.value_label = value_label  # Store reference
        card.add_widget(value_label)
        
        return card
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_data()
    
    def load_data(self, instance=None):
        """Load dashboard data"""
        Clock.schedule_once(self._fetch_data, 0.1)
    
    def _fetch_data(self, dt):
        """Fetch data from API"""
        try:
            # For demo, show sample data
            self.show_sample_data()
            
            # In real app:
            # summary = api_client.get_dashboard_summary()
            # today_attendance = api_client.get_today_attendance()
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def show_sample_data(self):
        """Show sample data for demo"""
        # Update summary cards
        self.total_card.value_label.text = "25"
        self.present_card.value_label.text = "22"
        self.absent_card.value_label.text = "3"
        
        # Sample attendance records
        sample_data = [
            ("1", "STU001", "Alice Johnson", "10-A", "08:30", "PRESENT"),
            ("2", "STU002", "Bob Williams", "10-A", "08:32", "PRESENT"),
            ("3", "STU003", "Carol Davis", "10-B", "08:28", "PRESENT"),
            ("4", "STU004", "David Brown", "10-B", "08:35", "PRESENT"),
            ("5", "STU005", "Emma Wilson", "11-A", "08:31", "PRESENT"),
            ("6", "STU006", "Frank Miller", "11-A", "09:15", "LATE"),
            ("7", "STU007", "Grace Lee", "11-B", "08:29", "PRESENT"),
            ("8", "STU008", "Henry Clark", "11-B", "-", "ABSENT"),
        ]
        
        # Update table
        self.data_table.row_data = sample_data
    
    def on_search(self, instance):
        """Handle search"""
        query = self.search_field.text.strip()
        if query:
            print(f"Searching for: {query}")
            # In real app: filter data based on query
    
    def logout(self):
        """Logout and return to login screen"""
        api_client.token = None
        api_client.current_user = None
        self.manager.current = 'login'
