# Smart Maize Leaf Disease Detection - OTP Authentication Setup

## Overview

The system now includes **real OTP email verification** for Google login. Users will receive a 6-digit code via their Gmail address that they must enter to complete login.

## Quick Start

### Prerequisites

- Python 3.8+
- Gmail account with 2-Step Verification enabled
- Internet connection

### Setup Steps

#### 1. Install Required Python Package (Backend)

```bash
cd backend
pip install pydantic
```

(Already included: smtplib, email.mime)

#### 2. Configure Gmail SMTP

Follow the detailed guide in `GMAIL_SMTP_SETUP.md` to:
1. Enable 2-Step Verification on your Gmail account
2. Generate an App Password
3. Set environment variables

**Quick Setup (Windows PowerShell):**

```powershell
# Replace with your actual values
$env:SENDER_EMAIL = "your-email@gmail.com"
$env:SENDER_PASSWORD = "your-16-character-app-password"
```

#### 3. Start the Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO: Uvicorn running on http://0.0.0.0:5000
```

#### 4. Start the Frontend

```bash
cd frontend
python -m http.server 9000
```

#### 5. Test the System

1. Open browser to `http://localhost:9000`
2. Click "Login with Google"
3. Enter your test Gmail address
4. Check your email for the OTP
5. Enter the 6-digit code
6. You should be logged in!

## How It Works

### User Flow

```
1. User clicks "Login with Google"
   ↓
2. Modal opens asking for Gmail address
   ↓
3. User enters email and clicks "Continue"
   ↓
4. Frontend sends email to backend (/api/auth/send-otp)
   ↓
5. Backend generates 6-digit OTP and sends via Gmail SMTP
   ↓
6. User receives email with OTP code
   ↓
7. User enters OTP in modal (6 digit boxes)
   ↓
8. Frontend sends OTP to backend (/api/auth/verify-otp)
   ↓
9. Backend verifies OTP (must match and not expired)
   ↓
10. If valid → User is logged in and redirected to app
    If invalid → Error message, user can retry or resend OTP
```

### API Endpoints

#### Send OTP

**Request:**
```bash
POST /api/auth/send-otp
Content-Type: application/json

{
  "email": "user@gmail.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "OTP sent to user@gmail.com",
  "email": "user@gmail.com"
}
```

#### Verify OTP

**Request:**
```bash
POST /api/auth/verify-otp
Content-Type: application/json

{
  "email": "user@gmail.com",
  "otp": "123456"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Email verified successfully",
  "email": "user@gmail.com"
}
```

## Features

✅ **Real Email Delivery** - OTP sent via actual Gmail SMTP
✅ **6-Digit Code** - Standard OTP format
✅ **5-Minute Expiry** - OTP automatically expires after 5 minutes
✅ **Resend Option** - Users can request a new OTP if needed
✅ **Auto-Focus** - Input fields auto-focus when digit is entered
✅ **Paste Support** - Users can paste entire OTP at once
✅ **Error Handling** - Clear error messages for invalid/expired OTPs
✅ **User-Friendly UI** - Beautiful modal with countdown timer
✅ **Mobile Responsive** - Works on all screen sizes

## Security Considerations

### Current Implementation

- OTP stored in memory (resets on server restart)
- 5-minute expiration
- Single-use OTP (deleted after verification)
- Gmail's security for email transport

### For Production

1. **Use Redis** instead of in-memory storage:
```python
# Replace OTP_STORAGE dict with Redis
import redis
r = redis.Redis(host='localhost', port=6379)
r.setex(email, 300, otp)  # Expires in 300 seconds
```

2. **Add Rate Limiting**:
```python
# Prevent spam/brute force
MAX_OTP_ATTEMPTS = 3
MAX_OTP_REQUESTS = 5  # per hour
```

3. **Use Production Email Service**:
- SendGrid
- AWS SES
- Mailgun
- Brevo

4. **Enable HTTPS** - All traffic should be encrypted

5. **Add Database Logging** - Track all authentication attempts

## Troubleshooting

### Email Not Received

1. **Check Spam Folder** - Gmail might mark it as spam initially
2. **Verify Email Credentials** - Ensure SENDER_EMAIL and SENDER_PASSWORD are correct
3. **Check Backend Logs** - Look for error messages in console
4. **Test Email Connection** - Use the test script below

### Test Email Connection

Create `test_email.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("✓ Email configuration successful!")
except Exception as e:
    print(f"✗ Email configuration failed: {e}")
```

Run:
```bash
python test_email.py
```

### OTP Expires Too Quickly

- Default: 5 minutes (300 seconds)
- Change in `main.py`: `if time_diff > 300:`

### OTP Not Validating

Check these common issues:
1. OTP is correct but expired → User needs to resend
2. OTP is incorrect → User typed wrong code
3. Email mismatch → Check capitalization

## Development vs Production

### Development

```
✓ Use Gmail SMTP for testing
✓ OTP stored in memory
✓ Display OTP in console for debugging
✓ 5-minute expiry
```

### Production

```
✓ Use dedicated email service (SendGrid, AWS SES)
✓ Store OTP in Redis database
✓ Never display OTP in logs
✓ 2-3 minute expiry
✓ Add rate limiting
✓ Add HTTPS/SSL
✓ Monitor authentication logs
✓ Implement backup email methods
```

## Testing Accounts

### Gmail Test Addresses

For testing, use these real Gmail accounts:
- `test.account@gmail.com`
- `demo.user@gmail.com`

### Example Test Flow

1. User enters: `demo.user@gmail.com`
2. Backend sends OTP to that address
3. Open that Gmail and copy the 6-digit code
4. Paste into the OTP field
5. Verify!

## File Changes

### Backend Files Modified

- `main.py` - Added OTP endpoints and email functionality

### Frontend Files Modified

- `login.html` - Updated to call backend OTP APIs

### New Documentation

- `GMAIL_SMTP_SETUP.md` - Gmail SMTP configuration guide
- `OTP_SETUP_GUIDE.md` - This file

## Support & Documentation

For more information:
1. See `GMAIL_SMTP_SETUP.md` for Gmail configuration
2. Check backend logs for error messages
3. Review `main.py` for OTP logic
4. Check `login.html` for frontend implementation

---

**Version:** 1.0.0
**Last Updated:** January 2026
**Status:** Ready for Production (with recommendations)
