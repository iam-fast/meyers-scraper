# Contributing to Meyers Scraper

Thank you for your interest in contributing to Meyers Scraper! This document provides guidelines for contributing to this project.

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate of others.

## How to Contribute

### Reporting Issues

1. Check if the issue has already been reported
2. Use the issue template if available
3. Provide clear and detailed information about the problem
4. Include steps to reproduce the issue
5. Mention your environment (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has already been suggested
2. Describe the feature clearly and explain why it would be useful
3. Consider the impact on existing functionality
4. Provide examples of how the feature would work

### Submitting Code Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following the coding standards below
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes with clear commit messages
7. Push to your fork and submit a pull request

## Coding Standards

### Python Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Code Structure

- Keep the modular structure intact
- Add new functionality in appropriate modules
- Update environment variables for new settings
- Add proper error handling and logging

### Testing

- Write unit tests for new functionality
- Ensure existing tests continue to pass
- Use descriptive test names
- Test both success and error cases

### Documentation

- Update README.md if adding new features
- Add docstrings for new functions and classes
- Update API documentation if changing endpoints
- Include examples for new functionality

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure as needed
6. Run tests: `python run_tests.py`

## Pull Request Guidelines

1. Provide a clear description of the changes
2. Reference any related issues
3. Include tests for new functionality
4. Ensure the code follows the project's style guidelines
5. Update documentation as needed

## Questions or Need Help?

If you have questions or need help with contributing, please open an issue or reach out to the maintainers.

Thank you for contributing to Meyers Scraper! 