import time
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import settings


class HttpClient:
    """Cliente HTTP focado em testes: timeout, retry e rate-limit simples."""

    def __init__(self, base_url: str, connect_timeout: float, read_timeout: float, retry_total: int, rate_sleep: float):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        retry = Retry(
            total=retry_total,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(
            max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = (connect_timeout, read_timeout)
        self.rate_sleep = rate_sleep

    def get(self, path_or_url: str, **kwargs) -> requests.Response:
        """GET com base_url opcional e respeito a rate-limit."""
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            url = path_or_url
        else:
            url = f"{self.base_url}/{path_or_url.lstrip('/')}"
        time.sleep(self.rate_sleep)  # rate-limit simples
        return self.session.get(url, timeout=self.timeout, **kwargs)


@pytest.fixture(scope="session")
def base_url() -> str:
    return settings.BASE_URL


@pytest.fixture(scope="session")
def http() -> HttpClient:
    return HttpClient(
        base_url=settings.BASE_URL,
        connect_timeout=settings.CONNECT_TIMEOUT,
        read_timeout=settings.READ_TIMEOUT,
        retry_total=settings.RETRY_TOTAL,
        rate_sleep=settings.RATE_LIMIT_SLEEP,
    )

