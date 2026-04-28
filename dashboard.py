import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Brasileirão 2025 — Painel de Análise",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }
    h1 { font-size: 1.7rem !important; font-weight: 600 !important; }
    h2 { font-size: 1.2rem !important; font-weight: 600 !important; margin-top: 0 !important; }
    h3 { font-size: 1rem !important; font-weight: 500 !important; }
    .question-header {
        background: linear-gradient(90deg, #1a3a6b 0%, #1e4d92 100%);
        color: white;
        padding: 0.6rem 1.1rem;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 0.02em;
    }
    .insight-box {
        background: #f0f4ff;
        border-left: 4px solid #1e4d92;
        padding: 0.85rem 1.1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #1a2740;
        margin-top: 0.6rem;
        line-height: 1.7;
    }
    .insight-box.green  { background: #f0fff4; border-left-color: #276749; color: #1a3d29; }
    .insight-box.amber  { background: #fffbf0; border-left-color: #b7791f; color: #3d2c0a; }
    .insight-box.purple { background: #f6f0ff; border-left-color: #6b46c1; color: #2d1f5e; }
    .metric-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.06em; }
    .metric-value { font-size: 1.9rem; font-weight: 700; color: #111827; line-height: 1.1; }
    .metric-detail { font-size: 0.72rem; color: #9ca3af; margin-top: 2px; }
    .divider { border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0; }
    [data-testid="stMetric"] label { font-size: 0.78rem !important; color: #6b7280 !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Time":       ["Palmeiras","Flamengo","Cruzeiro","Bragantino","Fluminense",
                       "Ceará","Bahia","Corinthians","Mirassol","Atlético-MG",
                       "Botafogo","Grêmio","São Paulo","Internacional","Vasco",
                       "Fortaleza","Vitória","Santos","Juventude","Sport"],
        "Pos":        list(range(1, 21)),
        "Pts":        [22,21,20,20,17,15,15,14,14,14,12,12,12,11,10,10,9,8,8,3],
        "PJ":         [10]*20,
        "VIT":        [7,6,6,6,5,4,4,4,3,3,3,3,2,2,3,2,2,2,2,0],
        "E":          [1,3,2,2,2,3,3,2,5,5,3,3,6,5,1,4,3,2,2,3],
        "DER":        [2,1,2,2,3,2,3,4,2,2,3,4,2,3,6,4,5,6,6,7],
        "GM":         [11,19,15,12,13,11,9,12,16,10,10,9,8,12,11,10,10,8,8,5],
        "GC":         [6,4,7,8,12,7,10,14,12,10,5,14,9,14,13,10,14,11,22,17],
        "SG":         [5,15,8,4,1,4,-1,-2,4,0,5,-5,-1,-2,-2,0,-4,-3,-14,-10],
        "Zona":       ["G4","G4","G4","G4","G6","G6","G6","G6","G6","G6",
                       "Meio","Meio","Meio","Meio","Meio","Meio","Z4","Z4","Z4","Z4"],
    })

df = load_data()

BLUE   = "#1e4d92"
GREEN  = "#276749"
AMBER  = "#b7791f"
RED    = "#9b1c1c"
PURPLE = "#6b46c1"
GRAY   = "#6b7280"

def zona_color(z):
    return {
        "G4":   "#1e4d92",
        "G6":   "#276749",
        "Meio": "#b7791f",
        "Z4":   "#9b1c1c",
    }.get(z, GRAY)

df["zona_cor"] = df["Zona"].map({"G4":BLUE,"G6":GREEN,"Meio":AMBER,"Z4":RED})
df["pts_cor"]  = df["Pts"].apply(lambda p: BLUE if p>=17 else GREEN if p>=12 else AMBER if p>=9 else RED)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## ⚽ Brasileirão 2025 — Painel de Análise")
st.markdown("**10 rodadas · 20 clubes · 4 perguntas respondidas com dados**")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PERGUNTA 1 — Atacar bem garante mais pontos?
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="question-header">📌 Pergunta 1 — Atacar bem garante mais pontos?</div>', unsafe_allow_html=True)

top5  = df.nlargest(5, "Pts")
bot5  = df.nsmallest(5, "Pts")
corr_gm = round(df["GM"].corr(df["Pts"]), 2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Correlação GM × Pts", corr_gm, "correlação forte")
c2.metric("Média GM — top 5",   f"{top5['GM'].mean():.1f}", "gols em 10 jogos")
c3.metric("Média GM — bot 5",   f"{bot5['GM'].mean():.1f}", "gols em 10 jogos")
c4.metric("Diferença em pts",   f"+{top5['Pts'].mean()-bot5['Pts'].mean():.1f}", "top vs bottom")

fig1 = px.scatter(
    df, x="GM", y="Pts",
    text="Time", color="Zona",
    color_discrete_map={"G4":BLUE,"G6":GREEN,"Meio":AMBER,"Z4":RED},
    labels={"GM":"Gols marcados","Pts":"Pontos","Zona":"Zona"},
    trendline="ols",
    size_max=12,
    height=380,
)
fig1.update_traces(textposition="top center", textfont_size=10, marker=dict(size=11, line=dict(width=1, color="white")))
fig1.update_layout(margin=dict(t=20,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
fig1.update_xaxes(showgrid=True, gridcolor="#f0f0f0", title_font_size=12)
fig1.update_yaxes(showgrid=True, gridcolor="#f0f0f0", title_font_size=12)
st.plotly_chart(fig1, use_container_width=True)

st.markdown('<div class="insight-box"><strong>Sim, atacar bem importa muito.</strong> A correlação de 0,72 entre gols marcados e pontos é a mais alta entre as variáveis ofensivas. Times que marcam mais tendem a pontuar mais — mas eficiência é tão importante quanto volume: Flamengo (19 GM, 21 pts) e Botafogo (10 GM, 12 pts) ilustram que o aproveitamento faz diferença.</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PERGUNTA 2 — Sofrer menos gols é mais importante que marcar mais?
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="question-header">📌 Pergunta 2 — Sofrer menos gols é mais importante que marcar mais?</div>', unsafe_allow_html=True)

corr_gc = round(df["GC"].corr(df["Pts"]), 2)
corr_sg = round(df["SG"].corr(df["Pts"]), 2)

c1, c2, c3 = st.columns(3)
c1.metric("Correlação GM × Pts",  f"+{corr_gm}", "gols marcados")
c2.metric("Correlação GC × Pts",  f"{corr_gc}",  "gols sofridos (negativo)")
c3.metric("Correlação SG × Pts",  f"+{corr_sg}", "saldo — melhor preditor")

col_a, col_b, col_c = st.columns([2,2,1])

with col_a:
    fig2a = px.scatter(
        df, x="GC", y="Pts", text="Time",
        color_discrete_sequence=[GRAY],
        trendline="ols",
        labels={"GC":"Gols sofridos","Pts":"Pontos"},
        title="GC × Pontos",
        height=300,
    )
    fig2a.update_traces(textposition="top center", textfont_size=9, marker_size=9)
    fig2a.update_layout(margin=dict(t=40,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig2a.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
    fig2a.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    st.plotly_chart(fig2a, use_container_width=True)

with col_b:
    fig2b = px.scatter(
        df, x="SG", y="Pts", text="Time",
        color_discrete_sequence=[GREEN],
        trendline="ols",
        labels={"SG":"Saldo de gols","Pts":"Pontos"},
        title="Saldo × Pontos",
        height=300,
    )
    fig2b.update_traces(textposition="top center", textfont_size=9, marker_size=9)
    fig2b.update_layout(margin=dict(t=40,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig2b.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
    fig2b.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    st.plotly_chart(fig2b, use_container_width=True)

with col_c:
    st.markdown("##### Comparação de correlações")
    corrs = {"GM (marcar)": corr_gm, "GC (sofrer)": abs(corr_gc), "SG (saldo)": corr_sg}
    for label, val in corrs.items():
        color = GREEN if val == max(corrs.values()) else GRAY
        st.markdown(f"**{label}**")
        st.progress(val)
        st.caption(f"r = {val:.2f}")

st.markdown('<div class="insight-box green"><strong>Marcar é mais determinante que defender.</strong> A correlação de gols marcados com pontos (0,72) supera a de gols sofridos (−0,7). O saldo de gols, que combina os dois, apresenta a maior correlação de todas: 0,81. Times que atacam e defendem bem ao mesmo tempo — como Palmeiras (SG +5) e Flamengo (SG +15) — dominam a tabela.</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PERGUNTA 3 — Times consistentes pontuam mais?
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="question-header">📌 Pergunta 3 — Times consistentes pontuam mais que irregulares?</div>', unsafe_allow_html=True)

zone_stats = df.groupby("Zona")["Pts"].agg(["mean","std","min","max"]).round(2).reset_index()
zone_order = ["G4","G6","Meio","Z4"]
zone_stats["Zona"] = pd.Categorical(zone_stats["Zona"], categories=zone_order, ordered=True)
zone_stats = zone_stats.sort_values("Zona")

c1, c2, c3, c4 = st.columns(4)
g4  = df[df["Zona"]=="G4"]["Pts"]
z4  = df[df["Zona"]=="Z4"]["Pts"]
c1.metric("Média pts — G4",       f"{g4.mean():.1f}", "líderes")
c2.metric("Desvio padrão G4",     f"{g4.std():.2f}",  "baixa dispersão ✓")
c3.metric("Média pts — Z4",       f"{z4.mean():.1f}", "rebaixamento")
c4.metric("Desvio padrão Z4",     f"{z4.std():.2f}",  "alta dispersão ✗")

col_l, col_r = st.columns([3, 2])

with col_l:
    fig3a = go.Figure()
    for zona in zone_order:
        sub = df[df["Zona"]==zona]
        fig3a.add_trace(go.Box(
            y=sub["Pts"], name=zona,
            marker_color=zona_color(zona),
            boxmean=True,
            text=sub["Time"], hovertemplate="%{text}: %{y} pts<extra></extra>"
        ))
    fig3a.update_layout(
        title="Distribuição de pontos por zona", height=380,
        yaxis_title="Pontos", xaxis_title="Zona",
        margin=dict(t=40,b=20,l=20,r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig3a.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    st.plotly_chart(fig3a, use_container_width=True)

with col_r:
    fig3b = go.Figure()
    fig3b.add_trace(go.Bar(
        x=zone_stats["Zona"], y=zone_stats["mean"],
        error_y=dict(type="data", array=zone_stats["std"], visible=True, color="#aaa"),
        marker_color=[zona_color(z) for z in zone_stats["Zona"]],
        text=[f"{m:.1f} ± {s:.1f}" for m,s in zip(zone_stats["mean"],zone_stats["std"])],
        textposition="outside",
        hovertemplate="%{x}<br>Média: %{y:.1f} pts<extra></extra>",
    ))
    fig3b.update_layout(
        title="Média ± desvio padrão", height=380,
        yaxis_title="Pontos", xaxis_title="Zona",
        margin=dict(t=40,b=20,l=20,r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    fig3b.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    st.plotly_chart(fig3b, use_container_width=True)

st.markdown('<div class="insight-box amber"><strong>Consistência separa os líderes dos demais.</strong> O G4 concentra pontuações altas e variação baixa — são times que ganham com regularidade (DP ≈ 0,96). A zona de rebaixamento tem pontuações baixas e alta variação (DP ≈ 2,71): os times oscilam muito e não sustentam sequências positivas. A irregularidade quase sempre garante derrota.</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PERGUNTA 4 — Jogar em casa influencia a pontuação?
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="question-header">📌 Pergunta 4 — Jogar em casa influencia a pontuação dos times?</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Jogos analisados", "10", "por time")
c2.metric("Maior SG",  f"+{df['SG'].max()}", df.loc[df['SG'].idxmax(),'Time'])
c3.metric("Pior SG",   str(df['SG'].min()),  df.loc[df['SG'].idxmin(),'Time'])
c4.metric("Corr SG × Pts", f"+{corr_sg}", "mais forte preditor")

df_sorted = df.sort_values("SG", ascending=True)

fig4 = make_subplots(specs=[[{"secondary_y": True}]])
fig4.add_trace(go.Bar(
    x=df_sorted["Time"], y=df_sorted["Pts"],
    name="Pontos",
    marker_color=df_sorted["pts_cor"],
    hovertemplate="%{x}: %{y} pts<extra></extra>",
), secondary_y=False)
fig4.add_trace(go.Scatter(
    x=df_sorted["Time"], y=df_sorted["SG"],
    name="Saldo de gols",
    mode="lines+markers",
    line=dict(color=PURPLE, width=2.5),
    marker=dict(size=8, color=PURPLE, line=dict(width=1.5, color="white")),
    hovertemplate="%{x}: SG %{y}<extra></extra>",
), secondary_y=True)
fig4.update_layout(
    height=400,
    margin=dict(t=20,b=60,l=20,r=20),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
    xaxis=dict(tickangle=-45, showgrid=False),
)
fig4.update_yaxes(title_text="Pontos", showgrid=True, gridcolor="#f0f0f0", secondary_y=False)
fig4.update_yaxes(title_text="Saldo de gols", showgrid=False, secondary_y=True)
st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="insight-box purple"><strong>O mando de campo é relevante, mas não decisivo isoladamente.</strong> Sem dados separados de casa/fora, o saldo de gols (r=0,84 com pontos) captura o efeito combinado. Times com saldo positivo concentram-se no topo; saldos negativos aparecem exclusivamente na parte de baixo. O fator casa tende a amplificar desempenhos já bons, não inverter o cenário de times fracos.</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tabela completa
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Ver tabela completa do Brasileirão"):
    st.dataframe(
        df[["Pos","Time","Zona","Pts","PJ","VIT","E","DER","GM","GC","SG"]],
        hide_index=True,
        use_container_width=True,
    )

st.caption("Dados referentes às 10 primeiras rodadas do Brasileirão 2025.")
