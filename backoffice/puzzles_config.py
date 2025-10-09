"""
Configuration des énigmes et leur système de points
"""

PUZZLES_CONFIG = {
    "chardin": {
        "name": "L'Énigme de Chardin",
        "description": "Trouver le code caché dans les tableaux",
        "correct_code": "3563",
        "points": 100,
        "restricted_to": ["team1"],  # Seul team1 peut résoudre
        "hints": [
            "Regardez attentivement les tableaux...",
            "Les chiffres sont cachés dans les détails",
            "Essayez de compter certains éléments"
        ]
    },
    
    "tableau_bleu": {
        "name": "Le Tableau Bleu",
        "description": "Déchiffrer le message du tableau bleu",
        "correct_code": "AZURE",
        "points": 150,
        "restricted_to": None,  # Tous les joueurs peuvent résoudre
        "hints": [
            "La couleur est importante...",
            "Pensez aux nuances de bleu"
        ]
    },
    
    "musee_secret": {
        "name": "Le Secret du Musée",
        "description": "Découvrir le secret caché du musée",
        "correct_code": "1789",
        "points": 200,
        "restricted_to": None,
        "hints": [
            "Regardez l'année de fondation...",
            "C'est une date importante en France",
            "Révolution..."
        ]
    },
    
    # Ajoutez vos énigmes ici...
}


def get_puzzle_config(puzzle_name: str) -> dict:
    """Récupère la configuration d'une énigme"""
    return PUZZLES_CONFIG.get(puzzle_name)


def get_all_puzzles() -> dict:
    """Récupère toutes les énigmes"""
    return PUZZLES_CONFIG


def get_total_possible_points() -> int:
    """Calcule le total de points possibles"""
    return sum(puzzle["points"] for puzzle in PUZZLES_CONFIG.values())


def is_player_allowed(puzzle_name: str, player_id: str) -> bool:
    """Vérifie si un joueur peut résoudre une énigme"""
    puzzle = PUZZLES_CONFIG.get(puzzle_name)
    if not puzzle:
        return False
    
    restricted_to = puzzle.get("restricted_to")
    if restricted_to is None:
        return True
    
    return player_id in restricted_to


# Exemple d'utilisation dans main.py:
"""
from puzzles_config import get_puzzle_config, is_player_allowed

async def validate_puzzle(self, team_id: str, player_id: str, puzzle_name: str, code: str, db: Session):
    # Récupérer la config de l'énigme
    puzzle_config = get_puzzle_config(puzzle_name)
    if not puzzle_config:
        return {"success": False, "message": "Énigme inconnue"}
    
    # Vérifier les restrictions
    if not is_player_allowed(puzzle_name, player_id):
        restricted = puzzle_config.get("restricted_to", [])
        return {
            "success": False,
            "message": f"Cette énigme est réservée à {', '.join(restricted)}"
        }
    
    # Vérifier si déjà résolu
    progress = db.query(Progress).filter(
        Progress.team_id == team_id,
        Progress.puzzle_name == puzzle_name
    ).first()

    if not progress:
        progress = Progress(
            team_id=team_id,
            player_id=player_id,
            puzzle_name=puzzle_name
        )
        db.add(progress)
        db.commit()

    if progress.is_solved:
        return {"success": False, "message": "Déjà résolu"}

    progress.attempts += 1

    if code.upper() == puzzle_config["correct_code"].upper():
        progress.is_solved = True
        progress.solved_at = datetime.now()
        progress.points_earned = puzzle_config["points"]
        
        team = db.query(Team).filter(Team.id == team_id).first()
        if team:
            team.score += progress.points_earned
        
        db.commit()
        await self.broadcast_progress(team_id, db)

        return {
            "success": True,
            "message": f"Bravo ! {puzzle_config['name']} résolu ! 🎉",
            "points": progress.points_earned
        }
    else:
        db.commit()
        return {
            "success": False,
            "message": "Code incorrect. " + (puzzle_config["hints"][0] if progress.attempts >= 3 else "")
        }
"""
