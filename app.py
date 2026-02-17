import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cloud.Cat Fitness & Music", page_icon="☁️", layout="wide")

# --- SELECCIÓN DE USUARIO ---
st.sidebar.header("👤 ¿Quién está cocinando?")
user = st.sidebar.radio("", ["Azul", "Alice"], horizontal=True)

# --- TEMAS POR USUARIO ---
if user == "Azul":
    # Tema oscuro azul neón
    bg_color = "#0a0a1a"
    text_color = "#ffffff"
    accent = "#00d4ff"
    accent_hover = "#00ffff"
    card_bg = "#1a1a2e"
    user_icon = "🎮"
    welcome = "¡Hola Azul! ¿Qué se te antoja hoy?"
else:
    # Tema claro rosa pastel
    bg_color = "#fff5f5"
    text_color = "#333333"
    accent = "#ff6b81"
    accent_hover = "#ff8fa3"
    card_bg = "#ffffff"
    user_icon = "💕"
    welcome = "¡Hola Alice! Vamos a cocinar algo delicioso"

# --- CSS DINÁMICO ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .main {{
        background: linear-gradient(135deg, {bg_color} 0%, {card_bg} 100%);
    }}
    .stButton>button {{
        background-color: {accent};
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {accent_hover};
        transform: scale(1.05);
        transition: all 0.3s;
    }}
    .user-badge {{
        background-color: {accent};
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }}
    .recipe-card {{
        background-color: {card_bg};
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid {accent};
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    h1, h2, h3 {{
        color: {accent} !important;
    }}
    .stTextArea>div>div>textarea {{
        background-color: {card_bg};
        color: {text_color};
        border: 2px solid {accent};
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.sidebar.markdown(f"<div class='user-badge'>{user_icon} Modo {user}</div>", unsafe_allow_html=True)
st.title(f"☁️🐈 Cloud.Cat - Cocina {user}")
st.markdown(f"### *{welcome}*")

# --- TABS ---
tab1, tab2 = st.tabs(["🥗 Recetas", "🎵 Música"])

with tab1:
    st.markdown("---")
    
    # API Key
    try:
        SPOON_KEY = st.secrets["SPOONACULAR_API_KEY"]
    except:
        SPOON_KEY = None
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("🛒 Ingredientes")
        ingredients = st.text_area(
            "¿Qué hay en el refri?",
            placeholder="Ej: pollo, brócoli, espinaca",
            help="Escribe ingredientes separados por coma"
        )
        
        st.header("🎯 Vibe")
        mood = st.selectbox(
            "¿Qué ambiente?",
            ["Fitness/Motivado", "Relajado/Zen", "Cena Romántica", "Gaming/Rápido"]
        )
        
        if st.button("🔍 Buscar Recetas Fit", use_container_width=True):
            if ingredients and SPOON_KEY:
                with st.spinner("Cloud.Cat está cocinando..."):
                    url = "https://api.spoonacular.com/recipes/complexSearch"
                    params = {
                        "apiKey": SPOON_KEY,
                        "query": ingredients,
                        "number": 3,
                        "diet": "low-carb",
                        "addRecipeNutrition": "true"
                    }
                    res = requests.get(url, params=params)
                    recipes = res.json().get("results", [])
                    
                    if recipes:
                        for recipe in recipes:
                            with col2:
                                nutrients = recipe.get('nutrition', {}).get('nutrients', [])
                                cals = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
                                protein = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                                
                                st.markdown(f"""
                                <div class="recipe-card">
                                    <h3>{recipe['title']}</h3>
                                    <img src="{recipe['image']}" style="width:100%; border-radius:10px;">
                                    <p>🔥 <b>{cals:.0f}</b> kcal | 💪 <b>{protein:.0f}</b>g proteína | ⏱️ {recipe['readyInMinutes']} min</p>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("No encontré recetas. Intenta otros ingredientes.")
            else:
                st.warning("Escribe ingredientes primero")

with tab2:
    st.markdown("---")
    st.header("🎵 Playlist Recomendada")
    
    music_mood = st.selectbox(
        "¿Para qué momento?",
        ["Entrenamiento 💪", "Cocinando 🥘", "Cita romántica 💕", "Relajándose 🌙", "Gaming 🎮"]
    )
    
    playlists = {
        "Entrenamiento 💪": ("https://open.spotify.com/playlist/7aIhHMnSsVFkVLO6NqjC2b", "Motivational Anime"),
        "Cocinando 🥘": ("https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK", "Japanese City Pop"),
        "Cita romántica 💕": ("https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4", "Bachatas Aventura"),
        "Relajándose 🌙": ("https://open.spotify.com/playlist/0J8eyNXyad9pdcM9igjtrU", "Vibes Stay"),
        "Gaming 🎮": ("https://open.spotify.com/playlist/5ase74F6CHi5XuncSIewvr", "Freedom Radio")
    }
    
    if st.button("🎧 Escuchar Playlist", use_container_width=True):
        url, name = playlists[music_mood]
        st.markdown(f"<h3 style='color:{accent}'>🎵 {name}</h3>", unsafe_allow_html=True)
        st.link_button("Abrir en Spotify", url)

st.sidebar.markdown("---")
st.sidebar.caption(f"☁️🐈 Cloud.Cat v3.0 - {datetime.now().year}")
