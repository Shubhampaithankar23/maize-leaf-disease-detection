# 🌾 Smart Maize Leaf Disease Detection System

A real-time web application for **Explainable Deep Learning–based Maize Leaf Disease Detection** with agronomic recommendations using **XAI (Explainable AI)** technology.

## 📋 Features

### 🎯 Core Functionality
- **Real-time Disease Detection**: Upload maize leaf images and get instant predictions
- **Explainable AI (Grad-CAM)**: Visual heatmaps showing which regions influenced the diagnosis
- **Agronomic Recommendations**: Pesticide, fertilizer, and prevention suggestions for each disease
- **Prediction History**: SQLite database stores all predictions and recommendations
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🎨 UI/UX
- **Modern Dark Mode**: Agriculture-inspired black background with green accents
- **Card-based Layout**: Clean, organized interface
- **Smooth Animations**: Professional hover effects and transitions
- **Accessibility**: Keyboard shortcuts and semantic HTML

### 🤖 AI/ML Features
- **CNN Architecture**: Pre-trained models (TensorFlow, PyTorch)
- **Grad-CAM Visualization**: Explainable predictions with attention maps
- **Input Size**: 224×224 normalized images
- **Mock Model Support**: Works without pre-trained model for demonstration

### 💾 Database
- **SQLite Integration**: Lightweight, zero-config database
- **Prediction Storage**: Image name, disease, confidence, timestamp
- **Recommendations Table**: Disease-specific treatment advice
- **Statistics Tracking**: Historical data analysis

## 🏗️ Project Structure

```
maize_ai_webapp/
│
├── backend/
│   ├── main.py                 # FastAPI application & API routes
│   ├── config.py               # Configuration settings
│   ├── model_loader.py         # CNN model loading & inference
│   ├── gradcam.py              # Grad-CAM heatmap generation
│   ├── database.py             # SQLite database management
│   └── database.db             # SQLite database file
│
├── frontend/
│   ├── index.html              # Main HTML interface
│   ├── style.css               # Dark mode styling
│   └── script.js               # Frontend JavaScript logic
│
├── static/
│   ├── uploads/                # Uploaded image storage
│   └── heatmaps/               # Generated heatmap visualizations
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone/Download the project**
```bash
cd maize_ai_webapp
```

2. **Create virtual environment (Optional but recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Start the FastAPI backend**
```bash
cd backend
python main.py
```
The API will run on `http://localhost:8000`

2. **Open the frontend**
```bash
# Open in your browser
frontend/index.html
```
Or serve it with a local server:
```bash
# Python 3
python -m http.server 8080 --directory frontend

# Then open: http://localhost:8080
```

## 📊 Supported Diseases

The system can detect the following maize leaf diseases:

1. **Healthy** - No disease detected
2. **Maize Common Rust** - Puccinia sorghi fungal infection
3. **Maize Southern Leaf Blight** - Bipolaris maydis fungal infection
4. **Maize Northern Leaf Blight** - Exserohilum turcicum infection
5. **Maize Gray Leaf Spot** - Cercospora zeae-maydis fungal disease
6. **Maize Anthracnose** - Colletotrichum graminicola infection
7. **Maize Eyespot** - Kabatiella zeae fungal disease
8. **Maize Turcicum Leaf Blight** - Exserohilum turcicum leaf blight

## 🎯 API Endpoints

### Predict Disease
```http
POST /api/predict
Content-Type: multipart/form-data

Body: file (image file)

Response:
{
  "success": true,
  "disease": "Maize Common Rust",
  "confidence": 0.92,
  "heatmap": "static/heatmaps/heatmap_image_20240101_120000.png",
  "recommendation": {
    "cause": "Fungal infection...",
    "pesticide": "Mancozeb 2g/L...",
    "fertilizer": "NPK 10-20-30...",
    "prevention": "Remove infected leaves..."
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Get Recommendations
```http
GET /api/recommendations/{disease_name}

Response:
{
  "success": true,
  "disease": "Maize Common Rust",
  "recommendation": {
    "cause": "...",
    "pesticide": "...",
    "fertilizer": "...",
    "prevention": "..."
  }
}
```

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# Image settings
MODEL_INPUT_SIZE = 224
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# API
API_HOST = "0.0.0.0"
API_PORT = 8000

# Database
DATABASE_PATH = "backend/database.db"
```

## 🤖 Using Pre-trained Models

### TensorFlow/Keras Model
1. Place `.h5` file in `backend/models/` directory
2. Model will auto-load on startup

### PyTorch Model
1. Place `.pt` file in `backend/models/` directory
2. Model will auto-load on startup

### Default Behavior
If no model found, system uses **mock predictions** for demonstration.

## 🔍 Understanding Grad-CAM

**Grad-CAM (Gradient-weighted Class Activation Mapping)** is an explainability technique that:

1. Highlights regions that influenced the prediction
2. Shows which leaf areas the model focused on
3. Provides visual evidence for the diagnosis
4. Helps validate model behavior

The heatmap shows:
- **Red regions**: High influence on prediction
- **Blue regions**: Low influence on prediction

## 💾 Database Schema

### Predictions Table
```sql
CREATE TABLE predictions (
  id INTEGER PRIMARY KEY,
  image_name TEXT,
  disease TEXT,
  confidence REAL,
  timestamp DATETIME
)
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
  id INTEGER PRIMARY KEY,
  disease_name TEXT UNIQUE,
  cause TEXT,
  pesticide TEXT,
  fertilizer TEXT,
  prevention TEXT
)
```

## 🎨 Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Background | Black | #0b0b0b |
| Primary Green | Bright Green | #00c853 |
| Secondary Green | Dark Green | #2e7d32 |
| Text | Light Gray | #e0e0e0 |
| Card Background | Dark Gray | #121212 |

## 🔐 Security Considerations

- Validate file uploads (type, size)
- Sanitize file names
- Use CORS for cross-origin requests
- Store sensitive data securely
- Implement rate limiting for production

## 📈 Performance Optimization

- Image preprocessing: ~50-100ms
- Model inference: <500ms (GPU) or <1000ms (CPU)
- Grad-CAM generation: ~200-300ms
- **Total response time**: <1 second (typical)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### CORS Errors
Ensure frontend and backend are properly configured in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
```

### Model Not Loading
Check `backend/models/` directory contains a valid `.h5` or `.pt` file. System will use mock predictions otherwise.

### Image Upload Issues
- Check max file size (10MB default)
- Ensure format is JPG, PNG, or WebP
- Verify `static/uploads/` directory exists

## 📚 Dependencies

- **FastAPI**: Modern web framework for API
- **TensorFlow/Keras**: Deep learning framework
- **OpenCV**: Image processing
- **NumPy**: Numerical computing
- **Uvicorn**: ASGI server
- **SQLite3**: Database (built-in)

## 🎓 Educational Value

This system demonstrates:
- Deep learning inference in production
- Explainable AI (XAI) with Grad-CAM
- RESTful API design
- Frontend-backend integration
- Agricultural AI applications
- Modern web development

## 🚢 Deployment Options

### Local Development
```bash
python backend/main.py
```

### Production (Gunicorn + Uvicorn)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

### Docker Deployment
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📄 License

This project is open-source and available for educational and research purposes.

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Examine backend logs

## 🔮 Future Enhancements

- [ ] Multi-GPU support
- [ ] Real-time video analysis
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Integration with IoT sensors
- [ ] Cloud deployment (AWS/GCP)
- [ ] Multi-language support
- [ ] Offline mode with service workers

---

**Built with ❤️ for precision agriculture and sustainable farming**

*Smart Maize Leaf Disease Detection System v1.0.0*
