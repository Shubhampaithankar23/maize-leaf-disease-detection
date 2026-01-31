# ⚡ Quick Start Commands

## 🚀 30-Second Setup

```bash
# 1. Navigate to project
cd c:\Users\sandi\OneDrive\Desktop\Leaf

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run system test
python test_system.py
```

## ▶️ Running the Application

### Terminal 1: Start Backend
```bash
cd backend
python main.py
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend

**Option A** - Direct Open:
```bash
# Just open this file in your browser
frontend/index.html
```

**Option B** - Local Server:
```bash
python -m http.server 8080 --directory frontend
# Visit: http://localhost:8080
```

---

## ✅ Verify Installation

```bash
# Test imports
python -c "import fastapi, cv2, numpy; print('✅ All imports OK')"

# Test API health
curl http://localhost:8000/api/health

# Test mock prediction
python -c "from backend.model_loader import _mock_prediction; print(_mock_prediction())"
```

---

## 📱 Expected Output

### When Backend Starts
```
INFO:     Started server process [1234]
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     Database initialized successfully
INFO:     Model loaded successfully (or: Using mock model)
INFO:     System ready for predictions
```

### When Frontend Loads
- Title: "Smart Maize Leaf Disease Detection System"
- Upload area with green accents
- Loading spinner animation
- Clean dark mode interface

### When You Upload an Image
- See disease prediction
- Confidence score bar
- Grad-CAM heatmap
- Agronomic recommendations

---

## 🧪 Test Commands

```bash
# 1. Health check
curl http://localhost:8000/api/health

# 2. Get API info
curl http://localhost:8000/

# 3. Upload image (requires image file)
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/predict

# 4. Get recommendations
curl http://localhost:8000/api/recommendations/Healthy
```

---

## 🔧 Useful Commands

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Verify Python Version
```bash
python --version  # Should be 3.8+
```

### Clear Python Cache
```bash
pip cache purge
```

### Run in Development Mode
```bash
cd backend
python -m uvicorn main:app --reload
```

### Stop Backend Server
```bash
Ctrl + C (in terminal)
```

### Check Port Usage
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

### Change Port
```bash
# Edit backend/main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

---

## 🐛 Troubleshooting Commands

### Port Already in Use
```bash
# Windows: Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Clear Database
```bash
# Delete and recreate
rm backend/database.db
# Database auto-creates on next run
```

### Reinstall Dependencies
```bash
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Reset Virtual Environment
```bash
# Remove old venv
rm -r venv

# Create new
python -m venv venv

# Activate and install
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 📊 Monitor Commands

### Check System Resources
```bash
# Windows
wmic process where name="python.exe" get WorkingSetSize

# macOS/Linux
ps aux | grep python
```

### View Backend Logs
```bash
# Just watch terminal output (already enabled)
# Use Ctrl+C to stop
```

### View Database
```bash
python -c "from backend.database import get_prediction_history; print(get_prediction_history())"
```

---

## 🚀 Deployment Commands

### Docker Build
```bash
docker build -t maize-disease-detection .
docker run -p 8000:8000 maize-disease-detection
```

### Gunicorn Production
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

### Python HTTP Server (Frontend)
```bash
python -m http.server 8080 --directory frontend
```

---

## 📁 Directory Commands

### Navigate Project
```bash
# Go to project
cd c:\Users\sandi\OneDrive\Desktop\Leaf

# Go to backend
cd backend

# Go to frontend
cd ../frontend

# Go back to root
cd ..
```

### List Files
```bash
# Windows
dir

# macOS/Linux
ls -la
```

### Check Directory Structure
```bash
# Windows
tree /F

# macOS/Linux
tree
```

---

## 🔐 Security Commands

### Set File Permissions
```bash
# macOS/Linux
chmod 644 frontend/*
chmod 755 backend/
chmod 600 backend/database.db
```

### Create .env File
```bash
# Create (optional for sensitive data)
echo "API_URL=http://localhost:8000" > .env
```

---

## 📈 Performance Commands

### Test Response Time
```bash
# Simple timing
time curl http://localhost:8000/api/health

# More detailed (requires 'hyperfine')
pip install hyperfine
hyperfine 'curl http://localhost:8000/api/health'
```

---

## 🎯 Complete Workflow

```bash
# 1. Navigate
cd c:\Users\sandi\OneDrive\Desktop\Leaf

# 2. Create & activate venv
python -m venv venv
venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Test
python test_system.py

# 5. Start backend (Terminal 1)
cd backend
python main.py

# 6. Start frontend (Terminal 2)
python -m http.server 8080 --directory ../frontend

# 7. Open browser
# Visit: http://localhost:8080

# 8. Upload image and test!
```

---

## 💡 Pro Tips

### Auto-reload on Changes
```bash
# Install
pip install python-dotenv

# Run
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Multiple Servers
```bash
# Backend on 8000
python -m uvicorn backend.main:app --port 8000

# Frontend on 8080
python -m http.server 8080 --directory frontend

# API docs on localhost:8000/docs
```

### Testing Script
```bash
# Verify everything works
python test_system.py

# Output: 
# ✅ All systems operational!
```

---

## 🆘 Emergency Help

### Reset Everything
```bash
# Remove generated files
rm -rf backend/database.db
rm -rf static/uploads/*
rm -rf static/heatmaps/*
rm -rf venv

# Reinstall
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Check Installation
```bash
# Verify each component
python test_system.py
```

### View Configuration
```bash
python -c "from backend.config import *; print(f'Input size: {MODEL_INPUT_SIZE}')"
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start backend | `cd backend && python main.py` |
| Start frontend | `python -m http.server 8080 --directory frontend` |
| Run tests | `python test_system.py` |
| Test API | `curl http://localhost:8000/api/health` |
| Check status | `curl http://localhost:8000/` |
| View API docs | Open `http://localhost:8000/docs` |
| Upload file | `curl -X POST -F "file=@image.jpg" http://localhost:8000/api/predict` |
| Get recommendations | `curl http://localhost:8000/api/recommendations/Healthy` |

---

## 🎉 You're All Set!

Everything is ready to use. Just follow the Quick Start section above.

```bash
# In one command (after setup):
cd backend && python main.py
# Then open: frontend/index.html in browser
```

**That's it! Start detecting diseases!** 🌾🤖

---

*For more info, see README.md, QUICKSTART.md, or INSTALLATION.md*
