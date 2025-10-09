# 🎮 PARCOURS UTILISATEURS COMPLETS

## 📊 Vue d'ensemble

Le jeu est un **escape game collaboratif** où deux joueurs (User1 et User2) doivent travailler ensemble pour résoudre des énigmes basées sur les œuvres d'art d'un musée.

---

## 🎭 Parcours User1 (Équipe 1)

### **Phase 1 : Énigme Chardin** 🖼️

**Composant affiché :** `EnigmeChardin.vue`

**Objectif :** Résoudre l'énigme en entrant le code correct

**Fonctionnalités :**
- Interface de saisie de code
- Validation du code auprès du backend
- Code correct : `3563`
- Points gagnés : 100 points

**Interactions :**
```javascript
handleChardinSubmit(data) {
  websocket.send({
    action: 'validate_chardin',
    code: data.code
  })
}
```

**Résultat :**
- ✅ Succès → Popup de félicitations → Passage à la Phase 2
- ❌ Échec → Message d'erreur, nouvelle tentative

---

### **Phase 2 : Énigme Sekhmet - Rôle Guide** 🏺

**Composant affiché :** `SchemaSekhmet.vue`

**Objectif :** Guider User2 pour identifier la bonne divinité

**Ce que voit User1 :**
- **4 divinités égyptiennes** avec leurs schémas détaillés :
  1. **Sekhmet** 🦁
     - Tête de lionne avec crinière
     - Disque solaire rouge sur la tête
     - Sceptre ouas
     - Hiéroglyphes : 𓌂𓅓𓏏𓆗
  
  2. **Anubis** 🐺
     - Tête de chacal noir
     - Longues oreilles pointues
     - Gardien des morts
     - Hiéroglyphes : 𓇋𓈖𓊪𓅱
  
  3. **Khépri** 🪲
     - Tête de scarabée
     - Symbolise le soleil levant
     - Hiéroglyphes : 𓆣𓂋𓇋
  
  4. **Seth** 🦎
     - Tête d'animal mystérieux
     - Longues oreilles carrées
     - Dieu du chaos
     - Hiéroglyphes : 𓃩𓏏𓁀

**Rôle de User1 :**
- Observer les schémas
- Identifier **Sekhmet** (la bonne réponse)
- Guider User2 via le **chat** en décrivant :
  - La forme de la tête
  - Les attributs (disque solaire)
  - Les hiéroglyphes à reproduire

**Communication :**
- Chat en temps réel avec User2
- Doit décrire les hiéroglyphes un par un

**Réception du résultat :**
```javascript
websocket.onmessage = (event) => {
  if (data.type === 'sekhmet_result') {
    if (result.success) {
      // Afficher popup de succès
      // Points : +300
    }
  }
}
```

---

## 🎭 Parcours User2 (Équipe 2)

### **Phase 1 : Attente & Interaction** ⏳

**Composant affiché :** Interface d'attente avec bouton

**Objectif :** Attendre que User1 résolve Chardin

**Ce que voit User2 :**
- Badge "Utilisateur 2"
- **Indicateur d'état du bouton** :
  - 🔒 Désactivé : "En attente que User 1 résolve l'énigme de Chardin..."
  - 🔓 Activé : "Cliquez sur le bouton pour activer l'Utilisateur 1"

**Fonctionnalités :**
- Bouton d'interaction (alternance avec User1)
- Chat en temps réel
- Système d'activation mutuelle

**Interaction bouton :**
```javascript
handleButtonClick() {
  if (isButtonEnabled.value) {
    websocket.send({
      action: 'button_click'
    })
  }
}
```

---

### **Phase 2 : Énigme Sekhmet - Rôle Valideur** 𓌂

**Composant affiché :** `HieroglyphKeyboard.vue`

**Objectif :** Reproduire le nom "SEKHMET" en hiéroglyphes

**Ce que voit User2 :**
- **Clavier hiéroglyphique** avec 12 symboles :
  - h1: 𓋴, h2: 𓊵, h3: 𓌂, h4: 𓐍
  - h5: 𓏏, h6: 𓅓, h7: 𓏤, h8: 𓆓
  - h9: 𓇋, h10: 𓆗, h11: 𓂋, h12: 𓅱

**Interface :**
- Zone d'affichage de la séquence saisie
- Bouton "⌫ Effacer" (dernier symbole)
- Bouton "🗑️ Tout effacer"
- Bouton de validation

**Workflow :**
1. User1 décrit les hiéroglyphes via le chat
2. User2 clique sur les symboles pour composer le mot
3. Aperçu en temps réel : 𓌂𓅓𓏏𓆗
4. Confirmation : "Êtes-vous sûr(e) de votre réponse ?"
5. Validation finale

**Code correct :** `h3-h6-h5-h10`
- h3 : 𓌂
- h6 : 𓅓
- h5 : 𓏏
- h10 : 𓆗

**Validation :**
```javascript
handleSekhmetValidate(data) {
  websocket.send({
    action: 'validate_sekhmet',
    hieroglyph_code: data.hieroglyph_code
  })
}
```

**Résultat :**
- ✅ Succès → Notification de succès + 300 points
- ❌ Échec → Message d'erreur, nouvelle tentative

---

## 🔄 Flux de communication WebSocket

### **Messages reçus par User1 :**
```javascript
{
  type: 'chardin_result',
  result: { success: true/false, message: "..." }
}

{
  type: 'sekhmet_schemas',
  enigma: {
    title: "La Fille de Rê",
    riddle: "...",
    divinities: [...]
  }
}

{
  type: 'sekhmet_result',
  result: { success: true/false, message: "..." }
}

{
  type: 'chat_history',
  messages: [...]
}

{
  type: 'chat_message',
  message: { user_id: "...", text: "...", timestamp: "..." }
}
```

### **Messages reçus par User2 :**
```javascript
{
  type: 'button_state',
  enabled: true/false
}

{
  type: 'sekhmet_selection',
  divinities: [{ id: "sekhmet", name: "Sekhmet" }, ...]
}

{
  type: 'sekhmet_result',
  result: { success: true/false, message: "..." }
}

{
  type: 'chat_history',
  messages: [...]
}

{
  type: 'chat_message',
  message: { user_id: "...", text: "...", timestamp: "..." }
}
```

---

## 🎯 Progression du jeu

```
┌────────────────────────────────────────┐
│            DÉBUT DU JEU                │
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│  User1 : Énigme Chardin               │
│  User2 : Attente (bouton désactivé)   │
└────────────────────────────────────────┘
              ↓ (Code: 3563)
┌────────────────────────────────────────┐
│  ✅ Chardin résolu (+100 points)      │
│  Déblocage de l'énigme Sekhmet        │
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│  User1 : Schémas des 4 divinités      │
│  User2 : Clavier hiéroglyphique       │
│  Chat : Communication active           │
└────────────────────────────────────────┘
              ↓ (h3-h6-h5-h10)
┌────────────────────────────────────────┐
│  ✅ Sekhmet identifié (+300 points)   │
│  Score total : 400 points              │
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│            JEU TERMINÉ                 │
└────────────────────────────────────────┘
```

---

## 📦 Composants utilisés

### **Communs aux deux users :**
- `ChatBox.vue` - Chat en temps réel

### **User1 uniquement :**
- `EnigmeChardin.vue` - Énigme initiale
- `SchemaSekhmet.vue` - Schémas des divinités (guide)
- `SuccessPopup.vue` - Popup de succès Chardin

### **User2 uniquement :**
- `HieroglyphKeyboard.vue` - Clavier pour écrire les hiéroglyphes
- Interface de bouton (intégrée dans User2.vue)

---

## 🎨 Design & UX

### **User1 (Équipe 1) :**
- Couleur : Violet/Bleu (`#667eea` → `#764ba2`)
- Rôle : **Leader / Guide**
- Badge : 👤 Utilisateur 1

### **User2 (Équipe 2) :**
- Couleur : Rose/Rouge (`#f093fb` → `#f5576c`)
- Rôle : **Exécutant / Valideur**
- Badge : 👤 Utilisateur 2

### **Points d'interaction :**
- Chat synchronisé
- Notifications en temps réel
- Transitions fluides entre les phases
- Feedback visuel sur les actions

---

## 📝 Notes importantes

1. **Collaboration obligatoire** : Les deux joueurs doivent communiquer
2. **Ordre des énigmes** : Chardin → Sekhmet (séquentiel)
3. **Validation** : Seul User2 peut valider Sekhmet
4. **Guide** : Seul User1 voit les schémas détaillés
5. **Score partagé** : Les deux users partagent le même score d'équipe

---

## 🔧 Adaptation pour votre architecture

Pour intégrer ces parcours dans votre architecture team1/team2 :

1. Remplacer `user1` → `team1`
2. Remplacer `user2` → `team2`
3. Utiliser votre système de team_id personnalisé
4. Intégrer dans vos tables MySQL existantes
5. Respecter vos clés composites (team_id, player_id)

**Les parcours sont parfaitement adaptables ! 🎯**
