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


st.set_page_config(page_title="Un dia como hoy", page_icon=":calendar:", layout="centered")

# Usa colores del tema nativo de Streamlit y solo ajusta contraste local.
css_vars = """
:root {
    --app-bg: transparent;
    --text-main: var(--text-color);
    --text-muted: color-mix(in srgb, var(--text-color) 72%, transparent);
    --hero-title: var(--text-color);
    --card-bg: color-mix(in srgb, var(--secondary-background-color) 82%, var(--background-color));
    --card-border: color-mix(in srgb, var(--text-color) 18%, transparent);
    --btn-bg: var(--primary-color);
    --btn-fg: #ffffff;
    --btn-hover: color-mix(in srgb, var(--primary-color) 80%, white);
    --link-color: var(--primary-color);
}
"""

st.markdown(
    """
    <style>
    """
    + css_vars
    + """
    .stApp {
        background: var(--app-bg);
        color: var(--text-main);
    }
    [data-testid="stAppViewContainer"] {
        background: transparent;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stToolbar"] {
        right: 0.75rem;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] label,
    .stSlider label,
    .stTabs [data-baseweb="tab"] {
        color: var(--text-main);
    }
    .stButton > button {
        background: var(--btn-bg);
        color: var(--btn-fg);
        border: 1px solid var(--btn-bg);
        border-radius: 999px;
        font-weight: 700;
    }
    .stButton > button:hover {
        background: var(--btn-hover);
        border-color: var(--btn-hover);
        color: #0b1020;
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 0.2rem color-mix(in srgb, var(--btn-bg) 40%, transparent);
    }
    .hero {
        padding: 0.5rem 0 1.5rem 0;
    }
    .hero h1 {
        font-size: 3rem;
        line-height: 1;
        margin: 0;
        color: var(--hero-title);
    }
    .hero p {
        margin: 0.35rem 0 0;
        font-size: 1.1rem;
        color: var(--text-muted);
    }
    .evento-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
    }
    .evento-card .anio {
        font-size: 1.55rem;
        font-weight: 700;
        color: var(--link-color);
        margin-bottom: 0.45rem;
    }
    .evento-card .descripcion {
        color: var(--text-main);
        line-height: 1.5;
        margin-bottom: 0.6rem;
    }
    .evento-card a {
        color: var(--link-color);
        text-decoration: none;
        font-weight: 600;
    }
    .evento-card a:hover {
        text-decoration: underline;
    }
    [data-testid="stInfo"] {
        color: var(--text-main);
    }
    [data-testid="stAlertContentError"] {
        color: var(--text-main);
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
        <h1>{titulo}</h1>
        <p>esto paso en la historia</p>
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
