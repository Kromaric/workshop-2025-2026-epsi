from xmlrpc.client import DateTime
from fastapi import FastAPI, HTTPException, WebSocket, Depends
from typing import List
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
from .models import Base, TeamDB, ProgressDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/escape_room_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_teams():
    db = SessionLocal()
    try:
        for team_id, team_name in [(1, "Equipe 1"), (2, "Equipe 2")]:
            team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
            if not team:
                db.add(TeamDB(id=team_id, name=team_name, members=[], progress=[], door_open=False))
        db.commit()
    finally:
        db.close()


class Progress(BaseModel):
    level: int
    status: str

class Team(BaseModel):
    id: int
    name: str
    members: list
    progress: list
    door_open: bool
    score: int
    date: DateTime 



app = FastAPI()
websockets_by_team = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

team_2_sockets = websockets_by_team.get(2, [])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    init_teams()

@app.get("/teams/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.put("/teams/{team_id}/progress")
def update_progress(team_id: int, progress: List[Progress], db: Session = Depends(get_db)):
    # Supprime l'ancien progrès
    db.query(ProgressDB).filter(ProgressDB.team_id == team_id).delete()
    # Ajoute le nouveau progrès
    for p in progress:
        db.add(ProgressDB(team_id=team_id, level=p.level, status=p.status))
    db.commit()
    return {"message": "Progress updated"}


@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: int):
    await websocket.accept()
    if team_id not in websockets_by_team:
        websockets_by_team[team_id] = []
    websockets_by_team[team_id].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websockets_by_team[team_id].remove(websocket)

async def notify_team(team_id: int, message: str):
    sockets = websockets_by_team.get(team_id, [])
    for ws in sockets:
        await ws.send_text(message)

@app.post("/unlock")
async def unlock_button2():
    await notify_team(2, "door_unlocked")
    return {"message": "Porte de l'équipe 2 débloquée"}

@app.post("/solve_enigma")
async def solve_enigma(team_id: int, enigma_id: int):
    if team_id == 1 and enigma_id == 3:
        await notify_team(2, "door_unlocked")
        return {"message": "Équipe 1 a débloqué la porte de l'équipe 2"}
    return {"message": "Énigme résolue, mais aucune porte débloquée"}


@app.post("/teams/{team_id}/complete_level")
async def complete_level(team_id: int, level: int, db: Session = Depends(get_db)):
    progress = db.query(ProgressDB).filter(ProgressDB.team_id == team_id, ProgressDB.level == level).first()
    if not progress:
        progress = ProgressDB(team_id=team_id, level=level, status="completed")
        db.add(progress)
    else:
        progress.status = "completed"
    db.commit()

    # Synchronisation pour l'autre équipe
    if team_id == 1 and level == 2:
        target_progress = db.query(ProgressDB).filter(ProgressDB.team_id == 2, ProgressDB.level == level).first()
        if not target_progress:
            db.add(ProgressDB(team_id=2, level=level, status="in_progress"))
        else:
            target_progress.status = "in_progress"
        db.commit()
        await notify_team(2, "level_2_unlocked")
    return {"message": f"Niveau {level} terminé pour l'équipe {team_id}"}

@app.get("/teams/{team_id}/score")
def get_score(team_id: int, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"score": team.score}

@app.put("/teams/{team_id}/score")
def update_score(team_id: int, score: int, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.score = score
    db.commit()
    return {"message": "Score updated", "score": team.score}