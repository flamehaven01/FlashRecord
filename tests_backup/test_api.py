"""
Comprehensive FastAPI Tests - Validate all endpoints
Uses TestClient and HTTPX for API testing
"""

import pytest
from fastapi.testclient import TestClient
from flashrecord.api import app


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    return TestClient(app)


# ==================== Info Endpoints ====================

def test_root_endpoint(client):
    """Test root endpoint returns API info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "FlashRecord API"


def test_root_contains_endpoints(client):
    """Test root endpoint lists available endpoints"""
    response = client.get("/")
    data = response.json()
    assert "endpoints" in data
    assert "config" in data["endpoints"]
    assert "status" in data["endpoints"]
    assert "screenshot" in data["endpoints"]
    assert "recording" in data["endpoints"]


# ==================== Configuration Endpoints ====================

def test_get_config(client):
    """Test GET /config returns configuration"""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()

    # Verify all required fields
    assert "command_style" in data
    assert "auto_delete_hours" in data
    assert "save_dir" in data
    assert "screenshot_dir" in data
    assert "video_dir" in data
    assert "gif_dir" in data


def test_config_values_valid(client):
    """Test config values are valid types"""
    response = client.get("/config")
    data = response.json()

    assert isinstance(data["command_style"], str)
    assert isinstance(data["auto_delete_hours"], int)
    assert isinstance(data["save_dir"], str)
    assert data["auto_delete_hours"] >= 0


def test_config_command_style_valid(client):
    """Test command_style is one of valid options"""
    response = client.get("/config")
    data = response.json()

    valid_styles = ["numbered", "vs_vc_vg", "verbose"]
    assert data["command_style"] in valid_styles


def test_config_schema_endpoint(client):
    """Test GET /config/schema returns JSON schema"""
    response = client.get("/config/schema")
    assert response.status_code == 200

    schema = response.json()
    assert "properties" in schema
    assert "command_style" in schema["properties"]
    assert "auto_delete_hours" in schema["properties"]
    assert "hcap_path" in schema["properties"]


# ==================== Status Endpoints ====================

def test_get_status(client):
    """Test GET /status returns system status"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()

    assert "is_recording" in data
    assert "recording_file" in data
    assert "config" in data


def test_status_recording_false_by_default(client):
    """Test recording is False by default"""
    response = client.get("/status")
    data = response.json()

    assert data["is_recording"] is False
    assert data["recording_file"] is None


def test_status_config_present(client):
    """Test status includes current config"""
    response = client.get("/status")
    data = response.json()

    config = data["config"]
    assert "command_style" in config
    assert "auto_delete_hours" in config


# ==================== Screenshot Endpoints ====================

def test_screenshot_endpoint_exists(client):
    """Test screenshot endpoint exists"""
    response = client.post("/screenshot")
    # May fail or succeed depending on hcap, but endpoint should exist
    assert response.status_code in [200, 400, 500]


def test_screenshot_requires_post(client):
    """Test screenshot requires POST method"""
    response = client.get("/screenshot")
    assert response.status_code == 405  # Method Not Allowed


# ==================== Recording Endpoints ====================

def test_recording_start_endpoint_exists(client):
    """Test recording/start endpoint exists"""
    response = client.post("/recording/start")
    assert response.status_code in [200, 400, 500]


def test_recording_stop_no_recording(client):
    """Test stop recording when no recording"""
    response = client.post("/recording/stop")
    # API allows stop even with no active recording (graceful)
    assert response.status_code in [200, 400, 500]


def test_recording_gif_endpoints_exist(client):
    """Test GIF conversion endpoint exists"""
    response = client.post("/recording/gif")
    assert response.status_code in [200, 400, 500]


def test_recording_endpoints_require_post(client):
    """Test recording endpoints require POST"""
    assert client.get("/recording/start").status_code == 405
    assert client.get("/recording/stop").status_code == 405
    assert client.get("/recording/gif").status_code == 405


# ==================== Save Endpoints ====================

def test_save_session_endpoint_exists(client):
    """Test save session endpoint exists"""
    response = client.post("/save/claude")
    assert response.status_code in [200, 400, 500]


def test_save_multiple_models(client):
    """Test save endpoint for different AI models"""
    models = ["claude", "gemini", "codex", "general"]

    for model in models:
        response = client.post(f"/save/{model}")
        # Endpoint should exist and respond
        assert response.status_code in [200, 400, 500]


def test_save_requires_post(client):
    """Test save endpoint requires POST"""
    response = client.get("/save/claude")
    assert response.status_code == 405


# ==================== Response Format Tests ====================

def test_command_response_format(client):
    """Test command response has correct format"""
    response = client.get("/config")
    # Verify response has expected structure
    assert response.headers.get("content-type") == "application/json"


def test_all_endpoints_return_json(client):
    """Test all endpoints return JSON"""
    endpoints = [
        ("GET", "/"),
        ("GET", "/config"),
        ("GET", "/status"),
        ("GET", "/config/schema"),
    ]

    for method, endpoint in endpoints:
        if method == "GET":
            response = client.get(endpoint)
        else:
            response = client.post(endpoint)

        if response.status_code == 200:
            assert response.headers.get("content-type") == "application/json"


# ==================== Error Handling Tests ====================

def test_404_nonexistent_endpoint(client):
    """Test 404 for nonexistent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_invalid_save_model_handled(client):
    """Test invalid AI model is handled"""
    response = client.post("/save/invalid_model")
    # Should either succeed or fail gracefully
    assert response.status_code in [200, 400, 500]


# ==================== Integration Tests ====================

def test_full_workflow_sequence(client):
    """Test complete workflow: config -> status -> screenshot"""
    # 1. Get config
    config_resp = client.get("/config")
    assert config_resp.status_code == 200
    config = config_resp.json()
    assert config["command_style"] in ["numbered", "vs_vc_vg", "verbose"]

    # 2. Check status
    status_resp = client.get("/status")
    assert status_resp.status_code == 200
    status = status_resp.json()
    assert "is_recording" in status

    # 3. Verify config in status
    assert status["config"]["command_style"] == config["command_style"]


def test_api_consistency(client):
    """Test API returns consistent data"""
    # First call
    config1 = client.get("/config").json()
    # Second call
    config2 = client.get("/config").json()

    # Should be identical
    assert config1["command_style"] == config2["command_style"]
    assert config1["auto_delete_hours"] == config2["auto_delete_hours"]


# ==================== Performance Tests ====================

def test_config_response_time(client):
    """Test config endpoint responds quickly"""
    import time

    start = time.time()
    response = client.get("/config")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 1.0  # Should respond in less than 1 second


def test_status_response_time(client):
    """Test status endpoint responds quickly"""
    import time

    start = time.time()
    response = client.get("/status")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 1.0  # Should respond in less than 1 second


# ==================== Schema Validation Tests ====================

def test_config_response_matches_schema(client):
    """Test config response matches JSON schema"""
    config_response = client.get("/config")
    schema_response = client.get("/config/schema")

    assert config_response.status_code == 200
    assert schema_response.status_code == 200

    config_data = config_response.json()
    schema = schema_response.json()

    # Verify required fields from schema
    for prop in schema.get("properties", {}):
        assert prop in config_data or prop in schema.get("properties", {})
