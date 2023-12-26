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
    response_1 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/players", json=payload_1, headers=headers)
    assert response_1.status_code == 200
    assert json.loads(response_1.text) == {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}

    # Already registered username
    response_2 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/players", json=payload_2, headers=headers)
    assert response_2.status_code == 400
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Username already registered"

    # Already registered email
    response_3 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/players", json=payload_3, headers=headers)
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

    token_request = requests.post("https://project-api-service-wobr53.cloud.okteto.net/token", data=request_data, headers=headers)
    token = json.loads(token_request.text)["access_token"]

    headers_with_token = {
        "accept": "application/json",
        "Authorization": f'Bearer {token}'
    }

    return headers_with_token


# Test get_players function - END: GET /players
def test_get_players():
    # Unauthenticated
    response_1 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/players")
    response_dict_1 = json.loads(response_1.text)
    assert response_dict_1["detail"] == "Not authenticated"

    # Authenticated
    response_2 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/players", headers=test_token())
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
    response = requests.get("https://project-api-service-wobr53.cloud.okteto.net/players/test")
    assert response.status_code == 401
    response_dict = json.loads(response.text)
    assert response_dict["detail"] == "Not authenticated"

    # Authenticated, existing player
    response_1 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/players/test", headers=test_token())
    assert response_1.status_code == 200
    assert json.loads(response_1.text) == {
        "username": "test",
        "email": "t@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "player_id": 1,
        "progress": []}

    # Authenticated, non-existing player
    response_2 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/players/test_2", headers=test_token())
    assert response_2.status_code == 404
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Username not found"


# Test create_games functions - END: POST /games
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
    response_1a = requests.post("https://project-api-service-wobr53.cloud.okteto.net/games", json=payload_1, headers=headers)
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
    response_1b = requests.post("https://project-api-service-wobr53.cloud.okteto.net/games", json=payload_1, headers=headers)
    assert response_1b.status_code == 400
    response_dict_1 = json.loads(response_1b.text)
    assert response_dict_1["detail"] == "Game already registered"

    # Existing game title with different release date
    response_2 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/games", json=payload_2, headers=headers)
    assert response_2.status_code == 200


# Test get_games functions - END: GET /games
def test_get_games():
    # Unauthenticated
    response_1 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/games")
    assert response_1.status_code == 401
    response_dict_1 = json.loads(response_1.text)
    assert response_dict_1["detail"] == "Not authenticated"

    # Authenticated
    response_2 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/games", headers=test_token())
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


# Test create_progress functions - END: POST /progress
def test_create_progress():
    headers = {"Content-Type": "application/json"}

    payload_1 = {
        "player_id": 1,
        "game_id": 1,
        "high_score": 12500,
        "playtime": 4,
        "is_completed": False,
    }

    payload_2 = {
        "player_id": 0,
        "game_id": 1,
        "high_score": 9500,
        "playtime": 1,
        "is_completed": False,
    }

    payload_3 = {
        "player_id": 1,
        "game_id": 0,
        "high_score": 45000.00,
        "playtime": 22,
        "is_completed": True,
    }

    # Non-existing progress
    response_1a = requests.post("https://project-api-service-wobr53.cloud.okteto.net/progress", json=payload_1, headers=headers)
    assert response_1a.status_code == 200
    assert json.loads(response_1a.text) == {
        "player_id": 1,
        "game_id": 1,
        "high_score": 12500,
        "playtime": 4,
        "is_completed": False,
        "progress_id": 1
    }

    # Existing progress entry
    response_1b = requests.post("https://project-api-service-wobr53.cloud.okteto.net/progress", json=payload_1, headers=headers)
    assert response_1b.status_code == 400
    response_dict_1 = json.loads(response_1b.text)
    assert response_dict_1["detail"] == "Progress entry already exists"

    # Non-existing player
    response_2 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/progress", json=payload_2, headers=headers)
    assert response_2.status_code == 404
    response_dict_2 = json.loads(response_2.text)
    assert response_dict_2["detail"] == "Player not found"

    # Non-existing game
    response_3 = requests.post("https://project-api-service-wobr53.cloud.okteto.net/progress", json=payload_3, headers=headers)
    assert response_3.status_code == 404
    response_dict_3 = json.loads(response_3.text)
    assert response_dict_3["detail"] == "Game not found"


# Test get_progress function - END: GET /progress
def test_get_progress():
    # Unauthenticated
    response_1 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/progress")
    assert response_1.status_code == 401
    response_dict_1 = json.loads(response_1.text)
    assert response_dict_1["detail"] == "Not authenticated"

    # Authenticated
    response_2 = requests.get("https://project-api-service-wobr53.cloud.okteto.net/progress", headers=test_token())
    assert response_2.status_code == 200
    assert json.loads(response_2.text) == [{
        "player_id": 1,
        "game_id": 1,
        "high_score": 12500,
        "playtime": 4,
        "is_completed": False,
        "progress_id": 1
    }]


# Test update_progress function - END: PUT /progress
def test_update_progress():
    headers = {"Content-Type": "application/json"}

    payload_1 = {
        "high_score": 15000,
        "playtime": 6,
        "is_completed": True,
    }

    # Updatable progress
    response_1a = requests.put("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=1", json=payload_1, headers=headers)
    assert response_1a.status_code == 200
    assert json.loads(response_1a.text) == {
        "game_id": 1,
        "high_score": 15000.0,
        "is_completed": True,
        "player_id": 1,
        "playtime": 6,
        "progress_id": 1
    }

    # Non-existing player
    response_1b = requests.put("https://project-api-service-wobr53.cloud.okteto.net/progress?player=0&game=1", json=payload_1, headers=headers)
    assert response_1b.status_code == 404
    assert json.loads(response_1b.text)["detail"] == "Player not found"

    # Non-existing game
    response_1c = requests.put("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=0", json=payload_1, headers=headers)
    assert response_1c.status_code == 404
    assert json.loads(response_1c.text)["detail"] == "Game not found"

    # Non-existing progress
    # Create extra player
    player = {
        "username": "test2",
        "email": "test@t.com",
        "date_of_birth": "2023-12-18",
        "country": "BE",
        "password": "abc123!"}
    requests.post("https://project-api-service-wobr53.cloud.okteto.net/player", json=player, headers=headers)
    # Test non-existing progress
    response_1d = requests.put("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=2", json=payload_1, headers=headers)
    assert response_1d.status_code == 404
    assert json.loads(response_1d.text)["detail"] == "Progress not found"


# Test delete_progress function - END: DELETE /progress
def test_delete_progress():
    # Non-existing player
    response_1a = requests.delete("https://project-api-service-wobr53.cloud.okteto.net/progress?player=0&game=0")
    assert response_1a.status_code == 404
    assert json.loads(response_1a.text)["detail"] == "Player not found"

    # Non-existing game
    response_1b = requests.delete("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=0")
    assert response_1b.status_code == 404
    assert json.loads(response_1b.text)["detail"] == "Game not found"

    # Non-existing progress
    response_1c = requests.delete("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=2")
    assert response_1c.status_code == 404
    assert json.loads(response_1c.text)["detail"] == "Progress entry not found"

    response_1d = requests.delete("https://project-api-service-wobr53.cloud.okteto.net/progress?player=1&game=1")
    assert response_1d.status_code == 200
    assert json.loads(response_1d.text)["detail"] == "Progress of player 1 in game 1 has been deleted."


# Test delete_all function - END: DELETE /reset
def test_reset():
    response = requests.delete("https://project-api-service-wobr53.cloud.okteto.net/reset")
    assert response.status_code == 200
    response_dict = json.loads(response.text)
    assert response_dict["detail"] == "Reset successful, all data has been wiped."
