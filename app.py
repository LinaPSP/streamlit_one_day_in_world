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


st.set_page_config(page_title="Un dia como hoy", page_icon=":calendar:", layout="centered")

st.markdown(
    """
    <style>
    .hero {
        padding: 0.5rem 0 1.5rem 0;
    }
    .hero h1 {
        font-size: 3rem;
        line-height: 1;
        margin: 0;
        color: #102542;
    }
    .hero p {
        margin: 0.35rem 0 0;
        font-size: 1.1rem;
        color: #5c6b73;
    }
    .evento-card {
        background: linear-gradient(180deg, #ffffff 0%, #f6f8fb 100%);
        border: 1px solid #d9e2ec;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 10px 25px rgba(16, 37, 66, 0.06);
    }
    .evento-card .anio {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0b6e4f;
        margin-bottom: 0.45rem;
    }
    .evento-card .descripcion {
        color: #1f2933;
        line-height: 1.5;
        margin-bottom: 0.6rem;
    }
    .evento-card a {
        color: #0f5cc0;
        text-decoration: none;
        font-weight: 600;
    }
    .evento-card a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600)
def obtener_datos(mes: int, dia: int) -> dict:
    # Consulta la API y devuelve un diccionario vacio si ocurre un error.
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/es/onthisday/all/{mes}/{dia}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


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


def ir_a_hoy() -> None:
    # Restablece la fecha actual y fuerza el refresco de la interfaz.
    st.session_state.fecha = datetime.date.today()
    st.session_state.modo_random = False
    st.rerun()


def fecha_aleatoria() -> None:
    # Genera un mes y un dia validos para construir una fecha aleatoria.
    mes_r = random.randint(1, 12)
    max_dia = calendar.monthrange(2024, mes_r)[1]
    dia_r = random.randint(1, max_dia)
    st.session_state.fecha = datetime.date(2024, mes_r, dia_r)
    st.session_state.modo_random = True
    st.rerun()


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
    st.button("Hoy", use_container_width=True, on_click=ir_a_hoy)

with col_random:
    st.button("🎲 Sorprendeme", use_container_width=True, on_click=fecha_aleatoria)

datos = obtener_datos(mes, dia)

# Si la API no responde, se informa al usuario y se detiene la ejecucion.
if not datos:
    st.error("No se pudieron cargar los datos de Wikimedia. Revisa tu conexion e intenta de nuevo.")
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
