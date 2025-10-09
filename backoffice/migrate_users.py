"""
Script de migration : user1/user2 -> team1/team2
Ce script migre les anciennes données de la base de données
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SQLALCHEMY_DATABASE_URL, Base
from models import Team, Player, Progress, ChatMessage, ButtonState

def migrate_database():
    """Migre les données de user1/user2 vers team1/team2"""
    
    # Créer la connexion
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔄 Démarrage de la migration...")
        
        # 1. Migrer les joueurs user1 -> team1, user2 -> team2
        players_to_migrate = [
            ("user1", "team1"),
            ("user2", "team2")
        ]
        
        for old_id, new_id in players_to_migrate:
            player = db.query(Player).filter(Player.id == old_id).first()
            if player:
                print(f"   Suppression de l'ancien joueur: {old_id}")
                db.delete(player)
        
        db.commit()
        print("✅ Anciens joueurs supprimés")
        
        # 2. Créer les nouveaux joueurs team1 et team2
        for new_id in ["team1", "team2"]:
            existing = db.query(Player).filter(Player.id == new_id).first()
            if not existing:
                new_player = Player(
                    id=new_id,
                    team_id="escape_team",  # Équipe unique
                    name=f"Équipe {new_id[-1]}",
                    is_active=False
                )
                db.add(new_player)
                print(f"✅ Créé nouveau joueur: {new_id}")
        
        db.commit()
        
        # 3. Nettoyer les Progress avec les anciens user_ids
        old_progress = db.query(Progress).filter(
            Progress.player_id.in_(["user1", "user2"])
        ).all()
        
        for prog in old_progress:
            print(f"   Suppression progress pour: {prog.player_id}")
            db.delete(prog)
        
        db.commit()
        print("✅ Anciennes progressions nettoyées")
        
        # 4. Nettoyer les messages de chat avec les anciens user_ids
        old_messages = db.query(ChatMessage).filter(
            ChatMessage.player_id.in_(["user1", "user2"])
        ).all()
        
        for msg in old_messages:
            db.delete(msg)
        
        db.commit()
        print("✅ Anciens messages de chat nettoyés")
        
        # 5. Nettoyer les états de boutons avec les anciens user_ids
        old_buttons = db.query(ButtonState).filter(
            ButtonState.player_id.in_(["user1", "user2"])
        ).all()
        
        for btn in old_buttons:
            db.delete(btn)
        
        db.commit()
        print("✅ Anciens états de boutons nettoyés")
        
        # 6. Réinitialiser les scores de toutes les équipes
        teams = db.query(Team).all()
        for team in teams:
            team.score = 0
            print(f"   Réinitialisation du score de l'équipe: {team.id}")
        
        db.commit()
        print("✅ Scores d'équipes réinitialisés")
        
        print("\n🎉 Migration terminée avec succès !")
        print("\nVous pouvez maintenant utiliser team1 et team2")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la migration: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


def reset_database():
    """Réinitialise complètement la base de données"""
    
    # Créer la connexion
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les données !")
        response = input("Êtes-vous sûr ? (oui/non): ")
        
        if response.lower() != "oui":
            print("❌ Opération annulée")
            return
        
        print("\n🔄 Réinitialisation de la base de données...")
        
        # Supprimer toutes les données
        db.query(ButtonState).delete()
        db.query(ChatMessage).delete()
        db.query(Progress).delete()
        db.query(Player).delete()
        db.query(Team).delete()
        db.commit()
        
        print("✅ Toutes les données ont été supprimées")
        print("✅ Base de données réinitialisée")
        print("\nVous pouvez maintenant redémarrer l'application")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("   SCRIPT DE MIGRATION - user1/user2 → team1/team2")
    print("=" * 60)
    print()
    print("Choisissez une option:")
    print("1. Migrer user1/user2 vers team1/team2 (recommandé)")
    print("2. Réinitialiser complètement la base de données")
    print("3. Annuler")
    print()
    
    choice = input("Votre choix (1/2/3): ")
    
    if choice == "1":
        migrate_database()
    elif choice == "2":
        reset_database()
    else:
        print("❌ Opération annulée")
