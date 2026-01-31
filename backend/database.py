"""
Database Management - SQLite
Stores prediction history and disease recommendations
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import logging
from config import DATABASE_PATH, DISEASE_CLASSES

logger = logging.getLogger(__name__)

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    """Initialize database with required tables"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_name TEXT NOT NULL,
                disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_name TEXT UNIQUE NOT NULL,
                cause TEXT NOT NULL,
                pesticide TEXT NOT NULL,
                fertilizer TEXT NOT NULL,
                prevention TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        logger.info("Database tables created/verified")
        
        # Initialize default recommendations
        _initialize_recommendations(conn)
        
        conn.close()
    
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def _initialize_recommendations(conn):
    """Initialize comprehensive disease recommendations with detailed solutions"""
    
    recommendations_data = [
        {
            "disease": "Healthy",
            "cause": "Leaf is healthy with no visible disease symptoms or stress indicators",
            "pesticide": "No pesticide required. Apply preventive copper/sulfur sprays monthly as safeguard",
            "fertilizer": "Maintain with balanced NPK (15-15-15) + Micronutrients. Apply every 3-4 weeks",
            "prevention": "Continue regular monitoring, maintain optimal soil moisture, ensure good drainage"
        },
        {
            "disease": "Maize Common Rust",
            "cause": "Fungal infection caused by Puccinia sorghi. Identified by reddish-brown pustules on leaf surface. Spores spread via wind and water",
            "pesticide": "SPRAY SCHEDULE:\n• Mancozeb 75% WP: 2g/L every 10-14 days\n• OR Azoxystrobin 25% SC: 0.5mL/L bi-weekly\n• OR Tebuconazole 25% EC: 1mL/L every 14 days\n• Apply early morning or late evening\n• Complete coverage of leaf surface essential",
            "fertilizer": "• Apply Potassium-rich (NPK 10-20-30) 400kg/hectare\n• Foliar spray: Potassium nitrate 2% every 10 days\n• Add Magnesium sulfate 0.5% to control severity\n• Zinc sulfate 0.5% foliar spray improves resistance",
            "prevention": "• Remove infected leaves (10-15cm from infection)\n• Improve air circulation - prune lower leaves\n• Avoid overhead irrigation, water at soil level\n• Destroy crop residue after harvest\n• Plant rust-resistant varieties in future\n• Maintain field sanitation, clean equipment\n• Rotate crops to break disease cycle"
        },
        {
            "disease": "Maize Southern Leaf Blight",
            "cause": "Caused by Bipolaris maydis fungus. Produces large tan/brown elongated lesions with dark borders. Disease accelerates in warm, wet conditions (25-30°C)",
            "pesticide": "TREATMENT PROTOCOL:\n• Mancozeb 75% WP: 2.5g/L spray\n• OR Carbendazim 50% WP: 1g/L every 10 days\n• OR Chlorothalonil 75% WP: 1.5g/L bi-weekly\n• Start spraying at V4-V6 growth stage\n• Continue until grain formation\n• Apply minimum 800L water/hectare",
            "fertilizer": "• Base dose: NPK (20-10-10) at 500kg/hectare\n• Split application: 50% at planting, 50% at tasseling\n• Magnesium sulfate 500kg/hectare for vigor\n• Boron 2kg/hectare improves plant resistance\n• Iron chelate 5kg/hectare if yellowing observed",
            "prevention": "• Select disease-resistant hybrids (CR rating preferred)\n• Practice 2-3 year crop rotation\n• Use certified disease-free seed (95%+ purity)\n• Remove crop residue by burning/ploughing\n• Avoid planting in low-lying areas prone to moisture\n• Provide adequate spacing (60x20cm) for air movement\n• Monitor from V4 stage onwards, spray at first sign\n• Timely irrigation critical - not excessive\n• Field sanitation - remove volunteer plants"
        },
        {
            "disease": "Maize Northern Leaf Blight",
            "cause": "Fungus Exserohilum turcicum causes long, narrow (2-15cm), gray-green lesions with yellow halo. Severe in cool-wet conditions (18-24°C). Can cause total defoliation",
            "pesticide": "FUNGICIDE SCHEDULE:\n• Propiconazole 25% EC: 1mL/L spray every 14 days\n• OR Tebuconazole 25% EC: 2g/L every 12 days\n• OR Azoxystrobin 23% SC: 0.6mL/L bi-weekly\n• Start at V6 stage, continue until milk stage\n• Minimum 3-4 sprays recommended\n• Use spreader-sticker for better adhesion",
            "fertilizer": "• Balanced NPK (18-18-18) 600kg/hectare\n• Split as: 50% at planting, 25% at V6, 25% at V12\n• Zinc sulfate 25kg/hectare (deficiency increases severity)\n• Calcium nitrate 200kg/hectare improves leaf vigor\n• Potassium chloride 250kg/hectare boosts immunity",
            "prevention": "• Plant resistant hybrids (look for NLB resistance rating)\n• Clean seed treatment with Thiram 0.3%\n• Avoid planting susceptible varieties in endemic areas\n• Practice 3-year crop rotation (avoid sorghum)\n• Destroy all crop residue - do not use as mulch\n• Ensure spacing 60x20cm minimum\n• Avoid excessive nitrogen application\n• Manage irrigation - reduce leaf wetness duration\n• Scout fields from V4 onwards\n• Remove infected leaves when possible"
        },
        {
            "disease": "Maize Gray Leaf Spot",
            "cause": "Cercospora zeae-maydis fungal infection producing gray-tan rectangular spots with yellow halos. Spores overwinter on crop residue. Spreads rapidly in warm, humid weather",
            "pesticide": "APPLICATION PLAN:\n• Mancozeb 75% WP: 2g/L every 10 days\n• OR Copper oxychloride 50% WP: 3g/L spray\n• OR Pyraclostrobin 20% EC: 0.75mL/L bi-weekly\n• Begin spraying at tasseling stage\n• Apply 3-4 sprays minimum in susceptible areas\n• Ensure thorough coverage of both leaf surfaces",
            "fertilizer": "• High Potassium NPK (10-26-26) 400kg/hectare\n• Nitrogen: 100kg/hectare split application\n• Potassium: 100kg/hectare for disease resistance\n• Phosphorus: 50kg/hectare for root strength\n• Magnesium sulfate 250kg/hectare\n• Sulfur 3% foliar spray improves protection",
            "prevention": "• Use gray leaf spot resistant varieties\n• Implement strict crop rotation (2-3 years minimum)\n• Plow deep (25cm) to bury infected residue\n• Avoid overhead irrigation - drip/furrow irrigation preferred\n• Space plants 60x20cm for air circulation\n• Remove lower leaves after tasseling if infection appears\n• Scout from V8 stage onwards weekly\n• Maintain balanced nutrition - avoid excess nitrogen\n• Clean farm equipment to prevent spread\n• Monitor and treat early - critical for control"
        },
        {
            "disease": "Maize Anthracnose",
            "cause": "Colletotrichum graminicola fungus causes dark brown to black lesions on leaves, stems, and cobs. Can cause stalk rot and yield loss. Worse in cool-wet conditions",
            "pesticide": "TREATMENT SCHEDULE:\n• Carbendazim 50% WP: 1g/L + Mancozeb 0.2%\n• Apply every 10-12 days\n• OR Benomyl 50% WP: 0.5g/L\n• OR Hexaconazole 5% EC: 2mL/L\n• Start spraying at V6 stage\n• Continue for 4-5 weeks or until disease controlled",
            "fertilizer": "• NPK (15-15-15) base dose 500kg/hectare\n• Boron 2kg/hectare - critical for control\n• Zinc sulfate 20kg/hectare\n• Phosphorus emphasis: 60kg/hectare\n• Potassium: 60kg/hectare\n• Iron chelate if chlorosis observed\n• Foliar spray: Boron 0.1% weekly",
            "prevention": "• Select anthracnose-resistant varieties\n• Use disease-free certified seed\n• Seed treatment with Trichoderma viride 4g/kg\n• Remove crop debris completely\n• Avoid crop residue mulching\n• Practice 2-year rotation with cereals\n• Maintain proper spacing for ventilation\n• Ensure adequate drainage in fields\n• Avoid mechanical injury to plants\n• Manage soil moisture - not waterlogged\n• Scout fields every 5 days during growing season\n• Remove severely infected plants"
        },
        {
            "disease": "Maize Eyespot",
            "cause": "Kabatiella zeae fungus produces circular to oval lesions with concentric rings (target-like). Lesions have dark borders and light centers. Develops in cool-wet conditions",
            "pesticide": "CONTROL MEASURES:\n• Mancozeb 75% WP: 2g/L every 10 days\n• OR Chlorothalonil 75% WP: 1.5g/L spray\n• OR Tebuconazole 25% EC: 1mL/L every 14 days\n• Apply protective sprays from V6 stage\n• Continue until grain dough stage\n• Thorough coverage essential for effectiveness",
            "fertilizer": "• Balanced NPK (18-18-18) 450kg/hectare\n• Nitrogen: 90kg/hectare\n• Phosphorus: 45kg/hectare\n• Potassium: 45kg/hectare for vigor\n• Magnesium sulfate 200kg/hectare\n• Manganese sulfate 10kg/hectare\n• Apply 50% at planting, 50% at V6 stage",
            "prevention": "• Clean farm implements before field use\n• Destroy infected crop residue by burning\n• Avoid planting in low-lying wet areas\n• Use proper spacing (60x20cm minimum)\n• Maintain field sanitation throughout season\n• Avoid overhead irrigation\n• Scout fields from V6 onwards\n• Remove manually infected leaves in early stage\n• Ensure good air circulation in field\n• Use resistant varieties if available\n• Avoid working in wet fields\n• Remove weeds that harbor fungus"
        },
        {
            "disease": "Maize Turcicum Leaf Blight",
            "cause": "Exserohilum turcicum produces long narrow lesions (2-20cm) with concentric rings and necrotic centers. Similar to NLB but with distinct features. Severe in cool-wet weather at V8-V10",
            "pesticide": "SPRAY PROTOCOL:\n• Propiconazole 25% EC: 1mL/L every 14 days\n• OR Azoxystrobin 23% SC: 0.6mL/L bi-weekly\n• OR Mancozeb 75% WP: 2.5g/L + Carbendazim 1%\n• Begin at V8 growth stage\n• Minimum 3-4 applications needed\n• Apply in cool hours (morning preferred)\n• Use wetting agent for better coverage",
            "fertilizer": "• NPK (20-10-10) split application\n• Base: 50% at planting (300kg/hectare)\n• Top-dress: 50% at V12 stage\n• Sulfur 3% foliar spray every 10 days\n• Magnesium sulfate 250kg/hectare\n• Zinc sulfate 20kg/hectare\n• Calcium nitrate 150kg/hectare\n• Avoid excess nitrogen - promotes susceptibility",
            "prevention": "• Plant resistant hybrids rated for TLB\n• Use seed treatment with Thiram or Trichoderma\n• Clean all farm equipment\n• Practice strict crop rotation (2-3 years minimum)\n• Plow deep to bury infected residue\n• Scout from V8 stage twice weekly\n• Remove lower infected leaves to reduce inoculum\n• Ensure adequate spacing for air movement\n• Avoid overhead irrigation during evenings\n• Maintain optimal nitrogen levels\n• Monitor weather - spray at first sign\n• Remove volunteer maize plants"
        }
    ]
    
    try:
        cursor = conn.cursor()
        
        for rec in recommendations_data:
            cursor.execute('''
                INSERT OR IGNORE INTO recommendations 
                (disease_name, cause, pesticide, fertilizer, prevention)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                rec["disease"],
                rec["cause"],
                rec["pesticide"],
                rec["fertilizer"],
                rec["prevention"]
            ))
        
        conn.commit()
        logger.info(f"Initialized {len(recommendations_data)} comprehensive disease recommendations")
    
    except Exception as e:
        logger.error(f"Error initializing recommendations: {e}")

# ============================================
# PREDICTION OPERATIONS
# ============================================

def save_prediction(image_name: str, disease: str, confidence: float):
    """
    Save prediction to database
    
    Args:
        image_name: Name of uploaded image
        disease: Predicted disease name
        confidence: Confidence score (0-1)
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (image_name, disease, confidence)
            VALUES (?, ?, ?)
        ''', (image_name, disease, confidence))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved prediction: {disease} ({confidence:.2%})")
    
    except Exception as e:
        logger.error(f"Error saving prediction: {e}")
        raise

def get_prediction_history(limit: int = 10):
    """
    Get recent predictions from database
    
    Args:
        limit: Number of recent predictions to retrieve
    
    Returns:
        List of predictions
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, image_name, disease, confidence, timestamp
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        predictions = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": p[0],
                "image_name": p[1],
                "disease": p[2],
                "confidence": p[3],
                "timestamp": p[4]
            }
            for p in predictions
        ]
    
    except Exception as e:
        logger.error(f"Error retrieving predictions: {e}")
        return []

def get_statistics():
    """Get prediction statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total_predictions = cursor.fetchone()[0]
        
        # Disease distribution
        cursor.execute('''
            SELECT disease, COUNT(*) as count
            FROM predictions
            GROUP BY disease
            ORDER BY count DESC
        ''')
        disease_distribution = cursor.fetchall()
        
        # Average confidence by disease
        cursor.execute('''
            SELECT disease, AVG(confidence) as avg_confidence
            FROM predictions
            GROUP BY disease
        ''')
        avg_confidence = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_predictions": total_predictions,
            "disease_distribution": {d[0]: d[1] for d in disease_distribution},
            "avg_confidence": {d[0]: d[1] for d in avg_confidence}
        }
    
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        return {}

# ============================================
# RECOMMENDATION OPERATIONS
# ============================================

def get_recommendations(disease_name: str) -> dict:
    """
    Get agronomic recommendations for a disease
    
    Args:
        disease_name: Name of the disease
    
    Returns:
        Dictionary with recommendations
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cause, pesticide, fertilizer, prevention
            FROM recommendations
            WHERE disease_name = ?
        ''', (disease_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "cause": result[0],
                "pesticide": result[1],
                "fertilizer": result[2],
                "prevention": result[3]
            }
        else:
            logger.warning(f"Recommendations not found for: {disease_name}")
            return {
                "cause": "Unknown disease",
                "pesticide": "Consult an agricultural expert",
                "fertilizer": "Maintain balanced NPK fertilizer",
                "prevention": "Regular monitoring recommended"
            }
    
    except Exception as e:
        logger.error(f"Error retrieving recommendations: {e}")
        return {}

def get_all_diseases():
    """Get all diseases in database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT disease_name FROM recommendations ORDER BY disease_name')
        diseases = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return diseases
    
    except Exception as e:
        logger.error(f"Error retrieving diseases: {e}")
        return DISEASE_CLASSES

def update_recommendation(disease_name: str, cause: str, pesticide: str, 
                         fertilizer: str, prevention: str):
    """Update existing recommendation"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE recommendations
            SET cause = ?, pesticide = ?, fertilizer = ?, prevention = ?
            WHERE disease_name = ?
        ''', (cause, pesticide, fertilizer, prevention, disease_name))
        
        conn.commit()
        conn.close()
        logger.info(f"Updated recommendations for: {disease_name}")
    
    except Exception as e:
        logger.error(f"Error updating recommendations: {e}")
        raise
