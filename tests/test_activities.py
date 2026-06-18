"""
Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
Tests verify that activities data is correctly retrieved and formatted.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_200_status(self, client):
        """
        Test: GET /activities returns HTTP 200 status code
        
        Arrange: TestClient is ready (from fixture)
        Act: Make GET request to /activities endpoint
        Assert: Response status code is 200
        """
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_all_activities(self, client):
        """
        Test: GET /activities returns all 9 activities
        
        Arrange: Expected 9 activities from the in-memory database
        Act: Make GET request to /activities endpoint
        Assert: Response contains all 9 activities
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Robotics Club"
        ]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert len(activities_data) == expected_activity_count
        for activity_name in expected_activities:
            assert activity_name in activities_data

    def test_get_activities_response_has_required_fields(self, client):
        """
        Test: Each activity in response has required fields
        
        Arrange: Define required fields for each activity
        Act: Make GET request to /activities endpoint
        Assert: Each activity contains description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            for field in required_fields:
                assert field in activity_info, f"Field '{field}' missing from {activity_name}"

    def test_get_activities_participants_is_list(self, client):
        """
        Test: Each activity's participants field is a list
        
        Arrange: Expected participants field to be a list
        Act: Make GET request to /activities endpoint
        Assert: All participants fields are lists
        """
        # Arrange
        # (no specific setup needed)

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["participants"], list), \
                f"participants for {activity_name} is not a list"

    def test_get_activities_chess_club_has_participants(self, client):
        """
        Test: Chess Club has pre-populated participants
        
        Arrange: Chess Club should have 2 participants
        Act: Make GET request to /activities endpoint
        Assert: Chess Club contains michael@mergington.edu and daniel@mergington.edu
        """
        # Arrange
        activity_name = "Chess Club"
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data[activity_name]

        # Assert
        assert len(chess_club["participants"]) == 2
        for email in expected_participants:
            assert email in chess_club["participants"]

    def test_get_activities_programming_class_max_participants(self, client):
        """
        Test: Programming Class has correct max_participants capacity
        
        Arrange: Programming Class max_participants should be 20
        Act: Make GET request to /activities endpoint
        Assert: max_participants value is 20
        """
        # Arrange
        activity_name = "Programming Class"
        expected_max_participants = 20

        # Act
        response = client.get("/activities")
        activities_data = response.json()
        programming_class = activities_data[activity_name]

        # Assert
        assert programming_class["max_participants"] == expected_max_participants

    def test_get_activities_current_participants_count_is_correct(self, client):
        """
        Test: Verify current participant counts match pre-populated data
        
        Arrange: Define expected participant counts for select activities
        Act: Make GET request to /activities endpoint
        Assert: Verify participant counts match expectations
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Basketball Team": 1,
            "Tennis Club": 1,
            "Drama Club": 1,
            "Robotics Club": 1
        }

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, expected_count in expected_counts.items():
            actual_count = len(activities_data[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} has {actual_count} participants, expected {expected_count}"

    def test_get_activities_no_response_body_corruption(self, client):
        """
        Test: Response JSON is valid and complete
        
        Arrange: Make request to /activities endpoint
        Act: Parse response JSON
        Assert: JSON is valid and contains expected top-level keys
        """
        # Arrange
        # (no specific setup needed)

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert isinstance(activities_data, dict)
        assert len(activities_data) > 0
