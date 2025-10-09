# 🎮 Escape Game Musée - Guide d'Intégration Complet

## ✅ Récapitulatif de l'intégration Frontend-Backend

Votre application est maintenant **complètement intégrée** !

### 📦 Ce qui a été fait

#### Backend (Python/FastAPI/MariaDB)
✅ Base de données MariaDB persistante
✅ API WebSocket temps réel
✅ Système de score et progression
✅ Multi-équipes supporté
✅ Chat en temps réel
✅ Documentation complète

#### Frontend (Vue.js 3)
✅ **Nouveau :** Sélection d'équipe dynamique
✅ **Nouveau :** Services WebSocket et API
✅ **Nouveau :** Panel de progression temps réel
✅ **Modifié :** User1 et User2 adaptés pour multi-équipes
✅ **Modifié :** Router avec protection des routes
✅ Interface responsive (mobile/tablette/desktop)
✅ Chat intégré
✅ Système de boutons collaboratif

---

## 🚀 Lancement Rapide (2 terminaux)

### Terminal 1 : Backend

```bash
cd backoffice

# Installation (première fois)
pip install -r requirements.txt
python setup_mariadb.py full

# Lancer le serveur
fastapi dev main.py
```

**Backend accessible sur :** http://localhost:8000

### Terminal 2 : Frontend

```bash
cd frontoffice

# Installation (première fois)
npm install

# Lancer le frontend
npm run dev
```

**Frontend accessible sur :** http://localhost:5173

---

## 🔄 Flux Complet de l'Application

```
1. UTILISATEUR
   └─> Accède à http://localhost:5173

2. SÉLECTION D'ÉQUIPE
   └─> Entre "team1" (ID d'équipe)
   └─> Entre "Les Détectives" (nom optionnel)
   └─> Sauvegardé dans localStorage
   
3. CHOIX DU JOUEUR
   └─> Clique sur "Utilisateur 1" ou "Utilisateur 2"
   
4. CONNEXION WEBSOCKET
   └─> ws://localhost:8000/ws/team1/user1
   └─> Backend : Connexion MariaDB
   └─> Backend : Création/récupération de l'équipe
   └─> Backend : Envoi de l'état initial
   
5. INTERFACE INTERACTIVE
   └─> User1 : Résout l'énigme Chardin
   └─> Validation : Backend vérifie le code
   └─> Succès : +100 points → MariaDB
   └─> Progression diffusée aux deux users
   
6. COLLABORATION
   └─> Chat : Messages stockés en BDD
   └─> Boutons : États synchronisés
   └─> Progression : Mise à jour temps réel
```

---

## 📡 Communication Frontend ↔ Backend

### Connexion WebSocket

```javascript
// Frontend
const teamId = localStorage.getItem('teamId')  // "team1"
const userId = 'user1'  // ou 'user2'
const ws = new WebSocket(`ws://localhost:8000/ws/${teamId}/${userId}`)
```

```python
# Backend
@app.websocket("/ws/{team_id}/{player_id}")
async def websocket_endpoint(websocket, team_id, player_id, db):
    await manager.connect(websocket, team_id, player_id, db)
```

### Messages échangés

#### Frontend → Backend

```javascript
// Valider une énigme
ws.send(JSON.stringify({
  action: "validate_chardin",
  code: "3563"
}))

// Cliquer sur le bouton
ws.send(JSON.stringify({
  action: "button_click"
}))

// Envoyer un message
ws.send(JSON.stringify({
  action: "send_message",
  message: "Trouvé !"
}))
```

#### Backend → Frontend

```javascript
// État du bouton
{
  type: "button_state",
  enabled: true
}

// Historique chat
{
  type: "chat_history",
  messages: [...]
}

// Nouveau message
{
  type: "chat_message",
  message: {...}
}

// Progression
{
  type: "progress",
  data: {
    team_score: 100,
    puzzles: [...]
  }
}

// Résultat validation
{
  type: "chardin_result",
  result: {
    success: true,
    message: "Bravo!",
    points: 100
  }
}
```

---

## 🗄️ Base de Données MariaDB

### Tables utilisées

```sql
-- Équipes
teams (id, name, score, created_at, finished_at, total_time)

-- Joueurs
players (id, team_id, name, individual_score, is_active, last_activity)

-- Progression des énigmes
progress (id, team_id, player_id, puzzle_name, is_solved, solved_at, attempts, hints_used, points_earned)

-- Messages de chat
chat_messages (id, team_id, player_id, message, timestamp, is_system)

-- États des boutons
button_states (id, team_id, player_id, is_enabled, updated_at)

-- Sessions de jeu
game_sessions (id, team_id, started_at, ended_at, status, final_score)
```

### Exemple de données

```sql
-- Équipe
INSERT INTO teams (id, name, score) VALUES ('team1', 'Les Détectives', 100);

-- Joueurs
INSERT INTO players (id, team_id, name) VALUES ('user1', 'team1', 'Joueur 1');
INSERT INTO players (id, team_id, name) VALUES ('user2', 'team1', 'Joueur 2');

-- Progression
INSERT INTO progress (team_id, player_id, puzzle_name, is_solved, points_earned)
VALUES ('team1', 'user1', 'chardin', true, 100);

-- Messages
INSERT INTO chat_messages (team_id, player_id, message)
VALUES ('team1', 'user1', 'J\'ai trouvé le code !');
```

---

## 📊 Architecture Complète

```
┌─────────────────────────────────────────────────────────────┐
│                      UTILISATEUR                            │
│                    (Navigateur Web)                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (Vue.js 3)                        │
│                  http://localhost:5173                      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │TeamSelection │  │   User1.vue  │  │  User2.vue  │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │            Components                            │      │
│  │  • ChatBox       • EnigmeChardin                 │      │
│  │  • ProgressPanel • SuccessPopup                  │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │            Services                              │      │
│  │  • websocket.js  • api.js                        │      │
│  └──────────────────────────────────────────────────┘      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ WebSocket + HTTP REST
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                BACKEND (Python/FastAPI)                     │
│                http://localhost:8000                        │
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │             main.py                              │      │
│  │  • GameManager                                   │      │
│  │  • WebSocket endpoints                           │      │
│  │  • HTTP endpoints                                │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │            Modèles & Config                      │      │
│  │  • models.py      • database.py                  │      │
│  │  • config.py      • puzzles_config.py            │      │
│  └──────────────────────────────────────────────────┘      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   MARIADB DATABASE                          │
│                   localhost:3306                            │
│                   escape_game_db                            │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐   │
│  │  teams   │ │ players  │ │ progress │ │chat_messages│   │
│  └──────────┘ └──────────┘ └──────────┘ └─────────────┘   │
│                                                             │
│  ┌──────────────┐ ┌────────────────┐                       │
│  │button_states │ │ game_sessions  │                       │
│  └──────────────┘ └────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Scénarios d'Utilisation

### Scénario 1 : Une équipe joue

**Étape 1 :** Team1 accède à l'application
```
→ http://localhost:5173
→ Entre "team1" comme ID
→ Clique sur "Utilisateur 1"
```

**Étape 2 :** User1 résout l'énigme
```
→ Entre le code "3563"
→ Backend valide → +100 points
→ MariaDB : UPDATE teams SET score = 100
→ MariaDB : INSERT INTO progress (puzzle="chardin", is_solved=true)
→ Popup de succès affiché
```

**Étape 3 :** User2 se connecte (autre appareil/navigateur)
```
→ Entre "team1" (même équipe)
→ Clique sur "Utilisateur 2"
→ Voit la progression de team1 (100 points)
→ Peut chatter avec User1
```

**Étape 4 :** Collaboration via boutons
```
→ User2 clique sur le bouton
→ Backend : button_states updated
→ User1 reçoit l'événement
→ Le bouton de User1 s'active
```

### Scénario 2 : Plusieurs équipes

**Team Alpha :**
```
→ ID: "team_alpha"
→ User1 et User2 se connectent
→ Score indépendant
→ Chat isolé
```

**Team Beta :**
```
→ ID: "team_beta"
→ User1 et User2 se connectent
→ Score indépendant
→ Chat isolé
```

**Isolation complète** :
- Pas de mélange des messages
- Scores séparés
- Progressions indépendantes

---

## 🔧 Configuration Complète

### Backend (`backoffice/config.py`)

```python
MARIADB_CONFIG = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "port": "3306",
    "database": "escape_game_db"
}
```

### Frontend (`frontoffice/.env`)

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## 🐛 Debug & Troubleshooting

### Vérifier la connexion complète

#### 1. Backend fonctionne ?
```bash
curl http://localhost:8000
# Devrait retourner : {"message":"Escape Game Musée - API avec Base de Données"}
```

#### 2. MariaDB accessible ?
```bash
cd backoffice
python test_installation.py
# Devrait afficher : Score: 4/4
```

#### 3. Frontend accessible ?
```bash
curl http://localhost:5173
# Devrait retourner du HTML
```

#### 4. WebSocket fonctionne ?
```
Ouvrir http://localhost:5173
F12 → Console
Vérifier les messages :
✅ Connecté en tant que user1 équipe team1
📨 Message reçu: button_state
```

### Problèmes courants

#### ❌ "Déconnecté" dans le frontend

**Causes :**
1. Backend non démarré
2. MariaDB non démarré
3. Mauvaise configuration `.env`

**Solutions :**
```bash
# 1. Vérifier MariaDB
python backoffice/test_installation.py

# 2. Vérifier backend
cd backoffice
fastapi dev main.py

# 3. Vérifier .env
cat frontoffice/.env
```

#### ❌ Progression ne s'affiche pas

**Cause :** Backend ne diffuse pas le type `progress`

**Solution :** Vérifier que `broadcast_progress` est appelé après validation

#### ❌ Chat ne fonctionne pas

**Diagnostic :**
```
F12 → Network → WS → Messages
Vérifier que les messages sont bien envoyés/reçus
```

---

## 📈 Monitoring & Stats

### Voir les stats d'une équipe

**API REST :**
```bash
curl http://localhost:8000/teams/team1/stats
```

**Réponse :**
```json
{
  "team_id": "team1",
  "score": 100,
  "puzzles_solved": 1,
  "total_puzzles": 1,
  "progress": [
    {
      "puzzle": "chardin",
      "solved": true,
      "attempts": 1,
      "points": 100
    }
  ]
}
```

### Voir les stats dans la BDD

```bash
cd backoffice
python db_utils.py stats
```

**Ou via SQL :**
```sql
mysql -u root escape_game_db

SELECT * FROM teams;
SELECT * FROM progress;
SELECT * FROM chat_messages;
```

---

## 🎨 Personnalisation

### Ajouter une nouvelle énigme

#### 1. Backend (`backoffice/puzzles_config.py`)

```python
"enigme_nouvelle": {
    "name": "L'Énigme Nouvelle",
    "correct_code": "ABC123",
    "points": 150,
    "restricted_to": None,
    "hints": ["Indice 1", "Indice 2"]
}
```

#### 2. Backend (`backoffice/main.py`)

```python
elif data.get("action") == "validate_nouvelle":
    result = await manager.validate_puzzle(
        team_id, player_id, "enigme_nouvelle",
        data.get("code", ""), db
    )
```

#### 3. Frontend (créer `EnigmeNouvelle.vue`)

```vue
<script setup>
const emit = defineEmits(['submit-answer'])

function submitCode(code) {
  emit('submit-answer', { code })
}
</script>

<template>
  <div class="enigma-container">
    <!-- Votre énigme -->
  </div>
</template>
```

#### 4. Frontend (`User1.vue`)

```vue
<EnigmeNouvelle
  v-if="!nouvelleResolved"
  @submit-answer="handleNouvelleSubmit"
/>
```

---

## ✅ Checklist Production

### Backend
- [ ] MariaDB installé et démarré
- [ ] Base de données créée
- [ ] Tables créées
- [ ] Configuration `config.py` correcte
- [ ] Tests passent (`python test_installation.py`)
- [ ] Serveur démarre (`fastapi dev main.py`)
- [ ] Port 8000 accessible

### Frontend
- [ ] Dépendances installées (`npm install`)
- [ ] `.env` configuré avec les bonnes URLs
- [ ] Build réussi (`npm run build`)
- [ ] Preview fonctionne (`npm run preview`)
- [ ] WebSocket se connecte
- [ ] Chat fonctionne
- [ ] Boutons fonctionnent
- [ ] Progression s'affiche

### Intégration
- [ ] Backend → MariaDB ✅
- [ ] Frontend → Backend ✅
- [ ] WebSocket temps réel ✅
- [ ] Chat synchronisé ✅
- [ ] Progression temps réel ✅
- [ ] Multi-équipes ✅

---

## 🎉 L'application est complète !

Votre système d'escape game est maintenant **totalement fonctionnel** avec :

✅ **Backend Python/FastAPI** connecté à **MariaDB**
✅ **Frontend Vue.js 3** avec WebSocket temps réel
✅ **Multi-équipes** avec isolation complète
✅ **Système de progression** persistant
✅ **Chat en temps réel** sauvegardé
✅ **Interface responsive** mobile/tablette/desktop

### Lancer l'application

```bash
# Terminal 1 : Backend
cd backoffice
fastapi dev main.py

# Terminal 2 : Frontend
cd frontoffice
npm run dev

# Accéder à l'application
http://localhost:5173
```

**Bon workshop EPSI 2025-2026 ! 🚀🎮**

---

**Questions ?**
- Backend : Consultez `backoffice/README.md`
- Frontend : Consultez `frontoffice/README.md`
- Intégration : Ce fichier !
