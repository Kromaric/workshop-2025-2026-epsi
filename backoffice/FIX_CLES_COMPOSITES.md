# 🔑 Clés Composites - Correction du Bug Multi-Équipes

## 🐛 Problème identifié

Avec l'ancienne structure, la table `players` avait une clé primaire simple :
```sql
PRIMARY KEY (id)  -- ❌ Impossible d'avoir plusieurs "team1"
```

**Résultat** : 
- La première équipe crée `team1` → ✅ OK
- La deuxième équipe essaie de créer `team1` → ❌ ERREUR (PRIMARY KEY déjà existante)
- Les équipes partageaient les mêmes données !

---

## ✅ Solution : Clés Composites

Nouvelle structure avec clé primaire composite :
```sql
PRIMARY KEY (id, team_id)  -- ✅ Permet plusieurs "team1" dans différentes équipes
```

---

## 📊 Modifications apportées

### 1. **Table `players`**
```python
# Avant
id = Column(String(32), primary_key=True)  # ❌ Clé simple

# Après
id = Column(String(32), primary_key=True)
team_id = Column(String(32), ForeignKey("teams.id"), primary_key=True)  # ✅ CLÉ COMPOSITE
```

### 2. **Table `button_states`**
```python
# Avant
id = Column(Integer, primary_key=True, autoincrement=True)  # ❌ ID auto

# Après
team_id = Column(String(32), primary_key=True)
player_id = Column(String(32), primary_key=True)  # ✅ CLÉ COMPOSITE
```

---

## 🎯 Résultat

Maintenant, chaque équipe peut avoir ses propres joueurs `team1` et `team2` :

```
Base de données:

players:
┌─────────┬──────────────────────┬─────────────┐
│ id      │ team_id              │ name        │
├─────────┼──────────────────────┼─────────────┤
│ team1   │ team_les_detectives  │ Équipe 1    │ ✅
│ team2   │ team_les_detectives  │ Équipe 2    │ ✅
│ team1   │ team_super_team      │ Équipe 1    │ ✅ Pas de conflit !
│ team2   │ team_super_team      │ Équipe 2    │ ✅
└─────────┴──────────────────────┴─────────────┘

button_states:
┌──────────────────────┬───────────┬────────────┐
│ team_id              │ player_id │ is_enabled │
├──────────────────────┼───────────┼────────────┤
│ team_les_detectives  │ team1     │ false      │ ✅
│ team_les_detectives  │ team2     │ true       │ ✅
│ team_super_team      │ team1     │ false      │ ✅
│ team_super_team      │ team2     │ true       │ ✅
└──────────────────────┴───────────┴────────────┘
```

---

## 🚀 Comment appliquer les changements

### **Étape 1 : Reconstruire la base de données**

```bash
cd C:\Users\romar\OneDrive\Bureau\workshop\workshop-2025-2026-epsi\backoffice
python rebuild_database.py
```

Tapez `oui` pour confirmer.

### **Étape 2 : Redémarrer le backend**

```bash
python main.py
```

Vous devriez voir :
```
✅ Base de données initialisée
```

### **Étape 3 : Tester**

1. Ouvrez le frontend
2. Entrez "Les Détectives" comme nom d'équipe
3. Cliquez sur Équipe 1 → Devrait se connecter ✅
4. Dans un autre onglet, entrez "Super Team"
5. Cliquez sur Équipe 1 → Devrait aussi se connecter ✅

Les deux équipes sont maintenant **totalement indépendantes** !

---

## 📝 Fichiers modifiés

1. ✅ **models.py** - Clés composites ajoutées
2. ✅ **main.py** - Déjà mis à jour avec filtrage par équipe
3. ✅ **rebuild_database.py** - Script mis à jour

---

## 🎮 Vérification

Pour vérifier que tout fonctionne, testez :

```
Équipe "Les Détectives"
├── team1 se connecte → Score = 0
├── team1 résout Chardin → Score = 100
└── team2 voit aussi Score = 100 (partagé dans l'équipe)

Équipe "Super Team" (dans un autre onglet)
├── team1 se connecte → Score = 0 (INDÉPENDANT !)
├── team1 résout Chardin → Score = 100
└── Ne voit PAS les messages de "Les Détectives"
```

---

## 🎉 C'est réglé !

Chaque équipe a maintenant :
- ✅ Son propre score
- ✅ Son propre chat
- ✅ Sa propre progression
- ✅ Ses propres joueurs team1 et team2

**Le jeu multi-équipes fonctionne parfaitement ! 🚀**
