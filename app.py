#!/usr/bin/env python3
"""
Meyers API Scraper - FastAPI

A FastAPI-based API that provides endpoints to fetch and extract menu items from the Meyers API.
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Import the existing scraper components
from src.client import MeyersAPIClient
from src.processor import MenuDataProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

# Configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5015))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# Initialize FastAPI app
app = FastAPI(
    title="Meyers Scraper API",
    description="A FastAPI that provides endpoints to fetch and extract menu items from the Meyers API",
    version="1.0.0",
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation and documentation
class MenuItem(BaseModel):
    item_name: str = Field(..., description="Name of the menu item")
    item_category: str = Field(..., description="Category of the menu item")
    item_id: str = Field(..., description="Unique identifier for the menu item")
    menu_name: str = Field(..., description="Name of the menu")
    menu_description: str = Field(..., description="Description of the menu")
    pictograms: List[str] = Field(..., description="List of pictograms")
    labels: List[str] = Field(..., description="List of labels")
    allergens: List[str] = Field(..., description="List of allergens")

class DateMenuData(BaseModel):
    date: str = Field(..., description="Date of the menu")
    timestamp: str = Field(..., description="Timestamp of the menu")
    day_of_week: str = Field(..., description="Day of the week")
    items: List[MenuItem] = Field(..., description="List of menu items")

class Metadata(BaseModel):
    total_dates: Optional[int] = Field(None, description="Total number of dates")
    date: Optional[str] = Field(None, description="Specific date")
    school_id: str = Field(..., description="School ID")
    language: str = Field(..., description="Language code")
    target_offer_id: str = Field(..., description="Target Offer ID")
    fetched_at: str = Field(..., description="Timestamp when data was fetched")

class SuccessResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Response data")
    metadata: Metadata = Field(..., description="Response metadata")

class ErrorResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Error message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data (null for errors)")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current timestamp")
    service: str = Field(..., description="Service name")

@app.get(
    "/api/health/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Health check endpoint to verify the API is running",
    tags=["Health"]
)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="meyers-scraper-api"
    )

@app.get(
    "/api/menus/",
    response_model=SuccessResponse,
    summary="Get All Menus",
    description="Get all available menus for the specified parameters",
    responses={
        200: {"description": "Success", "model": SuccessResponse},
        404: {"description": "No menu data found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    },
    tags=["Menus"]
)
async def get_all_menus(
    school_id: str = Query(
        default=os.getenv('SCHOOL_ID', 'CxnRNYOtBo6VrqiCb4AA'),
        description="School ID"
    ),
    language: str = Query(
        default=os.getenv('DEFAULT_LANGUAGE', 'en'),
        description="Language code"
    ),
    target_offer_id: str = Query(
        default=os.getenv('TARGET_OFFER_ID', 'ob6V4HfZK9Gs95sii4Cf'),
        description="Target Offer ID"
    )
):
    """Get all available menus."""
    try:
        logger.info(f"Fetching menus for school_id: {school_id}, language: {language}, target_offer_id: {target_offer_id}")
        
        # Initialize API client
        client = MeyersAPIClient(school_id=school_id, language=language, target_offer_id=target_offer_id)
        
        # Fetch data from API
        data = client.fetch_data()
        
        # Process and extract menu items
        processor = MenuDataProcessor()
        date_menus = processor.extract_menu_items(data, target_offer_id)
        
        if not date_menus:
            raise HTTPException(
                status_code=404,
                detail="No menu data found"
            )
        
        # Convert to serializable format
        serializable_data = {}
        for date_str, date_data in date_menus.items():
            serializable_data[date_str] = {
                "date": date_data.date,
                "timestamp": date_data.timestamp,
                "day_of_week": date_data.day_of_week,
                "items": [
                    {
                        "item_name": item.item_name,
                        "item_category": item.item_category,
                        "item_id": item.item_id,
                        "menu_name": item.menu_name,
                        "menu_description": item.menu_description,
                        "pictograms": item.pictograms,
                        "labels": item.labels,
                        "allergens": item.allergens,
                    }
                    for item in date_data.items
                ]
            }
        
        return SuccessResponse(
            success=True,
            message=f'Successfully retrieved {len(date_menus)} date menus',
            data=serializable_data,
            metadata=Metadata(
                total_dates=len(date_menus),
                school_id=school_id,
                language=language,
                target_offer_id=target_offer_id,
                fetched_at=datetime.now().isoformat()
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching menus: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching menus: {str(e)}"
        )

@app.get(
    "/api/menus/{date}",
    response_model=SuccessResponse,
    summary="Get Menu by Date",
    description="Get menu for a specific date (YYYY-MM-DD format)",
    responses={
        200: {"description": "Success", "model": SuccessResponse},
        400: {"description": "Invalid date format", "model": ErrorResponse},
        404: {"description": "No menu data found for date", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    },
    tags=["Menus"]
)
async def get_menu_by_date(
    date: str = Path(..., description="Date in YYYY-MM-DD format"),
    school_id: str = Query(
        default=os.getenv('SCHOOL_ID', 'CxnRNYOtBo6VrqiCb4AA'),
        description="School ID"
    ),
    language: str = Query(
        default=os.getenv('DEFAULT_LANGUAGE', 'en'),
        description="Language code"
    ),
    target_offer_id: str = Query(
        default=os.getenv('TARGET_OFFER_ID', 'ob6V4HfZK9Gs95sii4Cf'),
        description="Target Offer ID"
    )
):
    """Get menu for a specific date (YYYY-MM-DD format)."""
    try:
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD format."
            )
        
        logger.info(f"Fetching menu for date: {date}, school_id: {school_id}, target_offer_id: {target_offer_id}")
        
        # Initialize API client
        client = MeyersAPIClient(school_id=school_id, language=language, target_offer_id=target_offer_id)
        
        # Fetch data from API
        data = client.fetch_data()
        
        # Process and extract menu items
        processor = MenuDataProcessor()
        date_menus = processor.extract_menu_items(data, target_offer_id)
        
        if date not in date_menus:
            raise HTTPException(
                status_code=404,
                detail=f"No menu data found for date: {date}"
            )
        
        # Convert to serializable format
        date_data = date_menus[date]
        serializable_data = {
            "date": date_data.date,
            "timestamp": date_data.timestamp,
            "day_of_week": date_data.day_of_week,
            "items": [
                {
                    "item_name": item.item_name,
                    "item_category": item.item_category,
                    "item_id": item.item_id,
                    "menu_name": item.menu_name,
                    "menu_description": item.menu_description,
                    "pictograms": item.pictograms,
                    "labels": item.labels,
                    "allergens": item.allergens,
                }
                for item in date_data.items
            ]
        }
        
        return SuccessResponse(
            success=True,
            message=f'Successfully retrieved menu for {date}',
            data=serializable_data,
            metadata=Metadata(
                date=date,
                school_id=school_id,
                language=language,
                target_offer_id=target_offer_id,
                fetched_at=datetime.now().isoformat()
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching menu for date {date}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching menu: {str(e)}"
        )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            'success': False,
            'message': 'Endpoint not found',
            'data': None
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            'success': False,
            'message': 'Internal server error',
            'data': None
        }
    )

def log_available_endpoints():
    """Log all available endpoints and their HTTP methods."""
    logger.info("=" * 60)
    logger.info("AVAILABLE API ENDPOINTS:")
    logger.info("=" * 60)
    
    for route in app.routes:
        if hasattr(route, 'methods'):
            methods = ','.join(sorted(route.methods))
            logger.info(f"{methods:8} {route.path}")
    
    logger.info("=" * 60)
    logger.info(f"Base URL: http://{API_HOST}:{API_PORT}")
    logger.info(f"Swagger docs: http://{API_HOST}:{API_PORT}/docs")
    logger.info(f"ReDoc docs: http://{API_HOST}:{API_PORT}/redoc")
    logger.info("=" * 60)

if __name__ == '__main__':
    import uvicorn
    logger.info(f"Starting Meyers Scraper API on {API_HOST}:{API_PORT}")
    log_available_endpoints()
    uvicorn.run(
        "app:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG_MODE
    ) 