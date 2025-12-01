import pytest


@pytest.mark.negative
@pytest.mark.parametrize("path", ["/people/99999/", "/people/?page=999"])
def test_not_found_or_bounds(http, path):
    r = http.get(path)
    assert r.status_code in (404, 200)
    # Se 200 para page=999 na API pública, valide que results pode estar vazio:
    if r.status_code == 200:
        assert isinstance(r.json().get("results"), list)