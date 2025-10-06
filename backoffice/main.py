# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de votre app Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gestion des connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.button_states: Dict[str, bool] = {}  # user_id: is_enabled

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        # Par défaut, user1 a le bouton disabled, user2 enabled
        self.button_states[user_id] = user_id == "user2"

        # Envoyer l'état initial à l'utilisateur
        await self.send_state(user_id)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.button_states:
            del self.button_states[user_id]

    async def send_state(self, user_id: str):
        """Envoie l'état du bouton à un utilisateur spécifique"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "button_state",
                "enabled": self.button_states.get(user_id, False)
            })

    async def broadcast_states(self):
        """Envoie l'état à tous les utilisateurs connectés"""
        for user_id in self.active_connections:
            await self.send_state(user_id)

    async def handle_button_click(self, user_id: str):
        """Gère le clic sur le bouton"""
        # Trouver l'autre utilisateur
        other_user = "user1" if user_id == "user2" else "user2"

        # Activer le bouton de l'autre utilisateur
        if other_user in self.button_states:
            self.button_states[other_user] = True
            self.button_states[user_id] = False

            # Envoyer les nouveaux états
            await self.broadcast_states()


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "button_click":
                await manager.handle_button_click(user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected")


@app.get("/")
def read_root():
    return {"message": "FastAPI WebSocket Server"}