"""
Data models for the Meyers Scraper.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class MenuItem:
    """Data class representing a menu item."""

    item_name: str
    item_category: str
    item_id: str
    menu_name: str
    menu_description: str
    pictograms: Dict[str, Any]
    labels: Dict[str, Any]
    allergens: Dict[str, Any]


@dataclass
class DateMenu:
    """Data class representing menu data for a specific date."""

    date: str
    timestamp: str
    day_of_week: str
    items: List[MenuItem]
