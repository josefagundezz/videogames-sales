# app.py (Análisis de Ventas de Videojuegos - Bilingüe)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. DICCIONARIO DE TEXTOS ---
TEXTS = {
    'es': {
        'page_title': "Análisis de Ventas de Videojuegos",
        'title': "Consola de Exploración de Ventas de Videojuegos 🎮",
        'sidebar_title': "Menú de Análisis",
        'radio_label': "Elige un tipo de análisis:",
        'nav': {
            'overview': "Visión General",
            'top_n': "Top N por Ventas",
            'genre': "Análisis por Género",
            'platform': "Análisis por Plataforma",
            'yearly': "Tendencia Anual"
        },
        'overview_header': "Visión General del Dataset",
        'overview_desc': "Primeros registros del conjunto de datos, que contiene información sobre más de 16,000 videojuegos.",
        'overview_stats': "Estadísticas Descriptivas",
        'top_n_header': "Los Videojuegos Más Vendidos",
        'top_n_slider': "Selecciona el número de juegos a mostrar:",
        'top_n_plot_title': "Top {} Videojuegos más Vendidos Globalmente",
        'sales_label': "Ventas Globales (en millones)",
        'game_label': "Videojuego",
        'genre_header': "Análisis de Ventas por Género",
        'genre_plot_title': "Ventas Globales Totales por Género",
        'genre_label': "Género",
        'platform_header': "Análisis de Ventas por Plataforma",
        'platform_plot_title': "Top 15 Plataformas por Ventas Globales",
        'platform_label': "Plataforma",
        'yearly_header': "Tendencia de Ventas Anuales",
        'yearly_plot_title': "Evolución Anual de las Ventas Globales",
        'year_label': "Año"
    },
    'en': {
        'page_title': "Video Game Sales Analysis",
        'title': "Video Game Sales Exploration Console 🎮",
        'sidebar_title': "Analysis Menu",
        'radio_label': "Choose an analysis type:",
        'nav': {
            'overview': "Overview",
            'top_n': "Top N by Sales",
            'genre': "Genre Analysis",
            'platform': "Platform Analysis",
            'yearly': "Yearly Trend"
        },
        'overview_header': "Dataset Overview",
        'overview_desc': "First records of the dataset, containing information on over 16,000 video games.",
        'overview_stats': "Descriptive Statistics",
        'top_n_header': "Best-Selling Video Games",
        'top_n_slider': "Select the number of games to display:",
        'top_n_plot_title': "Top {} Best-Selling Video Games Globally",
        'sales_label': "Global Sales (in millions)",
        'game_label': "Video Game",
        'genre_header': "Sales Analysis by Genre",
        'genre_plot_title': "Total Global Sales by Genre",
        'genre_label': "Genre",
        'platform_header': "Sales Analysis by Platform",
        'platform_plot_title': "Top 15 Platforms by Global Sales",
        'platform_label': "Platform",
        'yearly_header': "Annual Sales Trend",
        'yearly_plot_title': "Annual Evolution of Global Sales",
        'year_label': "Year"
    }
}

# --- LÓGICA DE LA APP ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
def toggle_language():
    st.session_state.lang = 'es' if st.session_state.lang == 'en' else 'en'
st.set_page_config(page_title=TEXTS[st.session_state.lang]['page_title'], page_icon="🎮", layout="wide")
texts = TEXTS[st.session_state.lang]

@st.cache_data
def load_data():
    df = pd.read_csv('vgsales.csv')
    df.dropna(inplace=True)
    df['Year'] = df['Year'].astype(int)
    return df
df = load_data()

# --- INTERFAZ ---
st.button('Español / English', on_click=toggle_language)
st.title(texts['title'])

st.sidebar.title(texts['sidebar_title'])
# Usamos una clave neutral para las opciones y `format_func` para mostrar la traducción
nav_options_keys = list(texts['nav'].keys())
analysis_choice_key = st.sidebar.radio(
    texts['radio_label'],
    nav_options_keys,
    format_func=lambda key: texts['nav'][key]
)

if analysis_choice_key == 'overview':
    st.header(texts['overview_header'])
    st.write(texts['overview_desc'])
    st.dataframe(df.head())
    st.subheader(texts['overview_stats'])
    st.write(df.describe())

elif analysis_choice_key == 'top_n':
    st.header(texts['top_n_header'])
    top_n = st.slider(texts['top_n_slider'], 5, 50, 10)
    top_games = df.head(top_n)
    fig, ax = plt.subplots(figsize=(12, top_n / 2.5))
    sns.barplot(x='Global_Sales', y='Name', data=top_games, palette='viridis', ax=ax, hue='Name', legend=False)
    ax.set_title(texts['top_n_plot_title'].format(top_n), fontsize=16)
    ax.set_xlabel(texts['sales_label'], fontsize=12)
    ax.set_ylabel(texts['game_label'], fontsize=12)
    st.pyplot(fig)

elif analysis_choice_key == 'genre':
    st.header(texts['genre_header'])
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x=genre_sales.values, y=genre_sales.index, palette='rocket', ax=ax, hue=genre_sales.index, legend=False)
    ax.set_title(texts['genre_plot_title'], fontsize=16)
    ax.set_xlabel(texts['sales_label'], fontsize=12)
    ax.set_ylabel(texts['genre_label'], fontsize=12)
    st.pyplot(fig)

elif analysis_choice_key == 'platform':
    st.header(texts['platform_header'])
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x=platform_sales.values, y=platform_sales.index, palette='mako', ax=ax, hue=platform_sales.index, legend=False)
    ax.set_title(texts['platform_plot_title'], fontsize=16)
    ax.set_xlabel(texts['sales_label'], fontsize=12)
    ax.set_ylabel(texts['platform_label'], fontsize=12)
    st.pyplot(fig)

elif analysis_choice_key == 'yearly':
    st.header(texts['yearly_header'])
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(yearly_sales.index, yearly_sales.values, marker='o', linestyle='-')
    ax.set_title(texts['yearly_plot_title'], fontsize=16)
    ax.set_xlabel(texts['year_label'], fontsize=12)
    ax.set_ylabel(texts['sales_label'], fontsize=12)
    ax.grid(True)
    st.pyplot(fig)