import json
import requests


# Test create_player functions - END: POST /players
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

    # Non-existing player
    response_1 = requests.post("http://127.0.0.1:8000/players", json=payload_1, headers=headers)
    assert response_1.status_code == 200
    assert json.loads(response_1.text) == {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}

    # Already registered username
    response_2 = requests.post("http://127.0.0.1:8000/players", json=payload_2, headers=headers)
    assert response_2.status_code == 400
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Username already registered"

    # Already registered email
    response_3 = requests.post("http://127.0.0.1:8000/players", json=payload_3, headers=headers)
    assert response_3.status_code == 400
    response_dict_3 = json.loads(response_3.text)
    assert response_dict_3["detail"] == "Email already registered"


# Test the OAuth-token functionality - END: GET /token
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
    token = json.loads(token_request.text)["access_token"]

    headers_with_token = {
        "accept": "application/json",
        "Authorization": f'Bearer {token}'
    }

    return headers_with_token


# Test get_players function - END: GET /players
def test_get_players():
    # Unauthenticated
    response_1 = requests.get("http://127.0.0.1:8000/players")
    response_dict_1 = json.loads(response_1.text)
    assert response_dict_1["detail"] == "Not authenticated"

    # Authenticated
    response_2 = requests.get("http://127.0.0.1:8000/players", headers=test_token())
    assert response_2.status_code == 200
    assert json.loads(response_2.text) == [{
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}]


# Test if the get_player_by_username function works correctly - END: GET /players/{username}
def test_get_player_by_username():
    # Unauthenticated
    response = requests.get("http://127.0.0.1:8000/players/test")
    assert response.status_code == 401
    response_dict = json.loads(response.text)
    assert response_dict["detail"] == "Not authenticated"

    # Authenticated, existing player
    response_1 = requests.get("http://127.0.0.1:8000/players/test", headers=test_token())
    # assert response_1.status_code == 200
    assert json.loads(response_1.text) == {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}

    # Authenticated, non-existing player
    response_2 = requests.get("http://127.0.0.1:8000/players/test_2", headers=test_token())
    assert response_2.status_code == 404
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Username not found"


# Test create_player functions - END: POST /players
def test_create_games():
    headers = {"Content-Type": "application/json"}

    payload_1 = {
        "title": "game_1",
        "release_date": "2023-12-19",
        "genre": "FPS",
        "developer": "Ubisoft"
    }

    payload_2 = {
        "title": "game_1",
        "release_date": "2022-09-08",
        "genre": "FPS",
        "developer": "Ubisoft"
    }

    # Non-existing game
    response_1a = requests.post("http://127.0.0.1:8000/games", json=payload_1, headers=headers)
    assert response_1a.status_code == 200
    assert json.loads(response_1a.text) == {
        "title": "game_1",
        "release_date": "2023-12-19",
        "genre": "FPS",
        "developer": "Ubisoft",
        "game_id": 1,
        "progress": []
    }

    # Existing game title with same release date
    response_1b = requests.post("http://127.0.0.1:8000/games", json=payload_1, headers=headers)
    assert response_1b.status_code == 400
    response_dict_1 = json.loads(response_1b.text)
    assert response_dict_1["detail"] == "Game already registered"

    # Existing game title with different release date
    response_2 = requests.post("http://127.0.0.1:8000/games", json=payload_2, headers=headers)
    assert response_2.status_code == 200


# Test get_games functions - END: GET /games
def test_get_games():
    # Unauthenticated
    response_1 = requests.get("http://127.0.0.1:8000/games")
    assert response_1.status_code == 401
    response_dict_1 = json.loads(response_1.text)
    assert response_dict_1["detail"] == "Not authenticated"

    # Authenticated
    response_2 = requests.get("http://127.0.0.1:8000/games", headers=test_token())
    assert response_2.status_code == 200
    assert json.loads(response_2.text) == [
        {
            "title": "game_1",
            "release_date": "2023-12-19",
            "genre": "FPS",
            "developer": "Ubisoft",
            "game_id": 1,
            "progress": []
        }, {
            "title": "game_1",
            "release_date": "2022-09-08",
            "genre": "FPS",
            "developer": "Ubisoft",
            "game_id": 2,
            "progress": []
        }
    ]


# Test delete_all function - END: DELETE /reset
def test_reset():
    response = requests.delete("http://127.0.0.1:8000/reset")
    assert response.status_code == 200
    response_dict = json.loads(response.text)
    assert response_dict["detail"] == "Reset successful, all data has been wiped."
