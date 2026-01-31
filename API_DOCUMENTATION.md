# API Documentation - Smart Maize Disease Detection System

## Overview

The API is built with **FastAPI** and provides real-time disease detection, explainability, and agronomic recommendations through RESTful endpoints.

**Base URL**: `http://localhost:8000`

---

## Authentication

Currently, the API has **no authentication**. For production deployment, implement:
- API key authentication
- JWT tokens
- OAuth 2.0

---

## API Endpoints

### 1. Health Check

Check if the API is running and healthy.

```http
GET /api/health
```

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

### 2. Predict Disease (Main Endpoint)

Upload an image and get disease prediction with Grad-CAM visualization.

```http
POST /api/predict
Content-Type: multipart/form-data

Body:
- file: <image_file> (JPG, PNG, WebP, max 10MB)
```

**Response (200 OK)**:
```json
{
  "success": true,
  "disease": "Maize Common Rust",
  "confidence": 0.92,
  "heatmap": "static/heatmaps/heatmap_image_20240115_103000.png",
  "recommendation": {
    "cause": "Fungal infection caused by Puccinia sorghi. Develops in moist conditions.",
    "pesticide": "Mancozeb 2g/L or Azoxystrobin 0.5mL/L every 10-14 days",
    "fertilizer": "Apply Potassium-rich fertilizer (NPK 10-20-30)",
    "prevention": "Remove infected leaves, improve air circulation, avoid excess moisture"
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "Invalid file type. Please upload JPG, PNG, or WebP image",
  "status_code": 400
}
```

**Response (500 Internal Server Error)**:
```json
{
  "success": false,
  "error": "Prediction failed: <error_message>",
  "status_code": 500
}
```

**Parameters**:
- `file` (required): Image file in multipart form data

**Supported Formats**:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

**Max File Size**: 10 MB

**Response Time**: < 1.5 seconds (typically)

---

### 3. Get Disease Recommendations

Retrieve agronomic recommendations for a specific disease.

```http
GET /api/recommendations/{disease_name}
```

**Path Parameters**:
- `disease_name` (string, URL encoded): Name of the disease

**Example**:
```
GET /api/recommendations/Maize%20Common%20Rust
```

**Response (200 OK)**:
```json
{
  "success": true,
  "disease": "Maize Common Rust",
  "recommendation": {
    "cause": "Fungal infection caused by Puccinia sorghi...",
    "pesticide": "Mancozeb 2g/L...",
    "fertilizer": "NPK 10-20-30...",
    "prevention": "Remove infected leaves..."
  }
}
```

**Response (404 Not Found)**:
```json
{
  "success": false,
  "error": "Disease not found",
  "status_code": 404
}
```

---

## Supported Diseases

The system recognizes the following diseases:

| ID | Disease Name | Symptoms |
|----|--------------|----------|
| 1 | Healthy | No disease present |
| 2 | Maize Common Rust | Reddish-brown circular pustules |
| 3 | Maize Southern Leaf Blight | Elongated tan lesions with dark border |
| 4 | Maize Northern Leaf Blight | Long narrow grayish lesions |
| 5 | Maize Gray Leaf Spot | Gray rectangular spots with dark margin |
| 6 | Maize Anthracnose | Dark brown irregular lesions |
| 7 | Maize Eyespot | Circular spots with concentric rings |
| 8 | Maize Turcicum Leaf Blight | Elongated lesions with chlorotic halo |

---

## Response Schema

### Prediction Response

```json
{
  "success": boolean,
  "disease": string,
  "confidence": number (0-1),
  "heatmap": string (URL) or null,
  "recommendation": {
    "cause": string,
    "pesticide": string,
    "fertilizer": string,
    "prevention": string
  },
  "timestamp": string (ISO 8601)
}
```

### Recommendation Response

```json
{
  "success": boolean,
  "disease": string,
  "recommendation": {
    "cause": string,
    "pesticide": string,
    "fertilizer": string,
    "prevention": string
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": string,
  "status_code": number
}
```

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Request successful |
| 400 | Bad request (invalid file, missing parameters) |
| 404 | Resource not found (disease not found) |
| 500 | Internal server error |

---

## Usage Examples

### cURL

**Health Check**:
```bash
curl http://localhost:8000/api/health
```

**Predict Disease**:
```bash
curl -X POST -F "file=@leaf_image.jpg" http://localhost:8000/api/predict
```

**Get Recommendations**:
```bash
curl http://localhost:8000/api/recommendations/Maize%20Common%20Rust
```

### Python Requests

```python
import requests
import json

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Predict
files = {"file": open("leaf_image.jpg", "rb")}
response = requests.post("http://localhost:8000/api/predict", files=files)
result = response.json()

print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Heatmap: {result['heatmap']}")

# Recommendations
response = requests.get(f"http://localhost:8000/api/recommendations/{result['disease']}")
print(json.dumps(response.json()['recommendation'], indent=2))
```

### JavaScript/Fetch API

```javascript
// Predict disease
async function predictDisease(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);
    
    const response = await fetch("http://localhost:8000/api/predict", {
        method: "POST",
        body: formData
    });
    
    const result = await response.json();
    return result;
}

// Usage
const fileInput = document.getElementById("imageInput");
const prediction = await predictDisease(fileInput.files[0]);
console.log(prediction.disease, prediction.confidence);
```

### JavaScript/Async Await

```javascript
// Get recommendations
async function getRecommendations(diseaseName) {
    const response = await fetch(
        `http://localhost:8000/api/recommendations/${encodeURIComponent(diseaseName)}`
    );
    
    const data = await response.json();
    return data.recommendation;
}

// Usage
const recs = await getRecommendations("Maize Common Rust");
console.log(recs.pesticide);
```

---

## Rate Limiting

Currently **not implemented**. For production, add:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/predict")
@limiter.limit("10/minute")  # 10 requests per minute
async def predict(request: Request, file: UploadFile):
    ...
```

---

## CORS Configuration

The API currently allows all origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

For production, restrict to specific origins:

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

---

## Error Handling

The API returns meaningful error messages:

**File Type Error**:
```json
{
  "success": false,
  "error": "Invalid file type. Please upload JPG, PNG, or WebP image",
  "status_code": 400
}
```

**File Size Error**:
```json
{
  "success": false,
  "error": "File size exceeds 10MB limit",
  "status_code": 400
}
```

**Prediction Error**:
```json
{
  "success": false,
  "error": "Prediction failed: <detailed_error>",
  "status_code": 500
}
```

---

## Performance Metrics

Typical response times:

| Operation | Time |
|-----------|------|
| Image validation | 10-50ms |
| Image preprocessing | 50-100ms |
| Model inference (CPU) | 800-1000ms |
| Model inference (GPU) | 100-200ms |
| Grad-CAM generation | 200-300ms |
| Database query | 10-50ms |
| **Total (CPU)** | **1.0-1.5s** |
| **Total (GPU)** | **0.5-0.8s** |

---

## Database Schema

### predictions table

```sql
CREATE TABLE predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_name TEXT NOT NULL,
  disease TEXT NOT NULL,
  confidence REAL NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### recommendations table

```sql
CREATE TABLE recommendations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_name TEXT UNIQUE NOT NULL,
  cause TEXT NOT NULL,
  pesticide TEXT NOT NULL,
  fertilizer TEXT NOT NULL,
  prevention TEXT NOT NULL
);
```

---

## File Upload Details

### Accepted Formats
- **JPEG**: .jpg, .jpeg
- **PNG**: .png
- **WebP**: .webp

### Size Limits
- Maximum: 10 MB
- Recommended: < 5 MB for faster processing

### Image Preprocessing
1. Read image (OpenCV)
2. Convert to RGB (if needed)
3. Resize to 224×224 pixels
4. Normalize to [0, 1] range
5. Add batch dimension

---

## Explainability (Grad-CAM)

The `heatmap` field contains a URL to the Grad-CAM visualization:

- **Red regions**: High influence on prediction
- **Blue regions**: Low influence on prediction
- **Colors**: Heat mapped from cold (blue) to hot (red)

This helps understand *why* the model made a specific prediction.

---

## Troubleshooting

### "Connection refused"
- Check if server is running: `python backend/main.py`
- Verify port 8000 is not blocked
- Check firewall settings

### "File type error"
- Only JPG, PNG, WebP supported
- Check file extension is correct
- Try converting image format

### "Request timeout"
- Server might be busy
- Try uploading smaller image
- Check network connection

### "Empty heatmap"
- Model not found (using mock predictions)
- Place `.h5` or `.pt` file in `backend/models/`
- Restart server

---

## Future Enhancements

- [ ] Batch prediction API
- [ ] Video stream analysis
- [ ] Model confidence calibration
- [ ] Advanced filtering options
- [ ] Export functionality
- [ ] User authentication
- [ ] Request logging
- [ ] Webhook support

---

## Support

For issues or questions, check:
1. Server logs: `backend/main.py` output
2. Database: `backend/database.db`
3. Uploaded files: `static/uploads/`
4. Generated heatmaps: `static/heatmaps/`

---

**API Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Framework**: FastAPI 0.104.1
