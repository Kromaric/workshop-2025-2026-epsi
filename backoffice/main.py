from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from datetime import datetime
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.button_states: Dict[str, bool] = {}
        self.chat_history: List[Dict] = []  # Historique des messages

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.button_states[user_id] = user_id == "user2"

        # Envoyer l'état initial
        await self.send_state(user_id)

        # Envoyer l'historique des messages
        await self.send_chat_history(user_id)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.button_states:
            del self.button_states[user_id]

    async def send_state(self, user_id: str):
        """Envoie l'état du bouton à un utilisateur"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "button_state",
                "enabled": self.button_states.get(user_id, False)
            })

    async def send_chat_history(self, user_id: str):
        """Envoie l'historique du chat à un utilisateur"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "chat_history",
                "messages": self.chat_history
            })

    async def broadcast_states(self):
        """Envoie l'état à tous les utilisateurs"""
        for user_id in self.active_connections:
            await self.send_state(user_id)

    async def broadcast_message(self, message: Dict):
        """Diffuse un message à tous les utilisateurs"""
        for user_id in self.active_connections:
            await self.active_connections[user_id].send_json({
                "type": "chat_message",
                "message": message
            })

    async def handle_button_click(self, user_id: str):
        """Gère le clic sur le bouton"""
        other_user = "user1" if user_id == "user2" else "user2"

        if other_user in self.button_states:
            self.button_states[other_user] = True
            self.button_states[user_id] = False
            await self.broadcast_states()

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


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "button_click":
                await manager.handle_button_click(user_id)

            elif data.get("action") == "send_message":
                message_text = data.get("message", "")
                if message_text.strip():
                    await manager.handle_chat_message(user_id, message_text)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected")


@app.get("/")
def read_root():
    return {"message": "FastAPI WebSocket Server with Chat"}