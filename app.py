import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="PureFusion // CD Monitor", layout="wide")

# 2. ESTILO VISUAL (CSS BLINDADO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500&display=swap');
    .stApp { background-color: #050a12; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main .block-container {
        background: rgba(13, 25, 48, 0.7);
        border: 2px solid #00d2ff;
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.3);
        margin-top: 2rem; padding: 2rem;
    }
    h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; color: #00d2ff !important; text-transform: uppercase; letter-spacing: 2px; }
    [data-testid="stMetric"] { background: rgba(0, 210, 255, 0.05); border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
    .stButton>button { width: 100%; background-color: transparent; color: #00d2ff; border: 2px solid #00d2ff; font-family: 'Orbitron'; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.title("PUREFUSION // CD MONITOR")
st.markdown("<p style='text-align: center; color: #00d2ff; opacity: 0.7;'>INDUSTRIAL AI INTERFACE | CHILE 2026</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar.form("input_form"):
    st.markdown("### PUREFUSION INPUT")
    inb = st.slider("INBOUND", 0, 100, 85)
    inv = st.slider("INVERSA", 0, 100, 70)
    pck = st.slider("PICKING", 0, 100, 90)
    out = st.slider("OUTBOUND", 0, 100, 88)
    dot = st.slider("DOTACIÓN", 0, 100, 95)
    st.form_submit_button("SINCRONIZAR DASHBOARD")

# --- MÉTRICAS ---
m = [inb, inv, pck, out, dot]
labels = ["INBOUND", "INVERSA", "PICKING", "OUTBOUND", "DOTACIÓN"]

cols = st.columns(5)
for i, col in enumerate(cols):
    col.metric(labels[i], f"{m[i]}%")

st.write("---")

# --- CUERPO CENTRAL ---
col_radar, col_status = st.columns([1.5, 1])

with col_radar:
    st.markdown("#### FIRMA OPERATIVA")
    # GRÁFICO RECONSTRUIDO CON SINTAXIS BÁSICA (A prueba de errores)
    df_radar = pd.DataFrame(dict(r=m, theta=labels))
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color='#00d2ff', fillcolor='rgba(0, 210, 255, 0.2)')
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col_status:
    st.markdown("#### ESTADO")
    if dot < 85:
        st.error("🚨 ALERTA: Dotación Crítica")
    elif inv < 75:
        st.warning("⚠️ CUELLO DE BOTELLA: Inversa")
    else:
        st.success("✅ OPERACIÓN ESTABLE")
    st.info("💡 RECOMENDACIÓN PUREFUSION: Balancear personal de Inbound a Picking para optimizar la curva de salida.")
