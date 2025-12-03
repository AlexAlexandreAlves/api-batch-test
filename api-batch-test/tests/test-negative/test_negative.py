import pytest

# Util para gravar os cassetes VCR, mas em CI continua usando o -record-mode=none para replay.
@pytest.mark.vcr(record_mode="once")
@pytest.mark.negative
@pytest.mark.parametrize(
    "path",
    [
        pytest.param("/people/99999/", id="people-99999"),
        pytest.param("/people/?page=999", id="page-999"),
    ],
)
def test_not_found_or_bounds(http, path):
    r = http.get(path)
    assert r.status_code in (404, 200)
    # Se 200 para page=999 na API pública, valide que results pode estar vazio:
    if r.status_code == 200:
        assert isinstance(r.json().get("results"), list)
