"""
Data processing utilities for the Meyers Scraper.
"""

import datetime
import logging
from typing import Dict, Any
from .models import MenuItem, DateMenu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default TARGET_OFFER_ID
TARGET_OFFER_ID = os.getenv('TARGET_OFFER_ID', 'ob6V4HfZK9Gs95sii4Cf')

logger = logging.getLogger(__name__)


class MenuDataProcessor:
    """Process and extract menu data from API responses."""
    
    @staticmethod
    def trim_string_fields(obj: Any) -> Any:
        """Recursively trim trailing spaces from all string fields in an object."""
        if isinstance(obj, dict):
            return {key: MenuDataProcessor.trim_string_fields(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [MenuDataProcessor.trim_string_fields(item) for item in obj]
        elif isinstance(obj, str):
            return obj.rstrip()
        else:
            return obj
    
    @staticmethod
    def _extract_menu_item(item_data: Dict[str, Any], date_timestamp: str, menu: Dict[str, Any]) -> MenuItem:
        """Extract a single menu item from the data."""
        return MenuItem(
            item_name=item_data['name'],
            item_category=item_data['category'],
            item_id=item_data['id'],
            menu_name=menu.get('name', ''),
            menu_description=menu.get('description', ''),
            pictograms=menu.get('pictograms', {}),
            labels=menu.get('labels', {}),
            allergens=menu.get('allergens', {})
        )
    
    @staticmethod
    def _process_date_info(item_data: Dict[str, Any], date_menus: Dict[str, DateMenu]) -> None:
        """Process date information for a menu item."""
        if 'dates' not in item_data:
            return
        
        for date_timestamp, date_info in item_data['dates'].items():
            if not date_info.get('available', False) or 'menu' not in date_info:
                continue
            
            menu = date_info['menu']
            date_str = datetime.datetime.fromtimestamp(int(date_timestamp)).strftime('%Y-%m-%d')
            
            # Initialize date entry if it doesn't exist
            if date_str not in date_menus:
                date_menus[date_str] = DateMenu(
                    date=date_str,
                    timestamp=date_timestamp,
                    day_of_week=datetime.datetime.fromtimestamp(int(date_timestamp)).strftime('%A'),
                    items=[]
                )
            
            # Add this item's menu to the date
            menu_item = MenuDataProcessor._extract_menu_item(item_data, date_timestamp, menu)
            menu_item = MenuDataProcessor.trim_string_fields(menu_item)
            date_menus[date_str].items.append(menu_item)
            
            logger.debug(f"Added menu for {date_str}: {menu.get('name', 'N/A')}")
    
    @classmethod
    def extract_menu_items(cls, data: Dict[str, Any], target_offer_id: str = TARGET_OFFER_ID) -> Dict[str, DateMenu]:
        """Extract all menu items from the API response."""
        date_menus: Dict[str, DateMenu] = {}
        
        logger.info(f"Top-level keys in response: {list(data.keys())}")
        
        if 'offers' not in data:
            logger.warning("No 'offers' key found in response")
            return date_menus
        
        offers = data['offers']
        logger.info(f"Found 'offers' key with {len(offers)} items")
        
        # Process the specific offer we're interested in
        if target_offer_id not in offers:
            logger.warning(f"Target offer {target_offer_id} not found")
            return date_menus
        
        offer_data = offers[target_offer_id]
        logger.debug(f"Offer {target_offer_id} keys: {list(offer_data.keys())}")
        
        if 'items' not in offer_data:
            logger.warning("No 'items' key found in offer data")
            return date_menus
        
        items = offer_data['items']
        logger.info(f"Found 'items' key with {len(items)} items")
        
        for item_data in items:
            logger.debug(f"Processing item: {item_data['name']} (Category: {item_data['category']})")
            cls._process_date_info(item_data, date_menus)
        
        # Trim trailing spaces from all extracted data
        return cls.trim_string_fields(date_menus) 