#!/usr/bin/env python3
"""
Meyers Scraper MCP Server

A Model Context Protocol (MCP) server that exposes the Meyers API scraper endpoints
as tools that can be used by MCP clients.
"""

import os
import logging
from datetime import datetime
from typing import Annotated, Dict, Any
from dotenv import load_dotenv
from pydantic import Field

from mcp.server.fastmcp import FastMCP

# Import the existing scraper components
from src.client import MeyersAPIClient
from src.processor import MenuDataProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format=os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"),
)
logger = logging.getLogger(__name__)

# Configuration
MCP_PORT = int(os.getenv("MCP_PORT", 8001))
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
SCHOOL_ID = os.getenv("SCHOOL_ID", "CxnRNYOtBo6VrqiCb4AA")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
TARGET_OFFER_ID = os.getenv("TARGET_OFFER_ID", "ob6V4HfZK9Gs95sii4Cf")

# Create the MCP server
mcp = FastMCP("Meyers Scraper", port=MCP_PORT, host=MCP_HOST, streamable_http_path="/meyers-scraper")


def register_meyers_tools(mcp: FastMCP):
    """Register all Meyers scraper tools with the MCP server"""

    @mcp.tool()
    async def get_all_menus(
        school_id: Annotated[
            str, Field(default=SCHOOL_ID, description="School ID for the Meyers API")
        ] = SCHOOL_ID,
        language: Annotated[
            str,
            Field(
                default=DEFAULT_LANGUAGE, description="Language code (e.g., 'en', 'de')"
            ),
        ] = DEFAULT_LANGUAGE,
        target_offer_id: Annotated[
            str,
            Field(
                default=TARGET_OFFER_ID,
                description="Target Offer ID for the Meyers API",
            ),
        ] = TARGET_OFFER_ID,
    ) -> Dict[str, Any]:
        """
        Get all available menus for the specified parameters.

        This tool fetches all menu data from the Meyers API and returns
        a comprehensive list of menu items organized by date.
        """
        try:
            logger.info(
                f"Fetching all menus for school_id: {school_id}, language: {language}, target_offer_id: {target_offer_id}"
            )

            # Initialize API client
            client = MeyersAPIClient(
                school_id=school_id, language=language, target_offer_id=target_offer_id
            )

            # Fetch data from API
            data = client.fetch_data()

            # Process and extract menu items
            processor = MenuDataProcessor()
            date_menus = processor.extract_menu_items(data, target_offer_id)

            if not date_menus:
                return {
                    "success": False,
                    "message": "No menu data found",
                    "data": {},
                    "metadata": {
                        "total_dates": 0,
                        "school_id": school_id,
                        "language": language,
                        "target_offer_id": target_offer_id,
                        "fetched_at": datetime.now().isoformat(),
                    },
                }

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
                    ],
                }

            return {
                "success": True,
                "message": f"Successfully retrieved {len(date_menus)} date menus",
                "data": serializable_data,
                "metadata": {
                    "total_dates": len(date_menus),
                    "school_id": school_id,
                    "language": language,
                    "target_offer_id": target_offer_id,
                    "fetched_at": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"Error fetching all menus: {e}")
            return {
                "success": False,
                "message": f"Error fetching menus: {str(e)}",
                "data": {},
                "metadata": {
                    "school_id": school_id,
                    "language": language,
                    "target_offer_id": target_offer_id,
                    "fetched_at": datetime.now().isoformat(),
                },
            }

    @mcp.tool()
    async def get_menu_by_date(
        date: Annotated[
            str, Field(description="Date in YYYY-MM-DD format (e.g., '2024-01-15')")
        ],
        school_id: Annotated[
            str, Field(default=SCHOOL_ID, description="School ID for the Meyers API")
        ] = SCHOOL_ID,
        language: Annotated[
            str,
            Field(
                default=DEFAULT_LANGUAGE, description="Language code (e.g., 'en', 'de')"
            ),
        ] = DEFAULT_LANGUAGE,
        target_offer_id: Annotated[
            str,
            Field(
                default=TARGET_OFFER_ID,
                description="Target Offer ID for the Meyers API",
            ),
        ] = TARGET_OFFER_ID,
    ) -> Dict[str, Any]:
        """
        Get menu for a specific date.

        This tool fetches menu data for a specific date from the Meyers API.
        The date should be in YYYY-MM-DD format.
        """
        try:
            logger.info(
                f"Fetching menu for date: {date}, school_id: {school_id}, "
                f"language: {language}, target_offer_id: {target_offer_id}"
            )

            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid date format. Please use YYYY-MM-DD format",
                    "data": {},
                    "metadata": {
                        "date": date,
                        "school_id": school_id,
                        "language": language,
                        "target_offer_id": target_offer_id,
                        "fetched_at": datetime.now().isoformat(),
                    },
                }

            # Initialize API client
            client = MeyersAPIClient(
                school_id=school_id, language=language, target_offer_id=target_offer_id
            )

            # Fetch data from API
            data = client.fetch_data()

            # Process and extract menu items
            processor = MenuDataProcessor()
            date_menus = processor.extract_menu_items(data, target_offer_id)

            # Find the specific date
            if date not in date_menus:
                return {
                    "success": False,
                    "message": f"No menu data found for date: {date}",
                    "data": {},
                    "metadata": {
                        "date": date,
                        "school_id": school_id,
                        "language": language,
                        "target_offer_id": target_offer_id,
                        "fetched_at": datetime.now().isoformat(),
                    },
                }

            date_data = date_menus[date]

            # Convert to serializable format
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
                ],
            }

            return {
                "success": True,
                "message": f"Successfully retrieved menu for {date}",
                "data": serializable_data,
                "metadata": {
                    "date": date,
                    "school_id": school_id,
                    "language": language,
                    "target_offer_id": target_offer_id,
                    "fetched_at": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"Error fetching menu for date {date}: {e}")
            return {
                "success": False,
                "message": f"Error fetching menu for date {date}: {str(e)}",
                "data": {},
                "metadata": {
                    "date": date,
                    "school_id": school_id,
                    "language": language,
                    "target_offer_id": target_offer_id,
                    "fetched_at": datetime.now().isoformat(),
                },
            }

    @mcp.tool()
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint to verify the MCP server is running.

        This tool provides basic health status information about the server.
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "meyers-scraper-mcp",
            "port": MCP_PORT,
            "streamable_http_path": "/meyers-scraper",
        }

    @mcp.tool()
    async def get_today_date() -> Dict[str, Any]:
        """
        Get today's date in various formats.

        This tool returns the current date in multiple formats including
        YYYY-MM-DD, day of week, and timestamp for easy integration
        with other date-based tools.
        """
        try:
            today = datetime.now()

            return {
                "success": True,
                "date": {
                    "iso_date": today.strftime("%Y-%m-%d"),
                    "day_of_week": today.strftime("%A"),
                    "day_of_week_short": today.strftime("%a"),
                    "month": today.strftime("%B"),
                    "month_short": today.strftime("%b"),
                    "year": today.year,
                    "day": today.day,
                    "month_num": today.month,
                    "timestamp": today.isoformat(),
                    "unix_timestamp": int(today.timestamp()),
                },
                "metadata": {"fetched_at": today.isoformat(), "timezone": "local"},
            }

        except Exception as e:
            logger.error(f"Error getting today's date: {e}")
            return {
                "success": False,
                "message": f"Error getting today's date: {str(e)}",
                "date": {},
                "metadata": {"fetched_at": datetime.now().isoformat()},
            }

    @mcp.tool()
    async def get_todays_menu(
        school_id: Annotated[
            str, Field(default=SCHOOL_ID, description="School ID for the Meyers API")
        ] = SCHOOL_ID,
        language: Annotated[
            str,
            Field(
                default=DEFAULT_LANGUAGE, description="Language code (e.g., 'en', 'de')"
            ),
        ] = DEFAULT_LANGUAGE,
        target_offer_id: Annotated[
            str,
            Field(
                default=TARGET_OFFER_ID,
                description="Target Offer ID for the Meyers API",
            ),
        ] = TARGET_OFFER_ID,
    ) -> Dict[str, Any]:
        """
        Get today's menu from the Meyers API.

        This tool automatically determines today's date and fetches the menu
        for that date using the existing get_menu_by_date functionality.
        """
        try:
            # Get today's date using the existing function
            today_result = await get_today_date()

            if not today_result.get("success"):
                return {
                    "success": False,
                    "message": "Failed to get today's date",
                    "data": {},
                    "metadata": {
                        "school_id": school_id,
                        "language": language,
                        "target_offer_id": target_offer_id,
                        "fetched_at": datetime.now().isoformat(),
                    },
                }

            today_date = today_result["date"]["iso_date"]

            # Use the existing get_menu_by_date function
            return await get_menu_by_date(
                date=today_date,
                school_id=school_id,
                language=language,
                target_offer_id=target_offer_id,
            )

        except Exception as e:
            logger.error(f"Error in get_todays_menu: {e}")
            return {
                "success": False,
                "message": f"Error fetching today's menu: {str(e)}",
                "data": {},
                "metadata": {
                    "school_id": school_id,
                    "language": language,
                    "target_offer_id": target_offer_id,
                    "fetched_at": datetime.now().isoformat(),
                },
            }


# Register all tools
register_meyers_tools(mcp)

if __name__ == "__main__":
    print("🚀 Starting Meyers Scraper MCP Server...")
    print(f"📍 Server will be available at: http://{MCP_HOST}:{MCP_PORT}")
    print("🔧 Streamable HTTP path: /meyers-scraper")
    print("📚 Available tools:")
    print("   - get_all_menus: Fetch all available menus")
    print("   - get_menu_by_date: Fetch menu for a specific date")
    print("   - get_todays_menu: Fetch today's menu automatically")
    print("   - health_check: Check server health")
    print("   - get_today_date: Get today's date in various formats")
    print("-" * 50)

    mcp.run(transport="streamable-http")
