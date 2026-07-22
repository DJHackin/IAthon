import json
import os
from google import genai
from google.genai import types

def get_genai_client(api_key: str = None):
    """Initialise le client officiel Google GenAI."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)

def evaluate_player_choice(client: genai.Client, scenario_title: str, scenario_desc: str, player_choice: str) -> dict:
    """
    Évalue sévèrement le choix selon le droit ivoirien et renvoie un JSON.
    """
    
    system_instruction = """Tu es le moteur de notation impitoyable d'un jeu de simulation de citoyenneté ivoirienne éclairée.
Ton but est de sanctionner sévèrement les comportements irresponsables, illégaux ou naïfs, et de récompenser uniquement l'excellence éthique et légale.

CADRE JURIDIQUE DE RÉFÉRENCE STRICT :
Toutes tes analyses juridiques et légales doivent se baser STRICTEMENT sur :
1. La Constitution de la République de Côte d'Ivoire.
2. Le Code Pénal ivoirien.
3. La Loi n°2013-451 relative à la cybercriminalité en Côte d'Ivoire (très stricte sur la diffamation, les fausses nouvelles, et le droit à l'image).

MÉTHODE DE NOTATION DURE :
- Les jauges du joueur commencent à 0 (Neutre/Nouveau Citoyen). Ton but est de les faire monter par des actions héroïques ou de les faire plonger en négatif pour faute grave.
- Sanctionne lourdement (-20 à -50 points) : La complicité passive, la diffusion de fausses infos, le partage d'images sans consentement, l'insulte, la triche, l'inaction face à un crime.
- Récompense modérément (+5 à +15 points) : Le signalement officiel, la vérification des faits avant action, la médiation constructive. L'excellence est dure à atteindre.

SITUATION À ÉVALUER :
- Scénario : {scenario_title}
- Contexte : {scenario_desc}
- Action du Joueur : {player_choice}

TA MISSION :
Analyse selon le droit et le civisme ivoirien. Tu dois répondre STRICTEMENT sous la forme d'un objet JSON valide respectant cette structure, sans aucun autre texte :

{{
    "score_citoyennete": <nombre entier sévère, ex: +10 ou -30>,
    "score_verite": <nombre entier sévère, ex: +5 ou -40>,
    "score_legalite": <nombre entier sévère, ex: +15 ou -50>,
    "debriefing": {{
        "juridique": "<Explication froide et précise basée sur la législation ivoirienne, citant si possible la loi sur la cybercriminalité>",
        "medias_verite": "<Analyse du niveau de discernement face à l'information>",
        "ethique_civisme": "<Verdict éthique sur l'impact pour le vivre-ensemble en Côte d'Ivoire>"
    }},
    "conseil_judicieux": "<Un conseil direct et formateur pour adopter le comportement d'un citoyen ivoirien exemplaire>"
}}
"""

    prompt = system_instruction.format(
        scenario_title=scenario_title,
        scenario_desc=scenario_desc,
        player_choice=player_choice
    )

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash', # Utilisation du modèle stable
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1 # Plus factuel et sévère
            )
        )
        
        raw_text = response.text.strip()
        # Nettoyage minimal du JSON si nécessaire
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
        
    except Exception as e:
        # Fallback neutre en cas d'erreur
        return {
            "score_citoyennete": -5, # Punition pour l'erreur technique
            "score_verite": 0,
            "score_legalite": -5,
            "debriefing": {
                "juridique": f"Défaut technique d'analyse juridique : {str(e)}",
                "medias_verite": "Évaluation indisponible.",
                "ethique_civisme": "Impact inconnu."
            },
            "conseil_judicieux": "Vérifiez votre connexion ou votre clé API."
        }