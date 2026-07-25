import json
import os
from google import genai
from google.genai import types

def get_genai_client(api_key: str = None):
    """
    Initialise et retourne le client officiel Google GenAI.
    Recherche la clé passée en paramètre ou dans les variables d'environnement.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)


def generate_scenario(client: genai.Client) -> dict:
    """
    Génère dynamiquement un scénario/cas pratique hyper pertinent et ancré 
    dans le contexte socioculturel et numérique de la Côte d'Ivoire.
    """
    system_instruction = """Tu es un concepteur pédagogique expert en civisme, droit et éthique en Côte d'Ivoire.
Génère une situation/cas pratique réaliste auquel un citoyen ivoirien (jeune, professionnel, étudiant) peut être confronté au quotidien.

THÉMATIQUES POSSIBLES (varie à chaque fois) :
- Rumeurs et fausses informations sur WhatsApp / Facebook / TikTok (ex: grèves, alertes sécuritaires, scandales).
- Arnaques et transactions suspectes sur Mobile Money (Orange, Wave, MTN, Moov).
- Droit à l'image et publication de vidéos sans consentement (ex: bagarres, accidents).
- Civisme routier et comportements face aux forces de l'ordre.
- Diffamation ou cyberharcèlement dans des groupes communautaires.

EXIGENCES :
- Propose 3 choix d'action distincts (ex: réagir à chaud, vérifier/signaler, ignorer/complicité).
- Le ton doit être authentique et local (vocable clair, situations concrètes d'Abidjan ou de l'intérieur).

Réponds STRICTEMENT sous forme d'objet JSON respectant ce schéma sans texte additionnel :
{
  "title": "<Titre percutant du cas>",
  "desc": "<Description détaillée du contexte et du dilemme>",
  "options": [
    "<Option A : Choix d'action 1>",
    "<Option B : Choix d'action 2>",
    "<Option C : Choix d'action 3>"
  ]
}
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Génère un nouveau dilemme citoyen ivoirien unique et très concret.",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.7 # Température légèrement élevée pour varier les scénarios
            )
        )
        raw_text = response.text.strip()
        
        # Nettoyage des balises Markdown de code si présentes
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())

    except Exception as e:
        # Scénario de secours ivoirien en cas de problème réseau/API
        return {
            "title": "Alerte Rumeur sur WhatsApp",
            "desc": "Vous recevez un transfert d'un message audio alarmiste dans un groupe de famille indiquant une pénurie imminente d'eau et d'électricité à Abidjan. L'auteur demande de transférer à tous vos proches.",
            "options": [
                "Je transfère immédiatement le message dans tous mes autres groupes pour prévenir mes amis.",
                "Je vérifie d'abord l'information sur les pages officielles de la CIE/SODECI ou des médias reconnus avant toute action.",
                "Je réponds dans le groupe que c'est sûrement faux et j'insulte la personne qui a envoyé l'audio."
            ]
        }


def evaluate_player_choice(client: genai.Client, scenario_title: str, scenario_desc: str, player_choice: str) -> dict:
    """
    Évalue le choix du joueur sous l'angle du Droit Ivoirien moderne et de l'Éthique Biblique.
    Pas de mauvaise réponse, uniquement une analyse de la pertinence et de la maturité civique.
    """
    system_instruction = """Tu es un guide pédagogique et un copilote citoyen éclairé en Côte d'Ivoire.
Ta mission est d'analyser l'action choisie par le joueur avec bienveillance, discernement et pédagogie.
Aucune réponse n'est considérée comme "mauvaise" ou "interdite" : il s'agit d'évaluer dans quelle mesure l'action est adéquate, prudente ou mûre face à la situation.

DIRECTIVES D'ANALYSE STRICTES :

1. CADRE JURIDIQUE IVOIRIEN RÉCENT :
Appuie tes analyses légales sur la législation ivoirienne en vigueur, notamment :
- Le Nouveau Code Pénal ivoirien (Loi n° 2019-574 du 26 juin 2019) concernant la diffamation, les injures publiques, l'usurpation d'identité et les fausses nouvelles.
- La Loi n° 2013-451 relative à la cybercriminalité en Côte d'Ivoire.
- La Loi n° 2013-450 relative à la protection des données à caractère personnel.

2. VOLET ÉTHIQUE ET SAGESSE BIBLIQUE :
L'analyse éthique et civique doit se fonder sur les valeurs et principes de la Bible (ex: la recherche de la vérité, la prudence, l'amour du prochain, la recherche de la paix, le refus de la calomnie, la maîtrise de soi).
Intègre subtilement une référence ou une citation biblique pertinente (ex: Proverbes, Évangiles, Épîtres) pour éclairer la décision du joueur.

SITUATION À ÉVALUER :
- Scénario : {scenario_title}
- Contexte : {scenario_desc}
- Action choisie par le joueur : {player_choice}

TA MISSION :
Analyse le choix et réponds STRICTEMENT sous la forme d'un objet JSON valide respectant cette structure, sans aucun autre texte autour :

{{
  "niveau_adequation": "<Choisis parmi : 'Très adéquate', 'Moyennement adéquate' ou 'Peu adéquate'>",
  "debriefing": {{
    "juridique": "<Explication claire basée sur les textes de loi ivoiriens récents>",
    "medias_verite": "<Analyse du niveau de discernement et d'esprit critique face à l'information>",
    "ethique_civisme": "<Analyse éthique fondée sur les valeurs et principes bibliques, incluant une référence biblique adaptée (Livre Chapitre:Verset)>"
  }},
  "conseil_judicieux": "<Un conseil citoyen et spirituel d'encouragement pour guider le joueur vers une posture exemplaire>"
}}
"""

    prompt = system_instruction.format(
        scenario_title=scenario_title,
        scenario_desc=scenario_desc,
        player_choice=player_choice
    )

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())

    except Exception as e:
        return {
            "niveau_adequation": "Analyse indisponible",
            "debriefing": {
                "juridique": f"Défaut d'analyse technique : {str(e)}",
                "medias_verite": "Indisponible.",
                "ethique_civisme": "Indisponible."
            },
            "conseil_judicieux": "Vérifiez votre connexion internet ou votre clé API Gemini."
        }
