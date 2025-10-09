# 🎮 Escape Game Musée - Workshop EPSI 2025-2026

## 📋 Vue d'ensemble

Application web complète d'escape game au musée avec **backend Python/FastAPI/MariaDB** et **frontend Vue.js 3**.

### 🎯 Fonctionnalités

✅ **Multi-équipes** - Plusieurs équipes peuvent jouer simultanément
✅ **WebSocket temps réel** - Communication instantanée
✅ **Base de données persistante** - MariaDB avec scores et progression
✅ **Chat intégré** - Communication entre les joueurs
✅ **Système collaboratif** - Boutons d'interaction entre users
✅ **Énigmes configurables** - Facile d'ajouter de nouvelles énigmes
✅ **Interface responsive** - Mobile, tablette, desktop
✅ **Documentation complète** - Guides détaillés

---

## 🚀 Démarrage Rapide (5 minutes)

### Prérequis

- **Python 3.x**
- **Node.js 20+**
- **MariaDB** (démarré sur port 3306)

### Installation

#### 1. Backend

```bash
cd backoffice

# Installer les dépendances
pip install -r requirements.txt

# Configurer MariaDB
python setup_mariadb.py full

# Tester l'installation
python test_installation.py

# Lancer le serveur
fastapi dev main.py
```

**Backend accessible sur :** http://localhost:8000

#### 2. Frontend

```bash
cd frontoffice

# Installer les dépendances
npm install

# Lancer le frontend
npm run dev
```

**Frontend accessible sur :** http://localhost:5173

---

## 📂 Structure du Projet

```
workshop-2025-2026-epsi/
│
├── backoffice/              # Backend Python/FastAPI
│   ├── main.py              # Application principale
│   ├── database.py          # Connexion MariaDB
│   ├── models.py            # Modèles SQLAlchemy
│   ├── config.py            # Configuration BDD
│   ├── setup_mariadb.py     # Setup automatique
│   ├── db_utils.py          # Utilitaires BDD
│   ├── puzzles_config.py    # Configuration énigmes
│   ├── requirements.txt     # Dépendances Python
│   └── *.md                 # Documentation
│
├── frontoffice/             # Frontend Vue.js 3
│   ├── src/
│   │   ├── views/           # Pages
│   │   ├── components/      # Composants
│   │   ├── services/        # Services WebSocket/API
│   │   └── router/          # Routage
│   ├── package.json
│   ├── .env                 # Configuration
│   └── README.md
│
└── INTEGRATION.md           # Guide d'intégration complet
```

---

## 🎮 Comment jouer ?

### 1. Créer une équipe

- Accéder à http://localhost:5173
- Entrer un **ID d'équipe** (ex: `team1`, `equipe-alpha`)
- Optionnellement un **nom d'équipe**

### 2. Choisir son rôle

- **Utilisateur 1** : Résout les énigmes (ex: énigme Chardin)
- **Utilisateur 2** : Collabore via le système de boutons

### 3. Jouer !

- **User1** résout l'énigme du code Chardin (code: `3563`)
- Les deux joueurs communiquent via le **chat**
- Ils collaborent avec le **système de boutons**
- La **progression** est affichée en temps réel
- Les **scores** sont sauvegardés dans MariaDB

---

## 🔧 Configuration

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

## 📡 Architecture

```
Frontend (Vue.js 3)
      ↕ WebSocket + HTTP
Backend (FastAPI)
      ↕ SQLAlchemy ORM
MariaDB Database
```

### Communication temps réel

- **WebSocket** : Chat, boutons, progression
- **HTTP REST** : Statistiques d'équipe

---

## 🗄️ Base de Données

### Tables principales

- **teams** : Équipes et scores
- **players** : Joueurs
- **progress** : Progression des énigmes
- **chat_messages** : Historique des messages
- **button_states** : États des boutons
- **game_sessions** : Sessions de jeu

### Voir les stats

```bash
cd backoffice
python db_utils.py stats
```

---

## 📚 Documentation

### Guides disponibles

1. **[INTEGRATION.md](INTEGRATION.md)** 🔗
   - Guide d'intégration complet
   - Architecture détaillée
   - Scénarios d'utilisation

2. **[backoffice/README.md](backoffice/README.md)** 🔗
   - Documentation backend
   - Configuration MariaDB
   - Ajouter des énigmes

3. **[backoffice/QUICKSTART_MARIADB.md](backoffice/QUICKSTART_MARIADB.md)** ⚡
   - Démarrage rapide backend
   - Commandes essentielles
   - Troubleshooting

4. **[backoffice/MIGRATION_MARIADB.md](backoffice/MIGRATION_MARIADB.md)** 🔄
   - Guide de migration complet
   - Configuration avancée

5. **[frontoffice/README.md](frontoffice/README.md)** 🎨
   - Documentation frontend
   - Composants Vue.js
   - Personnalisation

---

## 🎯 Fonctionnalités Clés

### Backend

- ✅ Base de données MariaDB persistante
- ✅ WebSocket pour communication temps réel
- ✅ Gestion multi-équipes
- ✅ Système de score et progression
- ✅ Chat avec historique
- ✅ États des boutons synchronisés
- ✅ API REST pour statistiques

### Frontend

- ✅ Sélection d'équipe dynamique
- ✅ Interface User1 et User2
- ✅ Énigme Chardin interactive
- ✅ Chat en temps réel
- ✅ Panel de progression
- ✅ Design responsive
- ✅ Animations et effets

---

## 🛠️ Commandes Utiles

### Backend

```bash
# Configuration MariaDB
python setup_mariadb.py full

# Statistiques
python db_utils.py stats

# Réinitialiser
python db_utils.py reset

# Lancer le serveur
fastapi dev main.py
```

### Frontend

```bash
# Installer
npm install

# Développement
npm run dev

# Build production
npm run build
```

---

## 🐛 Problèmes Courants

### ❌ MariaDB ne démarre pas

**Solution :**
- Windows (XAMPP) : Ouvrir le panneau → Start MySQL
- Linux : `sudo systemctl start mariadb`

### ❌ "Déconnecté" dans le frontend

**Vérifications :**
1. Backend démarré ?
2. MariaDB accessible ?
3. `.env` configuré ?

**Test rapide :**
```bash
curl http://localhost:8000
python backoffice/test_installation.py
```

### ❌ WebSocket ne se connecte pas

**Solution :**
- Vérifier que le backend tourne
- Vérifier `VITE_WS_URL` dans `.env`
- Ouvrir F12 → Console pour voir les erreurs

**Plus d'aide :** Consultez `INTEGRATION.md`

---

## 🎨 Ajouter une Énigme

### 1. Configuration (`backoffice/puzzles_config.py`)

```python
"ma_enigme": {
    "name": "Mon Énigme",
    "correct_code": "CODE123",
    "points": 150,
    "restricted_to": None,
    "hints": ["Indice 1"]
}
```

### 2. Handler Backend (`backoffice/main.py`)

```python
elif data.get("action") == "validate_ma_enigme":
    result = await manager.validate_puzzle(...)
```

### 3. Composant Frontend

Créer `frontoffice/src/components/EnigmaMaNouvelle.vue`

**Guide complet :** Consultez `backoffice/DATABASE_README.md`

---

## 📊 Monitoring

### Statistiques d'équipe

```bash
# Via CLI
python backoffice/db_utils.py stats

# Via API
curl http://localhost:8000/teams/team1/stats

# Via SQL
mysql -u root escape_game_db
SELECT * FROM teams;
```

---

## 🚀 Déploiement Production

### Backend

```bash
cd backoffice

# Configuration production
# Modifier config.py avec un utilisateur dédié

# Lancer avec Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend

```bash
cd frontoffice

# Build
npm run build

# Déployer le dossier dist/
# avec Nginx, Apache, ou autre serveur web
```

---

## ✅ Checklist avant de commencer

- [ ] Python 3.x installé
- [ ] Node.js 20+ installé
- [ ] MariaDB installé et démarré (port 3306)
- [ ] Backend : `pip install -r requirements.txt`
- [ ] Backend : `python setup_mariadb.py full`
- [ ] Backend : `python test_installation.py` → Score 4/4
- [ ] Frontend : `npm install`
- [ ] Frontend : `.env` configuré
- [ ] Backend lancé : `fastapi dev main.py`
- [ ] Frontend lancé : `npm run dev`
- [ ] http://localhost:5173 accessible
- [ ] WebSocket connecté ✅

---

## 🎓 Contexte

**Projet :** Workshop EPSI 2025-2026
**Sujet :** Escape Game au Musée
**Technologies :**
- Backend : Python, FastAPI, SQLAlchemy, MariaDB
- Frontend : Vue.js 3, Vite, WebSocket
- Design : CSS moderne avec animations

---

## 📞 Support

**Problème ?**
1. Consultez `INTEGRATION.md`
2. Vérifiez la documentation spécifique (backend/frontend)
3. Exécutez `python test_installation.py` (backend)
4. Vérifiez les logs dans la console (F12)

---

## 🎉 Prêt à jouer !

### Lancer l'application

```bash
# Terminal 1 : Backend
cd backoffice
fastapi dev main.py

# Terminal 2 : Frontend
cd frontoffice
npm run dev
```

**Accéder à l'application :** http://localhost:5173

**Bon workshop ! 🚀🎮**

---

**Version :** 2.0.0 - Intégration MariaDB
**Date :** Octobre 2025
**Auteurs :** Équipe Workshop EPSI
