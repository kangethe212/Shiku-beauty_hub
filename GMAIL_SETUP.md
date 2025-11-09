# 📧 GMAIL APP PASSWORD - 2 MINUTE SETUP

## ⚡ Get Instant Email Notifications!

Your email **bennymaish01@gmail.com** is configured! Just need one final step!

---

## 🔐 **GET YOUR GMAIL APP PASSWORD (2 Minutes):**

### Step 1: Go to Google Account
Open this link:
```
https://myaccount.google.com/
```
Login with: **bennymaish01@gmail.com**

### Step 2: Enable 2-Step Verification (If Not Already On)
1. Click **"Security"** on the left
2. Find **"2-Step Verification"**
3. If it says **"OFF"**, click and turn it ON
4. Follow the simple setup (use your phone)

### Step 3: Generate App Password
1. Still in **Security** section
2. Search for **"App passwords"** or scroll down
3. Click **"App passwords"**
4. You might need to sign in again
5. Select:
   - **App**: Choose "Mail"
   - **Device**: Choose "Other" and type: "Her Beauty Hub Website"
6. Click **"Generate"**

### Step 4: Copy Your Password
You'll see a **16-character password** like:
```
abcd efgh ijkl mnop
```

**Copy this password!** (without spaces: `abcdefghijklmnop`)

### Step 5: Add to Your Website
1. Open file: `her_beauty_hub\settings.py`
2. Find line 133:
   ```python
   EMAIL_HOST_PASSWORD = ''
   ```
3. Paste your app password:
   ```python
   EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'
   ```
4. **SAVE FILE!**

### Step 6: Restart Server
Stop server (Ctrl+C) and restart:
```bash
python manage.py runserver 3000
```

---

## 🧪 **TEST IT:**

1. **Visit website**:
   ```
   http://127.0.0.1:3000/hairstyles/
   ```

2. **Click any hairstyle**

3. **Fill booking form** with test data

4. **Submit**

5. **Check your email** (bennymaish01@gmail.com)

You should receive:
```
From: Her Beauty Hub
Subject: 🎉 New Booking: [Hairstyle Name] - [Customer]

🎉 NEW BOOKING ALERT!

👤 Customer: [Name]
📧 Email: [Email]
💇 Service: [Hairstyle]
📅 Date: [Date]
💰 Check admin!
```

---

## 🎯 **EXACT LOCATION TO ADD PASSWORD:**

Open: `her_beauty_hub\settings.py`

Find this section (around line 127-135):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bennymaish01@gmail.com'
EMAIL_HOST_PASSWORD = ''  # ← PASTE YOUR 16-CHAR PASSWORD HERE
DEFAULT_FROM_EMAIL = 'Her Beauty Hub <bennymaish01@gmail.com>'
```

Change the empty `''` to your password:
```python
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # ← YOUR APP PASSWORD
```

**That's it!** 🎉

---

## 💡 **TROUBLESHOOTING:**

### Can't Find "App Passwords"?
- Make sure 2-Step Verification is ON first
- Try searching "app password" in Google Account
- Or visit: https://myaccount.google.com/apppasswords

### "App Passwords Not Available"?
- You need 2-Step Verification enabled first
- Follow the steps in Security section

### Password Not Working?
- Copy WITHOUT spaces
- Make sure you're in `settings.py` file
- Password goes in quotes: `'password'`
- Restart server after saving

---

## ✅ **WHAT YOU'LL GET:**

### Every Booking/Order Sends Email To:
**bennymaish01@gmail.com**

### Email Includes:
- 🎉 Exciting subject line
- 👤 Customer details
- 🛍️ Product ordered
- 💰 Amount (KSH)
- 📋 Order number
- 🔗 Direct admin link
- ⏰ Timestamp

### Delivery Speed:
- Usually **2-5 minutes**
- Check Gmail app on phone
- Check Gmail on computer
- Check spam folder (first time only)

---

## 🎯 **AFTER SETUP:**

### You'll Receive Emails For:
✅ New hairstyle bookings
✅ New perfume orders
✅ New fashion orders
✅ Service appointments
✅ Contact form messages

### Email Goes To:
📧 **bennymaish01@gmail.com**

---

## 💚 **ALTERNATIVE: USE TELEGRAM INSTEAD**

If you want **faster notifications** (instant):
- Setup Telegram Bot (5 min)
- Get alerts in **under 1 second**
- Phone vibrates/rings
- Even easier than email!

**Want Telegram instead? Just say "setup telegram"!** 💬

---

## 🎉 **YOUR SETTINGS ARE READY!**

### All Configured:
- ✅ Gmail SMTP settings added
- ✅ Your email (bennymaish01@gmail.com) set as recipient
- ✅ "Her Beauty Hub" as sender name
- ✅ Notification code activated

### Just Need:
- 🔑 Gmail App Password (2 minutes to get)
- 📝 Paste it in settings.py
- 🔄 Restart server

**Then you're done!** 🎉✨

---

## 📱 **GET APP PASSWORD NOW:**

Visit: **https://myaccount.google.com/security**

Look for: **"App passwords"**

Generate: **Mail** app password

Copy: **16-character password**

Paste in: `her_beauty_hub\settings.py` line 133

**Save & Restart!** 🚀

---

**All set up for bennymaish01@gmail.com!** 📧💖

**Just add the app password and you're live!** ✨

