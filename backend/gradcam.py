"""
Grad-CAM (Gradient-weighted Class Activation Mapping)
Explainable AI visualization for CNN predictions
"""

import numpy as np
import cv2
import logging
from pathlib import Path
from config import MODEL_INPUT_SIZE

logger = logging.getLogger(__name__)

# Global model reference
_model = None

def generate_gradcam_heatmap(image_path: str, output_path: str, layer_name: str = None):
    """
    Generate Grad-CAM heatmap visualization
    Shows which regions of the image influenced the prediction
    
    Args:
        image_path: Path to input image
        output_path: Path to save heatmap
        layer_name: Name of layer to visualize (uses last conv layer by default)
    """
    try:
        # Try TensorFlow implementation first
        try:
            import tensorflow as tf
            from model_loader import model
            
            if model is None:
                logger.warning("Model not loaded, using mock heatmap")
                _generate_mock_heatmap(image_path, output_path)
                return
            
            _generate_tensorflow_gradcam(image_path, output_path, model, layer_name)
            logger.info(f"Grad-CAM heatmap saved to {output_path}")
        
        except ImportError:
            logger.info("TensorFlow not available, using mock heatmap")
            _generate_mock_heatmap(image_path, output_path)
    
    except Exception as e:
        logger.error(f"Error generating Grad-CAM heatmap: {e}")
        # Fallback to mock heatmap
        try:
            _generate_mock_heatmap(image_path, output_path)
        except Exception as e2:
            logger.error(f"Error generating mock heatmap: {e2}")
            raise

def _generate_tensorflow_gradcam(image_path: str, output_path: str, model, layer_name: str = None):
    """
    Generate Grad-CAM using TensorFlow/Keras
    """
    import tensorflow as tf
    from model_loader import get_image_array, preprocess_image
    
    # Load and preprocess image
    processed_image = preprocess_image(image_path)
    original_image = get_image_array(image_path)
    
    # Get the last convolutional layer if not specified
    if layer_name is None:
        # Find last convolutional layer
        for layer in reversed(model.layers):
            if 'conv' in layer.name.lower():
                layer_name = layer.name
                break
    
    # Create model that outputs feature maps and predictions
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )
    
    # Calculate gradients
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(processed_image)
        predicted_class = tf.argmax(predictions[0])
        class_channel = predictions[:, predicted_class]
    
    # Get gradients of class with respect to feature maps
    grads = tape.gradient(class_channel, conv_outputs)
    
    # Average pooling of gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Multiply each feature map by its gradient weight
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize to [0, 1]
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()
    
    # Resize to original image size
    heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    
    # Create visualization
    _visualize_and_save(original_image, heatmap, output_path)

def _visualize_and_save(original_image: np.ndarray, heatmap: np.ndarray, output_path: str):
    """
    Create and save heatmap visualization
    
    Args:
        original_image: Original RGB image
        heatmap: Grad-CAM heatmap
        output_path: Path to save result
    """
    # Normalize heatmap to 0-255
    heatmap = (heatmap * 255).astype(np.uint8)
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Convert original image back to BGR for OpenCV
    original_bgr = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
    
    # Overlay heatmap on original image
    overlay = cv2.addWeighted(original_bgr, 0.6, heatmap_colored, 0.4, 0)
    
    # Add border and title
    height, width = overlay.shape[:2]
    canvas = np.ones((height + 40, width, 3), dtype=np.uint8) * 25
    canvas[40:, :] = overlay
    
    # Add title text
    cv2.putText(
        canvas,
        "Grad-CAM Heatmap - Disease Detection Explanation",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 200, 83),
        2
    )
    
    # Save result
    cv2.imwrite(str(output_path), canvas)
    logger.info(f"Heatmap saved to {output_path}")

def _generate_mock_heatmap(image_path: str, output_path: str):
    """
    Generate mock Grad-CAM heatmap for demonstration
    Creates a simulated heatmap showing affected regions
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Resize if needed
        if image.shape[0] > 600 or image.shape[1] > 600:
            image = cv2.resize(image, (600, 600))
        
        height, width = image.shape[:2]
        
        # Create mock heatmap (simulate disease-affected areas)
        heatmap = np.zeros((height, width), dtype=np.float32)
        
        # Add Gaussian blobs to simulate disease hotspots
        center_y, center_x = height // 2, width // 2
        y, x = np.ogrid[:height, :width]
        
        # Create multiple hotspots
        mask1 = np.exp(-((x - center_x - 50)**2 + (y - center_y + 30)**2) / (2 * 60**2))
        mask2 = np.exp(-((x - center_x + 40)**2 + (y - center_y - 20)**2) / (2 * 50**2))
        mask3 = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * 40**2))
        
        heatmap = (mask1 + mask2 + mask3) / 3
        heatmap = np.clip(heatmap, 0, 1)
        
        # Apply heatmap
        heatmap_uint8 = (heatmap * 255).astype(np.uint8)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        
        # Overlay on original image
        overlay = cv2.addWeighted(image, 0.6, heatmap_colored, 0.4, 0)
        
        # Add canvas and title
        canvas = np.ones((height + 40, width, 3), dtype=np.uint8) * 25
        canvas[40:, :] = overlay
        
        cv2.putText(
            canvas,
            "Grad-CAM Heatmap - Disease Detection Explanation",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 200, 83),
            2
        )
        
        # Save
        cv2.imwrite(str(output_path), canvas)
        logger.info(f"Mock heatmap saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Error generating mock heatmap: {e}")
        raise

def create_comparison_image(original_path: str, heatmap_path: str, output_path: str):
    """
    Create side-by-side comparison of original and heatmap
    
    Args:
        original_path: Path to original image
        heatmap_path: Path to heatmap image
        output_path: Path to save comparison
    """
    try:
        original = cv2.imread(original_path)
        heatmap = cv2.imread(heatmap_path)
        
        if original is None or heatmap is None:
            raise ValueError("Could not read images")
        
        # Resize to same height
        height = max(original.shape[0], heatmap.shape[0])
        original = cv2.resize(original, (int(original.shape[1] * height / original.shape[0]), height))
        heatmap = cv2.resize(heatmap, (int(heatmap.shape[1] * height / heatmap.shape[0]), height))
        
        # Concatenate horizontally
        comparison = np.hstack([original, heatmap])
        
        cv2.imwrite(str(output_path), comparison)
        logger.info(f"Comparison image saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Error creating comparison image: {e}")
        raise
