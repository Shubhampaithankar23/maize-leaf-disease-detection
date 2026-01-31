"""
Configuration settings for the application
"""

import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent
UPLOAD_FOLDER = PROJECT_ROOT / "static" / "uploads"
HEATMAP_FOLDER = PROJECT_ROOT / "static" / "heatmaps"
MODEL_PATH = BACKEND_DIR / "models"

# Create directories if they don't exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
HEATMAP_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_PATH = BACKEND_DIR / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Model configuration
MODEL_INPUT_SIZE = 224
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Disease classes (for classification model)
DISEASE_CLASSES = [
    "Healthy",
    "Maize Common Rust",
    "Maize Southern Leaf Blight",
    "Maize Northern Leaf Blight",
    "Maize Gray Leaf Spot",
    "Maize Anthracnose",
    "Maize Eyespot",
    "Maize Turcicum Leaf Blight"
]

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# Confidence threshold for predictions
CONFIDENCE_THRESHOLD = 0.5
