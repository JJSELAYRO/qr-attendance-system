# QR Attendance System - Buildozer Specification
# Configuration for building Android APK

[app]

# Title of your application
title = QR Attendance

# Package name (must be unique)
package.name = qrattendance

# Package domain (needed for android/ios packaging)
package.domain = org.school.attendance

# Source code where the main.py live
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt

# Version of your application
version = 1.0.0

# Requirements - same as requirements.txt
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer==2.1.0,pyjnius==1.6.1,pillow==10.1.0,numpy==1.26.2,requests==2.31.0,python-dateutil==2.8.2

# Orientation (portrait for mobile)
orientation = portrait

# Fullscreen mode
fullscreen = 0

# Android specific
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a

# Android permissions
android.permissions = CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS,INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android features
android.features = android.hardware.camera,android.hardware.camera.autofocus,android.hardware.location,android.hardware.location.gps

# Android app entry point
android.entrypoint = org.kivy.android.PythonActivity

# Android manifest intent filters
android.manifest_intent_filters = %(source.dir)s/intent_filters.xml

# Android logcat filters
android.logcat_filters = *:S python:D

# Copy library
android.copy_libs = 1

# Version code
android.numeric_version = 1

# Allow backup
android.allow_backup = True

# Release artifact format
android.release_artifact = apk
android.debug_artifact = apk

# Enable AndroidX
android.enable_androidx = True

# Android metadata
android.meta_data = android.hardware.camera=true,android.hardware.camera.autofocus=true

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if run as root
warn_on_root = 1
