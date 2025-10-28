"""API Agent with HTTP requests, retry logic, and error handling."""

import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base_agent import BaseAgent


class APIAgent(BaseAgent):
    """Agent that makes HTTP requests with retry logic and error handling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the API agent with configuration."""
        super().__init__(config)
        self.base_url = self.config.get("base_url", "")
        self.timeout = self.config.get("timeout", 30)
        self.max_retries = self.config.get("max_retries", 3)
        self.backoff_factor = self.config.get("backoff_factor", 0.3)
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update(
            {
                "User-Agent": "SmallAgents/0.1.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        return session

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request to the specified endpoint."""
        url = urljoin(self.base_url, endpoint) if self.base_url else endpoint

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "headers": dict(response.headers),
            }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "error_type": type(e).__name__}

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request to the specified endpoint."""
        url = urljoin(self.base_url, endpoint) if self.base_url else endpoint

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "headers": dict(response.headers),
            }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "error_type": type(e).__name__}

    def run(
        self, method: str = "GET", endpoint: str = "/", **kwargs: Any
    ) -> Dict[str, Any]:
        """Run the API agent with specified method and endpoint."""
        if not isinstance(method, str):
            raise TypeError("method must be a string")
        if not isinstance(endpoint, str):
            raise TypeError("endpoint must be a string")

        method = method.upper()

        start_time = time.time()

        if method == "GET":
            result = self.get(endpoint, kwargs.get("params"))
        elif method == "POST":
            result = self.post(endpoint, kwargs.get("data"))
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        result["execution_time"] = time.time() - start_time
        result["method"] = method
        result["endpoint"] = endpoint

        return result

    def close(self) -> None:
        """Close the HTTP session."""
        if self.session:
            self.session.close()
