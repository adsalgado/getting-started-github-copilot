"""
Tests for POST /activities/{activity_name}/signup and POST /activities/{activity_name}/unregister
endpoints using AAA (Arrange-Act-Assert) pattern.
Tests verify signup/unregister functionality, error handling, and state management.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_returns_200_on_success(self, client, sample_email):
        """
        Test: POST /signup returns HTTP 200 on successful signup
        
        Arrange: Set up activity name and new student email
        Act: Make POST request to signup endpoint
        Assert: Response status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = sample_email
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_signup_adds_student_to_participants(self, client, sample_email):
        """
        Test: Student is added to activity participants list after signup
        
        Arrange: Identify an activity and new student email
        Act: Signup student for activity, then get activities list
        Assert: Student email is in participants list for that activity
        """
        # Arrange
        activity_name = "Tennis Club"
        student_email = sample_email

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert student_email in activities_data[activity_name]["participants"]

    def test_signup_returns_success_message(self, client, sample_email):
        """
        Test: POST /signup returns confirmation message
        
        Arrange: Set up activity and student details
        Act: Make POST request to signup endpoint
        Assert: Response contains success message with student email and activity name
        """
        # Arrange
        activity_name = "Art Studio"
        student_email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        response_data = response.json()

        # Assert
        assert "message" in response_data
        assert student_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_signup_duplicate_signup_returns_400(self, client):
        """
        Test: Duplicate signup returns HTTP 400 (Bad Request)
        
        Arrange: Get an activity with pre-existing student
        Act: Try to signup same student again
        Assert: Response status code is 400
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Already signed up
        expected_status = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_signup_duplicate_signup_returns_error_message(self, client):
        """
        Test: Duplicate signup returns appropriate error message
        
        Arrange: Get an activity with pre-existing student
        Act: Try to signup same student again
        Assert: Response contains error detail about duplicate signup
        """
        # Arrange
        activity_name = "Programming Class"
        student_email = "emma@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        response_data = response.json()

        # Assert
        assert "detail" in response_data
        assert "already signed up" in response_data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, sample_email):
        """
        Test: Signup for non-existent activity returns HTTP 404
        
        Arrange: Use non-existent activity name
        Act: Make POST request to signup endpoint with fake activity
        Assert: Response status code is 404
        """
        # Arrange
        activity_name = "Fake Activity That Does Not Exist"
        student_email = sample_email
        expected_status = 404

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_signup_nonexistent_activity_returns_not_found_message(self, client, sample_email):
        """
        Test: Signup for non-existent activity returns "not found" error
        
        Arrange: Use non-existent activity name
        Act: Make POST request to signup endpoint
        Assert: Response contains "not found" error message
        """
        # Arrange
        activity_name = "Mystery Club"
        student_email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        response_data = response.json()

        # Assert
        assert "detail" in response_data
        assert "not found" in response_data["detail"].lower()

    def test_signup_missing_email_parameter_returns_error(self, client):
        """
        Test: Signup request without email parameter returns error
        
        Arrange: Prepare activity name but omit email query parameter
        Act: Make POST request without email parameter
        Assert: Response indicates missing/invalid parameter (422 or 400)
        """
        # Arrange
        activity_name = "Debate Team"
        expected_statuses = [422, 400]  # FastAPI returns 422 for missing query params

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code in expected_statuses

    def test_signup_activity_with_spaces_in_name(self, client, sample_email, activity_with_space):
        """
        Test: Signup works for activity names with spaces
        
        Arrange: Use activity name with spaces (Programming Class)
        Act: Make POST request to signup endpoint
        Assert: Response is 200 and student is added to correct activity
        """
        # Arrange
        activity_name = activity_with_space
        student_email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        # Verify student was added to Programming Class, not somewhere else
        activities_response = client.get("/activities")
        assert student_email in activities_response.json()[activity_name]["participants"]

    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Test: Multiple different students can signup for same activity
        
        Arrange: Prepare two different student emails and one activity
        Act: Signup first student, then signup second student
        Assert: Both students appear in participants list
        """
        # Arrange
        activity_name = "Robotics Club"
        student1_email = "newstudent1@mergington.edu"
        student2_email = "newstudent2@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1_email}
        )
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2_email}
        )
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]

        # Assert
        assert student1_email in participants
        assert student2_email in participants


class TestUnregisterFromActivity:
    """Test suite for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_returns_200_on_success(self, client):
        """
        Test: POST /unregister returns HTTP 200 on successful unregister
        
        Arrange: Use student already signed up for an activity
        Act: Make POST request to unregister endpoint
        Assert: Response status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Pre-registered
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_unregister_removes_student_from_participants(self, client):
        """
        Test: Student is removed from participants list after unregister
        
        Arrange: Identify student already in activity
        Act: Unregister student, then get activities list
        Assert: Student email is no longer in participants list
        """
        # Arrange
        activity_name = "Basketball Team"
        student_email = "alex@mergington.edu"  # Pre-registered

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert student_email not in activities_data[activity_name]["participants"]

    def test_unregister_returns_success_message(self, client):
        """
        Test: POST /unregister returns confirmation message
        
        Arrange: Set up registered student details
        Act: Make POST request to unregister endpoint
        Assert: Response contains success message with student email and activity name
        """
        # Arrange
        activity_name = "Drama Club"
        student_email = "jessica@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        response_data = response.json()

        # Assert
        assert "message" in response_data
        assert student_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_unregister_not_registered_returns_400(self, client, sample_email):
        """
        Test: Unregister for non-registered student returns HTTP 400
        
        Arrange: Use student NOT signed up for an activity
        Act: Try to unregister student
        Assert: Response status code is 400
        """
        # Arrange
        activity_name = "Tennis Club"
        student_email = sample_email  # Not registered
        expected_status = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_unregister_not_registered_returns_error_message(self, client):
        """
        Test: Unregister for non-registered student returns appropriate error
        
        Arrange: Use student NOT signed up for an activity
        Act: Try to unregister student
        Assert: Response contains error about student not being signed up
        """
        # Arrange
        activity_name = "Art Studio"
        student_email = "notregistered@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        response_data = response.json()

        # Assert
        assert "detail" in response_data
        assert "not signed up" in response_data["detail"].lower()

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test: Unregister from non-existent activity returns HTTP 404
        
        Arrange: Use non-existent activity name
        Act: Make POST request to unregister endpoint with fake activity
        Assert: Response status code is 404
        """
        # Arrange
        activity_name = "Fake Activity That Does Not Exist"
        student_email = "someone@mergington.edu"
        expected_status = 404

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status

    def test_unregister_missing_email_parameter_returns_error(self, client):
        """
        Test: Unregister request without email parameter returns error
        
        Arrange: Prepare activity name but omit email query parameter
        Act: Make POST request without email parameter
        Assert: Response indicates missing/invalid parameter (422 or 400)
        """
        # Arrange
        activity_name = "Debate Team"
        expected_statuses = [422, 400]

        # Act
        response = client.post(f"/activities/{activity_name}/unregister")

        # Assert
        assert response.status_code in expected_statuses


class TestSignupUnregisterIntegration:
    """Integration tests for signup and unregister workflows"""

    def test_signup_then_unregister_workflow(self, client, sample_email):
        """
        Test: Student can signup, unregister, and signup again (state consistency)
        
        Arrange: Prepare student email and activity
        Act: Signup student, unregister, then signup again
        Assert: Student present after first signup, absent after unregister, present again after re-signup
        """
        # Arrange
        activity_name = "Gym Class"
        student_email = sample_email

        # Act & Assert - First signup
        signup_response_1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        assert signup_response_1.status_code == 200
        activities_1 = client.get("/activities").json()
        assert student_email in activities_1[activity_name]["participants"]

        # Act & Assert - Unregister
        unregister_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        assert unregister_response.status_code == 200
        activities_2 = client.get("/activities").json()
        assert student_email not in activities_2[activity_name]["participants"]

        # Act & Assert - Re-signup
        signup_response_2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        assert signup_response_2.status_code == 200
        activities_3 = client.get("/activities").json()
        assert student_email in activities_3[activity_name]["participants"]

    def test_signup_then_signup_different_activity(self, client, sample_email):
        """
        Test: Student can signup for multiple different activities
        
        Arrange: Prepare student email and two activities
        Act: Signup for first activity, then signup for second activity
        Assert: Student appears in participants for both activities
        """
        # Arrange
        student_email = sample_email
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act
        client.post(
            f"/activities/{activity1}/signup",
            params={"email": student_email}
        )
        client.post(
            f"/activities/{activity2}/signup",
            params={"email": student_email}
        )
        activities = client.get("/activities").json()

        # Assert
        assert student_email in activities[activity1]["participants"]
        assert student_email in activities[activity2]["participants"]

    def test_unregister_then_different_student_signup(self, client, sample_email):
        """
        Test: After one student unregisters, another student can signup
        
        Arrange: One student unregisters, prepare different student email
        Act: First student unregisters, second student signs up for same activity
        Assert: First student absent, second student present
        """
        # Arrange
        activity_name = "Debate Team"
        student1_email = "noah@mergington.edu"  # Pre-registered
        student2_email = sample_email

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": student1_email}
        )
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2_email}
        )
        activities = client.get("/activities").json()
        participants = activities[activity_name]["participants"]

        # Assert
        assert student1_email not in participants
        assert student2_email in participants
