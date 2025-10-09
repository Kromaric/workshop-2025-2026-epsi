"""
Script utilitaire pour gérer la base de données MariaDB
"""
from database import engine, Base, SessionLocal, test_connection
from models import Team, Player, Progress, ChatMessage, ButtonState, GameSession
from datetime import datetime


def reset_database():
    """Réinitialise complètement la base de données"""
    print("⚠️  Suppression de toutes les tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables supprimées")
    
    print("📦 Création des nouvelles tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès dans MariaDB!")


def init_test_data():
    """Initialise des données de test"""
    db = SessionLocal()
    
    try:
        # Créer une équipe de test
        team = Team(
            id="team_test",
            name="Équipe de Test",
            score=0
        )
        db.add(team)
        
        # Créer des joueurs
        player1 = Player(
            id="user1",
            team_id="team_test",
            name="Joueur 1",
            is_active=False
        )
        player2 = Player(
            id="user2",
            team_id="team_test",
            name="Joueur 2",
            is_active=False
        )
        db.add(player1)
        db.add(player2)
        
        # Créer des états de bouton
        button1 = ButtonState(
            team_id="team_test",
            player_id="user1",
            is_enabled=False
        )
        button2 = ButtonState(
            team_id="team_test",
            player_id="user2",
            is_enabled=True
        )
        db.add(button1)
        db.add(button2)
        
        db.commit()
        print("✅ Données de test initialisées dans MariaDB!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


def show_stats():
    """Affiche les statistiques de la base de données"""
    db = SessionLocal()
    
    try:
        teams_count = db.query(Team).count()
        players_count = db.query(Player).count()
        progress_count = db.query(Progress).count()
        messages_count = db.query(ChatMessage).count()
        
        print("\n📊 Statistiques de la base de données MariaDB")
        print("=" * 40)
        print(f"Équipes: {teams_count}")
        print(f"Joueurs: {players_count}")
        print(f"Énigmes en cours: {progress_count}")
        print(f"Messages de chat: {messages_count}")
        print("=" * 40)
        
        # Afficher les équipes
        if teams_count > 0:
            print("\n🏆 Équipes:")
            teams = db.query(Team).all()
            for team in teams:
                print(f"  - {team.name} (ID: {team.id}) - Score: {team.score}")
                players = db.query(Player).filter(Player.team_id == team.id).all()
                for player in players:
                    status = "🟢" if player.is_active else "🔴"
                    print(f"    {status} {player.name} (Score: {player.individual_score})")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()


def clear_old_sessions():
    """Nettoie les anciennes sessions"""
    db = SessionLocal()
    
    try:
        # Marquer tous les joueurs comme inactifs
        db.query(Player).update({"is_active": False})
        db.commit()
        print("✅ Toutes les sessions ont été nettoyées")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


def check_connection():
    """Vérifie la connexion à MariaDB"""
    print("\n🔍 Vérification de la connexion MariaDB...")
    if test_connection():
        print("✅ Connexion OK - MariaDB est accessible")
        return True
    else:
        print("❌ Impossible de se connecter à MariaDB")
        print("\n💡 Solutions possibles:")
        print("   1. Vérifiez que MariaDB est démarré")
        print("   2. Vérifiez le port 3306")
        print("   3. Exécutez: python setup_mariadb.py create")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
Usage: python db_utils.py [command]

Commandes disponibles:
  check       - Vérifie la connexion à MariaDB
  reset       - Réinitialise complètement la base de données
  init        - Initialise des données de test
  stats       - Affiche les statistiques
  clear       - Nettoie les anciennes sessions
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        check_connection()
    
    elif command == "reset":
        if not check_connection():
            sys.exit(1)
        response = input("⚠️  Êtes-vous sûr de vouloir réinitialiser la BDD? (yes/no): ")
        if response.lower() == "yes":
            reset_database()
        else:
            print("❌ Opération annulée")
    
    elif command == "init":
        if not check_connection():
            sys.exit(1)
        init_test_data()
    
    elif command == "stats":
        if not check_connection():
            sys.exit(1)
        show_stats()
    
    elif command == "clear":
        if not check_connection():
            sys.exit(1)
        clear_old_sessions()
    
    else:
        print(f"❌ Commande inconnue: {command}")
