# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release
- FastAPI server with comprehensive endpoints
- MCP server with tools for menu data access
- Docker support with health checks
- Comprehensive test suite
- Documentation and examples

## [1.0.0] - 2024-01-15

### Added
- Core Meyers API scraper functionality
- Modular architecture with separate client, processor, and display components
- Type-safe data models using dataclasses
- Comprehensive error handling and logging
- Configuration management system
- JSON output with organized menu data by date
- FastAPI server with RESTful endpoints
- Model Context Protocol (MCP) server
- Docker containerization
- Health check endpoints
- CORS middleware support
- Comprehensive API documentation with Swagger/OpenAPI
- Test suite with unit and integration tests
- Startup scripts for easy deployment
- Environment variable configuration
- User agent and timeout configuration
- Data validation and sanitization
- Support for multiple languages
- Configurable school and offer IDs

### Features
- **API Endpoints**:
  - `GET /api/health/` - Health check
  - `GET /api/menus/` - Get all menus
  - `GET /api/menus/{date}` - Get menu by specific date
  - `GET /api/menus/today` - Get today's menu

- **MCP Tools**:
  - `get_all_menus` - Fetch all available menus
  - `get_menu_by_date` - Fetch menu for specific date
  - `get_todays_menu` - Fetch today's menu automatically
  - `health_check` - Check server health
  - `get_today_date` - Get today's date in various formats

### Technical Details
- Python 3.8+ compatibility
- FastAPI framework for API server
- Uvicorn/Gunicorn for production deployment
- Pydantic for data validation
- Requests library for HTTP communication
- Comprehensive logging with configurable levels
- Docker multi-stage builds for optimization
- Non-root user execution in containers
- Health checks for container orchestration

### Documentation
- Comprehensive README with usage examples
- API documentation with OpenAPI/Swagger
- MCP server documentation
- Docker deployment guide
- Testing instructions
- Configuration guide
- Contributing guidelines
- Security policy
- License information 