# 🎮 Escape Game Musée - Backoffice API

## 📋 Vue d'ensemble

API FastAPI avec base de données **MariaDB** pour gérer un escape game multijoueur au musée.

### 🎯 Fonctionnalités

✅ **Base de données persistante** (MariaDB)
✅ **Multi-équipes** simultanées
✅ **Système de score** avec progression
✅ **WebSocket temps réel** pour le chat et les interactions
✅ **Énigmes configurables** avec points
✅ **Statistiques** et classement
✅ **API REST** pour l'administration

---

## 🚀 Démarrage Rapide

### Installation en 3 commandes :

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer MariaDB
python setup_mariadb.py full

# 3. Lancer le serveur
fastapi dev main.py
```

**Serveur accessible sur :** http://localhost:8000

### Vérifier l'installation :

```bash
python test_installation.py
```

---

## 📚 Documentation

### Guides disponibles :

1. **[QUICKSTART_MARIADB.md](QUICKSTART_MARIADB.md)** ⚡
   - Installation rapide
   - Commandes essentielles
   - Résolution de problèmes

2. **[MIGRATION_MARIADB.md](MIGRATION_MARIADB.md)** 🔄
   - Guide complet de migration
   - Configuration détaillée
   - Troubleshooting avancé

3. **[DATABASE_README.md](DATABASE_README.md)** 📖
   - Structure de la base de données
   - Ajouter des énigmes
   - API endpoints

4. **[STRUCTURE.md](STRUCTURE.md)** 🏗️
   - Architecture du projet
   - Diagrammes
   - Flux de données

---

## ⚙️ Configuration

### Fichier : `config.py`

```python
# Configuration MariaDB
MARIADB_CONFIG = {
    "user": "root",
    "password": "",  # Votre mot de passe
    "host": "localhost",
    "port": "3306",
    "database": "escape_game_db"
}
```

**Pour modifier :** Éditez `config.py` puis redémarrez le serveur

---

## 🛠️ Scripts Utiles

### Configuration MariaDB

```bash
python setup_mariadb.py full      # Setup complet
python setup_mariadb.py create    # Créer la BDD
python setup_mariadb.py test      # Tester connexion
python setup_mariadb.py tables    # Voir les tables
```

### Gestion de la base de données

```bash
python db_utils.py check    # Vérifier connexion
python db_utils.py stats    # Voir statistiques
python db_utils.py reset    # Réinitialiser
python db_utils.py init     # Données de test
python db_utils.py clear    # Nettoyer sessions
```

### Tests

```bash
python test_installation.py    # Test complet
python config.py               # Voir config
python database.py             # Tester BDD
```

---

## 📡 API Endpoints

### WebSocket

```
ws://localhost:8000/ws/{team_id}/{player_id}
```

**Actions :**
- `validate_chardin` - Valider énigme Chardin
- `button_click` - Cliquer sur le bouton
- `send_message` - Envoyer un message

### HTTP REST

```
GET  /                          # Bienvenue
GET  /teams/{team_id}/stats     # Stats d'équipe
```

### Administration (optionnel)

Activez dans `main.py` :
```python
from admin_routes import router as admin_router
app.include_router(admin_router)
```

Puis :
```
GET    /admin/teams              # Liste équipes
GET    /admin/leaderboard        # Classement
GET    /admin/stats/global       # Stats globales
DELETE /admin/teams/{id}         # Supprimer équipe
```

---

## 📊 Structure de la Base de Données

### Tables principales :

- **teams** - Équipes et scores
- **players** - Joueurs
- **progress** - Progression énigmes
- **chat_messages** - Messages
- **button_states** - États boutons
- **game_sessions** - Sessions de jeu

**Voir :** `STRUCTURE.md` pour les diagrammes complets

---

## 🎯 Ajouter une Énigme

### 1. Configurer dans `puzzles_config.py` :

```python
"ma_enigme": {
    "name": "Mon Énigme",
    "correct_code": "CODE123",
    "points": 150,
    "restricted_to": None,  # ou ["user1"]
    "hints": ["Indice 1", "Indice 2"]
}
```

### 2. Ajouter le handler dans `main.py` :

```python
elif data.get("action") == "validate_ma_enigme":
    result = await manager.validate_puzzle(
        team_id, player_id, "ma_enigme",
        data.get("code", ""), db
    )
```

### 3. Frontend (JavaScript) :

```javascript
ws.send(JSON.stringify({
    action: "validate_ma_enigme",
    code: "CODE123"
}));
```

---

## 🏗️ Architecture

```
Frontend (React)
      ↓ WebSocket
FastAPI Backend
      ↓ SQLAlchemy ORM
MariaDB Database
```

**Stack technique :**
- Python 3.x
- FastAPI (WebSocket + REST)
- SQLAlchemy (ORM)
- MariaDB/MySQL
- PyMySQL (driver)

---

## 📦 Dépendances

```
fastapi[standard]==0.113.0
pydantic==2.8.0
sqlalchemy==2.0.23
pymysql==1.1.0
cryptography==41.0.7
```

**Installation :**
```bash
pip install -r requirements.txt
```

---

## 🐛 Problèmes Courants

### MariaDB ne démarre pas
```bash
# Windows (XAMPP)
Ouvrir le panneau XAMPP → Start MySQL

# Linux
sudo systemctl start mariadb

# Mac
brew services start mariadb
```

### Base de données n'existe pas
```bash
python setup_mariadb.py create
```

### Tables manquantes
```bash
python db_utils.py reset
```

### Erreur de connexion
```bash
python test_installation.py
```

**Plus d'aide :** Consultez `MIGRATION_MARIADB.md`

---

## 💾 Sauvegardes

### Sauvegarder la base de données :

```bash
mysqldump -u root escape_game_db > backup.sql
```

### Restaurer :

```bash
mysql -u root escape_game_db < backup.sql
```

---

## 🔐 Sécurité

### Pour la production :

1. **Créer un utilisateur dédié** (pas root)
2. **Utiliser un mot de passe fort**
3. **Limiter les permissions**
4. **Activer HTTPS**
5. **Configurer un pare-feu**

**Voir :** `MIGRATION_MARIADB.md` section Sécurité

---

## 📊 Monitoring

### Voir les statistiques :

```bash
python db_utils.py stats
```

### Via MariaDB :

```sql
mysql -u root escape_game_db

SELECT COUNT(*) as teams FROM teams;
SELECT name, score FROM teams ORDER BY score DESC;
```

---

## 🎓 Projet EPSI 2025-2026

Développé pour le **Workshop EPSI** - Escape Game au Musée

### Structure du projet :

```
workshop-2025-2026-epsi/
├── backoffice/        # API FastAPI (ce dossier)
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── config.py
└── frontoffice/       # Frontend React
```

---

## 📞 Support

**Problème ?**
1. Consultez `QUICKSTART_MARIADB.md`
2. Exécutez `python test_installation.py`
3. Lisez `MIGRATION_MARIADB.md`
4. Vérifiez les logs MariaDB

---

## ✅ Checklist avant de commencer

- [ ] MariaDB installé et démarré
- [ ] Python 3.x installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Base de données créée (`python setup_mariadb.py full`)
- [ ] Tests passent (`python test_installation.py`)
- [ ] Configuration vérifiée (`config.py`)

---

## 🎉 Prêt !

```bash
# Lancer le serveur
fastapi dev main.py

# Visitez
http://localhost:8000
```

**Bon workshop ! 🚀**

---

**Dernière mise à jour :** Octobre 2025
**Version :** 2.0.0 (MariaDB)
