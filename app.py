# app.py (Análisis de Ventas de Videojuegos)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Ventas de Videojuegos", page_icon="🎮", layout="wide")

# --- Carga de Datos (con caché para eficiencia) ---
@st.cache_data
def load_data():
    df = pd.read_csv('vgsales.csv')
    df.dropna(inplace=True)
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

# --- Barra Lateral (Sidebar) para Navegación ---
st.sidebar.title("Menú de Análisis")
analysis_choice = st.sidebar.radio(
    "Elige un tipo de análisis:",
    ('Visión General', 'Top N por Ventas', 'Análisis por Género', 'Análisis por Plataforma', 'Tendencia Anual')
)

# --- Título Principal ---
st.title("Consola de Exploración de Ventas de Videojuegos 🎮")


# --- Lógica para mostrar el análisis seleccionado ---

if analysis_choice == 'Visión General':
    st.header("Visión General del Dataset")
    st.write("Estos son los primeros registros del conjunto de datos, que contiene información sobre más de 16,000 videojuegos.")
    st.dataframe(df.head())
    
    st.subheader("Estadísticas Descriptivas")
    st.write(df.describe())

elif analysis_choice == 'Top N por Ventas':
    st.header("Los Videojuegos Más Vendidos")
    
    top_n = st.slider("Selecciona el número de juegos a mostrar:", 5, 50, 10)
    
    top_games = df.head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, top_n / 2.5))
    sns.barplot(x='Global_Sales', y='Name', data=top_games, palette='viridis', ax=ax)
    ax.set_title(f'Top {top_n} Videojuegos más Vendidos Globalmente', fontsize=16)
    ax.set_xlabel('Ventas Globales (en millones)', fontsize=12)
    ax.set_ylabel('Videojuego', fontsize=12)
    st.pyplot(fig)

elif analysis_choice == 'Análisis por Género':
    st.header("Análisis de Ventas por Género")
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x=genre_sales.values, y=genre_sales.index, palette='rocket', ax=ax)
    ax.set_title('Ventas Globales Totales por Género', fontsize=16)
    ax.set_xlabel('Ventas Globales (en millones)', fontsize=12)
    ax.set_ylabel('Género', fontsize=12)
    st.pyplot(fig)

elif analysis_choice == 'Análisis por Plataforma':
    st.header("Análisis de Ventas por Plataforma")
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(15) # Top 15 para claridad
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x=platform_sales.values, y=platform_sales.index, palette='mako', ax=ax)
    ax.set_title('Top 15 Plataformas por Ventas Globales', fontsize=16)
    ax.set_xlabel('Ventas Globales (en millones)', fontsize=12)
    ax.set_ylabel('Plataforma', fontsize=12)
    st.pyplot(fig)

elif analysis_choice == 'Tendencia Anual':
    st.header("Tendencia de Ventas Anuales")
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(yearly_sales.index, yearly_sales.values, marker='o', linestyle='-')
    ax.set_title('Evolución Anual de las Ventas Globales', fontsize=16)
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Ventas Globales (en millones)', fontsize=12)
    ax.grid(True)
    st.pyplot(fig)