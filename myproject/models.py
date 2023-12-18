from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(Date, index=True)
    country = Column(String, index=True)
    password_hash = Column(String)

    progress = relationship("Progress", back_populates="player")


class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_date = Column(Date, index=True)
    genre = Column(String, index=True)
    developer = Column(String, index=True)

    progress = relationship("Progress", back_populates="game")


class Progress(Base):
    __tablename__ = "progress"
    progress_id = Column(Integer, primary_key=True, index=True)
    high_score = Column(Float, index=True)
    is_completed = Column(Boolean, index=True, default=False)
    playtime = Column(Integer, index=True)
    player_id = Column(Integer, ForeignKey("players.player_id"))
    game_id = Column(Integer, ForeignKey("games.game_id"))

    player = relationship("Player", back_populates="progress")
    game = relationship("Game", back_populates="progress")
