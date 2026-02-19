import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Recetario Azul", page_icon="👨‍🍳", layout="wide")

# --- USUARIO ---
st.sidebar.header("👤 ¿Quién cocina?")
user = st.sidebar.radio("", ["Azul", "Alice"], horizontal=True)

if user == "Azul":
    bg_color, text_color, accent = "#0a0a1a", "#ffffff", "#00d4ff"
    welcome = "¡Hey Chef Azul! ¿Qué cocinamos hoy?"
else:
    bg_color, text_color, accent = "#fff5f5", "#333", "#ff6b81"
    welcome = "¡Hola Alice! Vamos a crear algo delicioso 💕"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .emoji-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}
    .emoji-btn {{ font-size: 2.5rem; padding: 10px; border-radius: 15px; background: {accent}20; border: 2px solid {accent}; }}
    .emoji-btn:hover {{ transform: scale(1.1); background: {accent}40; }}
    .categoria {{ color: {accent}; font-weight: bold; margin: 15px 0 5px; }}

    /* Pinterest Cards */
    .pinterest-container {{ 
        display: flex; 
        flex-wrap: wrap; 
        gap: 20px; 
        justify-content: center;
    }}
    .pinterest-card {{
        background: {"#1e2130" if user == "Azul" else "#fff"};
        border-radius: 16px;
        overflow: hidden;
        width: 100%;
        max-width: 340px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.2s;
        margin-bottom: 20px;
    }}
    .pinterest-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.25); }}
    .pinterest-img {{ width: 100%; height: 200px; object-fit: cover; }}
    .pinterest-content {{ padding: 15px; }}
    .pinterest-title {{
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: {text_color};
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}
    .pinterest-badges {{
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }}
    .badge {{
        background: {accent}30;
        color: {accent};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    .spotify-link {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: white !important;
        padding: 10px 16px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    .stats {{
        color: {text_color}80;
        font-size: 0.85rem;
        margin-top: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title(f"👨‍🍳 Recetario Azul - {user}")
st.markdown(f"### {welcome}")

# --- INGREDIENTES ---
st.subheader("🛒 Elige ingredientes:")
if "selected_ingredientes" not in st.session_state:
    st.session_state.selected_ingredientes = []

ingredientes = {
    "🍗 Proteínas": ["🍗", "🥩", "🐟", "🥚", "🦐", "🍖"],
    "🥦 Verduras": ["🥦", "🥬", "🥕", "🌽", "🧅", "🧄", "🍄", "🌶️"],
    "🍚 Carbs": ["🍚", "🍝", "🥔", "🌾", "🍞", "🥯"],
    "🥑 Frescos": ["🥑", "🍋", "🍅", "🥒", "🥗", "🍎"]
}

cols = st.columns(4)
for idx, (cat, emojis) in enumerate(ingredientes.items()):
    with cols[idx]:
        st.markdown(f"<p class='categoria'>{cat}</p>", unsafe_allow_html=True)
        for e in emojis:
            if st.button(e, key=f"emoji_{e}", use_container_width=True):
                if e not in st.session_state.selected_ingredientes:
                    st.session_state.selected_ingredientes.append(e)
                    st.rerun()

if st.session_state.selected_ingredientes:
    st.markdown(f"**Seleccionados:** {' '.join(st.session_state.selected_ingredientes)}")
    if st.button("❌ Limpiar"):
        st.session_state.selected_ingredientes = []
        st.rerun()

# --- TEXTO EXTRA ---
st.markdown("---")
texto_extra = st.text_input("⌨️ ¿Algo más?", placeholder="Ej: quinoa, especias...")

# --- BUSCAR ---
mood = st.selectbox("🎯 Vibe", ["Fit/Gym 💪", "Romántica 💕", "Rápida ⚡", "Relax 🌿"])

if st.button("🔍 Buscar", use_container_width=True):
    emojis_txt = " ".join(st.session_state.selected_ingredientes)
    busqueda = f"{emojis_txt} {texto_extra}".strip()
    
    if busqueda:
        try:
            SPOON_KEY = st.secrets["SPOONACULAR_API_KEY"]
            with st.spinner("Buscando delicias..."):
                res = requests.get("https://api.spoonacular.com/recipes/complexSearch",
                    params={"apiKey": SPOON_KEY, "query": busqueda, "number": 3, 
                           "diet": "low-carb", "addRecipeNutrition": "true"}).json()
                
                recipes = res.get("results", [])
                if recipes:
                    st.success(f"¡{len(recipes)} recetas!")
                    
                    playlists = {
                        "Fit/Gym 💪": ("https://open.spotify.com/playlist/7aIhHMnSsVFkVLO6NqjC2b", "Gym Vibes"),
                        "Romántica 💕": ("https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4", "Bachatas"),
                        "Rápida ⚡": ("https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK", "City Pop"),
                        "Relax 🌿": ("https://open.spotify.com/playlist/0J8eyNXyad9pdcM9igjtrU", "Chill")
                    }
                    pl_url, pl_name = playlists.get(mood, playlists["Fit/Gym 💪"])
                    
                    cols = st.columns(3)
                    for idx, r in enumerate(recipes):
                        with cols[idx % 3]:
                            nut = r.get('nutrition', {}).get('nutrients', [])
                            cals = next((n['amount'] for n in nut if n['name'] == 'Calories'), 0)
                            prot = next((n['amount'] for n in nut if n['name'] == 'Protein'), 0)
                            fat = next((n['amount'] for n in nut if n['name'] == 'Fat'), 0)
                            
                            # Tarjeta Pinterest Clean
                            st.markdown(f"""
                            <div style="background:{'#1e1e2e' if user=='Azul' else '#fff'}; border-radius:16px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.15); margin-bottom:15px; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                <img src="{r['image']}" style="width:100%; height:220px; object-fit:cover;">
                                <div style="padding:12px 16px 16px 16px;">
                                    <h4 style="margin:0 0 8px 0; font-size:1.1em; color:{accent}; line-height:1.3;">{r['title'][:40]}{'...' if len(r['title'])>40 else ''}</h4>
                                    <div style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap;">
                                        <span style="background:{accent}20; color:{accent}; padding:4px 12px; border-radius:12px; font-size:0.85em; font-weight:600;">🔥 {cals:.0f}</span>
                                        <span style="background:{accent}20; color:{accent}; padding:4px 12px; border-radius:12px; font-size:0.85em; font-weight:600;">💪 {prot:.0f}g</span>
                                        <span style="background:{accent}20; color:{accent}; padding:4px 12px; border-radius:12px; font-size:0.85em; font-weight:600;">⏱️ {r['readyInMinutes']}m</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span style="font-size:0.9em; opacity:0.7;">🥑 {fat:.0f}g grasa</span>
                                        <a href="{pl_url}" target="_blank" style="background:linear-gradient(90deg,#1DB954,#191414); color:white; text-decoration:none; padding:8px 16px; border-radius:20px; font-size:0.9em; font-weight:600;">🎵 {pl_name}</a>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No encontré recetas. Prueba otros ingredientes.")
        except Exception as e:
            st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption(f"☁️🐈 Recetario Azul v3.0 - {datetime.now().year}")
