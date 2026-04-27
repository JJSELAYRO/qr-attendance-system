"""
SMS Helper
Opens SMS app with pre-filled message using Android Intent
"""

from kivy.utils import platform
from urllib.parse import quote

# Android platform detection
IS_ANDROID = platform == 'android'

if IS_ANDROID:
    from jnius import autoclass
    import android
    
    # Android classes
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')


class SMSHelper:
    """Helper class for sending SMS via Android Intent"""
    
    @staticmethod
    def send_sms(phone_number: str, message: str) -> bool:
        """
        Open SMS app with pre-filled message
        User must manually press SEND
        
        Format: sms:{phone_number}?body={message}
        """
        if not IS_ANDROID:
            print(f"SMS Intent would open with:\nTo: {phone_number}\nMessage: {message}")
            return True
        
        try:
            # Encode the message for URL
            encoded_message = quote(message)
            
            # Create SMS URI
            sms_uri = Uri.parse(f"sms:{phone_number}?body={encoded_message}")
            
            # Create intent
            intent = Intent(Intent.ACTION_VIEW, sms_uri)
            
            # Add flag to start new task
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            
            # Start activity
            current_activity = PythonActivity.mActivity
            current_activity.startActivity(intent)
            
            print(f"SMS app opened with message to {phone_number}")
            return True
            
        except Exception as e:
            print(f"Error opening SMS app: {e}")
            return False
    
    @staticmethod
    def create_attendance_sms(student_name: str, time: str, 
                              latitude: float, longitude: float,
                              status: str = "PRESENT") -> tuple:
        """
        Create SMS message for attendance notification
        Returns (phone_number placeholder, message)
        """
        location_text = f"{latitude:.6f}, {longitude:.6f}" if latitude and longitude else "Location not available"
        
        message = (
            f"{student_name} checked in at {time}.\n"
            f"Location: {location_text}\n"
            f"Status: {status}"
        )
        
        return message


# Global SMS helper instance
sms_helper = SMSHelper()
