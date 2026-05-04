# 🌍 Un día como hoy

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3.x-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Wikimedia-API-006699?style=for-the-badge&logo=wikipedia&logoColor=white" alt="Wikimedia API">
</p>

<p align="center">
  Una app en Streamlit para descubrir eventos, nacimientos y muertes históricas de cualquier día del año.
</p>

---

## ✨ Qué hace

- Muestra hechos históricos del día seleccionado
- Organiza la información en `Eventos`, `Nacimientos` y `Muertes`
- Permite filtrar por rango de años
- Incluye un botón `Hoy`
- Incluye un botón `🎲 Sorpréndeme` para explorar fechas al azar
- Enlaza a Wikipedia cuando el dato lo permite

## 🔗 Enlaces

- Repositorio: [github.com/LinaPSP/streamlit_one_day_in_world](https://github.com/LinaPSP/streamlit_one_day_in_world)
- App desplegada: [apponedayinworld.streamlit.app](https://apponedayinworld.streamlit.app/)

## 🧠 Enfoque del ejercicio

Este proyecto también sirve como ejercicio académico de lógica y estructuras de control.

En [app.py](/mnt/c/Users/Lina/Documents/un-dia-en-el-mundo/app.py) se usan:

- `if` para controlar estado y errores
- `for` para recorrer categorías y resultados
- `try/except` para manejar respuestas incompletas de la API

La app resuelve un problema concreto de análisis de datos:

- obtiene información desde una API externa
- filtra resultados por año
- clasifica la información
- decide qué mostrar según el estado de los datos

## 🚀 Cómo ejecutarla

```bash
pip install -r requirements.txt
streamlit run app.py
```

Luego abre la URL local que Streamlit muestra en consola.

## 🧩 Stack

- `Python`
- `Streamlit`
- `requests`
- API oficial de Wikimedia

## 📁 Archivos principales

- [app.py](/mnt/c/Users/Lina/Documents/un-dia-en-el-mundo/app.py): lógica e interfaz de la app
- [requirements.txt](/mnt/c/Users/Lina/Documents/un-dia-en-el-mundo/requirements.txt): dependencias del proyecto

## 🛠️ Si algo falla

Si Wikimedia no responde o no hay conexión, la aplicación muestra un mensaje de error amigable en lugar de romperse.

## 📌 Nota

La aplicación es pequeña a propósito: se entiende rápido, es defendible en una entrega académica y muestra lógica real sin complejidad innecesaria.
