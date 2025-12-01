import pytest

@pytest.mark.smoke
def test_api_available(http, base_url):
    r = http.get("/people/")
    assert r.status_code == 200
    assert r.headers.get("Content-Type", "").startswith("application/json")