import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN
st.set_page_config(page_title="PureFusion // CD Monitor", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

    /* Fondo principal y texto */
    .stApp {
        background-color: #050a12;
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Contenedor principal con efecto de brillo azul */
    .main .block-container {
        background: rgba(13, 25, 48, 0.7);
        border: 2px solid #00d2ff;
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.3);
        margin-top: 2rem;
        padding: 2rem;
    }

    /* Títulos con fuente tecnológica */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d2ff !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    /* Sidebar con diseño oscuro */
    [data-testid="stSidebar"] {
        background-color: #03070d;
        border-right: 1px solid #1a2a40;
    }

    /* Estilo para las métricas (Cuadritos de arriba) */
    [data-testid="stMetric"] {
        background: rgba(0, 210, 255, 0.05);
        border: 1px solid #00d2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }

    /* Botón de Sincronizar */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00d2ff;
        border: 2px solid #00d2ff;
        font-family: 'Orbitron';
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00d2ff;
        color: black;
        box-shadow: 0 0 20px #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.title("PUREFUSION // CD MONITOR")
st.markdown("<p style='text-align: center; color: #00d2ff; opacity: 0.7;'>INDUSTRIAL AI INTERFACE | CHILE 2026</p>", unsafe_allow_html=True)

# --- SIDEBAR / INPUTS ---
st.sidebar.markdown("### PUREFUSION INPUT")
with st.sidebar.form("input_form"):
    inb = st.slider("INBOUND", 0, 100, 85)
    inv = st.slider("INVERSA", 0, 100, 70)
    pck = st.slider("PICKING", 0, 100, 90)
    out = st.slider("OUTBOUND", 0, 100, 88)
    dot = st.slider("DOTACIÓN", 0, 100, 95)
    st.form_submit_button("SINCRONIZAR DASHBOARD")

# --- MÉTRICAS SUPERIORES ---
m = [inb, inv, pck, out, dot]
labels = ["INBOUND", "INVERSA", "PICKING", "OUTBOUND", "DOTACIÓN"]

cols = st.columns(5)
for i, col in enumerate(cols):
    col.metric(labels[i], f"{m[i]}%")

st.markdown("<hr style='border: 1px solid #1a2a40;'>", unsafe_allow_html=True)

# --- CUERPO CENTRAL: RADAR Y ESTADO ---
col_radar, col_status = st.columns([1.5, 1])

with col_radar:
    st.markdown("#### FIRMA OPERATIVA DEL CENTRO")
    fig = go.Figure(go.Scatterpolar(
        r=m + [m[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor='rgba(0, 210, 255, 0.2)',
        line=dict(color='#00d2ff', width=3)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False),
            angularaxis=dict(color="#e0e0e0", font_family="Rajdhani", font_size=14),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_status:
    st.markdown("#### ESTADO DE LA OPERACIÓN")
    
    # Lógica de estados
    if dot < 85:
        st.error("🚨 ALERTA: Dotación Crítica")
    elif inv < 75:
        st.warning("⚠️ CUELLO DE BOTELLA: Inversa")
    else:
        st.success("✅ OPERACIÓN ESTABLE")
        
    st.info("💡 RECOMENDACIÓN PUREFUSION: Balancear personal de Inbound a Picking para optimizar la curva de salida.")
