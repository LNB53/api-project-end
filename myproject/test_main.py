import json
import requests


# Test if the get_players functions blocks out unauthenticated requests
def test_get_players_without_authentication():
    response = requests.get("http://127.0.0.1:8000/players")
    response_dict = json.loads(response.text)
    assert response_dict["detail"] == "Not authenticated"


# Test if the create_player endpoint works properly
def test_create_player():
    headers = {"Content-Type": "application/json"}
    payload_1 = {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "password": "abc123!"}

    payload_2 = {
        "username": "test",
        "email": "test@test.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "password": "abc123!"}

    payload_3 = {
        "username": "test2",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "password": "abc123!"}

    response_1 = requests.post("http://127.0.0.1:8000/players", json=payload_1, headers=headers)
    assert response_1.status_code == 200
    assert json.loads(response_1.text) == {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}

    response_2 = requests.post("http://127.0.0.1:8000/players", json=payload_2, headers=headers)
    assert response_2.status_code == 400
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Username already registered"

    response_3 = requests.post("http://127.0.0.1:8000/players", json=payload_3, headers=headers)
    assert response_3.status_code == 400
    response_dict_3 = json.loads(response_3.text)
    assert response_dict_3["detail"] == "Email already registered"


# Test the OAuth-token functionality
def test_token():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_data = {
        "client_id": "",
        "client_secret": "",
        "scope": "",
        "grant_type": "",
        "refresh_token": "",
        "username": "test",
        "password": "abc123!"
    }

    token_request = requests.post("http://localhost:8000/token", data=request_data, headers=headers)
    # print(token_request.text) -> test purposes
    token = json.loads(token_request.text)["access_token"]

    headers_with_token = {
        "accept": "application/json",
        "Authorization": f'Bearer {token}'
    }
    get_request = requests.get("http://localhost:8000/users/me", headers=headers_with_token)
    # print(get_request.text) -> test purposes
