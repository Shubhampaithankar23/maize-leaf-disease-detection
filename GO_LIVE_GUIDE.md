# 🚀 Go Live - Deployment Guide

## ✅ Pre-Deployment Checklist

Your system is ready! Current status:
- ✅ Backend running on `localhost:8001`
- ✅ Frontend running on `localhost:9000`
- ✅ Database with 8 disease recommendations
- ✅ Gradient UI (Green & Black theme)
- ✅ Enhanced accuracy & detailed solutions

---

## 🌍 **FASTEST OPTIONS (Choose One)**

### **Option 1: Heroku (EASIEST - 5 minutes)**

1. **Sign up** at https://heroku.com (free tier available)

2. **Install Heroku CLI**:
   ```bash
   # Windows
   choco install heroku-cli
   ```

3. **Deploy**:
   ```bash
   cd c:\Users\sandi\OneDrive\Desktop\Leaf
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **Access**: `https://your-app-name.herokuapp.com`

---

### **Option 2: Railway (EASY - 5 minutes)**

1. **Sign up** at https://railway.app

2. **Connect GitHub** (or upload files directly)

3. **Deploy**: Click "Deploy"

4. **Access**: Auto-generated URL

**Cost**: Free tier with $5 monthly credit

---

### **Option 3: Replit (SIMPLEST - 2 minutes)**

1. **Go to** https://replit.com

2. **Create new Repl**:
   - Language: Python
   - Upload your project folder

3. **Run**: Click "Run"

4. **Share**: Public URL automatically generated

**Cost**: Free with basic plan

---

### **Option 4: Google Cloud Run (FREE TIER)**

1. **Sign up** at https://console.cloud.google.com

2. **Enable Cloud Run API**

3. **Deploy**:
   ```bash
   gcloud run deploy maize-disease \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Access**: Auto-generated URL

**Cost**: Free tier (2M requests/month)

---

### **Option 5: Azure App Service (FREE TIER)**

1. **Sign up** at https://azure.microsoft.com

2. **Deploy**:
   ```bash
   az webapp up --name maize-disease --runtime "python:3.10"
   ```

3. **Access**: `https://maize-disease.azurewebsites.net`

**Cost**: Free tier available

---

## 🔧 **Configuration Before Going Live**

### **Step 1: Update Backend Config**

Edit `backend/config.py`:
```python
API_HOST = "0.0.0.0"      # Keep as is for deployment
API_PORT = 8000            # Heroku assigns automatically
DEBUG = False              # Disable debug mode
```

### **Step 2: Update Frontend API URL**

Edit `frontend/script.js`:
```javascript
const CONFIG = {
    API_URL: 'https://your-app-name.herokuapp.com',  // Your live backend URL
    MAX_FILE_SIZE: 10 * 1024 * 1024,
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
};
```

### **Step 3: Create .gitignore**

```
__pycache__/
*.pyc
.venv/
*.db
.env
node_modules/
.DS_Store
```

### **Step 4: Create Procfile** (for Heroku)

```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📊 **Recommended: Railway (Best Balance)**

**Why?**
- ✅ Free tier generous ($5/month credit)
- ✅ GitHub integration easy
- ✅ Auto-deploys on push
- ✅ No credit card for free tier
- ✅ One-click rollback

**Steps**:

1. **Create Railway account**: https://railway.app

2. **Connect GitHub** or **Upload Project**

3. **Create 2 Services**:
   - **Backend**: `python -m uvicorn backend.main:app --host 0.0.0.0`
   - **Frontend**: Static file hosting

4. **Set Environment Variables**:
   - `DATABASE_URL` (if needed)
   - `API_URL` (frontend backend URL)

5. **Deploy**: Auto-deploys from Git

6. **Get URL**: Railway provides public URL

---

## 📱 **Get Custom Domain (Optional)**

1. Buy domain at:
   - **Namecheap** (~$5/year)
   - **GoDaddy** (~$10/year)
   - **Google Domains** (~$12/year)

2. Point to your hosting:
   - Update DNS records
   - Platform usually provides instructions

---

## 🔒 **SSL Certificate (HTTPS)**

Most platforms provide **FREE SSL**:
- Heroku ✅
- Railway ✅
- Google Cloud Run ✅
- Azure ✅
- Replit ✅

No additional setup needed!

---

## 📈 **After Going Live**

1. **Monitor**: Check uptime & performance
2. **Backup**: Database backups daily
3. **Updates**: Deploy new models easily
4. **Analytics**: Track usage
5. **Scaling**: Upgrade tier if needed

---

## ⚡ **Quick Start (Railway)**

```bash
cd c:\Users\sandi\OneDrive\Desktop\Leaf

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Connect to Railway
# 1. Go to https://railway.app
# 2. Click "New Project" → "Deploy from GitHub"
# 3. Select your repo
# 4. Done! 🚀
```

---

## 💰 **Cost Comparison**

| Platform | Cost | Easiest | Speed |
|----------|------|---------|-------|
| **Railway** | $5/mo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Heroku** | $7/mo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Google Cloud** | Free | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Azure** | Free | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Replit** | Free | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 **My Recommendation: Railway**

**Best for you because:**
- ✅ Simplest setup
- ✅ Affordable ($5/month with free credit)
- ✅ GitHub auto-deploy
- ✅ One URL for both frontend & backend
- ✅ Great documentation
- ✅ 24/7 uptime

**Total setup time**: ~10 minutes

---

## 📞 **Need Help?**

Once you pick a platform, I can help with:
- ✅ Exact deployment commands
- ✅ Configuration files
- ✅ Domain setup
- ✅ SSL certificates
- ✅ Environment variables

**Let me know which platform you choose!** 🚀

---

**Your app is production-ready. Let's make it live!** 🌾
