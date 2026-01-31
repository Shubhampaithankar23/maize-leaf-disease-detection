"""
Demo/Testing Script - Quick verification of the system
Run this to test all components before deployment
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import cv2
        print("✅ OpenCV")
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    
    try:
        import numpy
        print("✅ NumPy")
    except ImportError:
        print("❌ NumPy not installed")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    print("✅ All core imports successful\n")
    return True

def test_directories():
    """Test if all required directories exist"""
    print("📂 Testing directory structure...")
    
    required_dirs = [
        "backend",
        "frontend",
        "static/uploads",
        "static/heatmaps"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - Creating...")
            os.makedirs(dir_path, exist_ok=True)
    
    print("✅ All directories verified\n")
    return True

def test_files():
    """Test if all required files exist"""
    print("📄 Testing required files...")
    
    required_files = [
        "backend/main.py",
        "backend/model_loader.py",
        "backend/gradcam.py",
        "backend/database.py",
        "backend/config.py",
        "frontend/index.html",
        "frontend/style.css",
        "frontend/script.js",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    print()
    return all_exist

def test_config():
    """Test if configuration loads correctly"""
    print("⚙️  Testing configuration...")
    
    try:
        from backend.config import (
            MODEL_INPUT_SIZE,
            DISEASE_CLASSES,
            UPLOAD_FOLDER,
            HEATMAP_FOLDER,
            DATABASE_PATH
        )
        
        print(f"✅ Model input size: {MODEL_INPUT_SIZE}×{MODEL_INPUT_SIZE}")
        print(f"✅ Disease classes: {len(DISEASE_CLASSES)}")
        print(f"✅ Upload folder: {UPLOAD_FOLDER}")
        print(f"✅ Heatmap folder: {HEATMAP_FOLDER}")
        print(f"✅ Database: {DATABASE_PATH}")
        print("✅ Configuration loaded successfully\n")
        return True
    
    except Exception as e:
        print(f"❌ Configuration error: {e}\n")
        return False

def test_database():
    """Test database initialization"""
    print("💾 Testing database...")
    
    try:
        from backend.database import init_db, get_all_diseases
        
        init_db()
        print("✅ Database initialized")
        
        diseases = get_all_diseases()
        print(f"✅ Loaded {len(diseases)} diseases")
        for disease in diseases[:3]:
            print(f"   - {disease}")
        print()
        return True
    
    except Exception as e:
        print(f"❌ Database error: {e}\n")
        return False

def test_model_loader():
    """Test model loading capability"""
    print("🤖 Testing model loader...")
    
    try:
        from backend.model_loader import _mock_prediction
        
        result = _mock_prediction()
        print(f"✅ Mock prediction works")
        print(f"   - Disease: {result['disease']}")
        print(f"   - Confidence: {result['confidence']:.2%}")
        print()
        return True
    
    except Exception as e:
        print(f"❌ Model loader error: {e}\n")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🌾 Smart Maize Disease Detection System - Test Suite")
    print("=" * 60)
    print()
    
    results = {
        "Imports": test_imports(),
        "Directories": test_directories(),
        "Files": test_files(),
        "Configuration": test_config(),
        "Database": test_database(),
        "Model Loader": test_model_loader(),
    }
    
    print("=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✅ All systems operational!")
        print("\n🚀 Ready to run:")
        print("   1. Start backend: cd backend && python main.py")
        print("   2. Open frontend: frontend/index.html")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    print()
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
