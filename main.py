#!/usr/bin/env python3
"""
Meyers API Scraper

A script to fetch and extract menu items from the Meyers API endpoint.
Organizes menu data by date and saves results to JSON format.
"""

import logging
import os
from dotenv import load_dotenv
from src.client import MeyersAPIClient
from src.processor import MenuDataProcessor
from src.display import MenuDisplay

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the Meyers scraper."""
    try:
        logger.info("Starting Meyers API scraper...")

        # Initialize API client
        client = MeyersAPIClient()

        # Fetch data from API
        logger.info("Fetching data from Meyers API...")
        data = client.fetch_data()

        # Process and extract menu items
        logger.info("Processing menu data...")
        processor = MenuDataProcessor()
        date_menus = processor.extract_menu_items(data)

        if not date_menus:
            logger.warning("No menu data found")
            print("❌ No menu data found")
            return

        # Display results
        logger.info("Displaying results...")
        MenuDisplay.display_date_menus(date_menus)

        # Save to JSON file
        logger.info("Saving data to JSON file...")
        MenuDisplay.save_to_json(date_menus)

        logger.info("Scraper completed successfully!")

    except Exception as e:
        logger.error(f"Scraper failed: {e}")
        print(f"❌ Scraper failed: {e}")
        raise


if __name__ == "__main__":
    main()
