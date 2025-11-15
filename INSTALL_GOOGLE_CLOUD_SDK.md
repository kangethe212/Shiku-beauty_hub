# 📥 Install Google Cloud SDK - Step by Step Guide

## ✅ Quick Check

First, let's check if it's already installed:

```bash
gcloud --version
```

If you see version information, it's already installed! ✅

---

## 🪟 Windows Installation

### Method 1: Interactive Installer (Recommended)

1. **Download the installer:**
   - Go to: https://cloud.google.com/sdk/docs/install
   - Click "Download Google Cloud SDK"
   - Choose "Windows 64-bit" (or your system type)
   - Download the `.exe` file

2. **Run the installer:**
   - Double-click the downloaded `.exe` file
   - Follow the installation wizard
   - **Important:** Check "Run gcloud init" at the end

3. **Initialize:**
   - The installer will open a terminal
   - Follow the prompts to:
     - Login to your Google account
     - Select project: `shiku-beuty-hub`
     - Choose default region: `us-central1`

### Method 2: Using PowerShell (Advanced)

```powershell
# Download installer
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "$env:TEMP\GoogleCloudSDKInstaller.exe"

# Run installer
Start-Process -FilePath "$env:TEMP\GoogleCloudSDKInstaller.exe" -Wait
```

### Method 3: Using Chocolatey (If you have it)

```bash
choco install gcloudsdk
```

---

## ✅ Verify Installation

After installation, **restart your terminal** and run:

```bash
gcloud --version
```

You should see:
```
Google Cloud SDK 450.0.0
...
```

---

## 🔐 Initial Setup

### 1. Login to Google Cloud

```bash
gcloud auth login
```

This will open your browser - login with your Google account.

### 2. Set Default Project

```bash
gcloud config set project shiku-beuty-hub
```

### 3. Verify Project

```bash
gcloud config get-value project
```

Should output: `shiku-beuty-hub`

### 4. Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

---

## 🆘 Troubleshooting

### "gcloud is not recognized"

**Solution:**
1. Restart your terminal/command prompt
2. If still not working, add to PATH manually:
   - Default location: `C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin`
   - Add to System PATH environment variable

### "Permission denied"

**Solution:**
- Run terminal as Administrator
- Or install to a user directory instead

### "Command not found after installation"

**Solution:**
1. Close and reopen terminal
2. Check PATH: `echo %PATH%`
3. Verify installation location

---

## 📋 Post-Installation Checklist

- [ ] Google Cloud SDK installed
- [ ] `gcloud --version` works
- [ ] Logged in: `gcloud auth login`
- [ ] Project set: `gcloud config set project shiku-beuty-hub`
- [ ] APIs enabled (see commands above)

---

## 🚀 Next Steps

After installation:

1. **Run the quick setup:**
   ```bash
   🚀 QUICK_DEPLOY.bat
   ```

2. **Or continue with deployment:**
   - See: `🚀 COMPLETE_DEPLOYMENT_GUIDE.md`

---

## 💡 Tips

- **Keep it updated:** `gcloud components update`
- **Check current config:** `gcloud config list`
- **Switch projects:** `gcloud config set project PROJECT_ID`
- **View all projects:** `gcloud projects list`

---

**📥 Ready to install? Download from: https://cloud.google.com/sdk/docs/install**

