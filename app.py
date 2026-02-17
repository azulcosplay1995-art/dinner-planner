import streamlit as st
import requests
import json
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Cloud.Cat Fitness & Music",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .recipe-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00d4ff;
        margin-bottom: 20px;
    }
    .spotify-btn {
        background: linear-gradient(90deg, #1DB954, #191414);
        color: white !important;
        text-align: center;
        padding: 10px;
        border-radius: 20px;
        text-decoration: none;
        display: block;
        margin-top: 10px;
    }
    .user-badge {
        background-color: #e94560;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- USUARIO ---
st.sidebar.header("👤 ¿Quién está usando?")
user = st.sidebar.radio("Selecciona usuario:", ["Azul", "Alice"])

if user == "Alice":
    st.sidebar.markdown("<span class='user-badge'>Hola Alice 💕</span>", unsafe_allow_html=True)
    welcome_msg = "¡Hola Alice! Vamos a cocinar algo delicioso"
else:
    st.sidebar.markdown("<span class='user-badge'>Hola Azul 🎮</span>", unsafe_allow_html=True)
    welcome_msg = "¡Hola Azul! ¿Qué se te antoja hoy?"

# --- TÍTULO ---
st.title("☁️🐈 Cloud.Cat Fitness & Music")
st.markdown(f"### *{welcome_msg}*")

# --- TABS ---
tab_recetas, tab_musica = st.tabs(["🥗 Recetas", "🎵 Música"])

# --- TAB RECETAS ---
with tab_recetas:
    st.markdown("---")
    
    # Obtener API Key de Secrets
    try:
        SPOON_KEY = st.secrets["SPOONACULAR_API_KEY"]
    except:
        SPOON_KEY = None
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("🛒 Ingredientes")
        ingredients_input = st.text_area(
            "¿Qué hay en el refri?",
            placeholder="Ej: pollo, brócoli, espinaca",
            help="Escribe ingredientes separados por coma"
        )
        
        st.header("🎯 Vibe")
        mood = st.selectbox(
            "¿Qué ambiente?",
            ["Fitness/Motivado", "Relajado/Zen", "Cena Romántica", "Gaming/Rápido"]
        )
        
        search_btn = st.button("🔍 Buscar Recetas Fit", use_container_width=True)
    
    with col2:
        if search_btn and ingredients_input and SPOON_KEY:
            with st.spinner("Cloud.Cat está cocinando..."):
                url = "https://api.spoonacular.com/recipes/complexSearch"
                params = {
                    "apiKey": SPOON_KEY,
                    "query": ingredients_input,
                    "number": 3,
                    "diet": "low-carb",
                    "addRecipeNutrition": "true"
                }
                response = requests.get(url, params=params)
                recipes = response.json().get("results", [])
                
                if recipes:
                    for recipe in recipes:
                        with st.container():
                            st.markdown(f"""
                            <div class="recipe-card">
                                <h3>{recipe['title']}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                st.image(recipe['image'], use_container_width=True)
                            with c2:
                                nutrients = recipe.get('nutrition', {}).get('nutrients', [])
                                cals = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
                                protein = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                                
                                st.write(f"🔥 **{cals}** kcal")
                                st.write(f"💪 **{protein}**g proteína")
                                st.write(f"⏱️ {recipe['readyInMinutes']} mins")
                else:
                    st.info("No encontré recetas. Intenta otros ingredientes.")
        else:
            st.info("👈 Escribe ingredientes y click en Buscar")

# --- TAB MÚSICA ---
with tab_musica:
    st.markdown("---")
    st.header("🎵 Playlist Generada por Cloud.Cat")
    
    music_mood = st.selectbox(
        "¿Para qué momento?",
        ["Entrenamiento 💪", "Cocinando 🥘", "Cita romántica 💕", "Relajándose 🌙", "Gaming 🎮", "Trabajando 💻"],
        key="music_mood"
    )
    
    if st.button("🎧 Generar Playlist", use_container_width=True):
        playlists = {
            "Entrenamiento 💪": {
                "name": "Motivational Anime Gym",
                "url": "https://open.spotify.com/playlist/7aIhHMnSsVFkVLO6NqjC2b",
                "desc": "57 tracks para darlo todo 💪",
                "reason": "Alta energía, perfecta para sudar"
            },
            "Cocinando 🥘": {
                "name": "Japanese City Pop",
                "url": "https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK",
                "desc": "250 tracks relajados 🌙",
                "reason": "Ritmo suave para concentrarte en la cocina"
            },
            "Cita romántica 💕": {
                "name": "Bachatas Aventura",
                "url": "https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4",
                "desc": "Romeo Santos, Prince Royce 💕",
                "reason": "Romántica y bailable, ideal para compartir"
            },
            "Relajándose 🌙": {
                "name": "Playlist de vibes stay",
                "url": "https://open.spotify.com/playlist/0J8eyNXyad9pdcM9igjtrU",
                "desc": "99 tracks chill ✨",
                "reason": "Para desconectar después de un día largo"
            },
            "Gaming 🎮": {
                "name": "Freedom Radio",
                "url": "https://open.spotify.com/playlist/5ase74F6CHi5XuncSIewvr",
                "desc": "Fallout vibes - 254 tracks 🎮",
                "reason": "Atmosférico, perfecto para inmersión"
            },
            "Trabajando 💻": {
                "name": "Anime Openings",
                "url": "https://open.spotify.com/playlist/1YA5cPIfDy3L03bGnNiDM7",
                "desc": "Top 100 - 115 tracks 🎌",
                "reason": "Energética pero no distractora"
            }
        }
        
        selected = playlists[music_mood]
        
        st.markdown(f"""
        <div class="recipe-card">
            <h2>🎵 {selected['name']}</h2>
            <p>{selected['desc']}</p>
            <p><i>💡 Por qué esta playlist: {selected['reason']}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("🎧 Abrir en Spotify", selected['url'])
        
        st.success(f"¡Playlist elegida para {user}! Disfruta 🎶")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"☁️🐈 Cloud.Cat v2.1 - {datetime.now().year}")
