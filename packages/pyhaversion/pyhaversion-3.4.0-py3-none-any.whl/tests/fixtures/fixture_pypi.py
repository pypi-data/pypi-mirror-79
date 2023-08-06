"""Fixtures."""
import pytest


@pytest.fixture()
def pypi_response():
    """Response when no active beta."""
    return {
        "info": {"version": "9.99.9"},
        "releases": {
            "9.97.9b0": [],
            "9.97.9": [],
            "9.98.9b0": [],
            "9.98.9": [],
            "9.99.9b0": [],
        },
    }


@pytest.fixture()
def pypi_response_beta_week():
    """Response when active beta."""
    return {
        "info": {"version": "9.98.9"},
        "releases": {
            "9.97.9b0": [],
            "9.97.9": [],
            "9.98.9b0": [],
            "9.98.9": [],
            "9.99.9b0": [],
        },
    }
