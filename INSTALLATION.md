# 🚀 Installation & Deployment Guide

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies
- **Network**: Internet for dependency installation
- **OS**: Windows, macOS, or Linux

---

## 📥 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\sandi\OneDrive\Desktop\Leaf
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

**Option A: Full Installation (with ML libraries)**
```bash
pip install -r requirements.txt
```

**Option B: Minimal Installation (lightweight)**
```bash
pip install -r requirements-minimal.txt
```

**Note**: Full installation includes TensorFlow and PyTorch (larger download). Minimal version works with mock predictions.

### Step 4: Verify Installation

```bash
python test_system.py
```

Expected output:
```
✅ All systems operational!
🚀 Ready to run:
   1. Start backend: cd backend && python main.py
   2. Open frontend: frontend/index.html
```

---

## 🎬 Running the Application

### Method 1: Basic Setup (Easiest)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2 - Frontend:**
```bash
# Just open this file in your browser:
frontend/index.html
```

Or use Python's built-in server:
```bash
python -m http.server 8080 --directory frontend
# Then visit: http://localhost:8080
```

### Method 2: Development Mode

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag auto-restarts on code changes.

### Method 3: Production Mode

```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2
```

Requires: `pip install gunicorn`

---

## 🐳 Docker Installation

### Option 1: Build Docker Image

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "backend/main.py"]
```

Build and run:
```bash
# Build image
docker build -t maize-disease-detection .

# Run container
docker run -p 8000:8000 -v $(pwd)/static:/app/static maize-disease-detection
```

### Option 2: Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./static:/app/static
      - ./backend/database.db:/app/backend/database.db
    environment:
      - PYTHONUNBUFFERED=1

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
```

Run:
```bash
docker-compose up
```

---

## ☁️ Cloud Deployment

### AWS EC2

1. Launch Ubuntu 20.04 LTS instance
2. SSH into instance
3. Install Python:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```
4. Clone/upload project
5. Follow installation steps
6. Run with PM2 or Systemd

### Heroku

Create `Procfile`:
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

Deploy:
```bash
heroku create app-name
heroku config:set PYTHONUNBUFFERED=1
git push heroku main
```

### Google Cloud Run

```bash
gcloud run deploy maize-disease \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Azure App Service

```bash
az webapp up --name maize-disease --runtime "python:3.10"
```

---

## 🔧 Configuration for Deployment

### Backend Configuration (backend/config.py)

```python
# Change these for production
API_HOST = "0.0.0.0"      # Accessible from all IPs
API_PORT = 8000            # Change if needed
DEBUG = False              # Disable debug mode
```

### CORS Settings (backend/main.py)

For production, restrict CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

### Frontend API URL (frontend/script.js)

Update:

```javascript
const CONFIG = {
    API_URL: 'http://localhost:8000',  // Change for production
    // ...
}
```

Change to:

```javascript
const CONFIG = {
    API_URL: 'https://api.yourdomain.com',
    // ...
}
```

---

## 📊 Using Pre-trained Models

### TensorFlow/Keras Model

1. Save your trained model:
   ```python
   # In your training script
   model.save('backend/models/maize_disease_model.h5')
   ```

2. The system auto-loads `.h5` files on startup

### PyTorch Model

1. Save your model:
   ```python
   torch.save(model, 'backend/models/maize_disease_model.pt')
   ```

2. The system auto-loads `.pt` files on startup

### Model Requirements

- Input size: 224×224 pixels
- Output: 8 disease classes
- Input format: Batch of RGB images (normalized 0-1)
- Output format: Logits or probabilities for 8 classes

---

## ✅ Verification Checklist

After installation, verify everything:

```bash
# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list

# Test database
python -c "from backend.database import init_db; init_db(); print('✅ Database OK')"

# Test model loader
python -c "from backend.model_loader import _mock_prediction; print(_mock_prediction())"

# Test API startup
cd backend && timeout 5 python main.py 2>&1 | head -5
```

---

## 🔍 Troubleshooting Installation

### Issue: Python not found
```bash
# Windows
python --version

# macOS/Linux
python3 --version
```

**Solution**: Install Python 3.8+ from python.org

### Issue: pip not found
```bash
# Install pip
python -m ensurepip --upgrade
```

### Issue: Permission denied
```bash
# macOS/Linux
sudo pip install -r requirements.txt

# Or use user installation
pip install --user -r requirements.txt
```

### Issue: Package installation fails
```bash
# Update pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Try again
pip install -r requirements.txt
```

### Issue: Virtual environment activation failed
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🚀 Quick Test Script

After installation, run:

```bash
python test_system.py
```

This verifies:
- ✅ All imports available
- ✅ Directory structure correct
- ✅ Configuration loads
- ✅ Database initializes
- ✅ Model loader works
- ✅ Mock predictions work

---

## 📈 Performance Optimization

### For Development
```bash
# Auto-reload on changes
python -m uvicorn backend.main:app --reload
```

### For Production
```bash
# Multiple workers for concurrency
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

### With GPU Support
```bash
# Install CUDA and TensorFlow-GPU
pip install tensorflow-gpu
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 🛡️ Production Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed successfully
- [ ] test_system.py passes all tests
- [ ] Backend starts without errors
- [ ] Frontend displays correctly
- [ ] API responds to requests
- [ ] Database initialized
- [ ] CORS configured properly
- [ ] Error handling tested
- [ ] File uploads working
- [ ] Heatmap generation verified
- [ ] Recommendations displayed
- [ ] Performance acceptable
- [ ] Security settings configured

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs**: Look at backend console output
2. **Run test system**: `python test_system.py`
3. **Review documentation**: 
   - QUICKSTART.md
   - README.md
   - API_DOCUMENTATION.md
4. **Check database**: `backend/database.db`
5. **Verify files**: See PROJECT_COMPLETION.md

---

## 🎓 Next Steps After Installation

1. **Test the System**
   - Upload a sample image
   - Verify predictions work
   - Check heatmap generation
   - Test recommendations

2. **Customize**
   - Add your own model
   - Modify disease recommendations
   - Adjust UI colors/styling
   - Add authentication

3. **Deploy**
   - Choose hosting platform
   - Configure domain/SSL
   - Set up monitoring
   - Enable logging

4. **Extend**
   - Add batch processing
   - Implement user accounts
   - Build analytics dashboard
   - Integrate with other systems

---

**Installation Complete! Ready to deploy.** 🚀

For more details, see:
- QUICKSTART.md - Fast start guide
- README.md - Full documentation
- API_DOCUMENTATION.md - API reference
