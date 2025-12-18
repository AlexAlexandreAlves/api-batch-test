from jsonschema import validate
from src.schemas.page_schema import PAGE_SCHEMA
from src.schemas.people_schema import PEOPLE_ITEM_SCHEMA
import pytest
from src.api_endpoints import Endpoints

@pytest.mark.contract
@pytest.mark.skip(reason="The API has changed, and it does not return expected page data structure.")
def test_people_page_schema(http):
    r = http.get(Endpoints.PEOPLE)
    r.raise_for_status()
    data = r.json()
    validate(instance=data, schema=PAGE_SCHEMA)
    assert isinstance(data["results"], list)
    assert data["count"] == 82
    for item in data["results"]:
        validate(instance=item, schema=PEOPLE_ITEM_SCHEMA)
        
        

@pytest.mark.contract
def test_people_page_schema_by_id(http):
    r = http.get(Endpoints.PEOPLE + "1")
    r.raise_for_status()
    data = r.json()
    validate(instance=data, schema=PEOPLE_ITEM_SCHEMA)
    assert isinstance(data, object)