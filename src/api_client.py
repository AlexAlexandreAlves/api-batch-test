import time
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import settings


class APIClient:
    """API client with retry, rate-limit, and URL formatting support."""

    def __init__(self, base_url: str, connect_timeout: float, read_timeout: float, retry_total: int, rate_sleep: float):
        """
        Initialize the API client.

        Args:
            base_url: API Base URL
            connect_timeout: Connection timeout in seconds
            read_timeout: Read timeout in seconds
            retry_total: Retry total attempts
            rate_sleep: Wait time between requests to handle rate limiting
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        retry = Retry(
            total=retry_total,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(
            max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = (connect_timeout, read_timeout)
        self.rate_sleep = rate_sleep

    def _build_url(self, endpoint: str, **path_params) -> str:
        """Build full URL with path parameters."""
        if path_params:
            endpoint = endpoint.format(**path_params)
        # If endpoint is a full URL, return it as is
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params=None, **kwargs) -> requests.Response:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint (can have placeholders like {id})
            params: Query parameters
            **kwargs: Path parameters such as id=123

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.get(url, params=params, timeout=self.timeout)

    def post(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            data: Data to send in the body (will be converted to JSON)
            **kwargs: Path parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.post(url, json=data, timeout=self.timeout)

    def put(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            data: Data to send in the body (will be converted to JSON)
            **kwargs: Path parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.put(url, json=data, timeout=self.timeout)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            **kwargs: Path parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.delete(url, timeout=self.timeout)


@pytest.fixture(scope="session")
def base_url() -> str:
    return settings.BASE_URL


@pytest.fixture(scope="session")
def http() -> APIClient:
    return APIClient(
        base_url=settings.BASE_URL,
        connect_timeout=settings.CONNECT_TIMEOUT,
        read_timeout=settings.READ_TIMEOUT,
        retry_total=settings.RETRY_TOTAL,
        rate_sleep=settings.RATE_LIMIT_SLEEP,
    )
