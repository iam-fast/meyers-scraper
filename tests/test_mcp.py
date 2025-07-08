#!/usr/bin/env python3
"""
Tests for the MCP server functionality.
"""

import unittest
import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the MCP server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server import register_meyers_tools
from mcp.server.fastmcp import FastMCP


class TestMCPServer(unittest.TestCase):
    """Test cases for the MCP server functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mcp = FastMCP("Test Server", port=8002, streamable_http_path="/test")
        register_meyers_tools(self.mcp)

    @patch("mcp_server.MeyersAPIClient")
    @patch("mcp_server.MenuDataProcessor")
    def test_health_check(self, mock_processor, mock_client):
        """Test the health check tool."""
        # Get the health_check tool
        health_check_tool = None
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == "health_check":
                health_check_tool = tool
                break

        self.assertIsNotNone(
            health_check_tool, "health_check tool should be registered"
        )

        # Test the tool function
        result = asyncio.run(health_check_tool.fn())

        self.assertIn("status", result)
        self.assertIn("timestamp", result)
        self.assertIn("service", result)
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["service"], "meyers-scraper-mcp")

    @patch("mcp_server.MeyersAPIClient")
    @patch("mcp_server.MenuDataProcessor")
    def test_get_menu_by_date_invalid_format(self, mock_processor, mock_client):
        """Test the get_menu_by_date tool with invalid date format."""
        # Get the get_menu_by_date tool
        get_menu_tool = None
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == "get_menu_by_date":
                get_menu_tool = tool
                break

        self.assertIsNotNone(
            get_menu_tool, "get_menu_by_date tool should be registered"
        )

        # Test with invalid date format
        result = asyncio.run(get_menu_tool.fn(date="invalid-date"))

        self.assertIn("success", result)
        self.assertIn("message", result)
        self.assertFalse(result["success"])
        self.assertIn("Invalid date format", result["message"])

    def test_tool_registration(self):
        """Test that all expected tools are registered."""
        expected_tools = [
            "get_all_menus",
            "get_menu_by_date",
            "health_check",
        ]

        registered_tools = [
            tool.name for tool in self.mcp._tool_manager._tools.values()
        ]

        for tool_name in expected_tools:
            self.assertIn(
                tool_name, registered_tools, f"Tool {tool_name} should be registered"
            )

    def test_tool_parameters(self):
        """Test that tools have the expected parameters."""
        # Test get_all_menus parameters
        get_all_menus_tool = None
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == "get_all_menus":
                get_all_menus_tool = tool
                break

        self.assertIsNotNone(get_all_menus_tool)
        self.assertEqual(
            len(get_all_menus_tool.parameters), 3
        )  # school_id, language, target_offer_id

        # Test get_menu_by_date parameters
        get_menu_tool = None
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == "get_menu_by_date":
                get_menu_tool = tool
                break

        self.assertIsNotNone(get_menu_tool)
        self.assertEqual(
            len(get_menu_tool.parameters), 4
        )  # date, school_id, language, target_offer_id


if __name__ == "__main__":
    unittest.main()
