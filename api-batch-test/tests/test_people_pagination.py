from tests.helpers.pagination import iter_pages
import pytest

@pytest.mark.pagination
def test_people_pagination_integrity(http):
    total_count = None
    seen_urls = set()
    total_items = 0
    page_index = 0

    for page in iter_pages(http, "/people/"):
        if total_count is None:
            total_count = page["count"]
            assert page["previous"] is None
        results = page.get("results", [])
        assert isinstance(results, list)
        for item in results:
            uid = item.get("url")
            assert uid and uid.startswith("http"), "Item sem URL válida"
            assert uid not in seen_urls, f"Duplicado: {uid}"
            seen_urls.add(uid)
        total_items += len(results)
        page_index += 1
        if page.get("next"):
            r = http.get(page["next"])
            assert r.status_code == 200

    assert isinstance(total_count, int) and total_count >= 0
    assert total_items == total_count, f"soma({total_items}) != count({total_count})"
    assert page_index >= 1