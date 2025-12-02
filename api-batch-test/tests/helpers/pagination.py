from typing import Dict, Generator
from src.api_client import APIClient


def iter_pages(http: APIClient, first_path: str) -> Generator[Dict, None, None]:
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