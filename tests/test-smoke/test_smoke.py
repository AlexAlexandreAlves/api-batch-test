import pytest
from src.api_endpoints import Endpoints

@pytest.mark.vcr(record_mode="once")
@pytest.mark.smoke
def test_api_available(http, base_url):
    r = http.get(Endpoints.PEOPLE)
    assert r.status_code == 200
    assert r.headers.get("Content-Type", "").startswith("application/json")