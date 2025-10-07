from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste des connexions WebSocket actives
websockets = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # on garde la connexion ouverte
    except:
        websockets.remove(websocket)

# Unlock le bouton 2 avec un event websocket
@app.post("/unlock")
async def unlock_button2():
    for ws in websockets:
        await ws.send_text("unlocked")
    return {"message": "Button2 débloqué"}