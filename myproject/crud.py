from sqlalchemy.orm import Session

import auth
import models
import schemas


# Player CRUD

# Search a player by id
def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()


# Search a player by email
def get_player_by_email(db: Session, email: str):
    return db.query(models.Player).filter(models.Player.email == email).first()


# Search a player by username
def get_player_by_username(db: Session, username: str):
    return db.query(models.Player).filter(models.Player.username == username).first()


# Retrieve all players
def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()


# Create a new player; password, username and email required, id will auto-generate
def create_player(db: Session, player: schemas.PlayerCreate):
    hashed_password = auth.get_password_hash(player.password)
    db_player = models.Player(username=player.username,
                              email=player.email,
                              date_of_birth=player.date_of_birth,
                              country=player.country,
                              password_hash=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


# Game CRUD

# Search a game by id
def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.game_id == game_id).first()


# Search a game by title
def get_game_by_title(db: Session, title: str):
    return db.query(models.Game).filter(models.Game.title == title).first()


# Retrieve all games
def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()


# Create a new Game, title and release date are required, id will auto-generate
def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(title=game.title,
                          release_date=game.release_date,
                          genre=game.genre,
                          developer=game.developer)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


# Progress CRUD

# Get all progress
def get_progress(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Progress).offset(skip).limit(limit).all()


# Create a progress entity
def create_progress(db: Session, progress: schemas.ProgressCreate):
    db_progress = models.Progress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


# Update a progress entity
def update_progress(db: Session, player: int, game: int, progress: schemas.ProgressUpdate):
    db_progress = get_progress_by_player_and_game(db, player, game)
    if db_progress is None:
        return None
    for key, value in progress.dict().items():
        setattr(db_progress, key, value)
    db.commit()
    db.refresh(db_progress)
    return db_progress


# Get progress based on the player_id and game_id
def get_progress_by_player_and_game(db: Session, player_id: int, game_id: int):
    return db.query(models.Progress).filter(models.Progress.player_id == player_id,
                                            models.Progress.game_id == game_id
                                            ).first()


# Delete progress based on the player_id and game_id
def delete_progress(db: Session, player_id: int, game_id: int):
    progress_to_delete = get_progress_by_player_and_game(db, player_id, game_id)
    db.delete(progress_to_delete)
    db.commit()
    return progress_to_delete


# CRUD Extra

# Delete everything
def delete_all(db: Session):
    db.query(models.Player).delete()
    db.query(models.Game).delete()
    db.query(models.Progress).delete()
    db.commit()
