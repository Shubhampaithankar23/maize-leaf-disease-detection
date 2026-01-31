# 🧪 Quick Start Guide - Login & Testing

## Running the Application

### Step 1: Start Backend (Terminal 1)
```bash
cd c:\Users\sandi\OneDrive\Desktop\Leaf\backend
python -m pip install -r requirements.txt  # (if not done)
python -m uvicorn main:app --reload --port 5000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
INFO:     Application startup complete
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd c:\Users\sandi\OneDrive\Desktop\Leaf\frontend
python -m http.server 9000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 9000 ...
```

### Step 3: Open Browser
Visit: **http://localhost:9000**

---

## 🔐 Demo Credentials

Choose any of these to login:

| Username | Password | Role |
|----------|----------|------|
| `admin` | `password123` | Administrator |
| `user` | `user123` | Regular User |
| `demo` | `demo123` | Demo Account |

---

## ✅ Login Flow Test

1. **You should see:**
   - Green "Smart Maize" login form
   - Three demo credential options
   - Username and password fields

2. **Enter credentials:**
   - Username: `admin`
   - Password: `password123`

3. **Click "Login"**
   - You'll see a loading spinner
   - After ~1 second, redirects to main app

4. **You should see:**
   - Main disease detection interface
   - "admin" displayed in top-right corner
   - "Logout" button next to username

---

## 🎯 Main App Test

1. **Upload Image:**
   - Click "Select Image" button
   - Choose any maize leaf image
   - Image preview shows

2. **Analyze:**
   - Click "Analyze Image"
   - Loading spinner appears (shows "Analyzing image...")
   - After analysis, results display:
     - Disease name
     - Confidence percentage
     - Confidence bar (green gradient)

3. **View Recommendations:**
   - Scroll down to see disease details:
     - **Cause** - Scientific explanation
     - **Pesticide** - Treatment protocol
     - **Fertilizer** - Nutrient recommendations
     - **Prevention** - Best practices

4. **Test Logout:**
   - Click "Logout" button in top-right
   - Redirected to login page
   - localStorage cleared

---

## 🔍 Browser DevTools Check

### Verify Authentication Data

1. **Open DevTools:** Press `F12`
2. **Go to:** Application → Storage → LocalStorage → localhost:9000
3. **You should see:**
   ```
   Key: isLoggedIn
   Value: true

   Key: currentUser
   Value: admin
   ```

### Clear Session (to test redirect)
1. **Delete both entries** from LocalStorage
2. **Refresh page** - should redirect to login.html
3. **Re-enter credentials** to get back to main app

---

## 🐛 Troubleshooting

### Issue: Blank page after login
**Solution:** 
- Check browser console (F12 → Console)
- Look for errors
- Verify index.html exists in frontend folder
- Refresh page

### Issue: Logout doesn't work
**Solution:**
- Check if logoutBtn is present in HTML
- Verify onclick handler in script.js
- Check console for JavaScript errors

### Issue: Backend connection error
**Solution:**
- Verify backend is running on port 5000
- Check API_URL in script.js is correct
- Look for CORS errors in console

### Issue: Images don't upload
**Solution:**
- Check file size < 10MB
- Verify format is JPEG/PNG/WebP
- Look for error message on page

---

## 📊 API Testing (curl/PowerShell)

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method GET
```

Expected: `{"status": "healthy"}`

### Get Recommendation
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/recommendations/Healthy%20Leaf" -Method GET
```

---

## 📱 Mobile Testing

1. **Responsive Design:**
   - Open DevTools (F12)
   - Click toggle device toolbar
   - Select iPhone 12 / iPad
   - Login page should be centered
   - Main app should stack vertically

2. **Touch Testing:**
   - Buttons should be 44x44px minimum (mobile standard)
   - No hover effects on mobile
   - Dropdowns should be readable

---

## ⚡ Performance Check

1. **Network Tab:**
   - Open DevTools → Network
   - Reload page
   - Check:
     - login.html loads < 1s
     - style.css loads < 500ms
     - Images load < 2s
     - API calls complete < 5s

2. **Performance Tab:**
   - DevTools → Performance
   - Click record
   - Login and navigate
   - FCP (First Contentful Paint) should be < 2s

---

## ✨ What to Expect

### Login Page
- Green gradient background
- "Smart Maize" title in green
- Black card with green border
- Demo credentials displayed
- Smooth animations on focus

### Main App
- Header with green gradient
- Username in top-right
- Logout button next to it
- Upload section in center
- Results section with disease info
- Responsive on all screen sizes

---

## 🎓 Learning Outcomes

After this test, you'll understand:
- ✅ How authentication works
- ✅ localStorage session management
- ✅ Page redirects & navigation
- ✅ API integration in JavaScript
- ✅ Disease prediction workflow
- ✅ How to read/clear browser storage

---

## 📝 Notes

- This uses demo authentication (localStorage)
- Not secure for production
- No database user storage
- No password hashing
- For production, implement server-side auth
- See AUTHENTICATION_SETUP.md for details

---

**Ready to test? Start with Step 1 above!** 🚀
