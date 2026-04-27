"""
Google Drive Upload Script
Optional: Upload APK file to Google Drive after building

SETUP:
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable Google Drive API
4. Create credentials (OAuth 2.0 Client ID)
5. Download client_secret.json and save it in this folder
6. Run this script once to authenticate (opens browser)
7. Token will be saved for future runs

USAGE:
    python upload_to_drive.py path/to/your/app.apk
"""

import os
import sys
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'client_secret.json')


def get_drive_service():
    """Get authenticated Google Drive service"""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print("ERROR: client_secret.json not found!")
                print("Please download it from Google Cloud Console.")
                print(f"Expected path: {CREDENTIALS_PATH}")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for future runs
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)


def upload_file(service, file_path, folder_id=None):
    """Upload a file to Google Drive"""
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return None
    
    file_name = os.path.basename(file_path)
    
    # File metadata
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.android.package-archive'
    }
    
    # Add to folder if specified
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Upload media
    media = MediaFileUpload(
        file_path,
        mimetype='application/vnd.android.package-archive',
        resumable=True
    )
    
    print(f"Uploading {file_name}...")
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()
    
    print(f"Upload complete!")
    print(f"File ID: {file.get('id')}")
    print(f"View link: {file.get('webViewLink')}")
    
    return file


def create_folder(service, folder_name):
    """Create a folder in Google Drive"""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()
    
    print(f"Created folder: {folder_name} (ID: {folder.get('id')})")
    return folder.get('id')


def main():
    """Main function"""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python upload_to_drive.py <path_to_apk_file>")
        print("\nExample:")
        print("  python upload_to_drive.py ../frontend/bin/qrattendance-1.0.0-arm64-v8a.apk")
        return
    
    file_path = sys.argv[1]
    
    # Get Drive service
    service = get_drive_service()
    if not service:
        return
    
    # Optional: Create or specify folder
    # folder_id = create_folder(service, "QR Attendance APKs")
    folder_id = None
    
    # Upload file
    upload_file(service, file_path, folder_id)


if __name__ == '__main__':
    main()
