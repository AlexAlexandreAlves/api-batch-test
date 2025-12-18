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
        data = r.json()
        if isinstance(data, dict):
            assert isinstance(data.get("results"), list)
        elif isinstance(data, list):
            # Se for lista, apenas valida que é lista (caso raro)
            assert isinstance(data, list)
