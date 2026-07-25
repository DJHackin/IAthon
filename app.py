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
        st.markdown('</div>', unsafe_allow_html=True)
