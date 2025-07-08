# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Meyers Scraper seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to the maintainers or through a private security advisory.

### What to Include

When reporting a vulnerability, please include:

1. **Description**: A clear description of the vulnerability
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Impact**: Potential impact of the vulnerability
4. **Suggested Fix**: If you have suggestions for fixing the issue
5. **Environment**: Your environment details (OS, Python version, etc.)

### What to Expect

1. **Acknowledgment**: You will receive an acknowledgment within 48 hours
2. **Assessment**: We will assess the reported vulnerability
3. **Updates**: We will keep you updated on our progress
4. **Resolution**: We will work to resolve the issue and release a fix

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest version of the software
2. **Environment Variables**: Store sensitive configuration in environment variables, not in code
3. **Network Security**: Use HTTPS when possible and secure your network connections
4. **Access Control**: Limit access to API endpoints and services

### For Developers

1. **Input Validation**: Always validate and sanitize input data
2. **Error Handling**: Don't expose sensitive information in error messages
3. **Dependencies**: Keep dependencies updated and monitor for security advisories
4. **Code Review**: Review code for security issues before merging

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new versions with the fixes
5. Publicly announce the vulnerability and the fix

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) and will be clearly marked as security releases in the changelog.

## Contact

For security-related issues, please contact the maintainers through the appropriate channels mentioned above.

Thank you for helping keep Meyers Scraper secure! 