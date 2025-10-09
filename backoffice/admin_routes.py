"""
Routes API supplémentaires pour l'administration
À ajouter dans main.py si besoin
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Team, Player, Progress, ChatMessage
from typing import List
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/teams")
def get_all_teams(db: Session = Depends(get_db)):
    """Récupère toutes les équipes"""
    teams = db.query(Team).all()
    return [{
        "id": team.id,
        "name": team.name,
        "score": team.score,
        "created_at": team.created_at.isoformat() if team.created_at else None,
        "finished_at": team.finished_at.isoformat() if team.finished_at else None
    } for team in teams]


@router.get("/teams/{team_id}")
def get_team_detail(team_id: str, db: Session = Depends(get_db)):
    """Récupère les détails d'une équipe"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    players = db.query(Player).filter(Player.team_id == team_id).all()
    progress = db.query(Progress).filter(Progress.team_id == team_id).all()
    
    return {
        "id": team.id,
        "name": team.name,
        "score": team.score,
        "created_at": team.created_at.isoformat() if team.created_at else None,
        "players": [{
            "id": p.id,
            "name": p.name,
            "individual_score": p.individual_score,
            "is_active": p.is_active
        } for p in players],
        "progress": [{
            "puzzle": p.puzzle_name,
            "solved": p.is_solved,
            "attempts": p.attempts,
            "points": p.points_earned,
            "solved_at": p.solved_at.isoformat() if p.solved_at else None
        } for p in progress]
    }


@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Récupère le classement des équipes"""
    teams = db.query(Team).order_by(Team.score.desc()).limit(limit).all()
    
    leaderboard = []
    for idx, team in enumerate(teams, 1):
        puzzles_solved = db.query(Progress).filter(
            Progress.team_id == team.id,
            Progress.is_solved == True
        ).count()
        
        leaderboard.append({
            "rank": idx,
            "team_id": team.id,
            "team_name": team.name,
            "score": team.score,
            "puzzles_solved": puzzles_solved,
            "created_at": team.created_at.isoformat() if team.created_at else None
        })
    
    return leaderboard


@router.get("/stats/global")
def get_global_stats(db: Session = Depends(get_db)):
    """Récupère les statistiques globales"""
    total_teams = db.query(Team).count()
    total_players = db.query(Player).count()
    total_messages = db.query(ChatMessage).count()
    
    puzzles_data = db.query(Progress).all()
    total_puzzles = len(puzzles_data)
    solved_puzzles = sum(1 for p in puzzles_data if p.is_solved)
    
    return {
        "total_teams": total_teams,
        "total_players": total_players,
        "total_messages": total_messages,
        "total_puzzles": total_puzzles,
        "solved_puzzles": solved_puzzles,
        "success_rate": (solved_puzzles / total_puzzles * 100) if total_puzzles > 0 else 0
    }


@router.delete("/teams/{team_id}")
def delete_team(team_id: str, db: Session = Depends(get_db)):
    """Supprime une équipe et toutes ses données"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Supprimer toutes les données liées
    db.query(Player).filter(Player.team_id == team_id).delete()
    db.query(Progress).filter(Progress.team_id == team_id).delete()
    db.query(ChatMessage).filter(ChatMessage.team_id == team_id).delete()
    db.query(Team).filter(Team.id == team_id).delete()
    
    db.commit()
    
    return {"message": f"Team {team_id} deleted successfully"}


@router.post("/teams/{team_id}/reset")
def reset_team_progress(team_id: str, db: Session = Depends(get_db)):
    """Réinitialise la progression d'une équipe"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Réinitialiser le score
    team.score = 0
    team.finished_at = None
    
    # Réinitialiser la progression
    db.query(Progress).filter(Progress.team_id == team_id).delete()
    
    db.commit()
    
    return {"message": f"Team {team_id} progress reset successfully"}


@router.get("/messages/{team_id}")
def get_team_messages(team_id: str, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les messages d'une équipe"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.team_id == team_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
    
    return [{
        "player_id": msg.player_id,
        "message": msg.message,
        "timestamp": msg.timestamp.isoformat(),
        "is_system": msg.is_system
    } for msg in reversed(messages)]


# Pour utiliser ces routes, ajoutez dans main.py :
"""
from admin_routes import router as admin_router
app.include_router(admin_router)
"""
