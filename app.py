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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

    :root {
        --ink:      #1a1410;
        --parchment:#f5efe3;
        --aged:     #e8dcc8;
        --gold:     #b8963e;
        --gold-lt:  #d4af5a;
        --rust:     #8b3a2a;
        --muted:    #6b5c44;
        --rule:     #c9b88a;
    }

    html, body, [class*="css"] {
        font-family: 'Source Serif 4', Georgia, serif;
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--parchment);
        background-image:
            radial-gradient(ellipse at 15% 20%, rgba(184,150,62,0.07) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 80%, rgba(139,58,42,0.06) 0%, transparent 55%),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Crect width='60' height='60' fill='none'/%3E%3Cpath d='M0 30 H60 M30 0 V60' stroke='%23c9b88a' stroke-width='0.3' opacity='0.4'/%3E%3C/svg%3E");
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem; }

    /* ── HERO ── */
    .hero {
        text-align: center;
        padding: 2rem 0 0.5rem;
        border-bottom: 2px solid var(--rule);
        margin-bottom: 1.6rem;
        position: relative;
    }
    .hero::before {
        content: '◆  ◆  ◆';
        display: block;
        color: var(--gold);
        font-size: 0.65rem;
        letter-spacing: 0.5em;
        margin-bottom: 0.8rem;
    }
    .hero .kicker {
        font-family: 'Source Serif 4', serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.5rem;
    }
    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2.4rem, 6vw, 4rem);
        font-weight: 900;
        font-style: italic;
        color: var(--ink);
        margin: 0 0 0.2rem;
        line-height: 1.05;
    }
    .hero .sub {
        font-family: 'Source Serif 4', serif;
        font-size: 0.8rem;
        font-style: italic;
        color: var(--muted);
        letter-spacing: 0.06em;
    }
    .hero::after {
        content: '';
        display: block;
        width: 80px;
        height: 1px;
        background: var(--gold);
        margin: 1.2rem auto 0;
    }

    /* ── BOTONES ── */
    .stButton > button {
        font-family: 'Source Serif 4', serif;
        font-weight: 600;
        font-size: 0.82rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--ink) !important;
        background: transparent;
        border: 1.5px solid var(--gold);
        border-radius: 2px;
        padding: 0.5rem 1.2rem;
        transition: background 0.2s, color 0.2s;
        box-shadow: none;
    }
    .stButton > button:hover {
        background: var(--gold) !important;
        color: var(--parchment) !important;
        border-color: var(--gold) !important;
        transform: none;
        box-shadow: none;
    }
    .stButton > button:active { opacity: 0.85; }

    /* ── SLIDER ── */
    .stSlider label p, .stSlider > label {
        font-family: 'Source Serif 4', serif !important;
        color: var(--muted) !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1.5px solid var(--rule);
        border-radius: 0;
        padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Source Serif 4', serif;
        font-size: 0.78rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-weight: 600;
        color: var(--muted);
        border-radius: 0;
        border: none;
        padding: 0.5rem 1.4rem;
        background: transparent;
        border-bottom: 2px solid transparent;
        margin-bottom: -1.5px;
    }
    .stTabs [aria-selected="true"] {
        color: var(--ink) !important;
        background: transparent !important;
        border-bottom: 2px solid var(--gold) !important;
    }

    /* ── CARDS ── */
    .evento-card {
        background: rgba(255,255,255,0.55);
        border: 1px solid var(--rule);
        border-left: 3px solid var(--gold);
        border-radius: 0;
        padding: 1rem 1.2rem 0.9rem;
        margin-bottom: 0.8rem;
        transition: border-left-color 0.2s, background 0.2s;
    }
    .evento-card:hover {
        background: rgba(255,255,255,0.85);
        border-left-color: var(--rust);
        transform: none;
        box-shadow: 2px 2px 8px rgba(26,20,16,0.08);
    }
    .evento-card .anio {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.5rem;
        font-weight: 700;
        font-style: italic;
        color: var(--gold);
        margin-bottom: 0.3rem;
        line-height: 1;
    }
    .evento-card .descripcion {
        font-family: 'Source Serif 4', serif;
        color: var(--ink);
        line-height: 1.65;
        font-size: 0.93rem;
        margin-bottom: 0.5rem;
    }
    .evento-card a {
        font-family: 'Source Serif 4', serif;
        color: var(--rust);
        text-decoration: none;
        font-size: 0.8rem;
        font-style: italic;
        letter-spacing: 0.04em;
    }
    .evento-card a:hover { text-decoration: underline; color: var(--gold); }

    /* ── ALERTS ── */
    [data-testid="stInfo"],
    [data-testid="stAlertContentError"] {
        font-family: 'Source Serif 4', serif !important;
        color: var(--muted) !important;
        font-style: italic;
    }

    /* ── TEXTO GENERAL ── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--ink);
        font-family: 'Source Serif 4', serif;
    }

    /* ── DATE INPUT ── */
    [data-testid="stDateInput"] input {
        font-family: 'Source Serif 4', serif !important;
        background: rgba(255,255,255,0.6) !important;
        border: 1px solid var(--rule) !important;
        border-radius: 2px !important;
        color: var(--ink) !important;
        text-align: center;
        font-weight: 400;
        letter-spacing: 0.05em;
    }
    [data-testid="stDateInput"] input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 2px rgba(184,150,62,0.2) !important;
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

col_hoy, col_random = st.columns(2)

with col_hoy:
    if st.button("Hoy", use_container_width=True):
        st.session_state.fecha = datetime.date.today()
        st.session_state.modo_random = False
        st.rerun()

with col_random:
    if st.button("🎲 Sorprendeme", use_container_width=True):
        mes_r = random.randint(1, 12)
        max_dia = calendar.monthrange(2024, mes_r)[1]
        dia_r = random.randint(1, max_dia)
        st.session_state.fecha = datetime.date(2024, mes_r, dia_r)
        st.session_state.modo_random = True
        st.rerun()

fecha_elegida = st.date_input(
    "fecha",
    value=st.session_state.fecha,
    format="DD/MM/YYYY",
    label_visibility="collapsed",
)
if fecha_elegida != st.session_state.fecha:
    st.session_state.fecha = fecha_elegida
    st.session_state.modo_random = False
    st.rerun()

fecha = st.session_state.fecha
mes = fecha.month
dia = fecha.day
titulo = f"{dia} de {SPANISH_MONTHS[mes]}"

st.markdown(
    f"""
    <div class="hero">
        <div class="kicker">🌍 &nbsp; Un día en el mundo</div>
        <h1>{titulo}</h1>
        <div class="sub">esto ocurrió en la historia</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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
