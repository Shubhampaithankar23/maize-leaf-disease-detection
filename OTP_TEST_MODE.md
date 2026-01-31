# ⚡ OTP Testing Guide

## Current Status: WORKING IN TEST MODE ✅

The OTP system is now working in **TEST MODE**. Here's how it works:

---

## 🧪 Test Mode (No Email Setup Required)

### How to Use

1. **Start the website** (already running)
2. Click **"Login with Google"**
3. Enter any **Gmail address** (e.g., test@gmail.com)
4. Click **"Continue"**
5. **An alert popup will appear** with your OTP code
6. **Copy the OTP** from the alert
7. **Paste it into the OTP input boxes**
8. Click **"Verify OTP"**
9. **You're logged in!** ✅

### Example Flow

```
User enters: john@gmail.com
↓
System generates OTP: 456789
↓
Alert appears: "📋 TEST MODE - Your OTP is: 456789"
↓
User copies: 456789
↓
User pastes into OTP fields
↓
User clicks "Verify OTP"
↓
✅ Logged in!
```

---

## 🚀 Enable Real Email (Optional)

If you want **real emails** sent instead of test alerts:

### Step 1: Gmail Setup

1. Go to: https://myaccount.google.com/security
2. Enable: **2-Step Verification**
3. Go to: https://myaccount.google.com/apppasswords
4. Select: **Mail** and **Windows Computer**
5. Copy: The 16-character **App Password**

### Step 2: Set Environment Variables

**PowerShell:**
```powershell
$env:SENDER_EMAIL = "your-email@gmail.com"
$env:SENDER_PASSWORD = "your-16-char-app-password"
```

**Then restart the backend:**
```powershell
cd c:\Users\sandi\OneDrive\Desktop\Leaf\backend
python main.py
```

### Step 3: Real Emails Will Work

After restart, when users enter Gmail:
- ✅ Real email sent to inbox
- ✅ No alert popup
- ❌ OTP not shown in browser (security)
- User checks email for 6-digit code

---

## 📋 Key Differences

| Mode | What Happens | Use Case |
|------|-------------|----------|
| **TEST MODE** (Current) | Alert shows OTP code | Development & Testing |
| **REAL EMAIL MODE** | Email sent to inbox | Production |

---

## ✅ Features That Work Now

- ✅ Gmail address validation
- ✅ 6-digit OTP generation
- ✅ OTP display in test mode
- ✅ 5-minute expiry timer
- ✅ Resend OTP
- ✅ Auto-focus between digit boxes
- ✅ Paste support
- ✅ Error handling
- ✅ Mobile responsive

---

## 🧪 Test These Features

### 1. Valid Email
```
Enter: test@gmail.com
Expected: OTP alert appears
```

### 2. Invalid Email
```
Enter: notanemail
Expected: Error message
```

### 3. OTP Entry
```
Get OTP from alert: 123456
Enter each digit: 1, 2, 3, 4, 5, 6
Expected: Auto-focus between fields
```

### 4. Wrong OTP
```
Enter OTP: 999999 (different from alert)
Expected: Error message "Invalid OTP"
```

### 5. Expired OTP
```
Wait 5+ minutes
Try to enter OTP
Expected: Error message "OTP expired"
```

### 6. Resend OTP
```
Click "Resend" button
Expected: New alert with different OTP
```

---

## 🔍 Checking Backend Logs

When you test, check the backend console for messages like:

```
INFO:     127.0.0.1:12345 - "POST /api/auth/send-otp HTTP/1.1" 200 OK
INFO: OTP sent to test@gmail.com
```

Or in test mode:

```
WARNING: Email not configured. OTP for test@gmail.com: 456789
INFO: To enable real email sending, set SENDER_EMAIL and SENDER_PASSWORD environment variables
```

---

## 📱 Browser Console

Open browser **F12 → Console** to see:

```
OTP Response: {success: true, message: "TEST MODE: OTP is 456789...", test_otp: "456789"}
```

---

## ⚠️ Troubleshooting

### "No OTP appears"

1. Check if alert is blocked (allow popups)
2. Check browser console (F12)
3. Check backend logs in terminal
4. Try refreshing page

### "OTP field won't accept numbers"

1. Click on first digit box
2. Type one digit
3. Should auto-focus to next box

### "Can't paste OTP"

1. Copy the OTP from alert
2. Right-click in first OTP box
3. Select "Paste"
4. Or use Ctrl+V

### "Keep getting 'Invalid OTP'"

1. Make sure you're using the OTP from the MOST RECENT alert
2. Enter all 6 digits
3. Don't leave any boxes empty

---

## 💡 Quick Reference

| Action | Step |
|--------|------|
| Start testing | Already running ✅ |
| Test OTP | Open http://localhost:9000 |
| See OTP code | Click "Login with Google" → Enter email → Look for alert |
| Enter OTP | Paste into 6 digit boxes |
| Verify | Click "Verify OTP" |
| Logged in | Check if redirected to main page |

---

## 🎯 Next Steps

- ✅ Test with test mode (working now)
- 🔄 Set email credentials when ready
- 🚀 Deploy to production

---

**Status:** ✅ **READY FOR TESTING**

No setup required! Just test with the OTP shown in the alert popup.
