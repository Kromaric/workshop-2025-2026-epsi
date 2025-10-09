"""
Script de configuration pour MariaDB
Crée la base de données si elle n'existe pas
"""
import pymysql
import sys

# Configuration
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "escape_game_db"


def create_database():
    """Crée la base de données si elle n'existe pas"""
    try:
        # Connexion à MariaDB sans spécifier de base de données
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Créer la base de données si elle n'existe pas
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Base de données '{DB_NAME}' créée ou déjà existante")
        
        # Vérifier que la base existe
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DB_NAME in databases:
            print(f"✅ Base de données '{DB_NAME}' confirmée")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Erreur MariaDB: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_connection():
    """Test la connexion à la base de données"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"✅ Connecté à MariaDB/MySQL version: {version[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Erreur de connexion: {e}")
        print("\n💡 Vérifiez que:")
        print("   1. MariaDB est bien démarré")
        print("   2. Le port 3306 est accessible")
        print("   3. L'utilisateur 'root' existe")
        return False


def show_tables():
    """Affiche les tables existantes"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n📊 Tables dans '{DB_NAME}':")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"\n⚠️  Aucune table dans '{DB_NAME}'")
            print("   Exécutez 'python db_utils.py reset' pour créer les tables")
        
        cursor.close()
        connection.close()
        
    except pymysql.Error as e:
        print(f"❌ Erreur: {e}")


def drop_database():
    """Supprime complètement la base de données (⚠️ DANGER)"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        print(f"✅ Base de données '{DB_NAME}' supprimée")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  CONFIGURATION MARIADB - ESCAPE GAME")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("""
Usage: python setup_mariadb.py [command]

Commandes disponibles:
  create      - Crée la base de données
  test        - Test la connexion
  tables      - Affiche les tables
  drop        - Supprime la base de données (⚠️ DANGER)
  full        - Crée la BDD et initialise les tables
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        create_database()
    
    elif command == "test":
        if create_database():
            test_connection()
    
    elif command == "tables":
        show_tables()
    
    elif command == "drop":
        response = input("⚠️  ATTENTION! Supprimer la base de données? (yes/no): ")
        if response.lower() == "yes":
            drop_database()
        else:
            print("❌ Opération annulée")
    
    elif command == "full":
        print("\n1️⃣ Création de la base de données...")
        if create_database():
            print("\n2️⃣ Test de connexion...")
            if test_connection():
                print("\n3️⃣ Création des tables...")
                from database import init_db
                try:
                    init_db()
                    print("\n4️⃣ Affichage des tables...")
                    show_tables()
                    print("\n✅ Configuration terminée avec succès!")
                except Exception as e:
                    print(f"❌ Erreur lors de la création des tables: {e}")
    
    else:
        print(f"❌ Commande inconnue: {command}")
