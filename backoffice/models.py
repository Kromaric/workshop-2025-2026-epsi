from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Team(Base):
    """Table des équipes"""
    __tablename__ = "teams"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(32), nullable=False)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    finished_at = Column(DateTime, nullable=True)
    total_time = Column(Float, default=0.0)  # En secondes

    # Relations
    players = relationship("Player", back_populates="team")
    progress = relationship("Progress", back_populates="team")


class Player(Base):
    """Table des joueurs - CLÉ COMPOSITE (id, team_id)"""
    __tablename__ = "players"

    id = Column(String(32), primary_key=True)  # team1 ou team2
    team_id = Column(String(32), ForeignKey("teams.id"), primary_key=True)  # CLÉ COMPOSITE
    name = Column(String(32), nullable=False)
    individual_score = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime, default=datetime.now)

    # Relations
    team = relationship("Team", back_populates="players")


class Progress(Base):
    """Table de progression des énigmes"""
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String(32), ForeignKey("teams.id"))
    player_id = Column(String(32), nullable=True)
    puzzle_name = Column(String(32), nullable=False)  # Ex: "chardin", "tableau_bleu", etc.
    is_solved = Column(Boolean, default=False)
    solved_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)

    # Relations
    team = relationship("Team", back_populates="progress")


class ChatMessage(Base):
    """Table des messages de chat"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String(32), nullable=False)
    player_id = Column(String(32), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    is_system = Column(Boolean, default=False)


class ButtonState(Base):
    """Table pour stocker l'état des boutons - CLÉ COMPOSITE"""
    __tablename__ = "button_states"

    team_id = Column(String(32), primary_key=True)
    player_id = Column(String(32), primary_key=True)  # CLÉ COMPOSITE
    is_enabled = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class GameSession(Base):
    """Table pour les sessions de jeu"""
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String(32), nullable=False)
    started_at = Column(DateTime, default=datetime.now)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(32), default="in_progress")  # in_progress, completed, abandoned
    final_score = Column(Integer, default=0)
