import streamlit as st
from utils.game_engine import get_genai_client, generate_scenario, evaluate_player_choice
import streamlit as st
from dotenv import load_dotenv  # <-- AJOUTER CECI

# Charge le fichier .env
load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Yeshualais", page_icon="🇨🇮", layout="centered")

# ==============================================================================
# INJECTION DU STYLE CSS (Montserrat + Polices Agrandies)
# ==============================================================================
st.markdown("""
    <style>
    /* Import de la police Montserrat depuis Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    /* 1. Arrière-plan global en dégradé Violet -> Noir sombre */
    .stApp {
        background: linear-gradient(180deg, #5D3EBF 0%, #121124 45%, #0B0B14 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Masquer les éléments Streamlit inutiles */
    #MainMenu, header, footer {visibility: hidden;}

    /* 2. Conteneur principal (Carte de question sombre) */
    .quiz-card {
        background-color: #1A1832;
        border-radius: 24px;
        padding: 35px 28px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 25px;
        text-align: center;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Titres et textes dans la carte */
    .quiz-title {
        color: #A0A0C0;
        font-size: 15px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .quiz-subtitle {
        color: #FFFFFF;
        font-size: 28px; /* Agrandie */
        font-weight: 800;
        margin-bottom: 18px;
    }

    .quiz-subtitle span {
        color: #FF6B00; /* Touche Orange */
    }

    .quiz-scenario {
        color: #E2E2EC;
        font-size: 18px; /* Agrandie */
        line-height: 1.6;
        font-weight: 500;
        background: rgba(255, 255, 255, 0.03);
        padding: 18px;
        border-radius: 12px;
        border-left: 4px solid #FF6B00;
        text-align: left;
    }

    /* 3. Style et Centrage global des Boutons Streamlit (Propositions) */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button {
        background-color: #161528 !important;
        color: #FFFFFF !important;
        border: 1px solid #2D2B4A !important;
        border-radius: 16px !important;
        padding: 18px 24px !important;
        font-size: 17px !important; /* Agrandie */
        font-weight: 600 !important;
        font-family: 'Montserrat', sans-serif !important;
        line-height: 1.4 !important;
        text-align: center !important;
        margin: 0 auto 12px auto !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Effet d'ouverture / Survol */
    div.stButton > button:hover {
        border-color: #FF6B00 !important;
        background-color: #211F3B !important;
        color: #FF6B00 !important;
        transform: translateY(-2px);
    }

    /* 4. Bouton principal d'action (Démarrer / Suivant) -> ORANGE PUNCHY */
    .stButton.btn-primary > button {
        background: linear-gradient(90deg, #FF6B00 0%, #FF8800 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 18px 36px !important;
        font-size: 20px !important; /* Agrandie */
        font-weight: 700 !important;
        text-align: center !important;
        box-shadow: 0px 8px 20px rgba(255, 107, 0, 0.35) !important;
    }

    .stButton.btn-primary > button:hover {
        box-shadow: 0px 12px 25px rgba(255, 107, 0, 0.5) !important;
        transform: scale(1.02);
    }

    /* Cartes de debriefing */
    .debrief-card {
        background-color: #1A1832;
        border-radius: 16px;
        padding: 22px;
        margin-top: 16px;
        border: 1px solid #2D2B4A;
        font-family: 'Montserrat', sans-serif !important;
    }

    .debrief-header {
        font-size: 18px; /* Agrandie */
        font-weight: 700;
        color: #FF6B00;
        margin-bottom: 10px;
    }

    .debrief-text {
        color: #D1D1E0;
        font-size: 16px; /* Agrandie */
        line-height: 1.6;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation du client AI
client = get_genai_client()

# Gestion des états de la session
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None
if "selected_analysis" not in st.session_state:
    st.session_state.selected_analysis = None

# ==============================================================================
# ÉCRAN 1 : ACCUEIL
# ==============================================================================
if not st.session_state.game_started:
    st.markdown("""
        <div class="quiz-card" style="margin-top: 50px;">
            <div class="quiz-title">très chers</div>
            <div class="quiz-subtitle">🧡 Yeshualais 🧡</div>
            <p style="color: #A0A0C0; font-size: 17px; font-weight: 500; line-height: 1.5;">
                Développez votre discernement face aux pièges du numérique, du droit et de l'éthique au quotidien.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Bouton de démarrage centré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Démarrer la partie", use_container_width=True):
            with st.spinner("Génération du scénario..."):
                st.session_state.current_scenario = generate_scenario(client)
                st.session_state.game_started = True
                st.session_state.selected_analysis = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# ÉCRAN 2 : APPLICATION & QUESTIONS
# ==============================================================================
else:
    scenario = st.session_state.current_scenario

    # Carte style "Question 01" de la maquette
    st.markdown(f"""
        <div class="quiz-card">
            <div class="quiz-title">Cas Pratique</div>
            <div class="quiz-subtitle"><span>{scenario['title']}</span></div>
            <div class="quiz-scenario">
                "{scenario['desc']}"
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Si aucune analyse n'a été demandée, on affiche les options
    if st.session_state.selected_analysis is None:
        st.markdown("<p style='color: #A0A0C0; font-weight:600; font-size: 17px; margin-bottom: 16px; text-align: center;'>Choisissez votre réaction :</p>", unsafe_allow_html=True)
        
        # Affichage centré des propositions
        for idx, option in enumerate(scenario['options']):
            if st.button(f"{option}", key=f"opt_{idx}", use_container_width=True):
                with st.spinner("Analyse légale et éthique en cours..."):
                    st.session_state.selected_analysis = evaluate_player_choice(
                        client, scenario['title'], scenario['desc'], option
                    )
                    st.rerun()

    # Si l'analyse a été générée, on affiche le Bilan
    else:
        res = st.session_state.selected_analysis
        
        # Statut d'adéquation
        st.markdown(f"""
            <div style="text-align: center; background: #251F47; padding: 14px; border-radius: 12px; border: 1px solid #FF6B00; margin-bottom: 20px;">
                <span style="color: #A0A0C0; font-size: 16px; font-weight: 500;">Adéquation de l'action :</span> 
                <strong style="color: #FF6B00; font-size: 20px; margin-left: 8px;">{res.get('niveau_adequation', 'Évalué')}</strong>
            </div>
        """, unsafe_allow_html=True)

        # Cartes explicatives
        st.markdown(f"""
            <div class="debrief-card">
                <div class="debrief-header">⚖️ Volet Juridique (Droit Ivoirien)</div>
                <div class="debrief-text">{res['debriefing']['juridique']}</div>
            </div>
            
            <div class="debrief-card">
                <div class="debrief-header">🔍 Discernement & Médias</div>
                <div class="debrief-text">{res['debriefing']['medias_verite']}</div>
            </div>
            
            <div class="debrief-card">
                <div class="debrief-header">📜 Éthique & Sagesse Biblique</div>
                <div class="debrief-text">{res['debriefing']['ethique_civisme']}</div>
            </div>
            
            <div class="debrief-card" style="border-left: 4px solid #00E676;">
                <div class="debrief-header" style="color: #00E676;">💡 Conseil Citoyen</div>
                <div class="debrief-text">{res.get('conseil_judicieux')}</div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        
        # Bouton Suivant Orange
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Cas suivant ➔", use_container_width=True):
            with st.spinner("Chargement..."):
                st.session_state.current_scenario = generate_scenario(client)
                st.session_state.selected_analysis = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)        "choices": [
            "Ajouter un commentaire moqueur pour 'faire comme tout le monde'.",
            "Avertir immédiatement un adulte référent et effectuer un signalement officiel.",
            "Envoyer un message privé insultant au créateur de la vidéo originale."
        ]
    },
    {
        "id": 3,
        "title": "Arnaque Wave / Mobile Money",
        "category": "Sécurité Numérique",
        "desc": "Vous recevez un SMS prétendant qu'un transfert Mobile Money de 25 000 FCFA a été effectué par erreur sur votre compte. Un inconnu vous appelle immédiatement en pleurant pour que vous lui renvoyiez l'argent.",
        "choices": [
            "Renvoyer immédiatement les 25 000 FCFA sans vérifier le solde.",
            "Consulter son solde réel via le code officiel USSD/Application puis contacter le service client.",
            "Insulter l'expéditeur du message pour lui donner une leçon."
        ]
    },
    {
        "id": 4,
        "title": "Faux Profil & Usurpation",
        "category": "Vie Privée & Droit",
        "desc": "Vous découvrez qu'un compte Facebook utilise la photo et le nom complet d'une de vos connaissances pour publier des propos politiques violents et injurieux.",
        "choices": [
            "Signaler le faux profil sur la plateforme et informer la personne concernée.",
            "Partager les publications du faux compte sur votre propre mur.",
            "Envoyer un message de menace en privé au compte usurpateur."
        ]
    },
    {
        "id": 5,
        "title": "Offre d'Emploi Suspecte",
        "category": "Prudence & Citoyenneté",
        "desc": "Sur LinkedIn, un recruteur propose un stage très rémunéré, mais demande d'envoyer une copie recto-verso de votre CNI ainsi qu'un paiement de 5 000 FCFA pour 'frais de dossier'.",
        "choices": [
            "Payer la somme immédiatement pour ne pas rater cette chance.",
            "Refuser d'envoyer de l'argent et vérifier la légitimité de l'entreprise.",
            "Envoyer sa CNI mais refuser de payer les 5 000 FCFA."
        ]
    }
]

# --- CSS COMPLET AVEC ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    .stAppDeployButton {display: none;}

    .stApp {
        background: radial-gradient(circle at top, #7C3AED 0%, #0F172A 70%);
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    .scenario-card {
        background: rgba(30, 41, 59, 0.92);
        backdrop-filter: blur(12px);
        padding: 2.3rem 2rem;
        border-radius: 28px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }

    .scenario-title { font-size: 1.85rem; margin: 1rem 0; animation: fadeInUp 0.7s ease-out 0.2s both; }
    .scenario-desc { animation: fadeInUp 0.7s ease-out 0.4s both; }

    /* Boutons choix avec cascade */
    div.stButton { animation: fadeInUp 0.5s ease-out both; }
    div.stButton:nth-of-type(1) { animation-delay: 0.1s; }
    div.stButton:nth-of-type(2) { animation-delay: 0.25s; }
    div.stButton:nth-of-type(3) { animation-delay: 0.4s; }

    div.stButton > button {
        width: 100% !important;
        max-width: 520px !important;
        margin: 0.7rem auto !important;
        background: rgba(255,255,255,0.06) !important;
        border: 1.5px solid rgba(255,255,255,0.18) !important;
        color: #E2E8F0 !important;
        font-size: 1.06rem !important;
        padding: 1.35rem 1.6rem !important;
        border-radius: 20px !important;
        transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        background: rgba(249, 115, 22, 0.28) !important;
        border-color: #F97316 !important;
        box-shadow: 0 15px 30px rgba(249, 115, 22, 0.4) !important;
    }

    /* Bilan */
    .bilan-card {
        background: rgba(30, 41, 59, 0.95);
        border-radius: 24px;
        padding: 2.2rem;
        margin: 2rem 0;
        border: 1px solid rgba(249, 115, 22, 0.3);
        box-shadow: 0 15px 40px rgba(0,0,0,0.35);
        animation: fadeInScale 0.6s ease-out;
    }

    .score-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 1.8rem 0;
        flex-wrap: wrap;
    }

    .score-item { text-align: center; }
    .score-value { font-size: 2.4rem; font-weight: 700; margin: 0.2rem 0; }
    .score-label { font-size: 0.95rem; color: #94A3B8; }

    .debrief-section {
        background: rgba(255,255,255,0.05);
        border-left: 5px solid #F97316;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: fadeInUp 0.5s ease-out;
    }

    .conseil {
        background: linear-gradient(90deg, rgba(16,185,129,0.18), rgba(16,185,129,0.06));
        border: 1px solid #10B981;
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 1.8rem;
        animation: fadeInUp 0.7s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "game_started" not in st.session_state: st.session_state.game_started = False
if "game_finished" not in st.session_state: st.session_state.game_finished = False
if "score_citoyen" not in st.session_state: st.session_state.score_citoyen = 0
if "score_verite" not in st.session_state: st.session_state.score_verite = 0
if "score_legalite" not in st.session_state: st.session_state.score_legalite = 0
if "current_scenario_index" not in st.session_state: st.session_state.current_scenario_index = 0
if "current_analysis" not in st.session_state: st.session_state.current_analysis = None
if "choice_made" not in st.session_state: st.session_state.choice_made = False

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def get_current_scenario():
    idx = st.session_state.current_scenario_index
    return SCENARIOS_DATABASE[idx] if idx < len(SCENARIOS_DATABASE) else None

def next_question():
    st.session_state.current_scenario_index += 1
    st.session_state.current_analysis = None
    st.session_state.choice_made = False
    if st.session_state.current_scenario_index >= len(SCENARIOS_DATABASE):
        st.session_state.game_finished = True

# Sidebar
with st.sidebar:
    st.title("Tableau de Bord")
    api_key = os.getenv("GEMINI_API_KEY") or st.text_input("Clé API Gemini", type="password")
    if st.button("Recommencer la partie"):
        reset_game()

# ==================== ACCUEIL ====================
if not st.session_state.game_started:
    st.markdown("""
        <div class="scenario-card" style="margin-top: 3rem;">
            <div class="scenario-id">Bienvenue sur</div>
            <div class="scenario-title" style="font-size: 2.4rem; color: #F97316;">CITOYEN COPILOT C.I.</div>
            <div class="scenario-desc">
                Testez vos réflexes civiques et juridiques face aux défis numériques en Côte d'Ivoire.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Débuter la Partie", type="primary", key="start"):
        st.session_state.game_started = True
        st.rerun()

# ==================== JEU ====================
elif st.session_state.game_started and not st.session_state.game_finished:
    current = get_current_scenario()
    if current:
        st.markdown(f"""
            <div class="scenario-card">
                <div class="scenario-id">Dilemme {st.session_state.current_scenario_index + 1} / {len(SCENARIOS_DATABASE)} • {current['category']}</div>
                <div class="scenario-title">{current['title']}</div>
                <div class="scenario-desc">{current['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.choice_made:
            st.markdown("<h3 style='text-align:center; margin: 2.5rem 0 1.8rem;'>Que faites-vous ?</h3>", unsafe_allow_html=True)
            
            for i, choice in enumerate(current["choices"]):
                col = st.columns([1, 4, 1])
                with col[1]:
                    if st.button(choice, key=f"opt_{i}", use_container_width=True):
                        if not api_key:
                            st.error("Clé API manquante.")
                        else:
                            client = get_genai_client(api_key)
                            with st.spinner("Analyse juridique et éthique en cours..."):
                                result = evaluate_player_choice(client, current["title"], current["desc"], choice)
                                st.session_state.score_citoyen += result.get("score_citoyennete", 0)
                                st.session_state.score_verite += result.get("score_verite", 0)
                                st.session_state.score_legalite += result.get("score_legalite", 0)
                                st.session_state.current_analysis = result
                                st.session_state.choice_made = True
                                st.rerun()

        # BILAN (Inclus à l'intérieur du contrôle st.session_state.choice_made)
        if st.session_state.choice_made and st.session_state.current_analysis:
            res = st.session_state.current_analysis

            st.markdown('<div class="bilan-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center; color:#F97316; margin-bottom:1.5rem;'>Bilan de votre Décision</h3>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class="score-container">
                    <div class="score-item"><div class="score-label">Civisme</div><div class="score-value" style="color:#F97316;">{res.get('score_citoyennete', 0)}</div></div>
                    <div class="score-item"><div class="score-label">Vérité</div><div class="score-value" style="color:#60A5FA;">{res.get('score_verite', 0)}</div></div>
                    <div class="score-item"><div class="score-label">Loi C.I.</div><div class="score-value" style="color:#34D399;">{res.get('score_legalite', 0)}</div></div>
                </div>
            """, unsafe_allow_html=True)

            for title, key in [
                ("📜 Cadre Juridique Ivoirien", "juridique"),
                ("📰 Éducation aux Médias", "medias_verite"),
                ("🤝 Impact Civique", "ethique_civisme")
            ]:
                if res.get("debriefing") and res["debriefing"].get(key):
                    st.markdown(f"""
                        <div class="debrief-section">
                            <strong>{title}</strong><br>{res["debriefing"][key]}
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="conseil">
                    <strong style="color:#34D399;">💡 Conseil Citoyen</strong><br>
                    {res.get('conseil_judicieux', 'Continuez à cultiver votre esprit critique !')}
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Navigation
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Dilemme Suivant", type="primary", use_container_width=True):
                    next_question()
                    st.rerun()
            with col2:
                if st.button("Quitter la partie", use_container_width=True):
                    st.session_state.game_finished = True
                    st.rerun()

# ==================== ÉCRAN FINAL ====================
else:
    total_scenarios = len(SCENARIOS_DATABASE)
    score_total = st.session_state.score_citoyen + st.session_state.score_verite + st.session_state.score_legalite
    max_possible = total_scenarios * 30  # Max si 10pts par critère par scenario

    # Détermination du profil citoyen en fonction du score global
    if score_total >= max_possible * 0.8:
        profil_title = "🏆 Citoyen Modèle & Éclairé"
        profil_desc = "Excellents réflexes ! Vous maîtrisez la vérification d'information, le respect des lois numériques et la bienveillance en ligne."
        profil_color = "#34D399"
    elif score_total >= max_possible * 0.5:
        profil_title = "🛡️ Citoyen Prudent mais Vigilant"
        profil_desc = "Bon parcours global ! Quelques petits détails juridiques ou d'esprit critique restent à affiner, mais vos intentions sont très civiques."
        profil_color = "#60A5FA"
    else:
        profil_title = "⚠️ Citoyen en Apprentissage"
        profil_desc = "Certains pièges du Web vous ont eu ! Prenez le temps de bien vérifier les sources et de connaître vos droits et devoirs numériques."
        profil_color = "#F97316"

    # Carte de fin de partie
    st.markdown(f"""
        <div class="scenario-card">
            <div class="scenario-id">FIN DE LA SESSION</div>
            <div class="scenario-title" style="color: {profil_color};">{profil_title}</div>
            <div class="scenario-desc" style="margin-top: 1rem;">
                {profil_desc}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Récapitulatif visuel des scores
    st.markdown(f"""
        <div class="bilan-card">
            <h3 style="text-align:center; color:#F97316; margin-bottom:1.5rem;">Bilan Global de vos Décisions</h3>
            <div class="score-container">
                <div class="score-item">
                    <div class="score-label">Civisme Total</div>
                    <div class="score-value" style="color:#F97316;">{st.session_state.score_citoyen}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Vérité Totale</div>
                    <div class="score-value" style="color:#60A5FA;">{st.session_state.score_verite}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Loi C.I. Total</div>
                    <div class="score-value" style="color:#34D399;">{st.session_state.score_legalite}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Action pour rejouer
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🔄 Lancer une Nouvelle Partie", type="primary", use_container_width=True):
            reset_game()
