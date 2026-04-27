"""
API Client
Handles all communication with the FastAPI backend
"""

import requests
import json
from typing import Optional, Dict, Any

# Backend API URL
# Change this to your backend server address
API_BASE_URL = "http://192.168.1.100:8000"  # Update with your server IP


class APIClient:
    """Simple API client for backend communication"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.current_user: Optional[Dict] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token if available"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            else:
                return {
                    "success": False,
                    "message": f"Error {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user"""
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"username": username, "password": password},
                headers=self._get_headers(),
                timeout=10
            )
            data = self._handle_response(response)
            
            if data.get("success"):
                self.token = data.get("token")
                self.current_user = data.get("user")
            
            return data
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def scan_qr(self, student_id: str, latitude: Optional[float] = None, 
                longitude: Optional[float] = None) -> Dict[str, Any]:
        """Send QR scan data to backend"""
        try:
            data = {
                "student_id": student_id,
                "latitude": latitude,
                "longitude": longitude
            }
            
            response = requests.post(
                f"{self.base_url}/scan",
                json=data,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def get_student_attendance(self, student_id: int) -> Dict[str, Any]:
        """Get attendance history for a student"""
        try:
            response = requests.get(
                f"{self.base_url}/attendance/student/{student_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def get_today_attendance(self) -> Dict[str, Any]:
        """Get today's attendance (for teachers)"""
        try:
            response = requests.get(
                f"{self.base_url}/attendance/today",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary"""
        try:
            response = requests.get(
                f"{self.base_url}/dashboard/summary",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def get_all_students(self) -> Dict[str, Any]:
        """Get all students (for admin)"""
        try:
            response = requests.get(
                f"{self.base_url}/students",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}
    
    def create_student(self, student_data: Dict) -> Dict[str, Any]:
        """Create a new student (for admin)"""
        try:
            response = requests.post(
                f"{self.base_url}/students",
                json=student_data,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "message": f"Connection error: {str(e)}"}


# Global API client instance
api_client = APIClient()
