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
