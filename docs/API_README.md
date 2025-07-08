# Meyers Scraper API

A Flask-based REST API that provides endpoints to fetch and extract menu items from the Meyers API. This API wraps the existing Meyers scraper functionality and provides a clean HTTP interface.

## Features

- **Health Check**: Monitor API status
- **Get All Menus**: Fetch all available menu data
- **Get Menu by Date**: Retrieve menu for a specific date
- **Export Menus**: Export menu data to JSON file
- **CORS Support**: Cross-origin resource sharing enabled
- **Environment Configuration**: Configurable via environment variables
- **Docker Support**: Containerized deployment
- **Error Handling**: Comprehensive error responses

## Quick Start

### Using Docker (Recommended)

1. **Clone and build:**
   ```bash
   docker-compose up --build
   ```

2. **Access the API:**
   - Health check: http://localhost:5015/api/health
   - API base: http://localhost:5015/api

### Using Python directly

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
```
GET /health
```
Returns the API status and basic information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "service": "meyers-scraper-api"
}
```

### Get All Menus
```
GET /api/menus
```

**Query Parameters:**
- `school_id` (optional): School ID (default: from config)
- `language` (optional): Language code (default: 'en')
- `target_offer_id` (optional): Target Offer ID (default: from config)

**Response:**
```json
{
  "success": true,
  "message": "Successfully retrieved 5 date menus",
  "data": {
    "2024-01-15": {
      "date": "2024-01-15",
      "timestamp": "1705312800",
      "day_of_week": "Monday",
      "items": [
        {
          "item_name": "Chicken Pasta",
          "item_category": "Main Course",
          "item_id": "item123",
          "menu_name": "Lunch Menu",
          "menu_description": "Delicious chicken pasta with vegetables",
          "pictograms": {},
          "labels": {},
          "allergens": {}
        }
      ]
    }
  },
  "metadata": {
    "total_dates": 5,
    "school_id": "CxnRNYOtBo6VrqiCb4AA",
    "language": "en",
    "fetched_at": "2024-01-15T10:30:00.123456"
  }
}
```

### Get Menu by Date
```
GET /api/menus/{date}
```

**Path Parameters:**
- `date`: Date in YYYY-MM-DD format

**Query Parameters:**
- `school_id` (optional): School ID (default: from environment variables)
- `language` (optional): Language code (default: 'en')
- `target_offer_id` (optional): Target Offer ID (default: from environment variables)

**Response:**
```json
{
  "success": true,
  "message": "Successfully retrieved menu for 2024-01-15",
  "data": {
    "date": "2024-01-15",
    "timestamp": "1705312800",
    "day_of_week": "Monday",
    "items": [
      {
        "item_name": "Chicken Pasta",
        "item_category": "Main Course",
        "item_id": "item123",
        "menu_name": "Lunch Menu",
        "menu_description": "Delicious chicken pasta with vegetables",
        "pictograms": {},
        "labels": {},
        "allergens": {}
      }
    ]
  },
  "metadata": {
    "date": "2024-01-15",
    "school_id": "CxnRNYOtBo6VrqiCb4AA",
    "language": "en",
    "fetched_at": "2024-01-15T10:30:00.123456"
  }
}
```

### Export Menus
```
POST /api/menus/export
```

**Request Body:**
```json
{
  "filename": "menus_export_20240115.json",
  "school_id": "CxnRNYOtBo6VrqiCb4AA",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully exported menus to menus_export_20240115.json",
  "data": {
    "filename": "menus_export_20240115.json",
    "total_dates": 5,
    "exported_at": "2024-01-15T10:30:00.123456"
  }
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "data": null
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (no data available)
- `500`: Internal Server Error

## Configuration

The API can be configured using environment variables or a `.env` file:

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | `0.0.0.0` | Host to bind the API to |
| `API_PORT` | `5015` | Port to run the API on |
| `DEBUG_MODE` | `False` | Enable debug mode |
| `SCHOOL_ID` | `CxnRNYOtBo6VrqiCb4AA` | Default school ID |
| `DEFAULT_LANGUAGE` | `en` | Default language |
| `LOG_LEVEL` | `INFO` | Logging level |
| `REQUEST_TIMEOUT` | `30` | API request timeout |

## Usage Examples

### Using curl

1. **Health check:**
   ```bash
   curl http://localhost:5015/api/health
   ```

2. **Get all menus:**
   ```bash
   curl "http://localhost:5015/api/menus?school_id=CxnRNYOtBo6VrqiCb4AA&language=en"
   ```

3. **Get menu for specific date:**
   ```bash
   curl "http://localhost:5015/api/menus/2024-01-15"
   ```

4. **Export menus:**
   ```bash
   curl -X POST http://localhost:5015/api/menus/export \
     -H "Content-Type: application/json" \
     -d '{"filename": "my_menus.json"}'
   ```

### Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:5015/api/health')
print(response.json())

# Get all menus
response = requests.get('http://localhost:5015/api/menus')
menus = response.json()
print(f"Found {menus['metadata']['total_dates']} dates with menus")

# Get menu for specific date
response = requests.get('http://localhost:5015/api/menus/2024-01-15')
menu_data = response.json()
print(f"Menu for 2024-01-15: {menu_data['data']['items']}")

# Export menus
response = requests.post('http://localhost:5015/api/menus/export', 
                        json={'filename': 'export.json'})
print(response.json())
```

## Development

### Running in Development Mode

1. Set `DEBUG_MODE=True` in your `.env` file
2. Run the API:
   ```bash
   python app.py
   ```

### Running Tests

```bash
# Install test dependencies
pip install pytest requests

# Run tests
pytest
```

### Code Structure

```
meyers-scraper/
├── app.py              # Main Flask API application
├── main.py             # Original scraper logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .env               # Environment variables
└── API_README.md      # This documentation
```

## Deployment

### Docker Deployment

1. **Build and run:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop:**
   ```bash
   docker-compose down
   ```

### Production Deployment

For production deployment, consider:

1. **Using a reverse proxy** (nginx, Apache)
2. **Setting up SSL/TLS** certificates
3. **Implementing rate limiting**
4. **Adding authentication** if needed
5. **Setting up monitoring** and logging
6. **Using environment-specific configurations**

### Environment Variables for Production

```bash
# Production settings
API_HOST=0.0.0.0
API_PORT=5015
DEBUG_MODE=False
LOG_LEVEL=WARNING
REQUEST_TIMEOUT=30
```

## Troubleshooting

### Common Issues

1. **API not responding:**
   - Check if the service is running: `docker-compose ps`
   - Check logs: `docker-compose logs meyers-api`
   - Verify port is not in use: `netstat -tulpn | grep 5015`

2. **No menu data returned:**
   - Verify the school ID is correct
   - Check if the Meyers API is accessible
   - Review the logs for error messages

3. **CORS issues:**
   - The API includes CORS headers by default
   - If issues persist, check your client configuration

### Logs

The API provides detailed logging. Check logs for:
- API request/response details
- Error messages and stack traces
- Performance metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 