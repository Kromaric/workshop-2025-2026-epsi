from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# États partagés
button_unlocked = False

@app.get("/status")
def get_status():
    global button_unlocked
    return {
        "button_unlocked": button_unlocked
    }

@app.post("/unlock")
def unlock_button2():
    global button_unlocked
    button_unlocked = True
    return {"message": "Button2 débloqué"}