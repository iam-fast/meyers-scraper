#!/usr/bin/env python3
"""
Test script for the core Meyers Scraper functionality
"""

import sys
import os
import unittest

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import MenuItem, DateMenu
from src.client import MeyersAPIClient
from src.processor import MenuDataProcessor


class TestModels(unittest.TestCase):
    """Test the data models."""

    def test_menu_item_creation(self):
        """Test creating a MenuItem."""
        item = MenuItem(
            item_name="Test Item",
            item_category="Test Category",
            item_id="123",
            menu_name="Test Menu",
            menu_description="Test Description",
            pictograms={},
            labels={},
            allergens={},
        )

        self.assertEqual(item.item_name, "Test Item")
        self.assertEqual(item.item_category, "Test Category")
        self.assertEqual(item.item_id, "123")

    def test_date_menu_creation(self):
        """Test creating a DateMenu."""
        menu = DateMenu(
            date="2024-01-15", timestamp="1705276800", day_of_week="Monday", items=[]
        )

        self.assertEqual(menu.date, "2024-01-15")
        self.assertEqual(menu.day_of_week, "Monday")
        self.assertEqual(len(menu.items), 0)


class TestProcessor(unittest.TestCase):
    """Test the data processor."""

    def test_trim_string_fields(self):
        """Test string field trimming."""
        test_data = {
            "name": "Test Item   ",
            "description": "Test Description  ",
            "nested": {"field": "Nested Value  "},
        }

        result = MenuDataProcessor.trim_string_fields(test_data)

        self.assertEqual(result["name"], "Test Item")
        self.assertEqual(result["description"], "Test Description")
        self.assertEqual(result["nested"]["field"], "Nested Value")


class TestClient(unittest.TestCase):
    """Test the API client."""

    def test_client_initialization(self):
        """Test client initialization."""
        client = MeyersAPIClient()

        self.assertIsNotNone(client.base_url)
        self.assertIsNotNone(client.school_id)
        self.assertIsNotNone(client.headers)

    def test_build_payload(self):
        """Test payload building."""
        client = MeyersAPIClient()
        payload = client._build_payload()

        self.assertIn("schoolId", payload)
        self.assertIn("language", payload)
        self.assertIn("path", payload)


def run_tests():
    """Run all tests."""
    print("🧪 Running core functionality tests...")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestClient))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
