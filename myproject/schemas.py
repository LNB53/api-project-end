from pydantic import BaseModel
from datetime import date


# Base class for all progress
class ProgressBase(BaseModel):
    player_id: int
    game_id: int
    high_score: float
    playtime: int
    is_completed: bool


# Schema for progress updates
class ProgressUpdate(BaseModel):
    high_score: float | None = None
    playtime: int | None = None
    is_completed: bool | None = None


# Progress OUT
class Progress(ProgressBase):
    progress_id: int

    class Config:
        orm_mode = True


# Progress IN
class ProgressCreate(ProgressBase):
    pass


# Base class for all players
class PlayerBase(BaseModel):
    username: str
    email: str
    date_of_birth: date
    country: str | None = None


# Player OUT
class Player(PlayerBase):
    player_id: int
    progress: list[Progress] = []

    class Config:
        orm_mode = True


# Player IN
class PlayerCreate(PlayerBase):
    password: str


# Base class for all games
class GameBase(BaseModel):
    title: str
    release_date: date
    genre: str | None = None
    developer: str | None = None


# Game OUT
class Game(GameBase):
    game_id: int
    progress: list[Progress] = []

    class Config:
        orm_mode = True


# Game IN
class GameCreate(GameBase):
    pass
