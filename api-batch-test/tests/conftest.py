from src.api_client import base_url, http
from pathlib import Path
import pytest

# Re-exporting fixtures from src.api_client
__all__ = ["base_url", "http"]

# Diretório onde os cassetes serão salvos/carregados
@pytest.fixture(scope="session")
def vcr_cassette_dir():
    # Sempre "tests/cassettes" ao lado deste conftest, independente do cwd
    return str(Path(__file__).parent / "cassettes")

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": ["Authorization"],
        "filter_query_parameters": ["api_key", "token"],
        "filter_post_data_parameters": ["timestamp"],
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "decode_compressed_response": True,
    }
