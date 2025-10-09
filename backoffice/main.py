from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, Tuple
from datetime import datetime

from database import get_db, init_db
from models import Team, Player, Progress, ChatMessage, ButtonState, GameSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Divinity(BaseModel):
    id: str
    name: str
    name_hieroglyphics: str
    description: str
    distinctive_features: List[str]
    image_url: str


class SekhmetEnigma(BaseModel):
    id: str = "sekhmet_enigma"
    title: str = "La Fille de Rê"
    description: str = "Trouvez Sekhmet, la déesse à tête de lionne, fille du dieu soleil Rê"
    riddle: str = "Suis la fille du soleil à travers les chemins dorés, écoute le murmure de ses pas sur la terre chaude, car elle seule connaît les secrets oubliés et t'indiquera la voie à suivre vers ta destinée."
    correct_answer: str = "sekhmet"
    points: int = 300

    # Divinités avec leurs schémas (pour User 1)
    divinities: List[Divinity] = [
        Divinity(
            id="sekhmet",
            name="Sekhmet",
            name_hieroglyphics="𓌂𓅓𓏏𓆗",
            description="Déesse guerrière à tête de lionne",
            distinctive_features=[
                "Tête de lionne avec crinière",
                "Corps de femme debout",
                "Disque solaire rouge sur la tête",
                "Sceptre ouas dans la main",
                "Robe longue moulante",
                "Attitude puissante et majestueuse"
            ],
            image_url="/800px-Sekhmet.png"
        ),
        Divinity(
            id="anubis",
            name="Anubis",
            name_hieroglyphics="𓇋𓈖𓊪𓅱",
            description="Dieu à tête de chacal",
            distinctive_features=[
                "Tête de chacal noir",
                "Longues oreilles pointues",
                "Corps d'homme debout",
                "Pagne court",
                "Souvent avec ankh ou sceptre",
                "Gardien des morts"
            ],
            image_url="/800px-Anubis_standing.png"
        ),
        Divinity(
            id="khepri",
            name="Khépri",
            name_hieroglyphics="𓆣𓂋𓇋",
            description="Dieu à tête de scarabée",
            distinctive_features=[
                "Tête de scarabée",
                "Corps humain masculin",
                "Scarabée complet sur la tête",
                "Symbolise le soleil levant",
                "Souvent avec disque solaire",
                "Dieu du renouveau"
            ],
            image_url="/800px-Khepri.png"
        ),
        Divinity(
            id="set",
            name="Seth",
            name_hieroglyphics="𓃩𓏏𓁀",
            description="Dieu à tête d'animal fantastique",
            distinctive_features=[
                "Tête d'animal mystérieux (âne/tamanoir)",
                "Longues oreilles carrées dressées",
                "Museau allongé et recourbé",
                "Corps d'homme",
                "Dieu du chaos et des tempêtes",
                "Souvent avec sceptre ouas"
            ],
            image_url="/800px-Set.png"
        )
    ]


class GameManager:
    def __init__(self):
        # Stocke les connexions avec (team_id, player_id) comme clé
        self.active_connections: Dict[Tuple[str, str], WebSocket] = {}
        self.solved_users = set()

    async def connect(self, websocket: WebSocket, team_id: str, player_id: str, db: Session):
        """Connexion d'un utilisateur"""
        await websocket.accept()
        # Stocker avec (team_id, player_id) pour pouvoir filtrer par équipe
        self.active_connections[(team_id, player_id)] = websocket
        
        print(f"✅ Connexion: team_id={team_id}, player_id={player_id}")

        # Vérifier si l'équipe existe, sinon la créer
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            team = Team(id=team_id, name=f"Équipe {team_id}")
            db.add(team)
            db.commit()
            print(f"🆕 Nouvelle équipe créée: {team_id}")

        # Vérifier si le joueur existe, sinon le créer
        player = db.query(Player).filter(
            Player.id == player_id,
            Player.team_id == team_id
        ).first()
        
        if not player:
            player = Player(
                id=player_id,
                team_id=team_id,
                name=f"Joueur {player_id}",
                is_active=True
            )
            db.add(player)
            db.commit()
        else:
            player.is_active = True
            player.last_activity = datetime.now()
            db.commit()

        # Initialiser l'état du bouton si nécessaire
        button_state = db.query(ButtonState).filter(
            ButtonState.team_id == team_id,
            ButtonState.player_id == player_id
        ).first()
        
        if not button_state:
            # Team2 commence avec le bouton activé
            is_enabled = player_id == "team2"
            button_state = ButtonState(
                team_id=team_id,
                player_id=player_id,
                is_enabled=is_enabled
            )
            db.add(button_state)
            db.commit()

        # Envoyer l'état initial
        await self.send_button_state(team_id, player_id, db)
        await self.send_chat_history(team_id, player_id, db)
        await self.send_progress(team_id, player_id, db)

    def disconnect(self, team_id: str, player_id: str, db: Session):
        """Déconnexion d'un utilisateur"""
        if (team_id, player_id) in self.active_connections:
            del self.active_connections[(team_id, player_id)]
        
        # Marquer le joueur comme inactif
        player = db.query(Player).filter(
            Player.id == player_id,
            Player.team_id == team_id
        ).first()
        if player:
            player.is_active = False
            player.last_activity = datetime.now()
            db.commit()

    async def send_button_state(self, team_id: str, player_id: str, db: Session):
        """Envoie l'état du bouton à un utilisateur"""
        if (team_id, player_id) in self.active_connections:
            button_state = db.query(ButtonState).filter(
                ButtonState.team_id == team_id,
                ButtonState.player_id == player_id
            ).first()
            
            await self.active_connections[(team_id, player_id)].send_json({
                "type": "button_state",
                "enabled": button_state.is_enabled if button_state else False
            })

    async def send_chat_history(self, team_id: str, player_id: str, db: Session):
        """Envoie l'historique du chat"""
        if (team_id, player_id) in self.active_connections:
            messages = db.query(ChatMessage).filter(
                ChatMessage.team_id == team_id
            ).order_by(ChatMessage.timestamp).limit(100).all()
            
            message_list = [{
                "user_id": msg.player_id,
                "text": msg.message,
                "timestamp": msg.timestamp.isoformat(),
                "is_system": msg.is_system
            } for msg in messages]
            
            await self.active_connections[(team_id, player_id)].send_json({
                "type": "chat_history",
                "messages": message_list
            })

    async def send_progress(self, team_id: str, player_id: str, db: Session):
        """Envoie la progression de l'équipe"""
        if (team_id, player_id) in self.active_connections:
            team = db.query(Team).filter(Team.id == team_id).first()
            progress_items = db.query(Progress).filter(
                Progress.team_id == team_id
            ).all()
            
            progress_data = {
                "team_score": team.score if team else 0,
                "puzzles": [{
                    "name": p.puzzle_name,
                    "is_solved": p.is_solved,
                    "attempts": p.attempts,
                    "hints_used": p.hints_used,
                    "points_earned": p.points_earned
                } for p in progress_items]
            }
            
            await self.active_connections[(team_id, player_id)].send_json({
                "type": "progress",
                "data": progress_data
            })

    async def broadcast_button_states(self, team_id: str, db: Session):
        """Diffuse l'état des boutons à tous les utilisateurs de l'équipe"""
        players = db.query(Player).filter(
            Player.team_id == team_id,
            Player.is_active == True
        ).all()
        
        for player in players:
            if (team_id, player.id) in self.active_connections:
                await self.send_button_state(team_id, player.id, db)

    async def broadcast_message(self, team_id: str, message: Dict):
        """Diffuse un message de chat à tous les membres de l'équipe"""
        # ✅ FILTRER PAR ÉQUIPE !
        for (t_id, p_id), ws in self.active_connections.items():
            if t_id == team_id:  # Envoyer seulement aux membres de cette équipe
                await ws.send_json({
                    "type": "chat_message",
                    "message": message
                })

    async def broadcast_progress(self, team_id: str, db: Session):
        """Diffuse la progression à tous les membres de l'équipe"""
        players = db.query(Player).filter(
            Player.team_id == team_id,
            Player.is_active == True
        ).all()
        
        for player in players:
            if (team_id, player.id) in self.active_connections:
                await self.send_progress(team_id, player.id, db)

    async def send_sekhmet_schemas(self, team_id: str, db: Session):
        """Envoie les schémas Sekhmet après résolution de Chardin"""
        from sekhmet_config import SEKHMET_ENIGMA
        
        # Envoyer les schémas complets à team1 (guide)
        if (team_id, "team1") in self.active_connections:
            await self.active_connections[(team_id, "team1")].send_json({
                "type": "sekhmet_schemas",
                "enigma": SEKHMET_ENIGMA
            })
        
        # Envoyer la sélection des divinités à team2 (validateur)
        if (team_id, "team2") in self.active_connections:
            await self.active_connections[(team_id, "team2")].send_json({
                "type": "sekhmet_selection",
                "divinities": [{"id": d["id"], "name": d["name"]} for d in SEKHMET_ENIGMA["divinities"]]
            })

    async def validate_chardin(self, team_id: str, player_id: str, code: str, db: Session):
        """Valide le code Chardin"""
        correct_code = "3563"

        if player_id != "team1":
            return {
                "success": False,
                "message": "Cette énigme est réservée à Team 1"
            }

        # Vérifier si déjà résolu
        progress = db.query(Progress).filter(
            Progress.team_id == team_id,
            Progress.puzzle_name == "chardin"
        ).first()

        if not progress:
            progress = Progress(
                team_id=team_id,
                player_id=player_id,
                puzzle_name="chardin"
            )
            db.add(progress)
            db.commit()

        if progress.is_solved:
            return {
                "success": False,
                "message": "Vous avez déjà résolu cette énigme"
            }

        # Incrémenter les tentatives
        progress.attempts += 1

        if code == correct_code:
            progress.is_solved = True
            progress.solved_at = datetime.now()
            progress.points_earned = 100
            
            # Mettre à jour le score de l'équipe
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                team.score += progress.points_earned
            
            db.commit()

            # Diffuser la progression
            await self.broadcast_progress(team_id, db)
            
            # Envoyer les schémas Sekhmet à team1
            await self.send_sekhmet_schemas(team_id, db)

            return {
                "success": True,
                "message": "Bravo ! Le code est correct ! 🎉",
                "points": progress.points_earned
            }
        else:
            db.commit()
            return {
                "success": False,
                "message": "Code incorrect. Observez plus attentivement les tableaux."
            }

    async def validate_sekhmet(self, team_id: str, player_id: str, hieroglyph_code: str, db: Session):
        """Valide l'énigme Sekhmet"""
        
        # Vérifier que c'est team2 qui valide
        if player_id != "team2":
            return {
                "success": False,
                "message": "Cette énigme doit être validée par Équipe 2"
            }
        
        # Vérifier si déjà résolu
        progress = db.query(Progress).filter(
            Progress.team_id == team_id,
            Progress.puzzle_name == "sekhmet"
        ).first()
        
        if not progress:
            progress = Progress(
                team_id=team_id,
                player_id=player_id,
                puzzle_name="sekhmet"
            )
            db.add(progress)
            db.commit()
        
        if progress.is_solved:
            return {
                "success": False,
                "message": "Vous avez déjà résolu cette énigme"
            }
        
        # Incrémenter les tentatives
        progress.attempts += 1
        
        # Code correct
        correct_code = "h3-h6-h5-h10"
        
        if hieroglyph_code == correct_code:
            progress.is_solved = True
            progress.solved_at = datetime.now()
            progress.points_earned = 300
            
            # Mettre à jour le score de l'équipe
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                team.score += progress.points_earned
            
            db.commit()
            
            # Diffuser la progression
            await self.broadcast_progress(team_id, db)
            
            return {
                "success": True,
                "message": "🎉 Bravo ! Vous avez correctement identifié SEKHMET !",
                "info": "Sekhmet était la déesse guerrière égyptienne, fille du dieu soleil Rê.",
                "points": progress.points_earned
            }
        else:
            db.commit()
            return {
                "success": False,
                "message": "❌ Ce n'est pas la bonne séquence de hiéroglyphes. Vérifiez avec Équipe 1 !",
                "attempted_code": hieroglyph_code
            }

    async def handle_button_click(self, team_id: str, player_id: str, db: Session):
        """Gère le clic sur le bouton"""
        other_user = "team1" if player_id == "team2" else "team2"

        # Récupérer les états des boutons
        current_state = db.query(ButtonState).filter(
            ButtonState.team_id == team_id,
            ButtonState.player_id == player_id
        ).first()
        
        other_state = db.query(ButtonState).filter(
            ButtonState.team_id == team_id,
            ButtonState.player_id == other_user
        ).first()

        # Créer l'autre état s'il n'existe pas
        if not other_state:
            other_state = ButtonState(
                team_id=team_id,
                player_id=other_user,
                is_enabled=False
            )
            db.add(other_state)

        # Inverser les états
        if current_state:
            current_state.is_enabled = False
            current_state.updated_at = datetime.now()
        
        other_state.is_enabled = True
        other_state.updated_at = datetime.now()
        
        db.commit()

        # Diffuser les nouveaux états
        await self.broadcast_button_states(team_id, db)

    async def handle_chat_message(self, team_id: str, player_id: str, text: str, db: Session):
        """Gère l'envoi d'un message de chat"""
        # Sauvegarder le message dans la BDD
        chat_message = ChatMessage(
            team_id=team_id,
            player_id=player_id,
            message=text,
            timestamp=datetime.now()
        )
        db.add(chat_message)
        db.commit()

        message_dict = {
            "user_id": player_id,
            "text": text,
            "timestamp": chat_message.timestamp.isoformat()
        }

        # Diffuser le message
        await self.broadcast_message(team_id, message_dict)



manager = GameManager()


@app.on_event("startup")
async def startup_event():
    """Initialiser la base de données au démarrage"""
    init_db()
    print("✅ Base de données initialisée")


@app.websocket("/ws/{team_id}/{player_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    team_id: str,
    player_id: str,
    db: Session = Depends(get_db)
):
    await manager.connect(websocket, team_id, player_id, db)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "validate_chardin":
                result = await manager.validate_chardin(
                    team_id,
                    player_id,
                    data.get("code", ""),
                    db
                )
                await websocket.send_json({
                    "type": "chardin_result",
                    "result": result
                })
            elif data.get("action") == "validate_sekhmet":
                result = await manager.validate_sekhmet(
                    team_id,
                    player_id,
                    data.get("hieroglyph_code", ""),
                    db
                )
                await websocket.send_json({
                    "type": "sekhmet_result",
                    "result": result
                })
            elif data.get("action") == "button_click":
                await manager.handle_button_click(team_id, player_id, db)

            elif data.get("action") == "send_message":
                message_text = data.get("message", "")
                if message_text.strip():
                    await manager.handle_chat_message(team_id, player_id, message_text, db)

    except WebSocketDisconnect:
        manager.disconnect(team_id, player_id, db)
        print(f"Player {player_id} from team {team_id} disconnected")


@app.get("/")
def read_root():
    return {"message": "Escape Game Musée - API avec Base de Données"}


@app.get("/teams/{team_id}/stats")
def get_team_stats(team_id: str, db: Session = Depends(get_db)):
    """Récupère les statistiques d'une équipe"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return {"error": "Team not found"}
    
    progress = db.query(Progress).filter(Progress.team_id == team_id).all()
    
    return {
        "team_id": team.id,
        "score": team.score,
        "puzzles_solved": sum(1 for p in progress if p.is_solved),
        "total_puzzles": len(progress),
        "created_at": team.created_at.isoformat() if team.created_at else None,
        "progress": [{
            "puzzle": p.puzzle_name,
            "solved": p.is_solved,
            "attempts": p.attempts,
            "points": p.points_earned
        } for p in progress]
    }
