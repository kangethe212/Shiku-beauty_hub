"""
Instant Notification System for Her Beauty Hub
Sends alerts to owner when bookings/orders are made
"""

import requests
from django.core.mail import send_mail
from django.conf import settings


def send_booking_notification(booking):
    """
    Send instant notification to owner about new booking
    Uses multiple channels for reliability
    """
    owner_phone = "254796465104"  # Owner's WhatsApp number
    owner_email = "admin@herbeautyhub.com"  # Change to owner's email
    
    # Prepare message content
    message = f"""
🎉 NEW BOOKING ALERT!

👤 Customer: {booking.name}
📧 Email: {booking.email}
📱 Phone: {booking.phone or 'Not provided'}

💇 Service: {booking.service.name}
📅 Date: {booking.date}
⏰ Time: {booking.time or 'Not specified'}

💬 Message: {booking.message or 'No message'}

🎛️ Manage: http://127.0.0.1:3000/admin/beautyhub/booking/{booking.id}/
    """.strip()
    
    # Track notification methods used
    notifications_sent = []
    
    # METHOD 1: Email Notification (Most Reliable)
    try:
        send_mail(
            subject=f'🎉 New Booking: {booking.service.name} - {booking.name}',
            message=message,
            from_email='noreply@herbeautyhub.com',
            recipient_list=[owner_email],
            fail_silently=False,
        )
        notifications_sent.append('Email')
        print(f"✅ Email notification sent to {owner_email}")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")
    
    # METHOD 2: WhatsApp Business API (Requires setup)
    try:
        whatsapp_message = f"🎉 NEW BOOKING!\n\n👤 {booking.name}\n💇 {booking.service.name}\n📅 {booking.date}\n💰 Check admin panel!"
        
        # Option A: Using Africa's Talking (Popular in Kenya)
        # Uncomment and add your API key
        # send_africas_talking_sms(owner_phone, whatsapp_message)
        
        # Option B: Using Twilio WhatsApp
        # Uncomment and add your credentials
        # send_twilio_whatsapp(owner_phone, whatsapp_message)
        
        # For now, just log
        print(f"📱 WhatsApp message prepared for {owner_phone}")
        print(f"   Message: {whatsapp_message[:50]}...")
        # notifications_sent.append('WhatsApp')
        
    except Exception as e:
        print(f"⚠️ WhatsApp notification failed: {e}")
    
    # METHOD 3: SMS Notification (Backup)
    try:
        sms_message = f"NEW BOOKING: {booking.name} booked {booking.service.name} for {booking.date}. Check admin!"
        
        # Using Africa's Talking SMS (Popular in Kenya)
        # Uncomment and configure
        # send_africas_talking_sms(owner_phone, sms_message)
        
        print(f"📲 SMS prepared for {owner_phone}")
        # notifications_sent.append('SMS')
        
    except Exception as e:
        print(f"⚠️ SMS failed: {e}")
    
    return notifications_sent


def send_order_notification(order):
    """
    Send instant notification about new product order
    """
    owner_phone = "254796465104"
    owner_email = "admin@herbeautyhub.com"
    
    # Prepare message
    message = f"""
🛒 NEW ORDER ALERT!

📋 Order: #{order.order_number}
👤 Customer: {order.name}
📧 Email: {order.email}
📱 Phone: {order.phone or 'Not provided'}

🛍️ Product: {order.product_type} - {order.product_name}
💰 Amount: KSH {int(order.total_amount_ksh)}
📦 Quantity: {order.quantity}

💬 Note: {order.message or 'No note'}

🎛️ Manage: http://127.0.0.1:3000/admin/beautyhub/ordermessage/{order.id}/
    """.strip()
    
    # Email notification
    try:
        send_mail(
            subject=f'🛒 New Order #{order.order_number} - KSH {int(order.total_amount_ksh)}',
            message=message,
            from_email='noreply@herbeautyhub.com',
            recipient_list=[owner_email],
            fail_silently=False,
        )
        print(f"✅ Order email sent to {owner_email}")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")
    
    # WhatsApp notification
    try:
        whatsapp_msg = f"🛒 NEW ORDER!\n\n#{order.order_number}\n👤 {order.name}\n🛍️ {order.product_name}\n💰 KSH {int(order.total_amount_ksh)}"
        print(f"📱 WhatsApp notification prepared")
        print(f"   To: {owner_phone}")
    except Exception as e:
        print(f"⚠️ WhatsApp failed: {e}")


# ============================================================
# AFRICA'S TALKING INTEGRATION (Kenya's #1 SMS/Voice Provider)
# ============================================================

def send_africas_talking_sms(phone, message):
    """
    Send SMS using Africa's Talking
    Popular in Kenya, very reliable
    
    Setup:
    1. Sign up at https://africastalking.com/
    2. Get API key and username
    3. Add to settings.py:
       AFRICASTALKING_USERNAME = 'your_username'
       AFRICASTALKING_API_KEY = 'your_api_key'
    """
    try:
        import africastalking
        
        # Initialize
        username = getattr(settings, 'AFRICASTALKING_USERNAME', 'sandbox')
        api_key = getattr(settings, 'AFRICASTALKING_API_KEY', '')
        
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        
        # Send SMS
        response = sms.send(message, [f"+{phone}"])
        print(f"✅ SMS sent via Africa's Talking")
        return True
        
    except Exception as e:
        print(f"⚠️ Africa's Talking SMS failed: {e}")
        return False


# ============================================================
# TWILIO INTEGRATION (International Option)
# ============================================================

def send_twilio_whatsapp(phone, message):
    """
    Send WhatsApp message using Twilio
    
    Setup:
    1. Sign up at https://twilio.com/
    2. Get Account SID and Auth Token
    3. Add to settings.py:
       TWILIO_ACCOUNT_SID = 'your_sid'
       TWILIO_AUTH_TOKEN = 'your_token'
       TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
    """
    try:
        from twilio.rest import Client
        
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=getattr(settings, 'TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886'),
            body=message,
            to=f'whatsapp:+{phone}'
        )
        
        print(f"✅ WhatsApp sent via Twilio")
        return True
        
    except Exception as e:
        print(f"⚠️ Twilio WhatsApp failed: {e}")
        return False


# ============================================================
# SIMPLE WEBHOOK OPTION (Free & Easy!)
# ============================================================

def send_webhook_notification(booking_data):
    """
    Send notification via webhook to services like:
    - Discord
    - Slack
    - Telegram
    - Custom endpoint
    
    EASIEST OPTION: Set up a Telegram bot!
    """
    try:
        # Example: Send to Discord webhook
        webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
        
        if webhook_url:
            payload = {
                "content": f"🎉 **NEW BOOKING!**\n\n👤 {booking_data['name']}\n💇 {booking_data['service']}\n📅 {booking_data['date']}"
            }
            response = requests.post(webhook_url, json=payload)
            print("✅ Webhook notification sent")
            return True
            
    except Exception as e:
        print(f"⚠️ Webhook failed: {e}")
        return False


# ============================================================
# TELEGRAM BOT (RECOMMENDED - FREE & INSTANT!)
# ============================================================

def send_telegram_notification(message):
    """
    Send instant notification via Telegram
    
    EASIEST & FREE OPTION!
    
    Setup (5 minutes):
    1. Open Telegram app
    2. Search for @BotFather
    3. Create bot: /newbot
    4. Get your bot token
    5. Start chat with your bot
    6. Get your chat ID: https://api.telegram.org/bot<TOKEN>/getUpdates
    7. Add to settings.py:
       TELEGRAM_BOT_TOKEN = 'your_token'
       TELEGRAM_CHAT_ID = 'your_chat_id'
    """
    try:
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
        
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print("✅ Telegram notification sent!")
                return True
            else:
                print(f"⚠️ Telegram failed: {response.text}")
                
    except Exception as e:
        print(f"⚠️ Telegram notification failed: {e}")
        
    return False

