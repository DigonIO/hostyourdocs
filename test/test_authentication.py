from starlette.testclient import TestClient

CREDENTIALS = {"grant_type": "password", "username": "admin", "password": "1234"}

####################################################################################################
#### Test Authentication, Login, Logout, etc.
####################################################################################################


def test_db_connection(client: TestClient):
    assert True


def test_authentication(client: TestClient):
    headers = authenticate(client)

    response = client.get("/api/v1/user/greet", headers=headers)
    assert response.status_code == 200
    assert response.text == "Hello admin :)"


####################################################################################################
#### Util
####################################################################################################


def authenticate(client: TestClient) -> dict[str, str]:
    response = client.post("/api/v1/user/login", data=CREDENTIALS)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["token_type"] == "bearer"

    access_token = response_data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
