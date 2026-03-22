import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from src.backend.api.main import app
import json

client = TestClient(app)

def test_full_auth_flow():
    # 1. Register a user
    register_data = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "candidate"
    }
    
    print("\n[1] Testing Registration...")
    # Clean up potentially existing test user if test script is re-run
    # (Though in a real test we'd use a test DB)
    response = client.post("/api/auth/register", json=register_data)
    
    if response.status_code == 409:
        print("User already exists, proceeding to login test.")
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == register_data["email"]
        assert "password" not in data
        print("Registration successful!")

    # 2. Test Login
    print("\n[2] Testing Login...")
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    print("Login successful! Token received.")

    # 3. Test Protected Route (/me)
    print("\n[3] Testing Protected Content (/me)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == register_data["email"]
    print(f"Me data retrieved: {me_data['first_name']} {me_data['last_name']}")

    # 4. Test Invalid credentials
    print("\n[4] Testing Invalid Credentials...")
    bad_login = {"username": "test@example.com", "password": "wrongpassword"}
    response = client.post("/api/auth/login", data=bad_login)
    assert response.status_code == 401
    print("Invalid credentials correctly rejected.")

if __name__ == "__main__":
    try:
        test_full_auth_flow()
        print("\n✅ All Auth API tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
