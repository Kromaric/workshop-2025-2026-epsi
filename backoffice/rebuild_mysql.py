"""
Script pour recréer les tables MySQL/MariaDB avec les clés composites
"""
from database import engine, Base
from models import Team, Player, Progress, ChatMessage, ButtonState, GameSession

def rebuild_mysql_tables():
    """Reconstruit les tables MySQL avec les nouvelles clés composites"""
    
    print("=" * 60)
    print("   RECONSTRUCTION DES TABLES MYSQL")
    print("=" * 60)
    print()
    print("⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les tables !")
    print()
    response = input("Êtes-vous sûr de vouloir continuer ? (oui/non): ")
    
    if response.lower() != "oui":
        print("❌ Opération annulée")
        return
    
    print("\n🔄 Reconstruction en cours...")
    
    try:
        # Supprimer toutes les tables
        print("🗑️  Suppression des anciennes tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Anciennes tables supprimées")
        
        # Créer toutes les tables avec la nouvelle structure
        print("🔨 Création des nouvelles tables avec clés composites...")
        Base.metadata.create_all(bind=engine)
        print("✅ Nouvelles tables créées")
        
        print("\n" + "=" * 60)
        print("   🎉 TABLES MYSQL RECONSTRUITES AVEC SUCCÈS !")
        print("=" * 60)
        print("\n📊 Structure des tables créées :")
        print("  1. teams           - Équipes et leurs scores")
        print("  2. players         - Joueurs (CLÉ COMPOSITE: id + team_id)")
        print("  3. progress        - Progression sur les énigmes")
        print("  4. chat_messages   - Historique des messages")
        print("  5. button_states   - États des boutons (CLÉ COMPOSITE: team_id + player_id)")
        print("  6. game_sessions   - Sessions de jeu")
        
        print("\n🔑 Clés composites implémentées :")
        print("  - players: PRIMARY KEY (id, team_id)")
        print("  - button_states: PRIMARY KEY (team_id, player_id)")
        
        print("\n🚀 Prochaines étapes :")
        print("  1. Démarrez le backend : python main.py")
        print("  2. Testez avec plusieurs équipes différentes")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la reconstruction: {e}")
        print("\nSi l'erreur persiste, supprimez manuellement les tables dans MySQL:")
        print("  mysql -u root -p")
        print("  USE votre_base;")
        print("  DROP TABLE IF EXISTS game_sessions, button_states, chat_messages, progress, players, teams;")
        print("  EXIT;")
        print("\nPuis relancez ce script.")

if __name__ == "__main__":
    rebuild_mysql_tables()
