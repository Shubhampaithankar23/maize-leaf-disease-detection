# Gmail SMTP Setup for OTP Email Delivery

This guide will help you set up Gmail SMTP to send OTP emails in the Smart Maize system.

## Prerequisites

You need a Gmail account with 2-Step Verification enabled.

## Step 1: Enable 2-Step Verification

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click on "2-Step Verification"
3. Follow the prompts to enable it

## Step 2: Generate App Password

1. Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer" (or your device)
3. Google will generate a 16-character app password
4. Copy this password (you'll need it in Step 3)

## Step 3: Set Environment Variables

### On Windows (PowerShell):

```powershell
$env:SENDER_EMAIL = "your-email@gmail.com"
$env:SENDER_PASSWORD = "your-16-char-app-password"
```

### On Windows (Command Prompt):

```cmd
set SENDER_EMAIL=your-email@gmail.com
set SENDER_PASSWORD=your-16-char-app-password
```

### On Windows (Permanent - Environment Variables):

1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" under "User variables"
5. Add:
   - Variable name: `SENDER_EMAIL`
   - Variable value: `your-email@gmail.com`
6. Add another:
   - Variable name: `SENDER_PASSWORD`
   - Variable value: `your-16-char-app-password`
7. Click OK and restart your terminal

## Step 4: Verify Configuration

After setting the environment variables, restart the FastAPI backend:

```bash
cd backend
python main.py
```

## Step 5: Test OTP Delivery

1. Start the frontend server
2. Go to login page
3. Click "Login with Google"
4. Enter your test Gmail address
5. Check your email for the OTP

## Troubleshooting

### Issue: "SMTP Authentication failed"

**Solution:** Make sure you're using an **App Password**, not your Gmail password. App passwords are 16 characters and are generated after enabling 2-Step Verification.

### Issue: "SMTP error: Connection refused"

**Solution:** This might be a firewall issue or Gmail blocking the connection. Try:
- Disabling firewall temporarily
- Using a VPN
- Checking Gmail's account security settings

### Issue: Email not received

**Solution:**
1. Check spam/junk folder
2. Verify the email address is correct
3. Check backend logs for error messages
4. Make sure environment variables are set correctly

## Production Deployment

For production, consider using:
- **SendGrid**: Reliable email service
- **AWS SES**: Amazon's email service
- **Mailgun**: Email API service
- **Brevo (formerly Sendinblue)**: Free tier available

These services are more reliable and have better deliverability than Gmail SMTP.

## Testing Without Email

If you don't want to set up Gmail SMTP, the system will:
1. Still generate OTP
2. Log it to console (for testing)
3. Show a test message in UI

This is useful for development but not recommended for production.

---

**Note:** Your Gmail credentials are never stored or logged. They are only used to send OTP emails.
