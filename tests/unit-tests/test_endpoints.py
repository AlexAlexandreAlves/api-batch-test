"""Tests for API endpoint constants."""
import pytest
from src.api_endpoints import Endpoints


class TestEndpointConstants:
    """Test suite for Endpoints class constants."""

    def test_endpoint_is_string(self):
        """All endpoint constants should be strings."""
        assert isinstance(Endpoints.PEOPLE, str)
        assert isinstance(Endpoints.PEOPLE_ID, str)

    def test_endpoint_starts_with_slash(self):
        """All endpoint paths should start with /."""
        assert Endpoints.PEOPLE.startswith("/")
        assert Endpoints.PEOPLE_ID.startswith("/")

    def test_endpoint_ends_with_slash(self):
        """All collection endpoint paths should end with /."""
        assert Endpoints.PEOPLE.endswith("/")

    def test_new_collection_endpoints_exist(self):
        """New collection endpoints for all resources should exist."""
        # Test that new collection endpoints are defined
        assert hasattr(Endpoints, "FILMS")
        assert hasattr(Endpoints, "STARSHIPS")
        assert hasattr(Endpoints, "VEHICLES")
        assert hasattr(Endpoints, "SPECIES")
        assert hasattr(Endpoints, "PLANETS")

    def test_new_collection_endpoints_format(self):
        """New collection endpoints should follow format conventions."""
        endpoints = [
            Endpoints.FILMS,
            Endpoints.STARSHIPS,
            Endpoints.VEHICLES,
            Endpoints.SPECIES,
            Endpoints.PLANETS,
        ]

        for endpoint in endpoints:
            assert isinstance(endpoint, str), f"{endpoint} should be string"
            assert endpoint.startswith("/"), f"{endpoint} should start with /"
            assert endpoint.endswith("/"), f"{endpoint} should end with /"

    def test_new_individual_endpoints_exist(self):
        """New individual resource endpoints should exist."""
        assert hasattr(Endpoints, "FILMS_ID")
        assert hasattr(Endpoints, "STARSHIPS_ID")
        assert hasattr(Endpoints, "VEHICLES_ID")
        assert hasattr(Endpoints, "SPECIES_ID")
        assert hasattr(Endpoints, "PLANETS_ID")

    def test_new_individual_endpoints_format(self):
        """New individual endpoints should have ID placeholder."""
        id_endpoints = [
            Endpoints.FILMS_ID,
            Endpoints.STARSHIPS_ID,
            Endpoints.VEHICLES_ID,
            Endpoints.SPECIES_ID,
            Endpoints.PLANETS_ID,
        ]

        for endpoint in id_endpoints:
            assert isinstance(endpoint, str), f"{endpoint} should be string"
            assert endpoint.startswith("/"), f"{endpoint} should start with /"
            assert endpoint.endswith("/"), f"{endpoint} should end with /"
            assert "{id}" in endpoint, f"{endpoint} should contain {{id}} placeholder"

    def test_schema_endpoints_exist(self):
        """Schema endpoints for all resources should exist."""
        assert hasattr(Endpoints, "PEOPLE_SCHEMA")
        assert hasattr(Endpoints, "FILMS_SCHEMA")
        assert hasattr(Endpoints, "STARSHIPS_SCHEMA")
        assert hasattr(Endpoints, "VEHICLES_SCHEMA")
        assert hasattr(Endpoints, "SPECIES_SCHEMA")
        assert hasattr(Endpoints, "PLANETS_SCHEMA")

    def test_schema_endpoints_format(self):
        """Schema endpoints should follow format conventions."""
        schema_endpoints = [
            Endpoints.PEOPLE_SCHEMA,
            Endpoints.FILMS_SCHEMA,
            Endpoints.STARSHIPS_SCHEMA,
            Endpoints.VEHICLES_SCHEMA,
            Endpoints.SPECIES_SCHEMA,
            Endpoints.PLANETS_SCHEMA,
        ]

        for endpoint in schema_endpoints:
            assert isinstance(endpoint, str), f"{endpoint} should be string"
            assert endpoint.startswith("/"), f"{endpoint} should start with /"
            assert endpoint.endswith("/"), f"{endpoint} should end with /"
            assert "/schema/" in endpoint, f"{endpoint} should contain /schema/"
