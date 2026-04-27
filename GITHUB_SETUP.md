# GitHub Actions Setup - Build APK Automatically

This guide helps you set up automatic APK building with GitHub Actions.

## ✅ What This Does

- Push code to GitHub → GitHub builds APK automatically
- Download APK from GitHub releases
- No need for WSL or local build tools!

---

## 🚀 Step-by-Step Setup

### Step 1: Create GitHub Account

1. Go to https://github.com
2. Click **"Sign up"**
3. Follow the steps (email, password, username)
4. Verify your email

---

### Step 2: Create New Repository

1. Click **"+"** (top right) → **"New repository"**
2. Repository name: `qr-attendance-system`
3. Description: `QR Code Attendance System with GPS and SMS`
4. Set to **"Public"** (or Private if you prefer)
5. **UNCHECK** "Initialize with README" (we already have one)
6. Click **"Create repository"**

---

### Step 3: Upload Your Code

**Option A: Using GitHub Website (Easiest)**

1. On your new repo page, click **"uploading an existing file"**
2. Drag and drop your entire `qr_attendance_system` folder
3. Wait for upload
4. Add commit message: `Initial upload`
5. Click **"Commit changes"**

**Option B: Using Git Command Line**

```bash
# Navigate to your project
cd c:\application\qr_attendance_system

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/qr-attendance-system.git

# Push
git branch -M main
git push -u origin main
```

---

### Step 4: Wait for Build

1. Go to your GitHub repo
2. Click **"Actions"** tab (top of page)
3. You'll see **"Build Android APK"** workflow running
4. Wait 10-15 minutes (first build takes longer)

**What you'll see:**
```
🟡 Build Android APK - in progress
   └── build-apk
       ├── Checkout code ✓
       ├── Set up Python ✓
       ├── Install dependencies ✓
       ├── Build APK ⏳ (this takes time)
       └── Upload APK
```

---

### Step 5: Download Your APK

**From Actions Tab:**
1. Click the completed workflow run
2. Scroll down to **"Artifacts"** section
3. Click `qr-attendance-apk` to download

**From Releases (if enabled):**
1. Click **"Releases"** on the right side
2. Download the APK file

---

## 📱 How to Install on Phone

1. **Download APK** from GitHub
2. **Transfer to phone** (email, USB, or cloud)
3. **On phone:** Enable "Install from unknown sources"
   - Settings → Security → Unknown sources
4. **Open APK file** on phone
5. **Install**

---

## 🔄 Update Your App

When you make changes:

1. **Edit code** on your computer
2. **Upload to GitHub** (drag & drop or git push)
3. **GitHub automatically rebuilds** the APK
4. **Download new APK** from Actions tab

---

## 🛠️ Troubleshooting

### Build Fails?

1. Click the failed workflow
2. Check the error message
3. Common fixes:
   - Check `buildozer.spec` is in `frontend/` folder
   - Make sure all Python files are uploaded

### Can't Download APK?

- Make sure you're logged into GitHub
- Check the workflow completed successfully
- Try refreshing the page

---

## 🎉 Success!

You now have:
- ✅ Code on GitHub
- ✅ Automatic APK building
- ✅ Download from anywhere

**Next:** Upload to Google Drive and share with friends!

---

## 💡 Tips

- **Make changes** → Push to GitHub → New APK in 10 min
- **Use GitHub mobile app** to monitor builds
- **Enable notifications** for build status
- **Star your repo** so you can find it easily
