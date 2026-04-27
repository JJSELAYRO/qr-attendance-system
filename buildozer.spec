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
source.dir = frontend

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt

# Version of your application
version = 1.0.0

# Requirements - same as requirements.txt
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer==2.1.0,pyjnius==1.6.1,pillow==10.1.0,numpy==1.26.2,requests==2.31.0,python-dateutil==2.8.2,opencv-python==4.8.1.78

# Garden requirements
garden_requirements = 

# Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# Supported orientation (portrait for mobile)
orientation = portrait

# Android specific
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a

# Android permissions
android.permissions = 
    CAMERA,
    ACCESS_FINE_LOCATION,
    ACCESS_COARSE_LOCATION,
    SEND_SMS,
    INTERNET,
    ACCESS_NETWORK_STATE,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE

# Android features
android.features = 
    android.hardware.camera,
    android.hardware.camera.autofocus,
    android.hardware.location,
    android.hardware.location.gps

# Android app entry point
android.entrypoint = org.kivy.android.PythonActivity

# Android manifest additions for SMS intent
android.manifest_placeholders = 
    [org.kivy.android]

# Android additional resources (optional)
#android.add_resources =

# (str) XML file to include as an intent filters in <activity> tag
android.manifest_intent_filters = %(source.dir)s/intent_filters.xml

# (str) launchMode to set for the main activity
android.activity_launch_mode = standard

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) XML file for custom JAVA names (example: android/build/maven/java_names.xml)
#android.add_maven_repositories =

# (str) XML file for custom gradle settings (example: android/build/gradle/settings.gradle)
#android.gradle_settings =

# (str) additional Java classes to add (activity = android.app.Activity)
android.add_activities = 

# (list) Gradle repositories to add {add_repositories is a common name}
#android.gradle_dependencies =

# (list) add java compile options
# this can for example be necessary when you want to use android.car.Car
#android.add_compile_options = sourceCompatibility JavaVersion.VERSION_1_8, targetCompatibility JavaVersion.VERSION_1_8

# (list) Packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# android.packaging_options = pickFirst '**/libc++_shared.so', pickFirst '**/libjsc.so'

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
android.ouya.category = APP

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides automatic versionCode computation
android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifest_placeholders property.
# This property takes a map of key-value pairs. (via a string)
# Usage example : android.manifest_placeholders = [myCustomUrl:\"org.example.custom/url\", \n#                                                  otherPlaceholder: \"value\"
# android.manifest_placeholders = [:]

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Activity
# Use that parameter if you want to implement your own PythonActivity class (e.g. for notification support)
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest_intent_filters =

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (bool) Apply Java classes transformation to support lambda (default True if android.minapi >= 24)
android.enable_androidx = True

# (list) Additionnal Java .jar files to add to the libs
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) Additionnal Java directories to add to the libs
#android.add_src =

# (str) additional Java classes to add (example: com.example.MyClass)
#android.add_src = com/example/MyClass.java

# (list) Gradle dependencies to add (currently works only with sdl2_gradle bootstrap)
#android.gradle_dependencies = com.android.support:support-compat:28.0.0

# (list) add java compile options
# this can for example be necessary when you want to use android.car.Car
#android.add_compile_options = sourceCompatibility JavaVersion.VERSION_1_8, targetCompatibility JavaVersion.VERSION_1_8

# (list) Packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# android.packaging_options = pickFirst '**/libc++_shared.so', pickFirst '**/libjsc.so'

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
android.ouya.category = APP

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data = 
    android.hardware.camera=true,
    android.hardware.camera.autofocus=true

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.arch = arm64-v8a

# (int) overrides automatic versionCode computation
#android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url =

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
#p4a.commit = HEAD

# (str) python-for-android git clone directory
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask/webview etc)
# p4a.port =


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Or copy it into the same folder as the buildozer.spec
#ios.kivy_ios_dir = ./kivy-ios

# (str) Path to your application entry point (main.py)
#ios.source_dir = frontend/

# (str) Title of your application
#ios.app_name = QR Attendance

# (str) Source code dir
#ios.source_dir = %(source.dir)s

# (list) Device to target when building for iOS
# ios.codesign.allowed_devices = iphone,ipad

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
