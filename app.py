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
    .nutrient-badge {
        background-color: #262730;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 0.8em;
        margin-right: 5px;
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
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("☁️🐈 Cloud.Cat Fitness & Music")
st.markdown("### *Comida saludable y buena música para Azul y Alice*")

# --- SIDEBAR: CONFIGURACIÓN Y MOOD ---
st.sidebar.header("🎯 Tus Preferencias")

# Obtener API Key de Secrets
try:
    SPOON_KEY = st.secrets["SPOONACULAR_API_KEY"]
except:
    st.sidebar.warning("⚠️ Falta configurar API Key en Secrets")
    SPOON_KEY = None

mood = st.sidebar.selectbox(
    "¿Qué vibra tienes hoy?",
    ["Fitness/Motivado", "Relajado/Zen", "Cena Romántica", "Gaming/Rápido"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.header("🛒 ¿Qué hay en casa?")
ingredients_input = st.sidebar.text_area("Lista tus ingredientes (separados por coma):", placeholder="Ej: pollo, brócoli, espinaca")

# --- LÓGICA DE BÚSQUEDA ---
def search_healthy_recipes(query):
    if not SPOON_KEY: return None
    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": SPOON_KEY,
        "query": query,
        "number": 3,
        "diet": "low-carb",
        "addRecipeNutrition": "true",
        "sort": "healthiness"
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

# --- CONTENIDO PRINCIPAL ---
if st.sidebar.button("🔍 Buscar Recetas Fit"):
    if ingredients_input and SPOON_KEY:
        with st.spinner("Cloud.Cat está buscando en la cocina..."):
            recipes = search_healthy_recipes(ingredients_input)
            
            if recipes:
                st.subheader(f"🥗 Top 3 Recetas Saludables con: {ingredients_input}")
                
                for recipe in recipes:
                    with st.container():
                        st.markdown(f"""
                        <div class="recipe-card">
                            <h2>{recipe['title']}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.image(recipe['image'], use_container_width=True)
                        
                        with col2:
                            # Nutrientes
                            nutrients = recipe.get('nutrition', {}).get('nutrients', [])
                            cals = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
                            protein = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                            
                            st.markdown(f"**🔥 Calorías:** {cals} kcal | **💪 Proteína:** {protein}g")
                            st.write(f"⏱️ Listo en: {recipe['readyInMinutes']} mins")
                            
                            # Spotify Suggestion
                            st.markdown("---")
                            st.markdown("#### 🎵 Música para cocinar este plato:")
                            
                            if mood == "Fitness/Motivado":
                                playlist_url = "https://open.spotify.com/playlist/7aIhHMnSsVFkVLO6NqjC2b"
                                p_name = "Motivational Anime Gym"
                            elif mood == "Relajado/Zen":
                                playlist_url = "https://open.spotify.com/playlist/3s1lcoN41cKKlLZFezjcSK"
                                p_name = "Japanese City Pop"
                            else:
                                playlist_url = "https://open.spotify.com/playlist/1nh8MuQtWwEhzqehm8MaO4"
                                p_name = "Vibes Stay"

                            st.markdown(f"**Recomendación:** {p_name}")
                            st.link_button("🎧 Escuchar en Spotify", playlist_url)
            else:
                st.error("No encontré recetas con esos ingredientes. ¡Prueba otros!")
    else:
        st.info("Escribe algunos ingredientes en la barra lateral para empezar.")
else:
    # Vista inicial
    st.info("👋 ¡Hola Azul! Escribe qué tienes en el refri a la izquierda y yo haré la magia.")
    
# Footer
st.sidebar.markdown("---")
st.sidebar.caption(f"Cloud.Cat v2.0 - {datetime.now().year}")
