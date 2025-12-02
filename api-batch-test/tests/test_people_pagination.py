from tests.helpers.pagination import iter_pages
from src.api_endpoints import Endpoints

from jsonschema import validate
from tests.schemas.page_schema import PAGE_SCHEMA
from tests.schemas.people_schema import PEOPLE_ITEM_SCHEMA

import pytest


@pytest.mark.heavy
@pytest.mark.pagination
def test_people_pagination_integrity(http):
    total_count = None
    seen_urls = set()
    total_items = 0
    page_index = 0

    for page in iter_pages(http, Endpoints.PEOPLE):
        # Validate the current page schema
        validate(instance=page, schema=PAGE_SCHEMA)
        if total_count is None:
            total_count = page["count"]
            # The first page should not have a previous page reference
            assert page["previous"] is None
        results = page.get("results", [])
        # The results must be a list
        assert isinstance(results, list)
        for item in results:
            # Validate the item/person schema
            validate(instance=item, schema=PEOPLE_ITEM_SCHEMA)
            uid = item.get("url")
            # Each item must have a valid URL starting with http/https
            assert uid and uid.startswith("http"), "Item sem URL válida"
            # Itens URLs must not repeat across pages
            assert uid not in seen_urls, f"Duplicado: {uid}"
            seen_urls.add(uid)
        total_items += len(results)
        page_index += 1
        if page.get("next"):
            r = http.get(page["next"])
            # Following the 'next' link must return 200 OK
            assert r.status_code == 200

    # The field 'count' must be a non-negative integer
    assert isinstance(total_count, int) and total_count >= 0
    # The total count must be exactly 82 people
    assert total_count == 82
    # The sum of collected items must equal the 'count' value
    assert total_items == total_count, f"soma({total_items}) != count({total_count})"
    # Must have seen at least one item if count > 0
    assert page_index >= 1
    # On the last page of pagination, 'next' must be null
    assert page.get("next") is None
