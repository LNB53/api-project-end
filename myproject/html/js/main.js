// main.js

let authToken = '';
// Request token function
function getToken(event) {
    event.preventDefault();

    const username = document.getElementById('usernameIn').value;
    const password = document.getElementById('passwordIn').value;

    const userData = {
        client_id: '',
        client_secret: '',
        scope: '',
        grant_type: '',
        refresh_token: '',
        username: username,
        password: password
    }

    const formData = new URLSearchParams();
    for (const key in userData) {
        formData.append(key, userData[key]);
    }

    fetch('https://project-api-service-wobr53.cloud.okteto.net/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            authToken = data.access_token;
            const formattedData = JSON.stringify(data, null, 2);
            document.getElementById('responseDiv').innerHTML = '<pre>' + formattedData + '</pre>';
        })
        .catch(response => {
            if (response.status === 401) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Get all Players
function getPlayers() {
    fetch('https://project-api-service-wobr53.cloud.okteto.net/players', {
        headers: {
            'Authorization': 'Bearer ' + authToken
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const formattedData = JSON.stringify(data, null, 2);
            document.getElementById('responseDiv').innerHTML = '<pre>' + formattedData + '</pre>';
        })
        .catch(response => {
            if (response.status === 401) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Get a Player by Username
function getPlayerByUsername() {
    event.preventDefault();

    const username = document.getElementById('findUsername').value;
    const url = `https://project-api-service-wobr53.cloud.okteto.net/players/${username}`
    console.log('Request URL:', url)
    fetch(url, {
        headers: {
            'Authorization': 'Bearer ' + authToken
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const formattedData = JSON.stringify(data, null, 2);
            document.getElementById('responseDiv').innerHTML = '<pre>' + formattedData + '</pre>';
        })
        .catch(response => {
            if ([401,404].includes(response.status)) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Create a Player
function postPlayer(event) {
    event.preventDefault();

    const username = document.getElementById('usernameInput').value;
    const email = document.getElementById('emailInput').value;
    const dob = document.getElementById('dobInput').value;
    const country = document.getElementById('countryInput').value;
    const password = document.getElementById('passwordInput').value;

    const playerData = {
        username: username,
        email: email,
        date_of_birth: dob,
        country: country,
        password: password
    };

    fetch('https://project-api-service-wobr53.cloud.okteto.net/players', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(playerData),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            document.getElementById('responseDiv').innerText =
                'Created a user "'+ data.username +
                '" with following identification:\n\tE-mail: '+ data.email +
                '\n\tDate of Birth: ' + data.date_of_birth +
                '\n\tCountry: ' + data.country;
        })
        .catch(response => {
            if (response.status === 400) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Get all Games
function getGames() {
    fetch('https://project-api-service-wobr53.cloud.okteto.net/games', {
        headers: {
            'Authorization': 'Bearer ' + authToken
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const formattedData = JSON.stringify(data, null, 2);
            document.getElementById('responseDiv').innerHTML = '<pre>' + formattedData + '</pre>';
        })
        .catch(response => {
            if (response.status === 401) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Create a Game
function postGame(event) {
    event.preventDefault();

    const title = document.getElementById('titleInput').value;
    const release_date = document.getElementById('rdInput').value;
    const genre = document.getElementById('genreInput').value;
    const developer = document.getElementById('developerInput').value;

    const gameData = {
        title: title,
        release_date: release_date,
        genre: genre,
        developer: developer
    };

    fetch('https://project-api-service-wobr53.cloud.okteto.net/games', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameData),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            document.getElementById('responseDiv').innerText =
                'Created a game "'+ data.title +
                '" with following specifications:\n\tRelease Date: '+ data.release_date +
                '\n\tGenre: ' + data.genre +
                '\n\tDeveloper: ' + data.developer;
        })
        .catch(response => {
            if (response.status === 400) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Get all Progress
function getProgress() {
    fetch('https://project-api-service-wobr53.cloud.okteto.net/progress', {
        headers: {
            'Authorization': 'Bearer ' + authToken
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const formattedData = JSON.stringify(data, null, 2);
            document.getElementById('responseDiv').innerHTML = '<pre>' + formattedData + '</pre>';
        })
        .catch(response => {
            if (response.status === 401) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Create a Progress Entry
function postProgress(event) {
    event.preventDefault();

    const player_id = document.getElementById('playerInput').value;
    const game_id = document.getElementById('gameInput').value;
    const high_score = document.getElementById('highScoreInput').value;
    const playtime = document.getElementById('playtimeInput').value;

    const checkbox = document.getElementById('isCompletedInput');
    const is_completed = checkbox.checked;

    const progressData = {
        player_id: player_id,
        game_id: game_id,
        high_score: high_score,
        playtime: playtime,
        is_completed: is_completed
    };

    fetch('https://project-api-service-wobr53.cloud.okteto.net/progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(progressData),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const completionStatus = data.is_completed ? 'has' : 'has not';
            document.getElementById('responseDiv').innerText =
                'Created a progress entry for player '+ data.player_id +
                ' in game ' + data.game_id +
                ' with following specifications:\n\tHighscore: '+ data.high_score +
                '\n\tPlaytime: ' + data.playtime +
                '\n\t' + 'The game ' + completionStatus + ' been completed by this player'
        })
        .catch(response => {
            if ([400,404].includes(response.status)) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Update a Progress Entry
function updateProgress(event) {
    event.preventDefault();

    const player = document.getElementById('playerIn').value;
    const game = document.getElementById('gameIn').value;
    const high_score = document.getElementById('highScoreIn').value;
    const playtime = document.getElementById('playtimeIn').value;

    const checkbox = document.getElementById('isCompletedIn');
    const is_completed = checkbox.checked;

    const progressData = {
        high_score: high_score,
        playtime: playtime,
        is_completed: is_completed
    };

    const url = `https://project-api-service-wobr53.cloud.okteto.net/progress/?player=${player}&game=${game}`
    console.log('Request URL:', url)
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(progressData),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            console.log('Response Data:', data)
            const completionStatus = data.is_completed ? 'has' : 'has still not';
            document.getElementById('responseDiv').innerText =
                'Updated a progress entry for player '+ data.player_id +
                ' in game ' + data.game_id +
                ' with following specifications:\n\tHighscore: '+ data.high_score +
                '\n\tPlaytime: ' + data.playtime +
                '\n\t' + 'The game ' + completionStatus + ' been completed by this player'
        })
        .catch(response => {
            if (response.status === 404) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Function to Delete a Progress Entry
function deleteProgress() {
    event.preventDefault();

    const player = document.getElementById('findPlayer').value;
    const game = document.getElementById('findGame').value;
    const url = `https://project-api-service-wobr53.cloud.okteto.net/progress/?player=${player}&game=${game}`
    console.log('Request URL:', url)
    fetch(url, {
        method: 'DELETE'
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(data => {
            document.getElementById('responseDiv').innerText = data.detail;                })
        .catch(response => {
            if (response.status === 404) {
                response.json().then(errorData => {
                    document.getElementById('responseDiv').innerText = errorData.detail;
                });
            } else {
                console.error('Error:', response);
            }
        });
}

// Reset function
function reset() {
    fetch('https://project-api-service-wobr53.cloud.okteto.net/reset', {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('responseDiv').innerText = data.detail;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}