"""
Admin Panel Screen
Basic CRUD UI for managing students and classes
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.metrics import dp
from kivy.clock import Clock

from utils.api_client import api_client


class TabBase(MDFloatLayout, MDTabsBase):
    """Base class for tabs"""
    pass


class AdminPanelScreen(Screen):
    """Admin panel with CRUD operations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the admin panel UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top App Bar
        app_bar = MDTopAppBar(
            title="Admin Panel",
            elevation=4,
            right_action_items=[
                ["logout", lambda x: self.logout()]
            ]
        )
        main_layout.add_widget(app_bar)
        
        # Tabs
        self.tabs = MDTabs()
        
        # Students Tab
        students_tab = TabBase(title="Students")
        students_tab.add_widget(self._build_students_tab())
        self.tabs.add_widget(students_tab)
        
        # Add Student Tab
        add_tab = TabBase(title="Add Student")
        add_tab.add_widget(self._build_add_student_tab())
        self.tabs.add_widget(add_tab)
        
        # Reports Tab
        reports_tab = TabBase(title="Reports")
        reports_tab.add_widget(self._build_reports_tab())
        self.tabs.add_widget(reports_tab)
        
        main_layout.add_widget(self.tabs)
        
        self.add_widget(main_layout)
    
    def _build_students_tab(self):
        """Build the students list tab"""
        layout = MDBoxLayout(orientation='vertical')
        
        # Search bar
        search_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(10)
        )
        
        self.search_field = MDTextField(
            hint_text="Search students...",
            mode="rectangle",
            size_hint_x=0.7
        )
        search_layout.add_widget(self.search_field)
        
        search_button = MDRaisedButton(
            text="Search",
            size_hint_x=0.3,
            on_press=self.on_search_students
        )
        search_layout.add_widget(search_button)
        
        layout.add_widget(search_layout)
        
        # Refresh button
        refresh_btn = MDFlatButton(
            text="Refresh List",
            pos_hint={'center_x': 0.5},
            on_press=self.load_students
        )
        layout.add_widget(refresh_btn)
        
        # Students list
        scroll = MDScrollView()
        self.students_list = MDList(padding=dp(10))
        scroll.add_widget(self.students_list)
        layout.add_widget(scroll)
        
        return layout
    
    def _build_add_student_tab(self):
        """Build the add student form tab"""
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Form card
        form_card = MDCard(
            orientation='vertical',
            elevation=2,
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Title
        title = MDLabel(
            text="Add New Student",
            font_style='H5',
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        form_card.add_widget(title)
        
        # Form fields
        self.new_username = MDTextField(
            hint_text="Username",
            mode="rectangle",
            icon_right="account"
        )
        form_card.add_widget(self.new_username)
        
        self.new_password = MDTextField(
            hint_text="Password",
            mode="rectangle",
            password=True,
            icon_right="lock"
        )
        form_card.add_widget(self.new_password)
        
        self.new_student_id = MDTextField(
            hint_text="Student ID",
            mode="rectangle",
            icon_right="card-account-details"
        )
        form_card.add_widget(self.new_student_id)
        
        self.new_full_name = MDTextField(
            hint_text="Full Name",
            mode="rectangle",
            icon_right="account-circle"
        )
        form_card.add_widget(self.new_full_name)
        
        self.new_class = MDTextField(
            hint_text="Class (e.g., Grade 10-A)",
            mode="rectangle",
            icon_right="school"
        )
        form_card.add_widget(self.new_class)
        
        self.new_parent_contact = MDTextField(
            hint_text="Parent Phone Number",
            mode="rectangle",
            icon_right="phone"
        )
        form_card.add_widget(self.new_parent_contact)
        
        # Submit button
        submit_btn = MDRaisedButton(
            text="ADD STUDENT",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            on_press=self.on_add_student
        )
        form_card.add_widget(submit_btn)
        
        # Status label
        self.add_status_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        form_card.add_widget(self.add_status_label)
        
        layout.add_widget(form_card)
        layout.add_widget(MDBoxLayout())  # Spacer
        
        return layout
    
    def _build_reports_tab(self):
        """Build the reports tab"""
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Summary card
        summary_card = MDCard(
            orientation='vertical',
            elevation=2,
            padding=dp(20),
            spacing=dp(15)
        )
        
        title = MDLabel(
            text="System Summary",
            font_style='H5',
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        summary_card.add_widget(title)
        
        # Stats
        self.total_students_label = MDLabel(
            text="Total Students: 0",
            font_style='H6',
            size_hint_y=None,
            height=dp(35)
        )
        summary_card.add_widget(self.total_students_label)
        
        self.total_teachers_label = MDLabel(
            text="Total Teachers: 0",
            font_style='H6',
            size_hint_y=None,
            height=dp(35)
        )
        summary_card.add_widget(self.total_teachers_label)
        
        self.today_attendance_label = MDLabel(
            text="Today's Attendance: 0",
            font_style='H6',
            size_hint_y=None,
            height=dp(35)
        )
        summary_card.add_widget(self.today_attendance_label)
        
        # Refresh button
        refresh_btn = MDRaisedButton(
            text="REFRESH STATS",
            pos_hint={'center_x': 0.5},
            on_press=self.load_stats
        )
        summary_card.add_widget(refresh_btn)
        
        layout.add_widget(summary_card)
        layout.add_widget(MDBoxLayout())  # Spacer
        
        return layout
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_students()
        self.load_stats()
    
    def load_students(self, instance=None):
        """Load students list"""
        self.students_list.clear_widgets()
        
        # Show loading
        loading = MDLabel(
            text="Loading students...",
            halign='center'
        )
        self.students_list.add_widget(loading)
        
        Clock.schedule_once(self._fetch_students, 0.1)
    
    def _fetch_students(self, dt):
        """Fetch students from API"""
        self.students_list.clear_widgets()
        
        # Sample data for demo
        sample_students = [
            {"student_id": "STU001", "full_name": "Alice Johnson", "class_name": "Grade 10-A"},
            {"student_id": "STU002", "full_name": "Bob Williams", "class_name": "Grade 10-A"},
            {"student_id": "STU003", "full_name": "Carol Davis", "class_name": "Grade 10-B"},
            {"student_id": "STU004", "full_name": "David Brown", "class_name": "Grade 10-B"},
            {"student_id": "STU005", "full_name": "Emma Wilson", "class_name": "Grade 11-A"},
        ]
        
        for student in sample_students:
            item = TwoLineAvatarIconListItem(
                text=student["full_name"],
                secondary_text=f"ID: {student['student_id']} | Class: {student['class_name']}"
            )
            self.students_list.add_widget(item)
    
    def on_search_students(self, instance):
        """Handle student search"""
        query = self.search_field.text.strip()
        print(f"Searching students: {query}")
    
    def on_add_student(self, instance):
        """Handle add student form submission"""
        # Validate inputs
        username = self.new_username.text.strip()
        password = self.new_password.text.strip()
        student_id = self.new_student_id.text.strip()
        full_name = self.new_full_name.text.strip()
        class_name = self.new_class.text.strip()
        parent_contact = self.new_parent_contact.text.strip()
        
        if not all([username, password, student_id, full_name, class_name, parent_contact]):
            self.add_status_label.text = "Please fill all fields"
            self.add_status_label.theme_text_color = 'Error'
            return
        
        # In real app: send to API
        self.add_status_label.text = "Student added successfully!"
        self.add_status_label.theme_text_color = 'Custom'
        self.add_status_label.text_color = (0.2, 0.7, 0.2, 1)
        
        # Clear form
        self.new_username.text = ""
        self.new_password.text = ""
        self.new_student_id.text = ""
        self.new_full_name.text = ""
        self.new_class.text = ""
        self.new_parent_contact.text = ""
        
        # Refresh list
        self.load_students()
    
    def load_stats(self, instance=None):
        """Load system statistics"""
        # In real app: fetch from API
        self.total_students_label.text = "Total Students: 25"
        self.total_teachers_label.text = "Total Teachers: 5"
        self.today_attendance_label.text = "Today's Attendance: 22/25"
    
    def logout(self):
        """Logout and return to login screen"""
        api_client.token = None
        api_client.current_user = None
        self.manager.current = 'login'
