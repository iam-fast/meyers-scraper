# Meyers API Scraper

A clean, well-structured Python script to fetch and extract menu items from the Meyers API endpoint. The script organizes menu data by date and saves results to JSON format.

## Features

- **Clean Architecture**: Object-oriented design with separate classes for API client, data processing, and display
- **Type Safety**: Full type hints for better code maintainability and IDE support
- **Error Handling**: Comprehensive error handling with proper logging
- **Configuration Management**: Centralized configuration in a separate file
- **Data Validation**: Proper data structure validation using dataclasses
- **Logging**: Structured logging with configurable levels

## Project Structure

```
meyers-scraper/
├── src/                    # Core application code
│   ├── __init__.py
│   ├── models.py          # Data models (MenuItem, DateMenu)
│   ├── client.py          # API client for Meyers
│   ├── processor.py       # Data processing logic
│   └── display.py         # Display and output utilities
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_api.py        # API endpoint tests
│   ├── test_core.py       # Core functionality tests
│   └── test_mcp.py        # MCP server tests
├── docs/                  # Documentation
│   ├── API_README.md      # API documentation
│   ├── MCP_README.md      # MCP server documentation
│   ├── CHANGELOG.md       # Version history
│   ├── CONTRIBUTING.md    # Contributing guidelines
│   └── SECURITY.md        # Security policy
├── scripts/               # Startup and utility scripts
│   ├── setup.sh           # Initial setup script
│   ├── start_api.sh       # API startup script
│   ├── start_mcp.sh       # MCP server startup script
│   └── run_tests.py       # Test runner
├── config/                # Configuration files
│   ├── .env               # Environment variables
│   └── .env.example       # Environment variables template
├── deploy/                # Deployment files
│   ├── Dockerfile         # Docker configuration
│   └── docker-compose.yml # Docker Compose setup
├── main.py                # Standalone script entry point
├── app.py                 # FastAPI entry point
├── mcp_server.py          # MCP server entry point
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md             # This file
└── LICENSE               # MIT License
```

## Installation

1. Clone or download this repository
2. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```

Or manually:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Standalone Script
Run the script:
```bash
python main.py
```

The script will:
1. Fetch menu data from the Meyers API
2. Process and organize the data by date
3. Save the results to `date_menus.json`
4. Display a formatted summary in the console

### API Server
Start the FastAPI server:
```bash
./scripts/start_api.sh
```

Or run directly:
```bash
python app.py
```

Or use Docker:
```bash
docker-compose -f deploy/docker-compose.yml up
```

The API will be available at `http://localhost:5015`

### MCP Server
Start the Model Context Protocol (MCP) server:
```bash
./scripts/start_mcp.sh
```

Or run directly:
```bash
python mcp_server.py
```

The MCP server will be available at `http://localhost:8001` with streamable HTTP path `/meyers-scraper`.

**Available MCP Tools:**
- `get_all_menus`: Fetch all available menus
- `get_menu_by_date`: Fetch menu for a specific date
- `get_todays_menu`: Fetch today's menu automatically
- `health_check`: Check server health
- `get_today_date`: Get today's date in various formats

For detailed MCP server documentation, see [docs/MCP_README.md](docs/MCP_README.md).

## Testing

Run all tests:
```bash
python scripts/run_tests.py
```

Or run individual test suites:
```bash
# Core functionality tests
python tests/test_core.py

# API tests (requires API to be running)
python tests/test_api.py
```

## Configuration

Set environment variables to customize:
- API endpoints and school ID
- Request timeouts and user agent
- Output file names
- Logging levels

## Code Improvements Made

### Original Code Issues:
- Monolithic structure with all logic in a single function
- No type hints or data validation
- Hardcoded values scattered throughout
- Basic error handling
- No separation of concerns

### Improvements:
1. **Modular Design**: Split into focused classes:
   - `MeyersAPIClient`: Handles API communication
   - `MenuDataProcessor`: Processes and extracts menu data
   - `MenuDisplay`: Handles output and display

2. **Type Safety**: Added comprehensive type hints and dataclasses for data structures

3. **Configuration Management**: Moved all configuration to environment variables

4. **Error Handling**: Added proper exception handling with logging

5. **Code Organization**: 
   - Clear separation of concerns
   - Static methods where appropriate
   - Consistent naming conventions

6. **Maintainability**: 
   - Better documentation
   - Consistent code style
   - Reusable components

## Output

The script generates a JSON file with the following structure:
```json
{
  "2024-01-15": {
    "date": "2024-01-15",
    "timestamp": "1705276800",
    "day_of_week": "Monday",
    "items": [
      {
        "item_name": "Main Course",
        "item_category": "Hot Food",
        "item_id": "123",
        "menu_name": "Grilled Chicken",
        "menu_description": "Served with vegetables",
        "pictograms": {},
        "labels": {},
        "allergens": {}
      }
    ]
  }
}
```

## Dependencies

- `requests`: HTTP library for API calls
- `fastapi`: Web framework for the API server
- `uvicorn`: ASGI server for FastAPI
- `pydantic`: Data validation and settings management
- `mcp`: Model Context Protocol server framework
- Standard library modules: `json`, `datetime`, `logging`, `typing`, `dataclasses`

## License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Security

If you discover a security vulnerability, please see our [Security Policy](docs/SECURITY.md) for reporting guidelines.

## Changelog

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for a list of changes and version history. 