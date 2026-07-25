import os
import json
import random
from google import genai
from google.genai import types

def get_genai_client(api_key: str = None):
    """Initialise le client Gemini avec la clé d'API."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)

def generate_scenario(client):
    """Génère un cas pratique dynamique à l'aide de l'IA."""
    if client is None:
        return {
            "title": "Alerte aux fausses informations",
            "desc": "Une vidéo accusant une personnalité circule rapidement sur les réseaux sociaux. Vos proches vous demandent de la partager.",
            "options": [
                "Transférer le message immédiatement",
                "Vérifier la source avant toute action",
                "Ignorer complètement le message"
            ]
        }

    # Liste de thèmes pour garantir la variété des cas
    themes = [
        "cyberharcèlement et réseaux sociaux",
        "droits d'auteur et propriété intellectuelle",
        "usurpation d'identité et arnaque Mobile Money",
        "diffamation en ligne et droit à l'image",
        "fake news et manipulation de l'information",
        "civisme numérique et respect de la vie privée"
    ]
    theme_choisi = random.choice(themes)

    prompt = f"""
    Génère un cas pratique réaliste axé sur le contexte de la Côte d'Ivoire concernant le thème suivant : {theme_choisi}.
    Le cas doit présenter une situation dilemme du quotidien.

    Renvoie UNIQUEMENT un objet JSON valide respectant cette structure exacte :
    {{
        "title": "Titre court et percutant",
        "desc": "Description du cas pratique (2 à 3 phrases)",
        "options": [
            "Option de réaction 1",
            "Option de réaction 2",
            "Option de réaction 3"
        ]
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erreur de génération : {e}")
        return {
            "title": "Cyber-prudence",
            "desc": "Vous recevez un SMS vous informant que vous avez gagné un lot, mais on vous demande d'envoyer des frais de dossier.",
            "options": [
                "Payer les frais immédiatement",
                "Bloquer le numéro et signaler l'arnaque",
                "Demander l'avis d'un proche"
            ]
        }

def evaluate_player_choice(client, scenario_title, scenario_desc, choice):
    """Évalue la réaction du joueur selon les axes légal, éthique et médiatique."""
    if client is None:
        return {
            "niveau_adequation": "Indisponible",
            "debriefing": {
                "juridique": "Défaut d'analyse : Clé API manquante.",
                "medias_verite": "Indisponible.",
                "ethique_civisme": "Indisponible."
            },
            "conseil_judicieux": "Vérifiez votre configuration ou votre fichier .env."
        }

    prompt = f"""
    Évalue la réaction d'un utilisateur face au cas suivant :
    - Titre : {scenario_title}
    - Description : {scenario_desc}
    - Choix de l'utilisateur : {choice}

    Renvoie un objet JSON structuré comme suit :
    {{
        "niveau_adequation": "Excellente / Modérée / Risquée",
        "debriefing": {{
            "juridique": "Explication sur le plan du droit et de la réglementation en Côte d'Ivoire.",
            "medias_verite": "Explication sur le discernement médiatique et la recherche de vérité.",
            "ethique_civisme": "Explication éthique et civique."
        }},
        "conseil_judicieux": "Un conseil pratique et bienveillant pour l'avenir."
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erreur d'évaluation : {e}")
        return {
            "niveau_adequation": "Analyse indisponible",
            "debriefing": {
                "juridique": f"Défaut d'analyse technique : {e}",
                "medias_verite": "Indisponible.",
                "ethique_civisme": "Indisponible."
            },
            "conseil_judicieux": "Vérifiez votre connexion internet ou votre clé API Gemini."
        }
