"""
Display and output utilities for the Meyers Scraper.
"""

import json
import logging
from typing import Dict
from .models import DateMenu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default output file
DEFAULT_OUTPUT_FILE = os.getenv('DEFAULT_OUTPUT_FILE', 'date_menus.json')

logger = logging.getLogger(__name__)


class MenuDisplay:
    """Handle display and output of menu data."""
    
    @staticmethod
    def display_date_menus(date_menus: Dict[str, DateMenu]) -> None:
        """Display date menus data in a formatted way."""
        print("\n" + "="*60)
        print("DATE MENUS EXTRACTED FROM MEYERS API")
        print("="*60)
        
        print(f"\nTotal dates with menus: {len(date_menus)}")
        
        for date_str, date_data in sorted(date_menus.items()):
            print(f"\n📅 {date_data.day_of_week}, {date_data.date}")
            print("-" * 40)
            
            if not date_data.items:
                print("  No menu items available")
                continue
            
            for item in date_data.items:
                print(f"  🍽️  {item.menu_name}")
                if item.menu_description:
                    print(f"     📝 {item.menu_description}")
                print(f"     📂 Category: {item.item_category}")
                
                # Display pictograms if any
                if item.pictograms:
                    pictogram_names = list(item.pictograms.keys())
                    print(f"     🏷️  Pictograms: {', '.join(pictogram_names)}")
                
                # Display labels if any
                if item.labels:
                    label_names = list(item.labels.keys())
                    print(f"     🏷️  Labels: {', '.join(label_names)}")
                
                # Display allergens if any
                if item.allergens:
                    allergen_names = list(item.allergens.keys())
                    print(f"     ⚠️  Allergens: {', '.join(allergen_names)}")
                
                print()
        
        print("="*60)
    
    @staticmethod
    def save_to_json(date_menus: Dict[str, DateMenu], filename: str = DEFAULT_OUTPUT_FILE) -> None:
        """Save date menus data to a JSON file."""
        # Convert dataclasses to dictionaries for JSON serialization
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
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to {filename}")
            print(f"\n✅ Data saved to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save data to {filename}: {e}")
            print(f"\n❌ Failed to save data to {filename}: {e}")
            raise 