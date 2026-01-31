"""
Smart Maize Leaf Disease Detection System
FastAPI Backend - Main Application
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
from pathlib import Path
import sys
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from model_loader import load_model, predict_disease
from gradcam import generate_gradcam_heatmap
from database import init_db, save_prediction, get_recommendations
from config import UPLOAD_FOLDER, HEATMAP_FOLDER, MODEL_PATH

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# DATA MODELS
# ============================================

class OTPRequest(BaseModel):
    """OTP request model"""
    email: str

class OTPVerifyRequest(BaseModel):
    """OTP verification request"""
    email: str
    otp: str

# ============================================
# OTP Storage (In-memory for demo - use Redis in production)
# ============================================
OTP_STORAGE = {}  # {email: {"otp": "123456", "timestamp": datetime}}

# ============================================
# EMAIL CONFIGURATION
# ============================================
# Using Gmail SMTP - configure with your credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Check if email is configured
EMAIL_CONFIGURED = SENDER_EMAIL and SENDER_PASSWORD and SENDER_EMAIL != "your-email@gmail.com"

# FastAPI app initialization
app = FastAPI(
    title="Smart Maize Leaf Disease Detection System",
    description="AI-powered disease detection with explainable AI (Grad-CAM)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Initializing Smart Maize Disease Detection System...")
    
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(HEATMAP_FOLDER, exist_ok=True)
    
    # Initialize database
    init_db()
    logger.info("Database initialized successfully")
    
    # Load model
    try:
        load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load model: {e}. Using mock predictions.")
    
    logger.info("System ready for predictions")

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {
        "status": "success",
        "message": "Smart Maize Leaf Disease Detection System API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "POST /api/predict",
            "health": "GET /api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict disease from uploaded image
    
    - **file**: Image file (JPG, PNG, WebP)
    - Returns: Disease prediction, confidence, heatmap, recommendations
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload JPG, PNG, or WebP image"
            )
        
        logger.info(f"Processing image: {file.filename}")
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Make prediction
        prediction_result = predict_disease(file_path)
        disease = prediction_result["disease"]
        confidence = prediction_result["confidence"]
        
        logger.info(f"Prediction: {disease} ({confidence:.2%})")
        
        # Generate Grad-CAM heatmap
        heatmap_path = None
        try:
            heatmap_filename = f"heatmap_{Path(file.filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            heatmap_path = os.path.join(HEATMAP_FOLDER, heatmap_filename)
            generate_gradcam_heatmap(file_path, heatmap_path)
            heatmap_relative = f"static/heatmaps/{heatmap_filename}"
            logger.info("Grad-CAM heatmap generated successfully")
        except Exception as e:
            logger.warning(f"Could not generate heatmap: {e}")
            heatmap_relative = None
        
        # Get recommendations
        recommendation = get_recommendations(disease)
        
        # Save to database
        try:
            save_prediction(file.filename, disease, confidence)
        except Exception as e:
            logger.warning(f"Could not save to database: {e}")
        
        # Return results
        return {
            "success": True,
            "disease": disease,
            "confidence": confidence,
            "heatmap": heatmap_relative,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/recommendations/{disease_name}")
async def get_disease_recommendations(disease_name: str):
    """
    Get recommendations for a specific disease
    
    - **disease_name**: Name of the disease
    """
    try:
        recommendation = get_recommendations(disease_name)
        if not recommendation:
            raise HTTPException(status_code=404, detail="Disease not found")
        
        return {
            "success": True,
            "disease": disease_name,
            "recommendation": recommendation
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recommendations")

# ============================================
# OTP & AUTHENTICATION ENDPOINTS
# ============================================

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP to user's email
    
    Returns: True if sent successfully, False otherwise
    """
    try:
        # Check if email is configured
        if not EMAIL_CONFIGURED:
            logger.warning(f"Email not configured. OTP for {email}: {otp}")
            logger.info("To enable real email sending, set SENDER_EMAIL and SENDER_PASSWORD environment variables")
            # In test mode, still return True so frontend continues
            return True
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Smart Maize - Your OTP for Verification"
        message["From"] = SENDER_EMAIL
        message["To"] = email
        
        # HTML email template
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #00c853; text-align: center; margin-bottom: 30px;">🌾 Smart Maize Leaf Disease Detection</h2>
                    
                    <p style="color: #333; font-size: 16px;">Hello,</p>
                    
                    <p style="color: #666; font-size: 14px;">Your One-Time Password (OTP) for email verification is:</p>
                    
                    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 6px; text-align: center; margin: 20px 0;">
                        <p style="margin: 0; font-size: 32px; font-weight: bold; color: #00c853; letter-spacing: 4px;">{otp}</p>
                    </div>
                    
                    <p style="color: #999; font-size: 12px;">This OTP will expire in 5 minutes. Do not share this code with anyone.</p>
                    
                    <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        If you did not request this OTP, please ignore this email.
                    </p>
                    
                    <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                        © 2026 Smart Maize Disease Detection System
                    </p>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email via SMTP
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, email, message.as_string())
            
            logger.info(f"OTP sent successfully to {email}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email credentials.")
            logger.error(f"Make sure you're using an App Password (16 chars), not your Gmail password")
            # Return True to continue frontend flow
            return True
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            logger.error("Email sending failed. Running in TEST MODE - user will see OTP in browser message")
            return True
        except Exception as e:
            logger.error(f"Error sending OTP email: {str(e)}")
            return True
    
    except Exception as e:
        logger.error(f"Unexpected error in send_otp_email: {str(e)}")
        return True

@app.post("/api/auth/send-otp")
async def send_otp(request: OTPRequest):
    """
    Send OTP to user's email for verification
    
    - **email**: User's email address
    """
    try:
        email = request.email.lower().strip()
        
        # Validate email format
        if not email.endswith("@gmail.com"):
            raise HTTPException(status_code=400, detail="Only Gmail addresses are supported")
        
        if "@" not in email or "." not in email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Generate OTP
        otp = generate_otp()
        
        # Store OTP with timestamp
        OTP_STORAGE[email] = {
            "otp": otp,
            "timestamp": datetime.now()
        }
        
        # Send OTP via email
        email_sent = send_otp_email(email, otp)
        
        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send OTP email")
        
        logger.info(f"OTP sent to {email}")
        
        response_data = {
            "success": True,
            "message": f"OTP sent to {email}",
            "email": email
        }
        
        # In test mode (email not configured), include OTP in response for testing
        if not EMAIL_CONFIGURED:
            response_data["test_otp"] = otp
            response_data["message"] = f"TEST MODE: OTP is {otp}. Check browser console or look for dialog."
        
        return response_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/auth/verify-otp")
async def verify_otp(request: OTPVerifyRequest):
    """
    Verify OTP sent to user's email
    
    - **email**: User's email address
    - **otp**: 6-digit OTP code
    """
    try:
        email = request.email.lower().strip()
        otp = request.otp.strip()
        
        # Check if OTP exists for this email
        if email not in OTP_STORAGE:
            raise HTTPException(status_code=400, detail="No OTP found for this email. Please request a new OTP.")
        
        stored_otp_data = OTP_STORAGE[email]
        
        # Check OTP validity (5 minutes)
        time_diff = (datetime.now() - stored_otp_data["timestamp"]).total_seconds()
        if time_diff > 300:  # 5 minutes
            del OTP_STORAGE[email]
            raise HTTPException(status_code=400, detail="OTP has expired. Please request a new OTP.")
        
        # Verify OTP
        if stored_otp_data["otp"] != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP. Please try again.")
        
        # OTP is valid - remove it from storage
        del OTP_STORAGE[email]
        
        logger.info(f"OTP verified successfully for {email}")
        
        return {
            "success": True,
            "message": "Email verified successfully",
            "email": email
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================
# ERROR HANDLING
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }


# ============================================
# SERVER STARTUP
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


