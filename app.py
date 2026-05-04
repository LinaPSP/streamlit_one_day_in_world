import calendar
import datetime
import random

import requests
import streamlit as st


# Mapea el numero de mes a su nombre en espanol para construir el titulo principal.
SPANISH_MONTHS = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}

REQUEST_HEADERS = {
    "User-Agent": (
        "un-dia-como-hoy/1.0 "
        "(https://apponedayinworld.streamlit.app/; "
        "https://github.com/LinaPSP/streamlit_one_day_in_world)"
    ),
    "Accept": "application/json",
}


st.set_page_config(page_title="Un día como hoy", page_icon="🌍", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo degradado sutil */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent; }

    /* Hero */
    .hero {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
    }
    .hero .emoji { font-size: 3rem; line-height: 1; }
    .hero h1 {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.3rem 0 0.2rem;
        line-height: 1.1;
    }
    .hero p {
        color: rgba(255,255,255,0.55);
        font-size: 1rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 0;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #fff;
        border: none;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 0.55rem 1.4rem;
        transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.55);
        color: #fff;
    }
    .stButton > button:active { transform: translateY(0); }

    /* Slider */
    .stSlider label, .stSlider p { color: rgba(255,255,255,0.7) !important; }
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #7c3aed;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        border-radius: 999px;
        padding: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        color: rgba(255,255,255,0.6);
        font-weight: 600;
        padding: 0.4rem 1.2rem;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: #fff !important;
    }

    /* Cards */
    .evento-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        backdrop-filter: blur(10px);
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .evento-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        border-color: rgba(167,139,250,0.35);
    }
    .evento-card .anio {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.4rem;
    }
    .evento-card .descripcion {
        color: rgba(255,255,255,0.85);
        line-height: 1.6;
        font-size: 0.95rem;
        margin-bottom: 0.55rem;
    }
    .evento-card a {
        color: #a78bfa;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.88rem;
    }
    .evento-card a:hover { text-decoration: underline; color: #c4b5fd; }

    /* Info / error */
    [data-testid="stInfo"] { color: rgba(255,255,255,0.8) !important; }
    [data-testid="stAlertContentError"] { color: rgba(255,255,255,0.8) !important; }

    /* Texto general */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: rgba(255,255,255,0.8);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600)
def obtener_datos(mes: int, dia: int) -> dict:
    # Cachea solo respuestas exitosas. Si falla, se levanta error y no se cachea.
    urls = [
        f"https://api.wikimedia.org/feed/v1/wikipedia/es/onthisday/all/{mes}/{dia}",
        f"https://es.wikipedia.org/api/rest_v1/feed/onthisday/all/{mes:02d}/{dia:02d}",
    ]
    ultimo_error = None

    for url in urls:
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=8)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and (
                data.get("events") or data.get("births") or data.get("deaths")
            ):
                return data
            ultimo_error = RuntimeError("La API respondio sin contenido util.")
        except Exception as exc:
            ultimo_error = exc

    raise RuntimeError(f"No fue posible obtener datos de Wikimedia: {ultimo_error}")


def filtrar_por_anio(items: list, anio_min: int, anio_max: int) -> list:
    # Recorre la lista y conserva solo los elementos cuyo ano cae en el rango elegido.
    filtrados = [item for item in items if anio_min <= item.get("year", 0) <= anio_max]
    return filtrados[:10]


def render_card(item: dict) -> None:
    # Construye la tarjeta visual de cada resultado y agrega el enlace si existe.
    anio = item.get("year", "?")
    texto = item.get("text", "Sin descripcion")
    link = ""

    try:
        url_wiki = item["pages"][0]["content_urls"]["desktop"]["page"]
        link = f'<a href="{url_wiki}" target="_blank">→ Ver en Wikipedia</a>'
    except (KeyError, IndexError, TypeError):
        pass

    st.markdown(
        f"""
        <div class="evento-card">
            <div class="anio">{anio}</div>
            <div class="descripcion">{texto}</div>
            {link}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Usa un condicional para inicializar la fecha solo una vez por sesion.
if "fecha" not in st.session_state:
    st.session_state.fecha = datetime.date.today()

# Guarda si la fecha fue generada aleatoriamente para conservar el estado de la app.
if "modo_random" not in st.session_state:
    st.session_state.modo_random = False


fecha = st.session_state.fecha
mes = fecha.month
dia = fecha.day
titulo = f"{dia} de {SPANISH_MONTHS[mes]}"

st.markdown(
    f"""
    <div class="hero">
        <div class="emoji">🌍</div>
        <h1>{titulo}</h1>
        <p>esto pasó en la historia</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_hoy, col_random = st.columns(2)

with col_hoy:
    if st.button("Hoy", use_container_width=True):
        st.session_state.fecha = datetime.date.today()
        st.session_state.modo_random = False

with col_random:
    if st.button("🎲 Sorprendeme", use_container_width=True):
        # Genera un mes y un dia validos para construir una fecha aleatoria.
        mes_r = random.randint(1, 12)
        max_dia = calendar.monthrange(2024, mes_r)[1]
        dia_r = random.randint(1, max_dia)
        st.session_state.fecha = datetime.date(2024, mes_r, dia_r)
        st.session_state.modo_random = True

try:
    datos = obtener_datos(mes, dia)
except Exception:
    st.error("No se pudieron cargar los datos de Wikimedia. Revisa tu conexion e intenta de nuevo.")
    if st.button("Reintentar carga", use_container_width=True):
        obtener_datos.clear()
        st.rerun()
    st.stop()

todos_los_items = []
# Recorre las categorias principales del JSON para reunir todos los anos disponibles.
for clave in ("events", "births", "deaths"):
    todos_los_items.extend(datos.get(clave, []))

anios = [item.get("year", 0) for item in todos_los_items if isinstance(item.get("year"), int)]
anio_min_default = min(anios) if anios else 0
anio_max_default = max(anios) if anios else datetime.date.today().year

rango = st.slider(
    "Filtrar por ano",
    min_value=anio_min_default,
    max_value=anio_max_default,
    value=(anio_min_default, anio_max_default),
)

tabs = st.tabs(["Eventos", "Nacimientos", "Muertes"])
claves = ["events", "births", "deaths"]

# Recorre las pestanas y muestra solo los elementos que cumplen el filtro seleccionado.
for tab, clave in zip(tabs, claves):
    with tab:
        items = filtrar_por_anio(datos.get(clave, []), rango[0], rango[1])
        if not items:
            st.info("No hay resultados para este rango de anos.")
            continue

        for item in items:
            render_card(item)
