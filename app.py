import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="PureFusion | Dashboard", layout="wide")

# 2. ESTILO VISUAL (DARK MODE INDUSTRIAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani:wght@500&display=swap');
    .main { background-color: #040508; color: #00FFD1; font-family: 'Rajdhani', sans-serif; }
    .stMetric { background: #0d1117; border-radius: 15px; border: 1px solid #1F2937; padding: 15px; }
    h1 { font-family: 'Orbitron', sans-serif; letter-spacing: 3px; color: #00FFD1; text-align: center; }
    div[data-testid="stMetricValue"] { color: #00FFD1 !important; font-family: 'Orbitron'; }
    </style>
    """, unsafe_allow_html=True)

st.title("PUREFUSION // CD MONITOR")
st.write("---")

# 3. PANEL LATERAL (OPERADOR)
st.sidebar.title("PUREFUSION INPUT")
with st.sidebar.form("input_form"):
    st.write("### CARGA DE DATOS DE TURNO")
    # Sliders para las 4 áreas clave + Dotación
    inb = st.slider("INBOUND (RECIBO)", 0, 100, 95)
    inv = st.slider("INVERSA (DEVOLUCIONES)", 0, 100, 80)
    pck = st.slider("PICKING (PREPARACIÓN)", 0, 100, 98)
    out = st.slider("OUTBOUND (DESPACHO)", 0, 100, 96)
    dot = st.slider("DOTACIÓN ACTUAL", 0, 100, 100)
    st.form_submit_button("SINCRONIZAR DASHBOARD")

# 4. CÁLCULOS Y MÉTRICAS
m = [inb, inv, pck, out, dot]
labels = ["INBOUND", "INVERSA", "PICKING", "OUTBOUND", "DOTACIÓN"]

# Fila Superior: KPIs Rápidos
cols = st.columns(5)
for i, col in enumerate(cols):
    col.metric(labels[i], f"{m[i]}%", delta=f"{m[i]-90}%" if m[i] >= 90 else f"{m[i]-90}%")

st.write("---")

# 5. VISUALIZACIÓN CENTRAL (RADAR Y ALERTAS)
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("FIRMA OPERATIVA DEL CENTRO")
    fig = go.Figure(go.Scatterpolar(
          r=m,
          theta=labels,
          fill='toself',
          line_color='#00FFD1'
    ))
    fig.update_layout(
      polar=dict(radialaxis=dict(visible=False), bgcolor="#07090c"),
      showlegend=False, 
      paper_bgcolor='rgba(0,0,0,0)', 
      height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("ESTADO DE LA OPERACIÓN")
    
    # Semáforo de Riesgo basado en Dotación e Inversa
    if dot < 85:
        st.error(f"🚨 ALERTA CRÍTICA: Dotación al {dot}%. Riesgo inminente de fatiga silenciosa.")
    elif inv < 75:
        st.warning("⚠️ CUELLO DE BOTELLA: Logística Inversa saturada. Impacto en flujo de picking.")
    else:
        st.success("✅ OPERACIÓN ESTABLE: Flujo constante y dotación segura.")
    
    st.write("---")
    st.markdown("**RECOMENDACIÓN PUREFUSION:**")
    if pck < inb:
        st.info("💡 Mover personal de Inbound a Picking para equilibrar la firma operativa.")
    else:
        st.info("💡 Mantener flujo actual. Sincronización detectada.")

st.markdown("<p style='text-align: center; color: #4F4F4F; font-family: Orbitron; font-size: 0.7rem; margin-top: 50px;'>PURE SOLUTIONS INDUSTRIAL DIVISION | CHILE 2026</p>", unsafe_allow_html=True)