"""Sample API tests demonstrating REST API testing patterns."""
import pytest
import json
import time


class TestAuthAPI:
    """Authentication API test suite."""

    @pytest.fixture
    def api_client(self):
        from src.api.clients.api_client import APIClient
        return APIClient(base_url="https://reqres.in/api")

    @pytest.fixture
    def auth_token(self, api_client):
        """Get authentication token for protected endpoints."""
        response = api_client.post("/login", json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        })
        if response.status_code == 200:
            return response.json().get("token")
        return None

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_list_of_users(self, api_client):
        """Test GET request to fetch users list."""
        response = api_client.get("/users", params={"page": 1})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "data" in data, "Response should contain 'data' key"
        assert len(data["data"]) > 0, "Should return at least one user"

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_single_user(self, api_client):
        """Test GET request to fetch single user."""
        response = api_client.get("/users/2")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == 2
        assert "email" in data["data"]

    @pytest.mark.api
    def test_get_nonexistent_user(self, api_client):
        """Test GET request for non-existent user returns 404."""
        response = api_client.get("/users/999")
        assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.smoke
    def test_successful_login(self, api_client):
        """Test successful login API call."""
        response = api_client.post("/login", json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data or "id" in data

    @pytest.mark.api
    def test_failed_login(self, api_client):
        """Test failed login with invalid credentials."""
        response = api_client.post("/login", json={
            "email": "test@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 400

    @pytest.mark.api
    def test_create_user(self, api_client):
        """Test POST request to create new user."""
        timestamp = int(time.time())
        response = api_client.post("/users", json={
            "name": f"TestUser{timestamp}",
            "job": "QA Engineer"
        })
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == f"TestUser{timestamp}"
        assert data["job"] == "QA Engineer"

    @pytest.mark.api
    def test_update_user(self, api_client):
        """Test PUT request to update user."""
        response = api_client.put("/users/2", json={
            "name": "Updated Name",
            "job": "Senior QA"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    @pytest.mark.api
    def test_delete_user(self, api_client):
        """Test DELETE request to remove user."""
        response = api_client.delete("/users/2")
        assert response.status_code == 204 or response.status_code == 200


@pytest.mark.api
@pytest.mark.smoke
class TestUsersAPI:
    """Users API test suite."""

    @pytest.fixture
    def api_client(self):
        from src.api.clients.api_client import APIClient
        return APIClient(base_url="https://reqres.in/api")

    def test_list_users_pagination(self, api_client):
        """Test users list with pagination."""
        response = api_client.get("/users", params={"page": 2, "per_page": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert len(data["data"]) <= 3

    def test_delay_response(self, api_client):
        """Test API response with delay."""
        start = time.time()
        response = api_client.get("/users", params={"delay": 1})
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed >= 1, "Should wait for delayed response"


@pytest.mark.api
class TestResourcesAPI:
    """Resources API test suite."""

    @pytest.fixture
    def api_client(self):
        from src.api.clients.api_client import APIClient
        return APIClient(base_url="https://reqres.in/api")

    @pytest.mark.api
    def test_get_list_resources(self, api_client):
        """Test GET request to fetch resources."""
        response = api_client.get("/unknown")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    @pytest.mark.api
    def test_get_single_resource(self, api_client):
        """Test GET request for single resource."""
        response = api_client.get("/unknown/2")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == 2
        assert "name" in data["data"]
        assert "color" in data["data"]
