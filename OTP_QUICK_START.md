# QUICK START - OTP Email Verification

## 5-Minute Setup

### 1. Get Gmail App Password (2 minutes)

```
1. Open: https://myaccount.google.com/apppasswords
2. Login → Select "Mail" and "Windows Computer"
3. Copy the 16-character password generated
```

### 2. Set Environment Variables (1 minute)

**Windows PowerShell:**
```powershell
$env:SENDER_EMAIL = "your-email@gmail.com"
$env:SENDER_PASSWORD = "paste-16-char-app-password-here"
```

### 3. Start Servers (2 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 9000
```

### 4. Test It

1. Open `http://localhost:9000`
2. Click "Login with Google"
3. Enter your Gmail: `yourname@gmail.com`
4. Check your email for OTP
5. Enter the 6-digit code
6. Done! ✅

---

## What You Need

- ✅ Gmail account
- ✅ 2-Step Verification enabled
- ✅ App Password generated
- ✅ Python 3.8+

---

## Common Issues & Fixes

### ❌ "Email not received"
→ Check spam folder, or verify SENDER_PASSWORD is correct (16 chars)

### ❌ "SMTP Authentication failed"
→ Use App Password, NOT Gmail password. App passwords are 16 characters.

### ❌ "Invalid OTP"
→ Make sure you enter all 6 digits and OTP hasn't expired (5 mins)

### ❌ Can't find 2-Step Verification?
→ Go to: https://myaccount.google.com/security → Find "2-Step Verification"

---

## Files Modified

- `backend/main.py` - Added OTP endpoints
- `frontend/login.html` - Added OTP UI and API calls

---

## API Endpoints

```bash
# Send OTP
POST http://localhost:5000/api/auth/send-otp
Body: {"email": "user@gmail.com"}

# Verify OTP
POST http://localhost:5000/api/auth/verify-otp
Body: {"email": "user@gmail.com", "otp": "123456"}
```

---

## Features

✅ Real email delivery via Gmail SMTP
✅ 6-digit OTP code
✅ 5-minute expiry
✅ Resend option
✅ Beautiful UI
✅ Error handling
✅ Mobile responsive

---

## Still Need Help?

1. **Gmail Setup?** → Read `GMAIL_SMTP_SETUP.md`
2. **Full Guide?** → Read `OTP_SETUP_GUIDE.md`
3. **System Overview?** → Read `OTP_IMPLEMENTATION_SUMMARY.md`

---

**Status:** Ready to use immediately after setting environment variables!
