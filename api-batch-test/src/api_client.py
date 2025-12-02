import time
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import settings


class APIClient:
    """Cliente API com suporte a retry, rate-limit e formatação de URLs."""

    def __init__(self, base_url: str, connect_timeout: float, read_timeout: float, retry_total: int, rate_sleep: float):
        """
        Inicializa o cliente API.

        Args:
            base_url: URL base da API
            connect_timeout: Timeout de conexão em segundos
            read_timeout: Timeout de leitura em segundos
            retry_total: Total de tentativas para requisições
            rate_sleep: Tempo de espera entre requisições (rate-limit)
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
        """Constrói a URL completa formatando parametros de caminho."""
        if path_params:
            endpoint = endpoint.format(**path_params)
        # Se já é uma URL completa, retorna como está
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params=None, **kwargs) -> requests.Response:
        """
        Faz uma requisição GET.

        Args:
            endpoint: Endpoint da API (pode ter placeholders como {id})
            params: Parâmetros de query
            **kwargs: Parâmetros de caminho como id=123

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.get(url, params=params, timeout=self.timeout)

    def post(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        """
        Faz uma requisição POST.

        Args:
            endpoint: Endpoint da API
            data: Dados a enviar no body (será convertido para JSON)
            **kwargs: Parâmetros de caminho

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.post(url, json=data, timeout=self.timeout)

    def put(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        """
        Faz uma requisição PUT.

        Args:
            endpoint: Endpoint da API
            data: Dados a enviar no body (será convertido para JSON)
            **kwargs: Parâmetros de caminho

        Returns:
            Response object
        """
        url = self._build_url(endpoint, **kwargs)
        time.sleep(self.rate_sleep)
        return self.session.put(url, json=data, timeout=self.timeout)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Faz uma requisição DELETE.

        Args:
            endpoint: Endpoint da API
            **kwargs: Parâmetros de caminho

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
