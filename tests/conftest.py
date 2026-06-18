"""
Shared pytest configuration and fixtures for FastAPI backend tests.
Provides TestClient instance and fresh app state for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for making HTTP requests to the app.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the in-memory activities database before each test.
    Ensures test isolation by providing a fresh state for every test.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performance and stage acting",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["jessica@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for STEM competitions",
            "schedule": "Wednesdays, 4:00 PM - 5:45 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities dictionary before test
    activities.clear()
    for key, value in original_activities.items():
        activities[key] = {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()  # Deep copy of participants list
        }
    
    yield
    
    # Cleanup after test: reset to original state
    activities.clear()
    for key, value in original_activities.items():
        activities[key] = {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()
        }


@pytest.fixture
def sample_email():
    """
    Fixture providing a sample student email for testing.
    """
    return "test.student@mergington.edu"


@pytest.fixture
def activity_with_space():
    """
    Fixture providing an activity name with spaces to test URL encoding.
    """
    return "Programming Class"
