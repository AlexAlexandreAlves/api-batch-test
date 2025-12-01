import pytest

@pytest.mark.testdb
def test_users(db_connection):
    people = db_connection.execute_query_dict(
        "SELECT * FROM people WHERE id = %s",
        (1,)
    )
    assert len(people) > 0
    
    person = people[0]
    assert person["fname"] == "Alice"
    assert person["age"] == 30