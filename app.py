import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Cloud.Cat Dinner Planner",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Dark theme styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a2e;
        color: #eee;
    }
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .sidebar .sidebar-content {
        background-color: #0f3460;
    }
    h1 {
        color: #e94560;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background-color: #e94560;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    .recipe-card {
        background-color: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #e94560;
    }
    .spotify-link {
        background: linear-gradient(90deg, #1DB954, #1ed760);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("☁️🐈 Cloud.Cat Dinner Planner")
st.markdown("*Powered by Azul's Spotify & Cloud.Cat AI*")
st.markdown("---")

# Data
RECIPES = {
    "romantic": {
        "name": "Pasta Alfredo",
        "time": "20 min",
        "difficulty": "Fácil",
        "ingredients": ["400g pasta", "250ml crema", "100g queso parmesano", "50g mantequilla", "4 dientes ajo", "Perejil fresco"],
        "notes": "Favorita de Alice 💕",
        "spotify": {
            "name": "Bachatas Aventura",
            "url": "https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4",
            "desc": "Romeo Santos, Prince Royce - 91 tracks 💕"
        }
    },
    "party": {
        "name": "Arepas de Huevo",
        "time": "30 min",
        "difficulty": "Medio",
        "ingredients": ["2 tazas harina de maíz", "4 huevos", "1 taza agua tibia", "Sal", "Aceite para freír"],
        "notes": "Perfectas para parranda 🎉",
        "spotify": {
            "name": "Salsa Vieja",
            "url": "https://open.spotify.com/playlist/2qcBXdn2HfxV1dPfHQ2UPE",
            "desc": "60s-80s - 599 tracks 💃"
        }
    },
    "chill": {
        "name": "Sopa de Verduras",
        "time": "25 min",
        "difficulty": "Fácil",
        "ingredients": ["2 zanahorias", "2 papas", "1 calabacín", "1 cebolla", "4 tazas caldo", "Cilantro"],
        "notes": "Noche relajada en casa 🌙",
        "spotify": {
            "name": "Japanese City Pop",
            "url": "https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK",
            "desc": "250 tracks - Midnight vibes ✨"
        }
    },
    "gaming": {
        "name": "Pizza Casera",
        "time": "45 min",
        "difficulty": "Medio",
        "ingredients": ["300g harina", "150ml agua", "10g levadura", "Salsa de tomate", "Queso mozarella", "Pepperoni"],
        "notes": "Noche de juegos con Alice 🎮",
        "spotify": {
            "name": "Freedom Radio",
            "url": "https://open.spotify.com/playlist/5ase74F6CHi5XuncSIewvr",
            "desc": "Fallout vibes - 254 tracks 🎮"
        }
    },
    "focus": {
        "name": "Salmón a la Plancha",
        "time": "30 min",
        "difficulty": "Medio",
        "ingredients": ["2 filetes de salmón", "Limón", "Eneldo fresco", "Espárragos", "Aceite de oliva", "Sal y pimienta"],
        "notes": "Cena ligera para trabajar 💻",
        "spotify": {
            "name": "Anime Openings",
            "url": "https://open.spotify.com/playlist/1YA5cPIfDy3L03bGnNiDM7",
            "desc": "Top 100 - 115 tracks 🎌"
        }
    }
}

# Sidebar
st.sidebar.header("🎭 Selecciona el Mood")
mood = st.sidebar.selectbox(
    "¿Qué ambiente buscas?",
    ["romantic", "party", "chill", "gaming", "focus"],
    format_func=lambda x: {
        "romantic": "💕 Romántico",
        "party": "🎉 Fiesta/Parranda",
        "chill": "🌙 Relajado",
        "gaming": "🎮 Gaming Night",
        "focus": "💻 Productivo"
    }[x]
)

st.sidebar.markdown("---")
st.sidebar.header("🎵 Spotify Integration")

# Main content
if mood:
    recipe = RECIPES[mood]
    
    st.subheader(f"🍽️ {recipe['name']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱️ Tiempo", recipe['time'])
    with col2:
        st.metric("📊 Dificultad", recipe['difficulty'])
    with col3:
        st.write(f"**{recipe['notes']}**")
    
    st.markdown("---")
    
    st.subheader("📝 Ingredientes:")
    for ing in recipe['ingredients']:
        st.markdown(f"• {ing}")
    
    st.markdown("---")
    
    # Spotify section
    st.subheader("🎵 Playlist Recomendada:")
    spotify = recipe['spotify']
    
    st.markdown(f"""
    <div class='spotify-link'>
        <h3 style='color: white; margin: 0;'>{spotify['name']}</h3>
        <p style='color: white; margin: 5px 0;'>{spotify['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎧 Abrir en Spotify", use_container_width=True):
        st.markdown(f"""
        <script>
            window.open('{spotify['url']}', '_blank');
        </script>
        """, unsafe_allow_html=True)
        st.success(f"¡Disfruta {spotify['name']} mientras cocinas!")
        st.markdown(f"[🔗 Abrir Spotify]({spotify['url']})")
    
    st.markdown("---")
    
    # Save recipe button
    if st.button("💾 Guardar Receta en Favoritos"):
        st.success(f"¡{recipe['name']} guardada en favoritos! 💕")

st.sidebar.markdown("---")
st.sidebar.caption("☁️🐈 Made with love by Cloud.Cat")
st.sidebar.caption(f"Ultima actualización: {datetime.now().strftime('%Y-%m-%d')}")

# Footer
st.markdown("---")
st.markdown("<center>☁️🐈 <i>Tu asistente personal para cocina y música</i></center>", unsafe_allow_html=True)
