"""
Script de test rapide pour vérifier l'installation MariaDB
"""
import sys

def test_imports():
    """Teste que tous les modules sont installés"""
    print("\n1️⃣ Test des imports Python...")
    try:
        import pymysql
        print("   ✅ pymysql installé")
    except ImportError:
        print("   ❌ pymysql manquant - Exécutez: pip install pymysql")
        return False
    
    try:
        import sqlalchemy
        print("   ✅ sqlalchemy installé")
    except ImportError:
        print("   ❌ sqlalchemy manquant - Exécutez: pip install sqlalchemy")
        return False
    
    try:
        import fastapi
        print("   ✅ fastapi installé")
    except ImportError:
        print("   ❌ fastapi manquant - Exécutez: pip install fastapi")
        return False
    
    return True


def test_mariadb_connection():
    """Teste la connexion à MariaDB"""
    print("\n2️⃣ Test de connexion à MariaDB...")
    try:
        import pymysql
        from config import MARIADB_CONFIG
        
        connection = pymysql.connect(
            host=MARIADB_CONFIG['host'],
            port=int(MARIADB_CONFIG['port']),
            user=MARIADB_CONFIG['user'],
            password=MARIADB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"   ✅ Connexion réussie!")
        print(f"   📊 Version: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        print("\n   💡 Vérifiez que:")
        print("      - MariaDB est démarré")
        print("      - Le port 3306 est accessible")
        print("      - Les identifiants dans config.py sont corrects")
        return False


def test_database_exists():
    """Teste si la base de données existe"""
    print("\n3️⃣ Test de la base de données...")
    try:
        import pymysql
        from config import MARIADB_CONFIG
        
        connection = pymysql.connect(
            host=MARIADB_CONFIG['host'],
            port=int(MARIADB_CONFIG['port']),
            user=MARIADB_CONFIG['user'],
            password=MARIADB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        db_name = MARIADB_CONFIG['database']
        if db_name in databases:
            print(f"   ✅ Base de données '{db_name}' existe")
            
            # Vérifier les tables
            cursor.execute(f"USE {db_name}")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"   ✅ {len(tables)} table(s) trouvée(s):")
                for table in tables:
                    print(f"      - {table[0]}")
            else:
                print("   ⚠️  Aucune table - Exécutez: python db_utils.py reset")
        else:
            print(f"   ❌ Base de données '{db_name}' n'existe pas")
            print("   💡 Exécutez: python setup_mariadb.py create")
            return False
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def test_sqlalchemy():
    """Teste SQLAlchemy"""
    print("\n4️⃣ Test SQLAlchemy...")
    try:
        from database import test_connection
        if test_connection():
            print("   ✅ SQLAlchemy fonctionne correctement")
            return True
        return False
    except Exception as e:
        print(f"   ❌ Erreur SQLAlchemy: {e}")
        return False


def main():
    """Lance tous les tests"""
    print("=" * 60)
    print("🧪 TEST DE L'INSTALLATION - ESCAPE GAME MARIADB")
    print("=" * 60)
    
    tests = [
        ("Imports Python", test_imports),
        ("Connexion MariaDB", test_mariadb_connection),
        ("Base de données", test_database_exists),
        ("SQLAlchemy", test_sqlalchemy)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erreur inattendue dans {name}: {e}")
            results.append((name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print("=" * 60)
    print(f"Score: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ Tous les tests passent! Vous pouvez lancer le serveur:")
        print("   fastapi dev main.py")
    else:
        print("⚠️  Certains tests ont échoué. Consultez les erreurs ci-dessus.")
        print("\n💡 Aide au démarrage:")
        print("   1. pip install -r requirements.txt")
        print("   2. python setup_mariadb.py full")
        print("   3. python test_installation.py")
    
    print("=" * 60)
    
    return success_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
