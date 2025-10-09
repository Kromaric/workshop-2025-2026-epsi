# 🗄️ Structure de la Base de Données - Escape Game Musée

## 📋 Vue d'ensemble

La base de données utilise **SQLite** et contient 6 tables principales pour gérer les équipes, joueurs, progression, chat, états des boutons et sessions de jeu.

---

## 📊 Structure des Tables

### 1️⃣ Table `teams` - Équipes

Stocke les informations sur chaque équipe.

```sql
CREATE TABLE teams (
    id VARCHAR(32) PRIMARY KEY,           -- Identifiant unique de l'équipe (ex: "team1")
    name VARCHAR(32) NOT NULL,            -- Nom de l'équipe (ex: "Équipe team1")
    score INTEGER DEFAULT 0,              -- Score total de l'équipe
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Date de création
    finished_at DATETIME,                 -- Date de fin (NULL si en cours)
    total_time REAL DEFAULT 0.0           -- Temps total en secondes
);
```

**Exemple de données :**
```sql
INSERT INTO teams (id, name, score) VALUES 
('escape_team', 'Escape Team', 100);
```

---

### 2️⃣ Table `players` - Joueurs

Stocke les informations sur chaque joueur/équipe participante.

```sql
CREATE TABLE players (
    id VARCHAR(32) PRIMARY KEY,           -- Identifiant unique du joueur (ex: "team1")
    team_id VARCHAR(32) NOT NULL,         -- ID de l'équipe (clé étrangère)
    name VARCHAR(32) NOT NULL,            -- Nom du joueur (ex: "Équipe 1")
    individual_score INTEGER DEFAULT 0,   -- Score individuel (non utilisé actuellement)
    is_active BOOLEAN DEFAULT TRUE,       -- Le joueur est-il actuellement connecté ?
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Dernière activité
    
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
```

**Exemple de données :**
```sql
INSERT INTO players (id, team_id, name, is_active) VALUES 
('team1', 'escape_team', 'Équipe 1', TRUE),
('team2', 'escape_team', 'Équipe 2', FALSE);
```

---

### 3️⃣ Table `progress` - Progression des énigmes

Stocke la progression de chaque équipe sur les différentes énigmes.

```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,         -- ID de l'équipe (clé étrangère)
    player_id VARCHAR(32),                -- ID du joueur qui a résolu (peut être NULL)
    puzzle_name VARCHAR(32) NOT NULL,     -- Nom de l'énigme (ex: "chardin")
    is_solved BOOLEAN DEFAULT FALSE,      -- L'énigme est-elle résolue ?
    solved_at DATETIME,                   -- Date de résolution (NULL si non résolu)
    attempts INTEGER DEFAULT 0,           -- Nombre de tentatives
    hints_used INTEGER DEFAULT 0,         -- Nombre d'indices utilisés
    points_earned INTEGER DEFAULT 0,      -- Points gagnés pour cette énigme
    
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
```

**Exemple de données :**
```sql
INSERT INTO progress (team_id, player_id, puzzle_name, is_solved, solved_at, attempts, points_earned) VALUES 
('escape_team', 'team1', 'chardin', TRUE, CURRENT_TIMESTAMP, 1, 100);
```

---

### 4️⃣ Table `chat_messages` - Messages du chat

Stocke l'historique des messages échangés dans le chat d'équipe.

```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,         -- ID de l'équipe
    player_id VARCHAR(32) NOT NULL,       -- ID du joueur qui a envoyé le message
    message TEXT NOT NULL,                -- Contenu du message
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Date/heure du message
    is_system BOOLEAN DEFAULT FALSE       -- Message système ou utilisateur ?
);
```

**Exemple de données :**
```sql
INSERT INTO chat_messages (team_id, player_id, message, is_system) VALUES 
('escape_team', 'team1', 'On essaye le code 3563 ?', FALSE),
('escape_team', 'team2', 'Oui bonne idée !', FALSE);
```

---

### 5️⃣ Table `button_states` - États des boutons

Stocke l'état des boutons d'interaction pour chaque joueur.

```sql
CREATE TABLE button_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,         -- ID de l'équipe
    player_id VARCHAR(32) NOT NULL,       -- ID du joueur
    is_enabled BOOLEAN DEFAULT FALSE,     -- Le bouton est-il activé ?
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Dernière mise à jour
);
```

**Exemple de données :**
```sql
INSERT INTO button_states (team_id, player_id, is_enabled) VALUES 
('escape_team', 'team1', FALSE),
('escape_team', 'team2', TRUE);  -- Team2 commence avec le bouton activé
```

---

### 6️⃣ Table `game_sessions` - Sessions de jeu

Stocke les informations sur les sessions de jeu (optionnel, pour statistiques).

```sql
CREATE TABLE game_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,         -- ID de l'équipe
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Début de la session
    ended_at DATETIME,                    -- Fin de la session (NULL si en cours)
    status VARCHAR(32) DEFAULT 'in_progress',  -- Statut: in_progress, completed, abandoned
    final_score INTEGER DEFAULT 0         -- Score final de la session
);
```

---

## 🔗 Relations entre les tables

```
teams (1) ──── (N) players
  │
  ├──── (N) progress
  │
  └──── (N) chat_messages

players (1) ──── (N) button_states
```

---

## 🛠️ Script de reconstruction complet

### Option 1 : Utiliser le script Python existant

```bash
cd C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi\backoffice
python migrate_users.py
# Choisir l'option 2 pour reset complet
```

### Option 2 : Script SQL manuel

Créez un fichier `rebuild_database.sql` :

```sql
-- Supprimer les tables existantes
DROP TABLE IF EXISTS game_sessions;
DROP TABLE IF EXISTS button_states;
DROP TABLE IF EXISTS chat_messages;
DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;

-- Créer les tables
CREATE TABLE teams (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    score INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    total_time REAL DEFAULT 0.0
);

CREATE TABLE players (
    id VARCHAR(32) PRIMARY KEY,
    team_id VARCHAR(32) NOT NULL,
    name VARCHAR(32) NOT NULL,
    individual_score INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,
    player_id VARCHAR(32),
    puzzle_name VARCHAR(32) NOT NULL,
    is_solved BOOLEAN DEFAULT FALSE,
    solved_at DATETIME,
    attempts INTEGER DEFAULT 0,
    hints_used INTEGER DEFAULT 0,
    points_earned INTEGER DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_system BOOLEAN DEFAULT FALSE
);

CREATE TABLE button_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    is_enabled BOOLEAN DEFAULT FALSE,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id VARCHAR(32) NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME,
    status VARCHAR(32) DEFAULT 'in_progress',
    final_score INTEGER DEFAULT 0
);

-- Données initiales (optionnel)
INSERT INTO teams (id, name, score) VALUES ('escape_team', 'Escape Team', 0);
```

Exécuter le script :
```bash
cd C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi\backoffice
sqlite3 escape_game.db < rebuild_database.sql
```

---

## 🐍 Script Python de reconstruction

Créez un fichier `rebuild_database.py` dans le dossier `backoffice` :

```python
"""
Script de reconstruction complète de la base de données
"""
import os
from database import engine, Base
from models import Team, Player, Progress, ChatMessage, ButtonState, GameSession

def rebuild_database():
    """Reconstruit complètement la base de données"""
    
    print("⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les données !")
    response = input("Êtes-vous sûr de vouloir continuer ? (oui/non): ")
    
    if response.lower() != "oui":
        print("❌ Opération annulée")
        return
    
    db_path = "escape_game.db"
    
    # Supprimer l'ancienne base de données
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Ancienne base de données supprimée: {db_path}")
    
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    print("✅ Nouvelles tables créées")
    
    print("\n🎉 Base de données reconstruite avec succès !")
    print("\nStructure des tables :")
    print("  - teams")
    print("  - players")
    print("  - progress")
    print("  - chat_messages")
    print("  - button_states")
    print("  - game_sessions")
    print("\nVous pouvez maintenant démarrer le backend.")

if __name__ == "__main__":
    rebuild_database()
```

Utilisation :
```bash
cd C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi\backoffice
python rebuild_database.py
```

---

## 📝 Vérification de la structure

Pour vérifier que tout est bien créé :

```bash
sqlite3 escape_game.db

# Dans SQLite
.tables              # Lister toutes les tables
.schema teams        # Voir la structure d'une table
SELECT * FROM teams; # Voir les données
.quit                # Quitter
```

---

## 🎯 Énigmes configurées

D'après `puzzles_config.py`, voici les énigmes disponibles :

| Énigme | Code correct | Points | Restriction |
|--------|-------------|--------|-------------|
| chardin | 3563 | 100 | team1 uniquement |
| tableau_bleu | AZURE | 150 | Tous |
| musee_secret | 1789 | 200 | Tous |

---

**Note** : Le backend crée automatiquement les tables au démarrage si elles n'existent pas, grâce à `init_db()` dans `main.py`.
