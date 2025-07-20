"""
FastAPI application for legal document classification service.
Provides REST API endpoints for classifying legal documents.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import logging
import time
import os
import json
from typing import Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Document Classifier API",
    description="API for classifying legal documents into categories: contract, lawsuit, complaint, request",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to classify")

class ClassificationResponse(BaseModel):
    category: str = Field(..., description="Predicted category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="Model version/timestamp")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_version: Optional[str] = Field(None, description="Model version")
    uptime: float = Field(..., description="Service uptime in seconds")

# Global variables
model = None
model_info = {}
start_time = time.time()

def load_model():
    """Load the trained ML model."""
    global model, model_info
    
    try:
        # Load model
        model_path = 'src/model.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load model info
        info_path = 'src/model_info.json'
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                model_info = json.load(f)
        
        logger.info("Model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    logger.info("Starting Legal Document Classifier API...")
    load_model()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic service information."""
    return {
        "message": "Legal Document Classifier API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    uptime = time.time() - start_time
    
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded"
        )
    
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_version=model_info.get('training_date', 'unknown'),
        uptime=uptime
    )

@app.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: TextRequest):
    """
    Classify legal document text into categories.
    
    Categories:
    - contract: Contracts and agreements
    - lawsuit: Lawsuits and legal claims
    - complaint: Complaints and grievances
    - request: Requests and petitions
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded"
        )
    
    start_time = time.time()
    
    try:
        # Make prediction
        prediction = model.predict([request.text])[0]
        probabilities = model.predict_proba([request.text])[0]
        confidence = max(probabilities)
        
        processing_time = time.time() - start_time
        
        # Log the request
        logger.info(
            f"Classification: text_length={len(request.text)}, "
            f"category={prediction}, confidence={confidence:.3f}, "
            f"time={processing_time:.3f}s"
        )
        
        return ClassificationResponse(
            category=prediction,
            confidence=confidence,
            processing_time=processing_time,
            model_version=model_info.get('training_date', 'unknown')
        )
    
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Classification failed: {str(e)}"
        )

@app.get("/categories")
async def get_categories():
    """Get available document categories and their descriptions."""
    return {
        "categories": ["contract", "lawsuit", "complaint", "request"],
        "descriptions": {
            "contract": "Contracts and agreements",
            "lawsuit": "Lawsuits and legal claims",
            "complaint": "Complaints and grievances",
            "request": "Requests and petitions"
        },
        "model_info": model_info
    }

@app.post("/classify/batch")
async def classify_batch_texts(requests: List[TextRequest]):
    """
    Classify multiple texts in batch.
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded"
        )
    
    if len(requests) > 100:  # Limit batch size
        raise HTTPException(
            status_code=400, 
            detail="Batch size too large. Maximum 100 texts allowed."
        )
    
    start_time = time.time()
    
    try:
        texts = [req.text for req in requests]
        predictions = model.predict(texts)
        probabilities = model.predict_proba(texts)
        
        results = []
        for i, (text, pred, prob) in enumerate(zip(texts, predictions, probabilities)):
            confidence = max(prob)
            results.append({
                "text": text,
                "category": pred,
                "confidence": confidence
            })
        
        processing_time = time.time() - start_time
        
        logger.info(
            f"Batch classification: count={len(texts)}, "
            f"time={processing_time:.3f}s"
        )
        
        return {
            "results": results,
            "processing_time": processing_time,
            "model_version": model_info.get('training_date', 'unknown')
        }
    
    except Exception as e:
        logger.error(f"Batch classification error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Batch classification failed: {str(e)}"
        )

@app.get("/model/info")
async def get_model_info():
    """Get information about the loaded model."""
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded"
        )
    
    return {
        "model_info": model_info,
        "classes": model.classes_.tolist() if hasattr(model, 'classes_') else [],
        "model_type": type(model).__name__
    }

if __name__ == "__main__":
    import uvicorn
    
    # Load model before starting server
    if not load_model():
        logger.error("Failed to load model. Exiting.")
        exit(1)
    
    # Start the server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    ) 