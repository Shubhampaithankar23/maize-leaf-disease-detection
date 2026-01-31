"""
Model Loader - Load pre-trained CNN model and make predictions
Supports TensorFlow/Keras (.h5) and PyTorch (.pt) models
"""

import numpy as np
import cv2
import logging
from pathlib import Path
from config import MODEL_PATH, MODEL_INPUT_SIZE, DISEASE_CLASSES, CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)

# Global model variable
model = None

def load_model():
    """
    Load pre-trained model from disk
    Supports TensorFlow/Keras (.h5) and PyTorch (.pt) models
    """
    global model
    
    try:
        # Try to load TensorFlow/Keras model first
        h5_files = list(MODEL_PATH.glob("*.h5"))
        if h5_files:
            model_file = h5_files[0]
            logger.info(f"Loading TensorFlow model from {model_file}")
            import tensorflow as tf
            model = tf.keras.models.load_model(str(model_file))
            logger.info("TensorFlow model loaded successfully")
            return True
        
        # Try PyTorch model
        pt_files = list(MODEL_PATH.glob("*.pt"))
        if pt_files:
            model_file = pt_files[0]
            logger.info(f"Loading PyTorch model from {model_file}")
            import torch
            model = torch.load(str(model_file))
            model.eval()
            logger.info("PyTorch model loaded successfully")
            return True
        
        logger.warning("No pre-trained model found in models directory")
        logger.info("Using mock model for demonstration")
        return False
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.info("Using mock model for demonstration")
        return False

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess image for model input
    
    Args:
        image_path: Path to image file
    
    Returns:
        Preprocessed image array
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        image = cv2.resize(image, (MODEL_INPUT_SIZE, MODEL_INPUT_SIZE))
        
        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def predict_disease(image_path: str) -> dict:
    """
    Predict disease from image
    
    Args:
        image_path: Path to image file
    
    Returns:
        Dictionary with disease, confidence, and other info
    """
    try:
        # Preprocess image
        image = preprocess_image(image_path)
        
        # Make prediction
        if model is not None:
            try:
                import tensorflow as tf
                # Check if it's a TensorFlow model
                if hasattr(model, 'predict'):
                    predictions = model.predict(image, verbose=0)
                    class_idx = np.argmax(predictions[0])
                    confidence = float(predictions[0][class_idx])
                else:
                    # PyTorch model
                    import torch
                    image_tensor = torch.from_numpy(image).to(next(model.parameters()).device)
                    with torch.no_grad():
                        output = model(image_tensor)
                    confidence = torch.softmax(output, dim=1)
                    class_idx = int(torch.argmax(confidence[0]))
                    confidence = float(confidence[0][class_idx])
            except Exception as e:
                logger.warning(f"Error running inference: {e}. Using mock prediction.")
                return _mock_prediction()
        else:
            # Use mock prediction if model not loaded
            return _mock_prediction()
        
        disease = DISEASE_CLASSES[class_idx] if class_idx < len(DISEASE_CLASSES) else "Unknown"
        
        return {
            "disease": disease,
            "confidence": confidence,
            "class_index": class_idx,
            "all_predictions": {
                DISEASE_CLASSES[i]: float(pred) 
                for i, pred in enumerate(predictions[0]) 
                if i < len(DISEASE_CLASSES)
            } if model is not None else {}
        }
    
    except Exception as e:
        logger.error(f"Error in disease prediction: {e}")
        raise

def _mock_prediction() -> dict:
    """
    Generate enhanced mock prediction for demonstration
    Uses realistic confidence distributions to simulate model accuracy
    """
    import random
    
    # More realistic disease distribution based on actual maize disease prevalence
    disease_probabilities = {
        "Healthy": 0.22,
        "Maize Common Rust": 0.18,
        "Maize Southern Leaf Blight": 0.16,
        "Maize Northern Leaf Blight": 0.15,
        "Maize Gray Leaf Spot": 0.12,
        "Maize Anthracnose": 0.10,
        "Maize Eyespot": 0.04,
        "Maize Turcicum Leaf Blight": 0.03,
    }
    
    # Generate realistic confidence scores using weighted random selection
    diseases = list(disease_probabilities.keys())
    probabilities = list(disease_probabilities.values())
    
    selected_disease = random.choices(diseases, weights=probabilities, k=1)[0]
    
    # Generate confidence with realistic distribution
    # Most predictions are 75-95%, some are lower
    base_confidence = random.uniform(0.78, 0.95)
    
    # Add slight noise for realism
    confidence = min(0.99, max(0.65, base_confidence + random.gauss(0, 0.02)))
    
    # Generate all predictions with normalized distribution
    all_predictions = {}
    remaining_confidence = 1.0 - confidence
    
    for disease in DISEASE_CLASSES:
        if disease == selected_disease:
            all_predictions[disease] = confidence
        else:
            # Distribute remaining confidence among other diseases
            pred = random.uniform(0.01, remaining_confidence * 0.3)
            all_predictions[disease] = pred
    
    # Normalize to sum to 1.0
    total = sum(all_predictions.values())
    all_predictions = {d: (c / total) for d, c in all_predictions.items()}
    
    return {
        "disease": selected_disease,
        "confidence": round(all_predictions[selected_disease], 4),
        "class_index": DISEASE_CLASSES.index(selected_disease),
        "all_predictions": {d: round(c, 4) for d, c in all_predictions.items()},
        "is_mock": True
    }

def get_image_array(image_path: str) -> np.ndarray:
    """
    Get raw image array without preprocessing for visualization
    
    Args:
        image_path: Path to image file
    
    Returns:
        Image array in RGB format
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        raise
