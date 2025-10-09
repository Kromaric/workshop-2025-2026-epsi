"""
Script de nettoyage des fichiers inutiles - Version corrigée
"""
import os

# Chemins absolus des fichiers à supprimer
BASE_PATH = r"C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi"

FILES_TO_DELETE = [
    # Frontend
    r"frontoffice\src\views\User1.vue",
    r"frontoffice\src\views\User2.vue",
    r"frontoffice\src\views\Game.vue",
    r"frontoffice\src\views\TeamSelection.vue",
    
    # Backend
    r"backoffice\rebuild_database.py",
    r"backoffice\rebuild_with_composite.py",
    r"backoffice\DATABASE_README.md",
    r"backoffice\INSTALLATION_GUIDE.txt",
    r"backoffice\MIGRATION_GUIDE.md",
    r"backoffice\MIGRATION_MARIADB.md",
    r"backoffice\QUICKSTART.md",
    r"backoffice\QUICKSTART_MARIADB.md",
    r"backoffice\STRUCTURE.md",
    r"backoffice\SUMMARY.md",
]

def clean_files():
    """Supprime les fichiers inutiles"""
    
    print("=" * 60)
    print("   NETTOYAGE DES FICHIERS INUTILES")
    print("=" * 60)
    print()
    print(f"📁 Dossier de base : {BASE_PATH}")
    print()
    print("📋 Fichiers qui seront supprimés :")
    print()
    
    for filepath in FILES_TO_DELETE:
        print(f"  ❌ {filepath}")
    
    print()
    print(f"Total : {len(FILES_TO_DELETE)} fichiers")
    print()
    
    response = input("Voulez-vous continuer ? (oui/non): ")
    
    if response.lower() != "oui":
        print("❌ Nettoyage annulé")
        return
    
    print()
    print("🧹 Nettoyage en cours...")
    print()
    
    deleted_count = 0
    not_found_count = 0
    error_count = 0
    
    for filepath in FILES_TO_DELETE:
        full_path = os.path.join(BASE_PATH, filepath)
        
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"✅ Supprimé: {filepath}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur: {filepath} - {e}")
                error_count += 1
        else:
            print(f"⚠️  Non trouvé: {filepath}")
            not_found_count += 1
    
    print()
    print("=" * 60)
    print("   🎉 NETTOYAGE TERMINÉ !")
    print("=" * 60)
    print(f"\n✅ {deleted_count} fichiers supprimés")
    
    if not_found_count > 0:
        print(f"⚠️  {not_found_count} fichiers non trouvés")
    
    if error_count > 0:
        print(f"❌ {error_count} erreurs")
    
    print()
    print("📂 Fichiers conservés dans backoffice :")
    print("  ✅ migrate_users.py")
    print("  ✅ setup_mariadb.py")
    print("  ✅ test_installation.py")
    print()

if __name__ == "__main__":
    clean_files()
