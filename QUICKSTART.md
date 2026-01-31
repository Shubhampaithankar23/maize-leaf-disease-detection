# 🚀 Quick Start Guide - Smart Maize Disease Detection System

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
cd maize_ai_webapp
pip install -r requirements.txt
```

### Step 2: Start the Backend Server
```bash
cd backend
python main.py
```

✅ You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Open the Frontend
Open in your browser:
```
frontend/index.html
```

Or run a simple server:
```bash
# In a new terminal, from the project root
python -m http.server 8080 --directory frontend
# Then visit: http://localhost:8080
```

---

## 🧪 Testing the Application

### Using the Web Interface

1. **Upload an Image**
   - Click "Select Image" or drag & drop
   - Supported formats: JPG, PNG, WebP
   - Max size: 10MB

2. **View Results**
   - Disease name and confidence score
   - Grad-CAM heatmap visualization
   - Agronomic recommendations

3. **Check Recommendations**
   - Disease cause explanation
   - Suggested pesticide treatment
   - Fertilizer advice
   - Preventive measures

### Testing with cURL (Backend)

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test prediction (requires image file)
curl -X POST -F "file=@your_image.jpg" http://localhost:8000/api/predict

# Get specific disease recommendations
curl http://localhost:8000/api/recommendations/Maize%20Common%20Rust
```

### Python Testing Script

```python
import requests
import json

# Health check
response = requests.get("http://localhost:8000/api/health")
print("Health:", response.json())

# Predict disease
with open("sample_image.jpg", "rb") as img:
    files = {"file": img}
    response = requests.post("http://localhost:8000/api/predict", files=files)
    result = response.json()
    
print("Disease:", result["disease"])
print("Confidence:", f"{result['confidence']:.2%}")
print("Recommendation:")
print(json.dumps(result["recommendation"], indent=2))
```

---

## 🎯 Supported Maize Diseases

The model can detect:

| Disease | Symptoms |
|---------|----------|
| **Healthy** | No visible disease |
| **Common Rust** | Reddish-brown pustules |
| **Southern Leaf Blight** | Elongated tan lesions |
| **Northern Leaf Blight** | Long narrow lesions |
| **Gray Leaf Spot** | Gray rectangular spots |
| **Anthracnose** | Dark lesions |
| **Eyespot** | Target-like circular spots |
| **Turcicum Leaf Blight** | Elongated lesions |

---

## 📁 File Structure Explained

```
📦 maize_ai_webapp/
│
├── 📂 backend/                    # Python FastAPI backend
│   ├── main.py                    # API endpoints (POST /api/predict)
│   ├── model_loader.py            # Load CNN model, make predictions
│   ├── gradcam.py                 # Grad-CAM explainability
│   ├── database.py                # SQLite operations
│   ├── config.py                  # Settings (image size, diseases, etc)
│   └── database.db                # Predictions history
│
├── 📂 frontend/                   # HTML/CSS/JS interface
│   ├── index.html                 # Main UI layout
│   ├── style.css                  # Dark mode styling
│   └── script.js                  # Upload & prediction logic
│
├── 📂 static/                     # Static files
│   ├── uploads/                   # Saved user images
│   └── heatmaps/                  # Generated visualizations
│
├── requirements.txt               # Python dependencies
├── README.md                      # Full documentation
└── QUICKSTART.md                 # This file
```

---

## 🔧 Configuration

### Model Settings (backend/config.py)

```python
# Image input size for CNN
MODEL_INPUT_SIZE = 224

# Allowed image types
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# Max upload size
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### API Settings

```python
# Server configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
```

### UI Colors (frontend/style.css)

```css
--bg-primary: #0b0b0b;           /* Black background */
--color-primary: #00c853;        /* Bright green */
--color-secondary: #2e7d32;      /* Dark green */
--text-primary: #e0e0e0;         /* Light text */
```

---

## 🤖 Using Your Own Model

### Option 1: TensorFlow/Keras (.h5)

1. Save your trained model:
```python
model.save('backend/models/maize_disease_model.h5')
```

2. Model auto-loads on startup

### Option 2: PyTorch (.pt)

1. Save your model:
```python
torch.save(model, 'backend/models/maize_disease_model.pt')
```

2. System detects and loads it

### Option 3: Demo Mode

If no model found, system uses **mock predictions**:
- Random disease selection
- Realistic confidence scores
- Generated heatmaps

---

## 🐛 Common Issues & Solutions

### Issue: "Port 8000 already in use"
```bash
# Change port in backend/main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Issue: CORS errors
Frontend can't reach backend:
```python
# Check CORS is enabled in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
```

### Issue: Image upload fails
Check:
- File is JPG/PNG/WebP
- File size < 10MB
- `static/uploads/` directory exists
- File permissions are correct

### Issue: Model not loading
Check:
- `.h5` or `.pt` file in `backend/models/`
- TensorFlow/PyTorch installed
- File is not corrupted

---

## 📊 Database

### Viewing Predictions

```python
from backend.database import get_prediction_history, get_statistics

# Last 10 predictions
history = get_prediction_history(limit=10)

# Statistics
stats = get_statistics()
print(f"Total: {stats['total_predictions']}")
print(f"By disease: {stats['disease_distribution']}")
```

### Database File
- Location: `backend/database.db`
- Format: SQLite 3
- Tables: `predictions`, `recommendations`

---

## 🚀 Performance Tips

| Operation | Time |
|-----------|------|
| Image preprocessing | 50-100ms |
| Model inference (CPU) | 800-1000ms |
| Model inference (GPU) | 100-200ms |
| Grad-CAM generation | 200-300ms |
| **Total response** | **< 1.5 seconds** |

To improve speed:
1. Use GPU (NVIDIA CUDA)
2. Reduce image size
3. Use quantized models
4. Enable model caching

---

## 🎓 Learning Resources

### Understanding Grad-CAM
Grad-CAM visualizes which regions of the image influenced the model's decision by:
1. Computing gradients of predicted class
2. Weighting feature maps by importance
3. Overlaying on original image in red (high importance) to blue (low importance)

### Understanding the System

1. **Image Upload** → Validation
2. **Preprocessing** → Resize to 224×224, normalize
3. **Inference** → CNN predicts disease (outputs: name + confidence)
4. **Grad-CAM** → Generate explanation heatmap
5. **Recommendations** → Query database for advice
6. **Response** → Return results to frontend

---

## 📱 Responsive Design

The system works on:
- ✅ Desktop (1920×1080+)
- ✅ Tablet (768×1024)
- ✅ Mobile (320×640)

All UI elements automatically scale and reflow.

---

## 🔐 Security Notes

For production deployment:
1. Validate file uploads strictly
2. Implement rate limiting
3. Add authentication
4. Use HTTPS
5. Sanitize file names
6. Store sensitive data securely

---

## 📈 Next Steps

1. **Custom Model**: Train on your own dataset
2. **Database**: Query and visualize predictions
3. **API Integration**: Connect to mobile app
4. **Cloud Deployment**: Deploy to AWS/GCP/Azure
5. **Advanced Analytics**: Build prediction dashboard

---

## ❓ Frequently Asked Questions

**Q: Can I use this without GPU?**
A: Yes! CPU inference is slower but works fine for single images.

**Q: How accurate is the demo?**
A: Demo uses mock predictions. Real accuracy depends on training data.

**Q: Can I modify recommendations?**
A: Yes, edit `backend/database.py` or update via database directly.

**Q: How do I add new diseases?**
A: Add to `DISEASE_CLASSES` in `config.py` and retrain model.

**Q: Can I use this offline?**
A: Yes! System works completely offline after setup.

---

## 🎉 You're Ready!

Start the backend, open the frontend, and test the system. The mock model will give realistic results for demonstration.

```bash
# Terminal 1: Start backend
cd backend
python main.py

# Terminal 2: Open frontend
# Open: frontend/index.html in browser
```

**Happy detecting!** 🌾🤖

---

*For more details, see README.md*
