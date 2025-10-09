# 🎯 GUIDE D'INTÉGRATION - Énigme Sekhmet

## ✅ Ce qui a été fait automatiquement :

1. ✅ **Composants Vue copiés et adaptés** (user→team)
   - `frontoffice/src/components/SchemaSekhmet.vue`
   - `frontoffice/src/components/HieroglyphKeyboard.vue`
   - `frontoffice/src/components/SuccessPopup.vue`

2. ✅ **Configuration créée**
   - `backoffice/sekhmet_config.py`

---

## 📋 Étapes manuelles restantes :

### 1️⃣ Ajouter la configuration dans `puzzles_config.py`

Ouvrez `backoffice/puzzles_config.py` et ajoutez à la fin :

```python
# Importer la config Sekhmet
from sekhmet_config import SEKHMET_ENIGMA

# Ajouter dans PUZZLES_CONFIG
PUZZLES_CONFIG["sekhmet"] = SEKHMET_ENIGMA
```

---

### 2️⃣ Modifier `main.py` - Ajouter la validation Sekhmet

Dans `backoffice/main.py`, dans la classe `GameManager`, ajoutez cette méthode après `validate_chardin` :

```python
async def validate_sekhmet(self, team_id: str, player_id: str, hieroglyph_code: str, db: Session):
    """Valide l'énigme Sekhmet"""
    
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

Dans le WebSocket endpoint, ajoutez ce bloc après `validate_chardin` :

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

### 3️⃣ Intégrer dans `Team1.vue`

Ouvrez `frontoffice/src/views/Team1.vue` :

#### A. Imports (en haut du script)
```javascript
import SchemaSekhmet from '../components/SchemaSekhmet.vue'
import SuccessPopup from '../components/SuccessPopup.vue'
```

#### B. Variables réactives (dans le script)
```javascript
const chardinSolved = ref(false)
const sekhmметUnlocked = ref(false)
const sekhmметEnigma = ref(null)
const showSuccessPopup = ref(false)
const showSekhmметSuccess = ref(false)
const successMessage = ref('')
```

#### C. Fonctions
```javascript
function handleContinue() {
  showSuccessPopup.value = false
  sekhmметUnlocked.value = true
}

function closeSekhmметSuccess() {
  showSekhmметSuccess.value = false
}
```

#### D. WebSocket onmessage (ajouter ces cas)
```javascript
if (data.type === 'chardin_result') {
  const result = data.result
  if (result.success) {
    chardinSolved.value = true
    showSuccessPopup.value = true
    successMessage.value = result.message
    // Charger les données Sekhmet
    loadSekhmemetEnigma()
  }
} else if (data.type === 'sekhmet_result') {
  const result = data.result
  if (result.success) {
    showSekhmметSuccess.value = true
    successMessage.value = result.message
  }
}
```

#### E. Fonction pour charger Sekhmet
```javascript
function loadSekhmметEnigma() {
  // Charger depuis sekhmet_config.py ou via WebSocket
  // Pour simplifier, on peut le hard-coder côté frontend
  sekhmметEnigma.value = {
    title: "La Fille de Rê",
    riddle: "Suis la fille du soleil...",
    divinities: [
      // Copier depuis sekhmet_config.py
    ]
  }
}
```

#### F. Template (ajouter après EnigmeChardin)
```vue
<!-- Popup de succès Chardin -->
<SuccessPopup
  :show="showSuccessPopup"
  @continue="handleContinue"
  @close="showSuccessPopup = false"
/>

<!-- Notification succès Sekhmet -->
<transition name="slide-down">
  <div v-if="showSekhmметSuccess" class="notification success">
    <span>{{ successMessage }}</span>
    <button @click="closeSekhmmetSuccess" class="close-notif">×</button>
  </div>
</transition>

<!-- Énigme Sekhmet (Schémas pour team1) -->
<div v-if="sekhmметUnlocked" class="enigma-section">
  <SchemaSekhmet :enigma="sekhmметEnigma" />
</div>
```

---

### 4️⃣ Intégrer dans `Team2.vue`

Ouvrez `frontoffice/src/views/Team2.vue` :

#### A. Imports
```javascript
import HieroglyphKeyboard from '../components/HieroglyphKeyboard.vue'
```

#### B. Variables
```javascript
const sekhmметUnlocked = ref(false)
const showSekhmметSuccess = ref(false)
const successMessage = ref('')
```

#### C. Fonctions
```javascript
function validateSekhmet(data) {
  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'validate_sekhmet',
      hieroglyph_code: data.hieroglyph_code
    }))
  }
}

function closeSekhmетSuccess() {
  showSekhmметSuccess.value = false
}
```

#### D. WebSocket onmessage
```javascript
if (data.type === 'chardin_result') {
  const result = data.result
  if (result.success) {
    sekhmметUnlocked.value = true
  }
} else if (data.type === 'sekhmet_result') {
  const result = data.result
  if (result.success) {
    showSekhmметSuccess.value = true
    successMessage.value = result.message
  }
}
```

#### E. Template
```vue
<!-- Notification succès Sekhmet -->
<transition name="slide-down">
  <div v-if="showSekhmметSuccess" class="notification success">
    <span>{{ successMessage }}</span>
    <button @click="closeSekhmetSuccess" class="close-notif">×</button>
  </div>
</transition>

<!-- Énigme Sekhmet (Clavier hiéroglyphes pour team2) -->
<div v-if="sekhmметUnlocked" class="enigma-section">
  <HieroglyphKeyboard 
    :player-id="currentUserId"
    @validate-answer="validateSekhmet"
  />
</div>
```

---

### 5️⃣ Copier les images des divinités

Copiez ces 4 images dans `frontoffice/public/` :

1. `800px-Sekhmet.png`
2. `800px-Anubis_standing.png`
3. `800px-Khepri.png`
4. `800px-Set.png`

**Où les trouver ?**
- Dans `workshop-2025-2026-epsi-dev/frontoffice/public/`
- Ou téléchargez-les depuis Wikimedia Commons

---

## 🎯 Parcours final :

```
1. Chardin (team1, code: 3563, 100pts)
   ↓ Déblocage
2. Sekhmet (collaborative, h3-h6-h5-h10, 300pts)
   - team1: voit les schémas des 4 divinités
   - team2: écrit les hiéroglyphes et valide
   ↓
Score total: 400 points
```

---

## ✅ Architecture respectée :

- ✅ Noms d'équipe personnalisés
- ✅ Clés composites (team_id, player_id)
- ✅ Base MySQL avec Progress table
- ✅ Structure team1/team2
- ✅ Chat et boutons fonctionnent
- ✅ Score partagé par équipe

---

## 🚀 Prochaines étapes :

1. Suivez ce guide étape par étape
2. Testez avec deux navigateurs (team1 et team2)
3. Vérifiez le chat fonctionne entre les deux
4. Validez que le score s'incrémente

**Bonne intégration ! 🎨**
