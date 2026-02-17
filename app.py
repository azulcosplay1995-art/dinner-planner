import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="Cloud.Cat Fit & Music",
    page_icon="☁️",
    layout="wide"
)

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #ffffff; }
    .user-badge {
        background: linear-gradient(90deg, #e94560, #0f3460);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    .recipe-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00d4ff;
        margin: 10px 0;
    }
    .music-card {
        background: linear-gradient(135deg, #1DB954, #191414);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: USUARIO ---
st.sidebar.header("👤 ¿Quién está usando la app?")
user = st.sidebar.selectbox("", ["Azul", "Alice"], index=0)
st.sidebar.markdown(f"<div class='user-badge'>☁️🐈 Hola {user}!</div>", unsafe_allow_html=True)

# --- TÍTULO ---
st.title(f"☁️🐈 Cloud.Cat App para {user}")

# Tabs: Recetas y Música
tab1, tab2 = st.tabs(["🥗 Recetas Fit", "🎵 Solo Música"])

# === TAB 1: RECETAS ===
with tab1:
    st.header("Busca recetas saludables")
    
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_area("🛒 ¿Qué hay en casa?", 
                                   placeholder="Ej: pollo, brócoli, limón")
    with col2:
        mood_food = st.selectbox("🎭 Mood para comer:", 
                                  ["Fitness/Motivado", "Relajado/Zen", "Cena Romántica", "Gaming"])
    
    if st.button("🔍 Buscar Recetas", key="food_btn"):
        if ingredients:
            st.success(f"Buscando recetas con: {ingredients}")
            st.info("(Aquí aparecerán las recetas de Spoonacular)")
            
            # Placeholder para demo
            st.markdown("""
            <div class="recipe-card">
                <h3>🍗 Pollo al Limón con Brócoli</h3>
                <p>🔥 350 cal | 💪 40g proteína | ⏱️ 25 min</p>
                <p>Perfecto para tu mood: <b>{}</b></p>
            </div>
            """.format(mood_food), unsafe_allow_html=True)
        else:
            st.warning("Escribe algunos ingredientes primero")

# === TAB 2: SOLO MÚSICA ===
with tab2:
    st.header("🎵 Generador de Playlists por Mood")
    st.write("Escoge tu vibe y te recomiendo la playlist perfecta de Spotify")
    
    music_mood = st.selectbox(
        "¿Qué mood quieres musical?",
        ["💪 Gym/Fitness", "🌙 Relajado/Chill", "💕 Romántico", 
         "🎮 Gaming", "☕ Café Vibes", "🌅 Morning Energy"],
        key="music_mood"
    )
    
    if st.button("🎧 Generar Playlist", key="music_btn"):
        # Diccionario de playlists según mood
        playlists = {
            "💪 Gym/Fitness": {
                "name": "Motivational Anime Gym",
                "url": "https://open.spotify.com/playlist/7aIhHMnSsVFkVLO6NqjC2b",
                "desc": "57 tracks para romperla en el gym",
                "icon": "💪"
            },
            "🌙 Relajado/Chill": {
                "name": "Japanese City Pop",
                "url": "https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK",
                "desc": "250 tracks - Midnight vibes",
                "icon": "🌙"
            },
            "💕 Romántico": {
                "name": "Bachatas Aventura",
                "url": "https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4",
                "desc": "Romeo Santos, Prince Royce - 91 tracks",
                "icon": "💕"
            },
            "🎮 Gaming": {
                "name": "Freedom Radio",
                "url": "https://open.spotify.com/playlist/5ase74F6CHi5XuncSIewvr",
                "desc": "Fallout vibes - 254 tracks",
                "icon": "🎮"
            },
            "☕ Café Vibes": {
                "name": "Amelie Soundtrack",
                "url": "https://open.spotify.com/playlist/7Gk7XMEtEwa9R9KyJkQzv2",
                "desc": "22 tracks franceses para relajarte",
                "icon": "☕"
            },
            "🌅 Morning Energy": {
                "name": "Anime Openings",
                "url": "https://open.spotify.com/playlist/1YA5cPIfDy3L03bGnNiDM7",
                "desc": "Top 100 - 115 tracks para empezar el día",
                "icon": "🌅"
            }
        }
        
        selected = playlists[music_mood]
        
        st.markdown(f"""
        <div class="music-card">
            <h2>{selected['icon']} {selected['name']}</h2>
            <p>{selected['desc']}</p>
            <p><b>User:</b> {user} | <b>Mood:</b> {music_mood}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("🎵 Abrir en Spotify", selected['url'], use_container_width=True)
        
        # Opción para crear playlist personalizada
        st.markdown("---")
        st.write("💡 ¿Quieres que cree una playlist personalizada para ti en Spotify?")
        st.checkbox("Sí, créala con mi nombre de usuario", key="create_playlist")

# Footer
st.markdown("---")
st.caption(f"☁️🐈 Cloud.Cat v2.0 - Hecho con amor para Azul y Alice - {datetime.now().year}")
