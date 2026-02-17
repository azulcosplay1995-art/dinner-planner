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
    bg_color, text_color, accent = "#fff5f5", "#333333", "#ff6b81"
    welcome = "¡Hola Alice! Vamos a crear algo delicioso 💕"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .emoji-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; }}
    .emoji-btn {{ font-size: 2.5rem; cursor: pointer; padding: 10px; border-radius: 15px; background: {accent}20; border: 2px solid {accent}; transition: all 0.2s; }}
    .emoji-btn:hover {{ transform: scale(1.1); background: {accent}40; }}
    .emoji-selected {{ background: {accent} !important; color: white; }}
    .categoria {{ color: {accent}; font-weight: bold; margin-top: 15px; margin-bottom: 5px; }}
    .recipe-card {{ background-color: {"#1a1a2e" if user == "Azul" else "#ffffff"}; padding: 20px; border-radius: 15px; border-left: 5px solid {accent}; margin-bottom: 20px; }}
    </style>
""", unsafe_allow_html=True)

st.title(f"👨‍🍳 Recetario Azul - {user}")
st.markdown(f"### {welcome}")
st.markdown("---")

# --- INGREDIENTES EMOJI ---
st.subheader("🛒 Elige tus ingredientes:")

if "selected_ingredientes" not in st.session_state:
    st.session_state.selected_ingredientes = []

ingredientes = {
    "🍗 Proteínas": ["🍗", "🥩", "🐟", "🥚", "🦐", "🍖"],
    "🥦 Verduras": ["🥦", "🥬", "🥕", "🌽", "🧅", "🧄", "🍄", "🌶️"],
    "🍚 Carbohidratos": ["🍚", "🍝", "🥔", "🌾", "🍞", "🥯"],
    "🥑 Frescos": ["🥑", "🍋", "🍅", "🥒", "🥗", "🍎"]
}

cols = st.columns(4)
col_idx = 0

for categoria, emojis in ingredientes.items():
    with cols[col_idx % 4]:
        st.markdown(f"<p class='categoria'>{categoria}</p>", unsafe_allow_html=True)
        for emoji in emojis:
            if st.button(emoji, key=f"emoji_{emoji}", use_container_width=True):
                if emoji not in st.session_state.selected_ingredientes:
                    st.session_state.selected_ingredientes.append(emoji)
                    st.rerun()
    col_idx += 1

# --- MOSTRAR SELECCIONADOS ---
if st.session_state.selected_ingredientes:
    st.markdown(f"**Seleccionados:** {' '.join(st.session_state.selected_ingredientes)}")
    if st.button("❌ Limpiar selección", key="clear"):
        st.session_state.selected_ingredientes = []
        st.rerun()

# --- TEXTO EXTRA ---
st.markdown("---")
st.subheader("⌨️ ¿Algo más?")
st.caption("Escribe ingredientes adicionales separados por coma:")
texto_extra = st.text_input("", placeholder="Ej: quinoa, leche de almendras...")

# --- BUSCAR ---
mood = st.selectbox("🎯 ¿Qué vibe?", ["Fit/Gym 💪", "Romántica 💕", "Rápida ⚡", "Relax 🌿"])

if st.button("🔍 Buscar Recetas", use_container_width=True):
    emojis_text = " ".join(st.session_state.selected_ingredientes) if st.session_state.selected_ingredientes else ""
    busqueda = f"{emojis_text} {texto_extra}".strip()
    
    if busqueda:
        try:
            SPOON_KEY = st.secrets["SPOONACULAR_API_KEY"]
            with st.spinner("Buscando..."):
                res = requests.get("https://api.spoonacular.com/recipes/complexSearch", 
                    params={"apiKey": SPOON_KEY, "query": busqueda, "number": 3, 
                           "diet": "low-carb", "addRecipeNutrition": "true"}).json()
                
                recipes = res.get("results", [])
                if recipes:
                    st.success(f"¡{len(recipes)} recetas encontradas!")
                    for r in recipes:
                        nutrients = r.get('nutrition', {}).get('nutrients', [])
                        cals = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
                        prot = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                        
                        st.markdown(f"""
                        <div class="recipe-card">
                            <h3>{r['title']}</h3>
                            <img src="{r['image']}" style="width:100%; border-radius:10px;">
                            <p>🔥 {cals:.0f} kcal | 💪 {prot:.0f}g proteína | ⏱️ {r['readyInMinutes']} min</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No encontré recetas con eso. Intenta otros ingredientes.")
        except:
            st.error("Error con Spoonacular. Revisa la API key.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Recetario Azul v2.0 - {datetime.now().year}")
