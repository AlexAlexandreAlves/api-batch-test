from typing import Final


class Endpoints:
    """Centralized API endpoint paths for SWAPI resources."""

    # Collection endpoints (paginated)
    PEOPLE: Final[str] = "/people/"
    FILMS: Final[str] = "/films/"
    STARSHIPS: Final[str] = "/starships/"
    VEHICLES: Final[str] = "/vehicles/"
    SPECIES: Final[str] = "/species/"
    PLANETS: Final[str] = "/planets/"

    # Individual resource endpoints (with ID placeholder)
    PEOPLE_ID: Final[str] = "/people/{id}/"
    FILMS_ID: Final[str] = "/films/{id}/"
    STARSHIPS_ID: Final[str] = "/starships/{id}/"
    VEHICLES_ID: Final[str] = "/vehicles/{id}/"
    SPECIES_ID: Final[str] = "/species/{id}/"
    PLANETS_ID: Final[str] = "/planets/{id}/"

    # Schema endpoints (optional, for future use)
    PEOPLE_SCHEMA: Final[str] = "/people/schema/"
    FILMS_SCHEMA: Final[str] = "/films/schema/"
    STARSHIPS_SCHEMA: Final[str] = "/starships/schema/"
    VEHICLES_SCHEMA: Final[str] = "/vehicles/schema/"
    SPECIES_SCHEMA: Final[str] = "/species/schema/"
    PLANETS_SCHEMA: Final[str] = "/planets/schema/"