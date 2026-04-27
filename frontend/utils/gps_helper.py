"""
GPS Helper
Handles device location services for Android
"""

from kivy.utils import platform
from typing import Callable, Optional

# Android platform detection
IS_ANDROID = platform == 'android'

if IS_ANDROID:
    from plyer import gps


class GPSHelper:
    """Helper class for GPS location services"""
    
    def __init__(self):
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.accuracy: Optional[float] = None
        self.is_enabled = False
        self.on_location_callback: Optional[Callable] = None
    
    def enable(self, on_location: Optional[Callable] = None) -> bool:
        """Enable GPS and start listening for location updates"""
        if not IS_ANDROID:
            print("GPS not available on non-Android platform")
            return False
        
        try:
            self.on_location_callback = on_location
            
            # Configure GPS
            gps.configure(
                on_location=self._on_location,
                on_status=self._on_status
            )
            
            # Start GPS
            gps.start(minTime=1000, minDistance=0)
            self.is_enabled = True
            return True
            
        except Exception as e:
            print(f"Error enabling GPS: {e}")
            return False
    
    def disable(self):
        """Disable GPS and stop listening"""
        if IS_ANDROID and self.is_enabled:
            try:
                gps.stop()
                self.is_enabled = False
            except Exception as e:
                print(f"Error disabling GPS: {e}")
    
    def _on_location(self, **kwargs):
        """Handle location update"""
        try:
            self.latitude = kwargs.get('lat')
            self.longitude = kwargs.get('lon')
            self.accuracy = kwargs.get('accuracy', 0)
            
            print(f"Location updated: {self.latitude}, {self.longitude} (accuracy: {self.accuracy}m)")
            
            # Call callback if set
            if self.on_location_callback:
                self.on_location_callback(self.latitude, self.longitude, self.accuracy)
                
        except Exception as e:
            print(f"Error processing location: {e}")
    
    def _on_status(self, stype, status):
        """Handle GPS status change"""
        print(f"GPS Status: {stype} - {status}")
    
    def get_location(self) -> tuple:
        """Get current location as (latitude, longitude)"""
        return (self.latitude, self.longitude)
    
    def has_location(self) -> bool:
        """Check if we have a valid location"""
        return self.latitude is not None and self.longitude is not None
    
    def get_location_string(self) -> str:
        """Get location as formatted string"""
        if self.has_location():
            return f"{self.latitude:.6f}, {self.longitude:.6f}"
        return "Location not available"


# Global GPS helper instance
gps_helper = GPSHelper()
