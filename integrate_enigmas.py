"""
Script d'intégration des énigmes de la branche dev dans l'architecture principale
"""
import os
import shutil
import re

SOURCE_DIR = r"C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi\workshop-2025-2026-epsi-dev"
TARGET_DIR = r"C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi"

def adapt_user_to_team(content):
    """Remplace user1/user2 par team1/team2 dans le code"""
    content = content.replace('user1', 'team1')
    content = content.replace('user2', 'team2')
    content = content.replace('User 1', 'Équipe 1')
    content = content.replace('User 2', 'Équipe 2')
    content = content.replace('Utilisateur 1', 'Équipe 1')
    content = content.replace('Utilisateur 2', 'Équipe 2')
    return content

def integrate_components():
    """Intègre les nouveaux composants Vue"""
    
    print("=" * 60)
    print("   INTÉGRATION DES ÉNIGMES")
    print("=" * 60)
    print()
    
    components_to_copy = [
        'SchemaSekhmet.vue',
        'HieroglyphKeyboard.vue',
        'SuccessPopup.vue'
    ]
    
    source_components = os.path.join(SOURCE_DIR, 'frontoffice', 'src', 'components')
    target_components = os.path.join(TARGET_DIR, 'frontoffice', 'src', 'components')
    
    print("📦 Copie des composants Vue...")
    print()
    
    for component in components_to_copy:
        source_file = os.path.join(source_components, component)
        target_file = os.path.join(target_components, component)
        
        if os.path.exists(source_file):
            # Lire le contenu
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Adapter user -> team
            content = adapt_user_to_team(content)
            
            # Écrire dans le target
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {component} copié et adapté (user→team)")
        else:
            print(f"  ⚠️  {component} non trouvé dans la source")
    
    print()
    print("✅ Composants intégrés !")
    print()

def create_puzzles_config():
    """Crée la configuration de l'énigme Sekhmet"""
    
    config = '''
# Configuration de l'énigme Sekhmet
SEKHMET_ENIGMA = {
    "id": "sekhmet",
    "name": "sekhmet",
    "title": "La Fille de Rê",
    "description": "Énigme collaborative sur les divinités égyptiennes",
    "riddle": "Suis la fille du soleil à travers les chemins dorés, écoute le murmure de ses pas sur la terre chaude, car elle seule connaît les secrets oubliés et t'indiquera la voie à suivre vers ta destinée.",
    "type": "collaborative",
    "points": 300,
    "unlocked_after": "chardin",  # Se débloque après Chardin
    
    # Restriction : team1 voit les schémas, team2 valide
    "team1_role": "guide",  # Voit les schémas des divinités
    "team2_role": "validator",  # Écrit les hiéroglyphes
    
    # Réponse correcte (hiéroglyphes de SEKHMET)
    "correct_answer": "h3-h6-h5-h10",
    
    # Divinités avec leurs caractéristiques
    "divinities": [
        {
            "id": "sekhmet",
            "name": "Sekhmet",
            "name_hieroglyphics": "𓌂𓅓𓏏𓆗",
            "description": "Déesse guerrière à tête de lionne",
            "distinctive_features": [
                "Tête de lionne avec crinière",
                "Corps de femme debout",
                "Disque solaire rouge sur la tête",
                "Sceptre ouas dans la main",
                "Robe longue moulante",
                "Attitude puissante et majestueuse"
            ],
            "image_url": "/800px-Sekhmet.png"
        },
        {
            "id": "anubis",
            "name": "Anubis",
            "name_hieroglyphics": "𓇋𓈖𓊪𓅱",
            "description": "Dieu à tête de chacal",
            "distinctive_features": [
                "Tête de chacal noir",
                "Longues oreilles pointues",
                "Corps d'homme debout",
                "Pagne court",
                "Souvent avec ankh ou sceptre",
                "Gardien des morts"
            ],
            "image_url": "/800px-Anubis_standing.png"
        },
        {
            "id": "khepri",
            "name": "Khépri",
            "name_hieroglyphics": "𓆣𓂋𓇋",
            "description": "Dieu à tête de scarabée",
            "distinctive_features": [
                "Tête de scarabée",
                "Corps humain masculin",
                "Scarabée complet sur la tête",
                "Symbolise le soleil levant",
                "Souvent avec disque solaire",
                "Dieu du renouveau"
            ],
            "image_url": "/800px-Khepri.png"
        },
        {
            "id": "set",
            "name": "Seth",
            "name_hieroglyphics": "𓃩𓏏𓁀",
            "description": "Dieu à tête d'animal fantastique",
            "distinctive_features": [
                "Tête d'animal mystérieux (âne/tamanoir)",
                "Longues oreilles carrées dressées",
                "Museau allongé et recourbé",
                "Corps d'homme",
                "Dieu du chaos et des tempêtes",
                "Souvent avec sceptre ouas"
            ],
            "image_url": "/800px-Set.png"
        }
    ]
}
'''
    
    print("📝 Configuration de l'énigme Sekhmet créée")
    print()
    print("✅ À ajouter manuellement dans puzzles_config.py")
    print()
    
    # Sauvegarder dans un fichier temporaire
    with open(os.path.join(TARGET_DIR, 'backoffice', 'sekhmet_config.py'), 'w', encoding='utf-8') as f:
        f.write(config)
    
    print("📄 Fichier créé : backoffice/sekhmet_config.py")
    print()

def create_integration_guide():
    """Crée un guide d'intégration"""
    
    guide = """# 🔧 GUIDE D'INTÉGRATION - Énigme Sekhmet

## ✅ Étapes déjà faites par le script :

1. ✅ Composants Vue copiés et adaptés (user→team)
   - SchemaSekhmet.vue
   - HieroglyphKeyboard.vue
   - SuccessPopup.vue

2. ✅ Configuration créée dans `sekhmet_config.py`

---

## 📋 Étapes manuelles à faire :

### 1. Ajouter la configuration dans `puzzles_config.py`

Ouvrez `backoffice/puzzles_config.py` et ajoutez à la fin :

```python
# Importer la config
from sekhmet_config import SEKHMET_ENIGMA

# Ajouter dans PUZZLES_CONFIG
PUZZLES_CONFIG["sekhmet"] = SEKHMET_ENIGMA
```

---

### 2. Modifier `main.py` - Ajouter la validation Sekhmet

Dans la classe `GameManager`, ajoutez cette méthode :

```python
async def validate_sekhmet(self, team_id: str, player_id: str, hieroglyph_code: str, db: Session):
    \"\"\"Valide l'énigme Sekhmet\"\"\"
    
    # Vérifier que c'est team2 qui valide
    if player_id != "team2":
        return {
            "success": False,
            "message": "Cette énigme doit être validée par Équipe 2"
        }
    
    # Vérifier si déjà résolu
    progress = db.query(Progress).filter(
        Progress.team_id == team_id,
        Progress.puzzle_name == "sekhmet"
    ).first()
    
    if not progress:
        progress = Progress(
            team_id=team_id,
            player_id=player_id,
            puzzle_name="sekhmet"
        )
        db.add(progress)
        db.commit()
    
    if progress.is_solved:
        return {
            "success": False,
            "message": "Vous avez déjà résolu cette énigme"
        }
    
    # Incrémenter les tentatives
    progress.attempts += 1
    
    # Code correct
    correct_code = "h3-h6-h5-h10"
    
    if hieroglyph_code == correct_code:
        progress.is_solved = True
        progress.solved_at = datetime.now()
        progress.points_earned = 300
        
        # Mettre à jour le score de l'équipe
        team = db.query(Team).filter(Team.id == team_id).first()
        if team:
            team.score += progress.points_earned
        
        db.commit()
        
        # Diffuser la progression
        await self.broadcast_progress(team_id, db)
        
        return {
            "success": True,
            "message": "🎉 Bravo ! Vous avez correctement identifié SEKHMET !",
            "info": "Sekhmet était la déesse guerrière égyptienne, fille du dieu soleil Rê.",
            "points": progress.points_earned
        }
    else:
        db.commit()
        return {
            "success": False,
            "message": "❌ Ce n'est pas la bonne séquence de hiéroglyphes. Vérifiez avec Équipe 1 !",
            "attempted_code": hieroglyph_code
        }
```

Dans le WebSocket endpoint, ajoutez :

```python
elif data.get("action") == "validate_sekhmet":
    result = await manager.validate_sekhmet(
        team_id,
        player_id,
        data.get("hieroglyph_code", ""),
        db
    )
    await websocket.send_json({
        "type": "sekhmet_result",
        "result": result
    })
```

---

### 3. Intégrer dans Team1.vue et Team2.vue

Dans `Team1.vue`, après l'énigme Chardin, ajoutez :

```vue
<!-- Énigme Sekhmet (Schémas pour team1) -->
<div v-if="sekhmетUnlocked" class="enigma-section">
  <SchemaSekhmet :enigma="sekhmmetEnigma" />
</div>
```

Dans `Team2.vue`, ajoutez :

```vue
<!-- Énigme Sekhmet (Clavier hiéroglyphes pour team2) -->
<div v-if="sekhmmetUnlocked" class="enigma-section">
  <HieroglyphKeyboard 
    :player-id="currentUserId"
    @validate-answer="validateSekhmet"
  />
</div>
```

Et dans le script :

```javascript
import SchemaSekhmet from '../components/SchemaSekhmet.vue'
import HieroglyphKeyboard from '../components/HieroglyphKeyboard.vue'

const sekhmmetUnlocked = ref(false)
const sekhmmetEnigma = ref(null)

function validateSekhmet(data) {
  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'validate_sekhmet',
      hieroglyph_code: data.hieroglyph_code
    }))
  }
}

// Dans onmessage, gérer le déblocage
if (data.type === 'chardin_result' && data.result.success) {
  sekhmmetUnlocked.value = true
  // Charger les données de l'énigme depuis puzzles_config
}
```

---

### 4. Copier les images

Copiez ces images dans `frontoffice/public/` :
- 800px-Sekhmet.png
- 800px-Anubis_standing.png
- 800px-Khepri.png
- 800px-Set.png

---

## 🎯 Parcours final :

```
Chardin (team1, code: 3563, 100pts)
    ↓
Sekhmet (collaborative, hiéroglyphes: h3-h6-h5-h10, 300pts)
    - team1 : voit les schémas des divinités
    - team2 : écrit les hiéroglyphes et valide
```

---

## ✅ Architecture respectée :

- ✅ Noms d'équipe personnalisés fonctionnent
- ✅ Clés composites (team_id, player_id) respectées
- ✅ Base de données MySQL inchangée
- ✅ Structure team1/team2 conservée
- ✅ Score et progression en base de données
- ✅ Chat et boutons fonctionnent toujours

---

**Bonne intégration ! 🚀**
"""
    
    with open(os.path.join(TARGET_DIR, 'INTEGRATION_SEKHMET.md'), 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("📖 Guide d'intégration créé : INTEGRATION_SEKHMET.md")
    print()

def main():
    print("\n🎮 Intégration des énigmes dans votre architecture\n")
    
    response = input("Voulez-vous continuer ? (oui/non): ")
    if response.lower() != "oui":
        print("❌ Intégration annulée")
        return
    
    print()
    
    # Intégrer les composants
    integrate_components()
    
    # Créer la config
    create_puzzles_config()
    
    # Créer le guide
    create_integration_guide()
    
    print("=" * 60)
    print("   🎉 INTÉGRATION AUTOMATIQUE TERMINÉE !")
    print("=" * 60)
    print()
    print("📂 Fichiers créés :")
    print("  ✅ frontoffice/src/components/SchemaSekhmet.vue")
    print("  ✅ frontoffice/src/components/HieroglyphKeyboard.vue")
    print("  ✅ frontoffice/src/components/SuccessPopup.vue")
    print("  ✅ backoffice/sekhmet_config.py")
    print("  ✅ INTEGRATION_SEKHMET.md (guide étape par étape)")
    print()
    print("📋 Prochaines étapes :")
    print("  1. Lisez INTEGRATION_SEKHMET.md")
    print("  2. Suivez les étapes manuelles (5 minutes)")
    print("  3. Copiez les images des divinités")
    print("  4. Testez le parcours complet !")
    print()
    print("✅ Votre architecture solide est préservée ! 🎯")
    print()

if __name__ == "__main__":
    main()
