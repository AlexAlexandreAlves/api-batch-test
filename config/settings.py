import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://swapi.info/api/")
CONNECT_TIMEOUT = float(os.getenv("CONNECT_TIMEOUT", "3.0"))
READ_TIMEOUT = float(os.getenv("READ_TIMEOUT", "5.0"))
RETRY_TOTAL = int(os.getenv("RETRY_TOTAL", "3"))
RATE_LIMIT_SLEEP = float(os.getenv("RATE_LIMIT_SLEEP", "0.0"))  # seconds between requests