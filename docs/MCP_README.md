# Meyers Scraper MCP Server

A Model Context Protocol (MCP) server that exposes the Meyers API scraper endpoints as tools that can be used by MCP clients.

## Overview

The MCP server provides the same functionality as the FastAPI server but through the Model Context Protocol, making it accessible to MCP-compatible clients and AI assistants.

## Features

- **get_all_menus**: Fetch all available menus for specified parameters
- **get_menu_by_date**: Fetch menu for a specific date (YYYY-MM-DD format)
- **get_todays_menu**: Fetch today's menu automatically (no date parameter needed)
- **health_check**: Check server health status
- **get_today_date**: Get today's date in various formats

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd meyers-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The MCP server uses the same environment variables as the main API:

- `MCP_PORT`: Port for the MCP server (default: 8001)
- `SCHOOL_ID`: School ID for the Meyers API (default: "CxnRNYOtBo6VrqiCb4AA")
- `DEFAULT_LANGUAGE`: Language code (default: "en")
- `TARGET_OFFER_ID`: Target Offer ID (default: "ob6V4HfZK9Gs95sii4Cf")
- `LOG_LEVEL`: Logging level (default: "INFO")

## Running the MCP Server

### Option 1: Using the startup script
```bash
./start_mcp.sh
```

### Option 2: Direct execution
```bash
python mcp_server.py
```

### Option 3: With custom configuration
```bash
MCP_PORT=8002 SCHOOL_ID="your-school-id" python mcp_server.py
```

## Server Information

- **Server Name**: Meyers Scraper
- **Default Port**: 8001
- **Streamable HTTP Path**: `/meyers-scraper`
- **Transport**: Streamable HTTP

## Available Tools

### 1. get_all_menus

Fetches all available menus for the specified parameters.

**Parameters:**
- `school_id` (optional): School ID for the Meyers API
- `language` (optional): Language code (e.g., 'en', 'de')
- `target_offer_id` (optional): Target Offer ID for the Meyers API

**Returns:**
- Success response with all menu data organized by date
- Error response if no data is found or an error occurs

### 2. get_menu_by_date

Fetches menu data for a specific date.

**Parameters:**
- `date` (required): Date in YYYY-MM-DD format (e.g., '2024-01-15')
- `school_id` (optional): School ID for the Meyers API
- `language` (optional): Language code (e.g., 'en', 'de')
- `target_offer_id` (optional): Target Offer ID for the Meyers API

**Returns:**
- Success response with menu data for the specified date
- Error response if date is invalid or no data is found

### 3. health_check

Provides basic health status information about the server.

**Parameters:** None

**Returns:**
- Server status, timestamp, service name, port, and streamable HTTP path

### 4. get_todays_menu

Fetches today's menu automatically without requiring a date parameter.

**Parameters:**
- `school_id` (optional): School ID for the Meyers API
- `language` (optional): Language code (e.g., 'en', 'de')
- `target_offer_id` (optional): Target Offer ID for the Meyers API

**Returns:**
- Success response with today's menu data
- Error response if no menu is available for today

### 5. get_today_date

Returns today's date in various formats for easy integration with other tools.

**Parameters:** None

**Returns:**
- Success response with today's date in multiple formats (ISO, day of week, etc.)
- Error response if date calculation fails

## Response Format

All tools return responses in a consistent format:

```json
{
  "success": true/false,
  "message": "Description of the result",
  "data": {
    // Tool-specific data
  },
  "metadata": {
    "total_dates": 5,
    "school_id": "CxnRNYOtBo6VrqiCb4AA",
    "language": "en",
    "target_offer_id": "ob6V4HfZK9Gs95sii4Cf",
    "fetched_at": "2024-01-15T10:30:00"
  }
}
```

## Menu Item Structure

Each menu item contains:

```json
{
  "item_name": "Name of the menu item",
  "item_category": "Category of the menu item",
  "item_id": "Unique identifier",
  "menu_name": "Name of the menu",
  "menu_description": "Description of the menu",
  "pictograms": {},
  "labels": {},
  "allergens": {}
}
```

## Integration with MCP Clients

The MCP server can be integrated with any MCP-compatible client. The server exposes tools that can be called by AI assistants and other MCP clients.

### Example Client Configuration

```json
{
  "mcpServers": {
    "meyers-scraper": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "MCP_PORT": "8001",
        "SCHOOL_ID": "your-school-id"
      }
    }
  }
}
```

## Running Both Servers

You can run both the FastAPI server and the MCP server simultaneously:

```bash
# Terminal 1: Start the FastAPI server
./start_api.sh

# Terminal 2: Start the MCP server
./start_mcp.sh
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the `MCP_PORT` environment variable
2. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **API errors**: Check that the environment variables are set correctly

### Logs

The server logs information about:
- Tool calls and parameters
- API responses and errors
- Server startup and configuration

## Development

To modify the MCP server:

1. Edit `mcp_server.py` to add new tools or modify existing ones
2. Update the `register_meyers_tools` function
3. Test with an MCP client
4. Update this README if needed

## License

Same as the main project. 