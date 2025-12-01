import pytest
from src.api_client import APIClient
from src.database import DatabaseConnection
    
@pytest.fixture(scope="module")
def api_client():
    client = APIClient(base_url="https://fakerestapi.azurewebsites.net/")
    yield client


@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture to create a conection with PostreSQL DB.
    
    Set up the env variables or parameters as needed:
    - DB_HOST: localhost
    - DB_DATABASE: seu_banco
    - DB_USER: seu_usuario
    - DB_PASSWORD: sua_senha
    - DB_PORT: 5432
    """
    db = DatabaseConnection(
        host="localhost",
        database="testdb",
        user="user",
        password="1234",
        port=5432
    )
    yield db
    db.close()