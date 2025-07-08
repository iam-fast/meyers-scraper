"""
API client for interacting with the Meyers API.
"""

import requests
import json
import logging
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = "https://meyers.kanpla.dk/api/internal/load/frontend"
SCHOOL_ID = os.getenv("SCHOOL_ID", "CxnRNYOtBo6VrqiCb4AA")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
TARGET_OFFER_ID = os.getenv("TARGET_OFFER_ID", "ob6V4HfZK9Gs95sii4Cf")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
)

logger = logging.getLogger(__name__)


class MeyersAPIClient:
    """Client for interacting with the Meyers API."""

    def __init__(
        self,
        school_id: str = SCHOOL_ID,
        language: str = DEFAULT_LANGUAGE,
        target_offer_id: str = TARGET_OFFER_ID,
    ):
        self.base_url = API_BASE_URL
        self.school_id = school_id
        self.language = language
        self.target_offer_id = target_offer_id
        self.headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}

    def _build_payload(self) -> Dict[str, Any]:
        """Build the API request payload."""
        return {
            "userId": None,
            "schoolId": self.school_id,
            "url": "meyers",
            "_reloader": 0,
            "language": self.language,
            "path": "load/frontend",
        }

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch data from the Meyers API."""
        payload = self._build_payload()

        logger.info(f"Making POST request to: {self.base_url}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            logger.info(f"Request successful. Status code: {response.status_code}")
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response.text}")
            raise
