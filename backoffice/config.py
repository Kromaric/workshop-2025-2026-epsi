"""
Fichier de configuration centralisé pour la base de données
Modifiez ce fichier pour changer de base de données
"""

# =====================================================
# CONFIGURATION BASE DE DONNÉES
# =====================================================

# Type de base de données : "mariadb" ou "sqlite"
DATABASE_TYPE = "mariadb"

# =====================================================
# CONFIGURATION MARIADB
# =====================================================
MARIADB_CONFIG = {
    "user": "root",
    "password": "",  # Laissez vide si pas de mot de passe
    "host": "localhost",
    "port": "3306",
    "database": "escape_game_db"
}

# =====================================================
# CONFIGURATION SQLITE (alternative)
# =====================================================
SQLITE_CONFIG = {
    "database": "escape_game.db"  # Fichier local
}

# =====================================================
# PARAMÈTRES AVANCÉS
# =====================================================

# Pool de connexions
POOL_SIZE = 10
POOL_RECYCLE = 3600  # Recycler les connexions après 1h

# Debug
ECHO_SQL = False  # Afficher les requêtes SQL (True pour debug)

# =====================================================
# NE PAS MODIFIER EN DESSOUS
# =====================================================

def get_database_url():
    """Retourne l'URL de connexion en fonction de la configuration"""
    if DATABASE_TYPE == "mariadb":
        cfg = MARIADB_CONFIG
        password_part = f":{cfg['password']}" if cfg['password'] else ""
        return f"mysql+pymysql://{cfg['user']}{password_part}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
    
    elif DATABASE_TYPE == "sqlite":
        cfg = SQLITE_CONFIG
        return f"sqlite:///./{cfg['database']}"
    
    else:
        raise ValueError(f"Type de base de données inconnu: {DATABASE_TYPE}")


def get_connect_args():
    """Retourne les arguments de connexion spécifiques"""
    if DATABASE_TYPE == "sqlite":
        return {"check_same_thread": False}
    return {}


# Affichage de la configuration
if __name__ == "__main__":
    print("=" * 60)
    print("📊 CONFIGURATION BASE DE DONNÉES")
    print("=" * 60)
    print(f"Type: {DATABASE_TYPE.upper()}")
    print(f"URL: {get_database_url()}")
    print("=" * 60)
    
    if DATABASE_TYPE == "mariadb":
        cfg = MARIADB_CONFIG
        print("\n🔧 Configuration MariaDB:")
        print(f"   Hôte: {cfg['host']}")
        print(f"   Port: {cfg['port']}")
        print(f"   Utilisateur: {cfg['user']}")
        print(f"   Mot de passe: {'(vide)' if not cfg['password'] else '***'}")
        print(f"   Base de données: {cfg['database']}")
    
    elif DATABASE_TYPE == "sqlite":
        cfg = SQLITE_CONFIG
        print("\n🔧 Configuration SQLite:")
        print(f"   Fichier: {cfg['database']}")
    
    print("\n💡 Pour changer de base de données, éditez config.py")
