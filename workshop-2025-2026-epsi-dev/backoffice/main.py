from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

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
        self.active_connections: Dict[str, WebSocket] = {}
        self.solved_users = set()
        self.sekhmet_solved = False
        self.button_states: Dict[str, bool] = {
            "user1": False,
            "user2": True
        }
        self.chat_history: List[Dict] = []
        self.user1_hints_unlocked = False

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.send_button_state(user_id)
        await self.send_chat_history(user_id)

        # Envoyer l'énigme selon l'utilisateur
        if user_id == "user1" and self.user1_hints_unlocked:
            await self.send_sekhmet_schemas(user_id)
        elif user_id == "user2" and self.user1_hints_unlocked:
            await self.send_user2_interface(user_id)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_button_state(self, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "button_state",
                "enabled": self.button_states.get(user_id, False)
            })

    async def send_chat_history(self, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "chat_history",
                "messages": self.chat_history
            })

    async def send_sekhmet_schemas(self, user_id: str):
        """Envoie les schémas à User 1 (rôle de guide uniquement)"""
        if user_id in self.active_connections:
            enigma = SekhmetEnigma()
            await self.active_connections[user_id].send_json({
                "type": "sekhmet_schemas",
                "enigma": {
                    "id": enigma.id,
                    "title": enigma.title,
                    "description": enigma.description,
                    "riddle": enigma.riddle,
                    "divinities": [d.dict() for d in enigma.divinities]
                }
            })

    async def send_user2_interface(self, user_id: str):
        """Envoie l'interface de sélection à User 2"""
        if user_id in self.active_connections:
            enigma = SekhmetEnigma()
            await self.active_connections[user_id].send_json({
                "type": "sekhmet_selection",
                "divinities": [
                    {"id": d.id, "name": d.name}
                    for d in enigma.divinities
                ]
            })

    async def unlock_sekhmet_enigma(self):
        """Débloquer l'énigme Sekhmet pour les deux utilisateurs"""
        self.user1_hints_unlocked = True

        # Envoyer aux deux utilisateurs
        if "user1" in self.active_connections:
            await self.send_sekhmet_schemas("user1")

        if "user2" in self.active_connections:
            await self.send_user2_interface("user2")

    async def validate_sekhmet(self, user_id: str, hieroglyph_code: str):
        """Valide la réponse de l'énigme Sekhmet (uniquement User 2)"""

        if user_id != "user2":
            return {
                "success": False,
                "message": "Seul l'Utilisateur 2 peut valider cette énigme"
            }

        if self.sekhmet_solved:
            return {
                "success": False,
                "message": "Énigme déjà résolue"
            }

        # Séquence correcte pour SEKHMET basée sur l'image
        correct_code = "h3-h6-h5-h10"

        if hieroglyph_code == correct_code:
            self.sekhmet_solved = True

            success_data = {
                "success": True,
                "message": "🎉 Bravo ! Vous avez correctement reproduit le nom de SEKHMET en hiéroglyphes !",
                "info": "Sekhmet était la déesse guerrière égyptienne, fille du dieu soleil Rê. Redoutable et puissante, elle protégeait les pharaons."
            }

            # Notifier les deux utilisateurs
            for uid in ["user1", "user2"]:
                if uid in self.active_connections:
                    await self.active_connections[uid].send_json({
                        "type": "sekhmet_result",
                        "result": success_data
                    })

            return success_data
        else:
            return {
                "success": False,
                "message": "❌ Ce n'est pas la bonne séquence de hiéroglyphes. Vérifiez avec User 1 !",
                "attempted_code": hieroglyph_code
            }

    async def handle_validate_sekhmet(data: dict, ws_id: str):
        hieroglyph_code = data.get('hieroglyph_code', '')

        # Séquence correcte pour SEKHMET basée sur l'image
        # h3-h6-h5-h10
        correct_code = "h3-h6-h5-h10"

        if hieroglyph_code == correct_code:
            result = {
                "success": True,
                "message": "🎉 Bravo ! Vous avez correctement reproduit le nom de SEKHMET en hiéroglyphes !"
            }
        else:
            result = {
                "success": False,
                "message": f"❌ La séquence n'est pas correcte. Vérifiez avec User 1 et réessayez !"
            }

        await broadcast_to_team('team1', {
            'type': 'sekhmet_result',
            'result': result
        })

    async def validate_chardin(self, user_id: str, code: str):
        """Valide le code Chardin"""
        correct_code = "3563"

        if user_id != "user1":
            return {
                "success": False,
                "message": "Cette énigme est réservée à l'Utilisateur 1"
            }

        if "chardin" in self.solved_users:
            return {
                "success": False,
                "message": "Vous avez déjà résolu cette énigme"
            }

        if code == correct_code:
            self.solved_users.add("chardin")
            # Débloquer l'énigme Sekhmet
            await self.unlock_sekhmet_enigma()

            return {
                "success": True,
                "message": "Bravo ! Le code est correct ! 🎉",
                "next_enigma": "sekhmet"
            }
        else:
            return {
                "success": False,
                "message": "Code incorrect. Observez plus attentivement les tableaux."
            }

    async def broadcast_button_states(self):
        for user_id in self.active_connections:
            await self.send_button_state(user_id)

    async def broadcast_message(self, message: Dict):
        for user_id in self.active_connections:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_json({
                    "type": "chat_message",
                    "message": message
                })

    async def handle_button_click(self, user_id: str):
        other_user = "user1" if user_id == "user2" else "user2"
        self.button_states[other_user] = True
        self.button_states[user_id] = False
        await self.broadcast_button_states()

    async def handle_chat_message(self, user_id: str, text: str):
        message = {
            "user_id": user_id,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        self.chat_history.append(message)
        if len(self.chat_history) > 100:
            self.chat_history = self.chat_history[-100:]
        await self.broadcast_message(message)


manager = GameManager()


@app.websocket("/ws/{team_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: str, player_id: str):
    await manager.connect(websocket, player_id)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "validate_chardin":
                result = await manager.validate_chardin(
                    player_id,
                    data.get("code", "")
                )
                await websocket.send_json({
                    "type": "chardin_result",
                    "result": result
                })

            elif data.get("action") == "validate_sekhmet":
                hieroglyph_code = data.get("hieroglyph_code")
                result = await manager.validate_sekhmet(player_id, hieroglyph_code)
                await websocket.send_json({
                    "type": "sekhmet_result",
                    "result": result
                })

            elif data.get("action") == "button_click":
                await manager.handle_button_click(player_id)

            elif data.get("action") == "send_message":
                message_text = data.get("message", "")
                if message_text.strip():
                    await manager.handle_chat_message(player_id, message_text)

    except WebSocketDisconnect:
        manager.disconnect(player_id)
        print(f"User {player_id} disconnected")


@app.get("/")
def read_root():
    return {"message": "Escape Game Musée - API"}