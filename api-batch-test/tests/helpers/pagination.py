from typing import Dict, Generator
from tests.conftest import HttpClient

def iter_pages(http: HttpClient, first_path: str) -> Generator[Dict, None, None]:
    # Iterate through pages starting from first_path
    resp = http.get(first_path)
    resp.raise_for_status()
    data = resp.json()
    yield data
    next_url = data.get("next")
    while next_url:
        resp = http.get(next_url)
        resp.raise_for_status()
        data = resp.json()
        yield data
        next_url = data.get("next")