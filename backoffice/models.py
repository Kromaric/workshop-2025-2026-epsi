from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TeamDB(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    members = Column(JSON)
    progress = Column(JSON)
    door_open = Column(Boolean, default=False)
    score = Column(Integer, default=0)  
    date = Column(DateTime, default=None, nullable=True)  # Nouvelle colonne pour le timer

class ProgressDB(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    level = Column(Integer)
    status = Column(String(255))

