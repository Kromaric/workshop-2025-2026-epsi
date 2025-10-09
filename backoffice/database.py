from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_database_url, get_connect_args, POOL_SIZE, POOL_RECYCLE, ECHO_SQL, DATABASE_TYPE

# URL de connexion (MariaDB ou SQLite selon config.py)
SQLALCHEMY_DATABASE_URL = get_database_url()

# Configuration du moteur
engine_config = {
    "pool_pre_ping": True,
    "pool_recycle": POOL_RECYCLE,
    "echo": ECHO_SQL
}

# Ajouter le pool_size uniquement pour MariaDB
if DATABASE_TYPE == "mariadb":
    engine_config["pool_size"] = POOL_SIZE

# Ajouter les arguments de connexion
connect_args = get_connect_args()
if connect_args:
    engine_config["connect_args"] = connect_args

# Créer le moteur
engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_config)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialise la base de données - crée toutes les tables"""
    from models import Team, Player, Progress, ChatMessage, ButtonState, GameSession
    Base.metadata.create_all(bind=engine)
    db_type = DATABASE_TYPE.upper()
    print(f"✅ Tables créées avec succès dans {db_type}")


def test_connection():
    """Test la connexion à la base de données"""
    try:
        connection = engine.connect()
        connection.close()
        db_type = DATABASE_TYPE.upper()
        print(f"✅ Connexion à {db_type} réussie!")
        return True
    except Exception as e:
        db_type = DATABASE_TYPE.upper()
        print(f"❌ Erreur de connexion à {db_type}: {e}")
        if DATABASE_TYPE == "mariadb":
            print("\n💡 Vérifiez que:")
            print("   1. MariaDB est bien démarré")
            print("   2. Le port 3306 est accessible")
            print("   3. Les identifiants dans config.py sont corrects")
            print("   4. La base de données existe (python setup_mariadb.py create)")
        return False


# Afficher la configuration au démarrage
if __name__ == "__main__":
    from config import MARIADB_CONFIG, DATABASE_TYPE
    
    print("=" * 60)
    print("🗄️  CONFIGURATION BASE DE DONNÉES")
    print("=" * 60)
    print(f"Type: {DATABASE_TYPE.upper()}")
    
    if DATABASE_TYPE == "mariadb":
        print(f"Hôte: {MARIADB_CONFIG['host']}:{MARIADB_CONFIG['port']}")
        print(f"Base: {MARIADB_CONFIG['database']}")
        print(f"User: {MARIADB_CONFIG['user']}")
    
    print("=" * 60)
    
    print("\n🔍 Test de connexion...")
    test_connection()
