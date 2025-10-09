# 🏛️ Escape Game Musée

> Une expérience interactive pour rendre la visite des musées plus engageante grâce à des énigmes collaboratives en temps réel.

![Vue.js](https://img.shields.io/badge/Vue.js-3.4-4FC08D?logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)
![Responsive](https://img.shields.io/badge/Responsive-Mobile%20%7C%20Tablet%20%7C%20Desktop-blue)

---

## 🎯 Concept

**Escape Game Musée** est une application web collaborative qui transforme la visite d'un musée en une aventure ludique. Deux visiteurs explorent physiquement différentes zones du musée et doivent collaborer en temps réel pour résoudre des énigmes basées sur les œuvres exposées.

### Comment ça marche ?

1. **Deux joueurs** se promènent dans le musée avec leurs smartphones
2. **L'un résout des énigmes** basées sur les œuvres (ex: compter des éléments sur des tableaux)
3. **Ils communiquent** via un chat en temps réel
4. **Ils collaborent** grâce à un système de boutons interactifs
5. **Ils apprennent** en découvrant l'histoire des artistes

---

## ✨ Fonctionnalités

- 🎨 **Énigmes basées sur les œuvres** (ex: "Le Code des Natures Mortes" de Chardin)
- 💬 **Chat en temps réel** entre les deux joueurs
- 🔘 **Système d'interaction** : activation mutuelle des actions
- 📱 **100% Responsive** : mobile, tablette et desktop
- 📚 **Contenu culturel** : biographies et anecdotes sur les artistes
- ⚡ **Synchronisation instantanée** via WebSocket

---

## 🛠️ Technologies

### Frontend
- **Vue.js 3** - Framework JavaScript
- **Vue Router** - Navigation
- **Vite** - Build tool
- **WebSocket** - Communication temps réel

### Backend
- **FastAPI** - Framework web Python
- **Uvicorn** - Serveur ASGI
- **WebSocket** - Communication bidirectionnelle

---

## 📁 Structure du projet

```
escape-game-musee/
├── frontend/                     # Application Vue.js
│   ├── src/
│   │   ├── components/          # Composants réutilisables
│   │   │   ├── ChatBox.vue      # Chat en temps réel
│   │   │   ├── EnigmeChardin.vue # Énigme Chardin
│   │   │   └── SuccessPopup.vue  # Popup de succès
│   │   ├── views/               # Pages principales
│   │   │   ├── Home.vue         # Sélection utilisateur
│   │   │   ├── User1.vue        # Interface User 1
│   │   │   └── User2.vue        # Interface User 2
│   │   ├── router/
│   │   │   └── index.js         # Configuration des routes
│   │   └── main.js
│   └── package.json
│
└── backend/                      # API FastAPI
    ├── main.py                   # Serveur principal
    └── requirements.txt          # Dépendances Python
```

---

## 🚀 Installation

### Prérequis

- **Node.js** ≥ 18.0
- **Python** ≥ 3.10
- **npm**
- **pip**

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/escape-game-musee.git
cd escape-game-musee
```

### 2. Installation du Frontend

```bash
cd frontend
npm install
```

### 3. Installation du Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## 💻 Utilisation

### Lancer l'application en local

#### Terminal 1 : Backend

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

➡️ Le serveur démarre sur `http://localhost:8000`

#### Terminal 2 : Frontend

```bash
cd frontend
npm run dev
```

➡️ L'application démarre sur `http://localhost:5173`

### Tester avec 2 utilisateurs

#### Sur le même appareil
1. Ouvrez `http://localhost:5173` dans le navigateur 1
2. Cliquez sur **"Utilisateur 1"**
3. Ouvrez `http://localhost:5173` dans un autre onglet/navigateur
4. Cliquez sur **"Utilisateur 2"**

#### Sur 2 appareils (même réseau local)
1. Trouvez votre IP locale : `ipconfig` (Windows) ou `ifconfig` (Mac/Linux)
2. Sur l'appareil 1 : ouvrez `http://VOTRE_IP:5173` → **"Utilisateur 1"**
3. Sur l'appareil 2 : ouvrez `http://VOTRE_IP:5173` → **"Utilisateur 2"**

**Exemple :** Si votre IP est `192.168.1.100`, ouvrez `http://192.168.1.100:5173`

---

## 🎮 Exemple d'énigme

### "Le Code des Natures Mortes" - Jean Siméon Chardin

**Objectif :** User 1 doit trouver un code à 4 chiffres en observant 4 tableaux de Chardin.

**Comment jouer :**
1. User 1 observe les 4 natures mortes exposées
2. Il compte :
   - Les **pêches** sur le 1er tableau → **3**
   - Les **noix** sur le 2ème tableau → **2**
   - Les **œufs** sur le 3ème tableau → **6**
   - Les **poires** sur le 4ème tableau → **4**
3. Il entre le code **3264** dans l'application
4. Un popup apparaît avec une biographie de Chardin
5. Il peut ensuite interagir avec User 2 via le chat et les boutons

**Tableaux utilisés :**
- [Corbeille de pêches](https://collections.louvre.fr/ark:/53355/cl010059177)
- [Panier de raisins avec noix](https://collections.louvre.fr/ark:/53355/cl010059558)
- [Nature morte aux œufs](https://collections.louvre.fr/ark:/53355/cl010064801)
- [Panier de prunes avec poires](https://collections.louvre.fr/ark:/53355/cl010059538)

---

## 🔧 Configuration

### Variables d'environnement

#### Frontend (`frontend/.env`)

```env
VITE_API_URL=localhost
VITE_WS_URL=ws://localhost:8000
```

Pour un test sur le réseau local, remplacez par votre IP :
```env
VITE_API_URL=192.168.1.100
VITE_WS_URL=ws://192.168.1.100:8000
```

---

## 🎨 Architecture

```
┌──────────────┐                              ┌──────────────┐
│   User 1     │                              │   User 2     │
│  (Mobile)    │◄────── WebSocket ──────────►│  (Mobile)    │
│              │                              │              │
│  - Énigmes   │                              │  - Boutons   │
│  - Boutons   │         FastAPI              │  - Chat      │
│  - Chat      │       (Backend)              │              │
└──────────────┘                              └──────────────┘
       │                                             │
       └──────────────────┬─────────────────────────┘
                          │
                    Communication
                    temps réel
```

**Flow de communication :**
1. User 1 résout une énigme → Backend valide
2. Backend envoie un message à User 1 → Popup de succès
3. User 2 clique sur un bouton → Backend notifie User 1
4. User 1 envoie un message → Backend le transmet à User 2
5. Tout est synchronisé en temps réel ! ⚡

---

## 🤝 Contribution

Les contributions sont les bienvenues ! 

### Comment contribuer

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/ma-feature`)
3. Commitez vos changements (`git commit -m 'feat: ajout nouvelle énigme'`)
4. Push vers la branche (`git push origin feature/ma-feature`)
5. Ouvrez une Pull Request

### Conventions de commit

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactorisation
- `test:` Tests

---

## 📋 Roadmap

### ✅ Version actuelle (1.0)
- Énigme Chardin avec validation de code
- Chat en temps réel
- Système de boutons interactifs
- Design responsive

### 🔜 Prochaines étapes
- Scanner QR codes pour débloquer des indices
- Timer partagé avec compte à rebours
- Nouvelles énigmes (Van Gogh, Monet, etc.)
- Carte interactive du musée
- Système de hints/indices

### 💡 Idées futures
- Mode multijoueur (4+ joueurs)
- Système de scores et leaderboard
- Interface admin pour créer des énigmes
- Support multi-musées
- Mode hors-ligne (PWA)

---

## 👥 Auteurs

- **KOUADIO Romaric**
- **LANDAIS Alexis**
- **MERCERON Romain**
- **PEROLS Mathys**

