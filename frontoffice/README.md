# 🎨 Escape Game Musée - Frontend

## 📋 Vue d'ensemble

Application **Vue.js 3** avec **Vite** pour l'interface utilisateur de l'escape game au musée.

### 🎯 Fonctionnalités

✅ **Sélection d'équipe** - Plusieurs équipes peuvent jouer simultanément
✅ **Deux utilisateurs** - User1 (résout les énigmes) et User2 (collaboration)
✅ **WebSocket temps réel** - Communication instantanée
✅ **Chat intégré** - Communication entre les joueurs
✅ **Progression en temps réel** - Score et énigmes résolues
✅ **Interface responsive** - Mobile, tablette, desktop
✅ **Design moderne** - Animations et effets visuels

---

## 🚀 Démarrage Rapide

### Installation

```bash
cd frontoffice

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.exemple .env
# Éditer .env si nécessaire

# Lancer en développement
npm run dev
```

**Application accessible sur :** http://localhost:5173

### Build pour production

```bash
npm run build
npm run preview
```

---

## ⚙️ Configuration

### Fichier `.env`

```env
# URL du backend API (HTTP)
VITE_API_URL=http://localhost:8000

# URL du backend WebSocket
VITE_WS_URL=ws://localhost:8000
```

**Pour un serveur distant :**
```env
VITE_API_URL=http://votre-serveur:8000
VITE_WS_URL=ws://votre-serveur:8000
```

---

## 📂 Structure du Projet

```
frontoffice/
├── src/
│   ├── assets/          # CSS et images
│   ├── components/      # Composants réutilisables
│   │   ├── ButtonInteraction.vue
│   │   ├── ChatBox.vue
│   │   ├── EnigmeChardin.vue
│   │   ├── ProgressPanel.vue ⭐ NOUVEAU
│   │   └── SuccessPopup.vue
│   │
│   ├── services/        # Services ⭐ NOUVEAU
│   │   ├── api.js       # Appels HTTP REST
│   │   └── websocket.js # Gestion WebSocket
│   │
│   ├── views/           # Pages
│   │   ├── TeamSelection.vue ⭐ NOUVEAU
│   │   ├── User1.vue    🔄 MODIFIÉ
│   │   └── User2.vue    🔄 MODIFIÉ
│   │
│   ├── router/
│   │   └── index.js     🔄 MODIFIÉ
│   │
│   ├── App.vue
│   └── main.js
│
├── .env                 ⭐ NOUVEAU
├── .env.exemple
├── package.json
└── vite.config.js
```

⭐ = Nouveau fichier
🔄 = Fichier modifié

---

## 🎮 Flux de l'Application

### 1. Sélection de l'équipe

**Page :** `TeamSelection.vue`

- L'utilisateur entre un **ID d'équipe** (ex: `team1`, `equipe-alpha`)
- Optionnellement un **nom d'équipe** (ex: "Les Détectives")
- L'ID est sauvegardé dans le `localStorage`
- Redirection vers la sélection de l'utilisateur

### 2. Choix du joueur

- **Utilisateur 1** → `/user1`
  - Peut résoudre l'énigme Chardin
  - Système de boutons après résolution
  - Chat et progression

- **Utilisateur 2** → `/user2`
  - Système de boutons
  - Chat et progression

### 3. Connexion WebSocket

```javascript
// Connexion automatique
ws://localhost:8000/ws/{teamId}/{userId}

// Exemple
ws://localhost:8000/ws/team1/user1
```

### 4. Messages WebSocket

#### Messages reçus :

```javascript
// État du bouton
{
  type: "button_state",
  enabled: true
}

// Historique du chat
{
  type: "chat_history",
  messages: [...]
}

// Nouveau message
{
  type: "chat_message",
  message: {
    user_id: "user1",
    text: "Bonjour!",
    timestamp: "2025-10-09T10:30:00"
  }
}

// Progression de l'équipe
{
  type: "progress",
  data: {
    team_score: 100,
    puzzles: [...]
  }
}

// Résultat de validation
{
  type: "chardin_result",
  result: {
    success: true,
    message: "Bravo!",
    points: 100
  }
}
```

#### Messages envoyés :

```javascript
// Valider une énigme
{
  action: "validate_chardin",
  code: "3563"
}

// Cliquer sur le bouton
{
  action: "button_click"
}

// Envoyer un message
{
  action: "send_message",
  message: "Bonjour!"
}
```

---

## 🎨 Composants Principaux

### `TeamSelection.vue` ⭐

Page d'accueil avec :
- Formulaire de saisie de l'équipe
- Sélection de l'utilisateur
- Sauvegarde dans le localStorage

### `User1.vue` 🔄

Interface de l'utilisateur 1 :
- **Avant résolution :** Énigme Chardin + Panel de progression
- **Après résolution :** Boutons + Chat + Panel de progression

### `User2.vue` 🔄

Interface de l'utilisateur 2 :
- Boutons d'interaction
- Chat
- Panel de progression

### `EnigmeChardin.vue`

Énigme du code Chardin :
- Input pour code à 4 chiffres
- Instructions visuelles
- Validation en temps réel
- Restriction à User1

### `ChatBox.vue`

Système de chat :
- Messages en temps réel
- Auto-scroll
- Différenciation User1/User2
- Horodatage

### `ProgressPanel.vue` ⭐

Panel de progression :
- Score total de l'équipe
- Nombre d'énigmes résolues
- Barre de progression
- Liste détaillée des énigmes
- Tentatives et points

### `SuccessPopup.vue`

Popup de succès :
- Animation
- Informations sur Chardin
- Bouton pour continuer

---

## 🔧 Services

### `services/websocket.js` ⭐

Service WebSocket réutilisable :

```javascript
import wsService from '@/services/websocket'

// Connexion
wsService.connect('team1', 'user1')

// Envoyer des messages
wsService.validateChardin('3563')
wsService.clickButton()
wsService.sendMessage('Bonjour!')

// S'abonner aux messages
const unsubscribe = wsService.onMessage((data) => {
  console.log('Message reçu:', data)
})

// Se désabonner
unsubscribe()

// Déconnexion
wsService.disconnect()
```

### `services/api.js` ⭐

Service API REST :

```javascript
import apiService from '@/services/api'

// Récupérer les stats d'une équipe
const stats = await apiService.getTeamStats('team1')

// Vérifier le backend
const status = await apiService.checkBackend()
```

---

## 🎯 Intégration Backend

### Vérifier la connexion

1. **Backend démarré** sur `localhost:8000`
2. **Frontend démarré** sur `localhost:5173`
3. **Tester la connexion :**
   - Ouvrir l'application
   - Entrer un ID d'équipe
   - Choisir User1 ou User2
   - Vérifier le statut "Connecté" en haut à droite

### Debug WebSocket

Ouvrir la console du navigateur (F12) :

```
✅ Connecté en tant que user1 équipe team1
📨 Message reçu: button_state
📨 Message reçu: chat_history
📨 Message reçu: progress
```

---

## 🔄 Workflow Multi-Équipes

### Scénario 1 : Une seule équipe

1. Team1 sélectionne `team1`
2. User1 se connecte : `/user1`
3. User2 se connecte : `/user2`
4. Ils collaborent via chat et boutons

### Scénario 2 : Plusieurs équipes

1. **Team1** :
   - Sélectionne `team1`
   - User1 et User2 se connectent

2. **Team2** (autre navigateur/appareil) :
   - Sélectionne `team2`
   - User1 et User2 se connectent

3. **Isolation complète** :
   - Chaque équipe a son propre espace
   - Scores et progressions indépendants
   - Messages de chat séparés

---

## 📱 Responsive Design

### Mobile (< 640px)
- Navigation simplifiée
- Grilles en colonne unique
- Textes adaptés

### Tablette (641px - 1024px)
- Grille 2 colonnes
- Espacement optimisé

### Desktop (> 1024px)
- Grille 3 colonnes
- Effets hover avancés
- Espacements larges

---

## 🎨 Personnalisation

### Couleurs

**User1 :** Bleu/violet (`#667eea`, `#764ba2`)
**User2 :** Rose/violet (`#f093fb`, `#f5576c`)

Modifier dans les fichiers Vue :
```css
.user1-button {
  background: linear-gradient(135deg, #667eea 0%, #4f46e5 100%);
}
```

### Ajouter une nouvelle énigme

1. **Créer le composant** : `EnigmeNouvelle.vue`
2. **Ajouter dans User1.vue** :
```vue
<EnigmeNouvelle
  :player-id="currentUserId"
  @submit-answer="handleNouvelle"
/>
```

3. **Handler** :
```javascript
function handleNouvelle(data) {
  websocket.send(JSON.stringify({
    action: 'validate_nouvelle',
    code: data.code
  }))
}
```

4. **Backend** : Ajouter le handler dans `main.py`

---

## 🐛 Problèmes Courants

### ❌ WebSocket ne se connecte pas

**Cause :** Backend non démarré

**Solution :**
```bash
cd backoffice
fastapi dev main.py
```

### ❌ "Déconnecté" affiché

**Causes possibles :**
1. Backend arrêté
2. Mauvaise URL dans `.env`
3. Problème de CORS

**Solutions :**
- Vérifier que le backend tourne
- Vérifier `VITE_WS_URL` dans `.env`
- Redémarrer frontend et backend

### ❌ Progression ne s'affiche pas

**Cause :** Backend ne renvoie pas le type `progress`

**Solution :** Vérifier que le backend envoie bien les messages de progression

### ❌ Chat ne fonctionne pas

**Vérifications :**
1. WebSocket connecté
2. Messages envoyés au bon format
3. Backend traite l'action `send_message`

---

## 📊 Métriques de Performance

### Temps de chargement
- First Paint : < 1s
- Interactive : < 2s

### Optimisations
- Code splitting automatique (Vite)
- Lazy loading des routes
- Minification en production

---

## 🔄 Mise à jour depuis l'ancienne version

### Changements principaux

1. **Nouveau :** Sélection d'équipe
2. **Nouveau :** Services WebSocket et API
3. **Nouveau :** Panel de progression
4. **Modifié :** User1 et User2 utilisent le teamId
5. **Modifié :** Router avec guards

### Migration

```bash
# Sauvegarder l'ancien code
cp -r src src.backup

# Copier les nouveaux fichiers
# (déjà fait si vous suivez ce guide)

# Réinstaller les dépendances
npm install

# Tester
npm run dev
```

---

## 🚀 Déploiement

### Build

```bash
npm run build
```

Fichiers générés dans `dist/`

### Serveur Web

**Nginx** :
```nginx
server {
    listen 80;
    server_name escape-game.example.com;
    root /var/www/escape-game/dist;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**Apache** :
```apache
<VirtualHost *:80>
    DocumentRoot /var/www/escape-game/dist
    
    <Directory /var/www/escape-game/dist>
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
</VirtualHost>
```

---

## 📚 Documentation

### Vue.js 3
https://vuejs.org/

### Vite
https://vitejs.dev/

### WebSocket API
https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

---

## ✅ Checklist avant production

- [ ] `.env` configuré avec les bonnes URLs
- [ ] Backend accessible depuis le frontend
- [ ] WebSocket fonctionne
- [ ] Chat fonctionne
- [ ] Boutons fonctionnent
- [ ] Progression s'affiche
- [ ] Testé sur mobile
- [ ] Testé sur tablette
- [ ] Testé sur desktop
- [ ] Build réussi (`npm run build`)

---

## 🎉 C'est prêt !

L'application frontend est maintenant complètement intégrée avec le backend MariaDB !

```bash
# Lancer le frontend
npm run dev

# Visitez
http://localhost:5173
```

**Bon workshop ! 🎨🚀**

---

**Version :** 2.0.0 - Intégration MariaDB
**Date :** Octobre 2025
**Projet :** Workshop EPSI - Escape Game Musée
