from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GameManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.solved_users = set()
        self.button_states: Dict[str, bool] = {
            "user1": False,
            "user2": True  # User2 commence avec le bouton activé
        }
        self.chat_history: List[Dict] = []

    async def connect(self, websocket: WebSocket, user_id: str):
        """Connexion d'un utilisateur"""
        await websocket.accept()
        self.active_connections[user_id] = websocket

        # Envoyer l'état initial
        await self.send_button_state(user_id)
        await self.send_chat_history(user_id)

    def disconnect(self, user_id: str):
        """Déconnexion d'un utilisateur"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_button_state(self, user_id: str):
        """Envoie l'état du bouton à un utilisateur"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "button_state",
                "enabled": self.button_states.get(user_id, False)
            })

    async def send_chat_history(self, user_id: str):
        """Envoie l'historique du chat"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "chat_history",
                "messages": self.chat_history
            })

    async def broadcast_button_states(self):
        """Diffuse l'état des boutons à tous les utilisateurs"""
        for user_id in self.active_connections:
            await self.send_button_state(user_id)

    async def broadcast_message(self, message: Dict):
        """Diffuse un message de chat à tous"""
        for user_id in self.active_connections:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_json({
                    "type": "chat_message",
                    "message": message
                })

    async def validate_chardin(self, user_id: str, code: str):
        """Valide le code Chardin"""
        correct_code = "3563"

        if user_id != "user1":
            return {
                "success": False,
                "message": "Cette énigme est réservée à l'Utilisateur 1"
            }

        if user_id in self.solved_users:
            return {
                "success": False,
                "message": "Vous avez déjà résolu cette énigme"
            }

        if code == correct_code:
            self.solved_users.add(user_id)
            return {
                "success": True,
                "message": "Bravo ! Le code est correct ! 🎉"
            }
        else:
            return {
                "success": False,
                "message": "Code incorrect. Observez plus attentivement les tableaux."
            }

    async def handle_button_click(self, user_id: str):
        """Gère le clic sur le bouton"""
        other_user = "user1" if user_id == "user2" else "user2"

        # Inverser les états
        self.button_states[other_user] = True
        self.button_states[user_id] = False

        # Diffuser les nouveaux états
        await self.broadcast_button_states()

    async def handle_chat_message(self, user_id: str, text: str):
        """Gère l'envoi d'un message de chat"""
        message = {
            "user_id": user_id,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }

        # Ajouter à l'historique
        self.chat_history.append(message)

        # Limiter l'historique à 100 messages
        if len(self.chat_history) > 100:
            self.chat_history = self.chat_history[-100:]

        # Diffuser le message
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