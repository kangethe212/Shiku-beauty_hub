# 📱 TELEGRAM NOTIFICATIONS - 5 MINUTE SETUP

## ⚡ Get Instant Alerts on Your Phone When Students Book/Order!

---

## 🎯 **FOLLOW THESE SIMPLE STEPS:**

### Step 1️⃣: Open Telegram App (1 minute)
1. Open Telegram on your phone
2. In search, type: **@BotFather**
3. Click the verified BotFather (blue checkmark)
4. Click **START**

### Step 2️⃣: Create Your Bot (2 minutes)
1. Send this message: `/newbot`
2. BotFather asks for name, send: **Her Beauty Hub Bot**
3. BotFather asks for username, send: **herbeautyhub_notifier_bot**
4. BotFather gives you a TOKEN - **COPY IT!**
   - Looks like: `6789012345:ABCdefGHIjklMNOpqrstUVWxyz`
   - ⚠️ **SAVE THIS TOKEN!**

### Step 3️⃣: Start Chat with Your Bot (30 seconds)
1. Click the link BotFather gives you
2. Click **START** button
3. Send any message like: "Hello"

### Step 4️⃣: Get Your Chat ID (1 minute)
1. Open browser on your phone/computer
2. Copy this link and replace TOKEN with YOUR bot token:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. You'll see something like:
   ```json
   {"chat":{"id":123456789}}
   ```
4. **COPY THE NUMBER** (e.g., 123456789)

### Step 5️⃣: Add to Your Website (30 seconds)
1. Open file: `her_beauty_hub/settings.py`
2. Find these lines (around line 150):
   ```python
   TELEGRAM_BOT_TOKEN = ''
   TELEGRAM_CHAT_ID = ''
   ```
3. Paste your values:
   ```python
   TELEGRAM_BOT_TOKEN = '6789012345:ABCdefGHIjklMNOpqrstUVWxyz'
   TELEGRAM_CHAT_ID = '123456789'
   ```
4. **SAVE FILE**

### Step 6️⃣: Restart Server (10 seconds)
Stop server (Ctrl+C) and restart:
```bash
python manage.py runserver 3000
```

---

## 🎉 **DONE! TEST IT:**

1. Visit: http://127.0.0.1:3000/hairstyles/
2. Click any hairstyle
3. Fill order form
4. Submit
5. **CHECK YOUR TELEGRAM** → You'll get instant message! 📱💬

---

## 💬 **WHAT YOU'LL RECEIVE:**

```
─────────────────────────────
Her Beauty Hub Bot

🎉 NEW HAIRSTYLE BOOKING!

👤 Jane Doe
💇 Knotless Box Braids
💰 KSH 1000
📋 #HBH45678901

Just now
─────────────────────────────
```

**Instant notification on your phone!** ⚡

---

## 🔔 **NOTIFICATION FEATURES:**

- ✅ Vibrates your phone
- ✅ Shows on lock screen
- ✅ Badge on app icon
- ✅ Sound alert
- ✅ Works when phone is locked
- ✅ History saved in chat
- ✅ Can reply to customer (future feature)

---

## 💡 **TIPS:**

### Telegram Settings:
- Turn on **Notifications** for the bot
- Enable **Sound** for alerts
- Pin the bot chat (so it stays on top)

### For Business Use:
- Check Telegram every hour
- Reply "Got it!" to mark as seen
- Access admin panel to confirm bookings

---

## ✅ **ADVANTAGES:**

- 💰 **100% FREE** (forever!)
- ⚡ **INSTANT** (under 1 second)
- 📱 **Phone alerts** (vibration + sound)
- 🌍 **Works anywhere** (just need internet)
- 💪 **Very reliable** (Telegram has 99.9% uptime)
- 🎨 **Formatted messages** (bold, emojis)
- 📂 **History saved** (all notifications stored)

---

## 🆘 **NEED HELP?**

### Can't Find Chat ID?
1. Make sure you sent a message to your bot first
2. Visit the getUpdates URL
3. Look for `"chat":{"id":` followed by a number
4. That's your Chat ID!

### Bot Not Responding?
- Make sure you clicked START
- Send any message first
- Then get updates

### Still Not Working?
- Double-check token (no spaces)
- Make sure chat ID is just numbers
- Restart your server after adding settings

---

## 🎉 **ONCE SETUP, YOU GET:**

### Every Single Booking/Order:
- 📱 Phone notification
- 💬 Telegram message
- 🔔 Sound alert
- 📋 Order details
- 💰 Amount shown
- 👤 Customer info

**Never miss an order again!** 💖✨

---

**5 minutes of setup = Lifetime of instant notifications!**

**Start now and test with a booking!** 🚀📱💬

