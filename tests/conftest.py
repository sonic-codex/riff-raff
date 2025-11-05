"""Pytest configuration and shared fixtures"""
import json
from pathlib import Path

import pytest


@pytest.fixture
def sample_persona_data():
    """Provide sample persona data for testing."""
    return {
        "vocab": ["ice", "drip", "flex", "swag"],
        "styles": ["glow", "drip", "hiss", "teleport"]
    }


@pytest.fixture
def sample_lyrics():
    """Provide sample lyrics data for testing."""
    return [
        {
            "text": "My ice glows in the matrix",
            "persona": "Neon Alien",
            "theme": "Sci-Fi",
            "mode": "4-Bar Verse",
            "flex_level": 7,
            "nonsense": 5,
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "text": "Came through drippin'... Michelle Obama",
            "persona": "Beach Riff",
            "theme": "Fashion",
            "mode": "Hook Generator",
            "flex_level": 8,
            "nonsense": 6,
            "timestamp": "2024-01-01T00:05:00"
        }
    ]
