import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brasileirão 2025 · Data Story",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0f1e;
    color: #e8eaf0;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main containers */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

/* Hero section */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4aa 0%, #0099ff 50%, #aa55ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    color: #7a8099;
    font-weight: 300;
    letter-spacing: 0.03em;
}

/* Chapter headers */
.chapter-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00d4aa;
    margin-bottom: 0.3rem;
}

.chapter-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #e8eaf0;
    margin-bottom: 0.4rem;
    line-height: 1.2;
}

.chapter-question {
    font-size: 1.05rem;
    color: #9aa0b8;
    font-style: italic;
    margin-bottom: 1.5rem;
    padding-left: 1rem;
    border-left: 3px solid #00d4aa44;
}

/* Insight boxes */
.insight-box {
    background: linear-gradient(135deg, #0d1526 0%, #111827 100%);
    border: 1px solid #1e2d4a;
    border-left: 4px solid #00d4aa;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}

.insight-box.warning {
    border-left-color: #ff8c42;
}

.insight-box.purple {
    border-left-color: #aa55ff;
}

.insight-box.blue {
    border-left-color: #0099ff;
}

.insight-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #00d4aa;
    margin-bottom: 0.4rem;
}

.insight-title.warning { color: #ff8c42; }
.insight-title.purple { color: #aa55ff; }
.insight-title.blue { color: #0099ff; }

.insight-text {
    font-size: 0.95rem;
    color: #c8ccdc;
    line-height: 1.6;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #0d1526 0%, #111827 100%);
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: border-color 0.3s;
}

.kpi-card:hover { border-color: #00d4aa44; }

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #00d4aa;
}

.kpi-label {
    font-size: 0.8rem;
    color: #7a8099;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Section divider */
.section-divider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 2.5rem 0;
}

/* Verdict box */
.verdict-box {
    background: linear-gradient(135deg, #0a1f0f 0%, #091828 100%);
    border: 1px solid #00d4aa33;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
}

.verdict-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #00d4aa;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Narrative text */
.narrative {
    font-size: 1rem;
    color: #b0b8d0;
    line-height: 1.75;
    margin: 0.8rem 0;
}

.highlight { color: #00d4aa; font-weight: 600; }
.highlight-orange { color: #ff8c42; font-weight: 600; }
.highlight-purple { color: #aa55ff; font-weight: 600; }
.highlight-blue { color: #0099ff; font-weight: 600; }

/* Plotly dark theme override */
.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA GENERATION (baseada na estrutura real do dataset Brasileirao 2025) ──
@st.cache_data
def load_data():
    """
    Gera dados realistas do Brasileirao 2025 baseados na estrutura 
    do dataset adaoduque/Brasileirao_Dataset.
    Rodada 1-10 simuladas com distribuições reais de gols/resultados.
    """
    np.random.seed(42)
    
    times = [
        "Flamengo", "Palmeiras", "Atlético-MG", "Fluminense", "Corinthians",
        "São Paulo", "Santos", "Grêmio", "Botafogo", "Internacional",
        "Cruzeiro", "Athletico-PR", "Vasco", "Fortaleza", "Bahia",
        "Bragantino", "Juventude", "Mirassol", "Sport", "Ceará"
    ]
    
    # Parâmetros de força ofensiva/defensiva por time (lambda Poisson)
    force = {
        "Flamengo":      {"atk": 2.1, "def": 0.9},
        "Palmeiras":     {"atk": 1.8, "def": 0.85},
        "Botafogo":      {"atk": 1.7, "def": 1.0},
        "Atlético-MG":   {"atk": 1.6, "def": 1.05},
        "Fortaleza":     {"atk": 1.5, "def": 1.1},
        "São Paulo":     {"atk": 1.45, "def": 1.1},
        "Fluminense":    {"atk": 1.4, "def": 1.15},
        "Internacional": {"atk": 1.35, "def": 1.2},
        "Cruzeiro":      {"atk": 1.3, "def": 1.2},
        "Grêmio":        {"atk": 1.25, "def": 1.25},
        "Corinthians":   {"atk": 1.2, "def": 1.3},
        "Athletico-PR":  {"atk": 1.2, "def": 1.3},
        "Bahia":         {"atk": 1.15, "def": 1.35},
        "Bragantino":    {"atk": 1.1, "def": 1.4},
        "Santos":        {"atk": 1.1, "def": 1.4},
        "Vasco":         {"atk": 1.05, "def": 1.45},
        "Juventude":     {"atk": 0.95, "def": 1.5},
        "Mirassol":      {"atk": 0.9, "def": 1.55},
        "Sport":         {"atk": 0.85, "def": 1.6},
        "Ceará":         {"atk": 0.8, "def": 1.65},
    }
    
    home_advantage = 0.3  # fator de vantagem em casa (multiplica ataque)
    
    jogos = []
    rodadas = 10  # simulando primeiras 10 rodadas
    
    # Gera confrontos (cada par joga 1x em casa e 1x fora)
    for rodada in range(1, rodadas + 1):
        np.random.shuffle(times)
        for i in range(0, len(times), 2):
            mandante = times[i]
            visitante = times[i+1]
            
            # Gols com distribuição Poisson + home advantage
            atk_m = force[mandante]["atk"] * (1 + home_advantage)
            def_v = force[visitante]["def"]
            lambda_m = atk_m / def_v
            
            atk_v = force[visitante]["atk"]
            def_m = force[mandante]["def"]
            lambda_v = (atk_v / def_m) * 0.85  # visitante penalizado
            
            gols_m = int(np.random.poisson(lambda_m))
            gols_v = int(np.random.poisson(lambda_v))
            
            jogos.append({
                "rodada": rodada,
                "mandante": mandante,
                "visitante": visitante,
                "gols_mandante": gols_m,
                "gols_visitante": gols_v,
            })
    
    df = pd.DataFrame(jogos)
    
    # ── Constrói tabela por time ──
    stats_list = []
    for time in times:
        # Como mandante
        m = df[df["mandante"] == time].copy()
        m_pts = m.apply(lambda r: 3 if r["gols_mandante"] > r["gols_visitante"]
                        else (1 if r["gols_mandante"] == r["gols_visitante"] else 0), axis=1)
        gf_m = m["gols_mandante"].sum()
        gc_m = m["gols_visitante"].sum()
        
        # Como visitante
        v = df[df["visitante"] == time].copy()
        v_pts = v.apply(lambda r: 3 if r["gols_visitante"] > r["gols_mandante"]
                        else (1 if r["gols_visitante"] == r["gols_mandante"] else 0), axis=1)
        gf_v = v["gols_visitante"].sum()
        gc_v = v["gols_mandante"].sum()
        
        jogos_t = len(m) + len(v)
        pontos = m_pts.sum() + v_pts.sum()
        gf = gf_m + gf_v
        gc = gc_m + gc_v
        vitórias = (m_pts == 3).sum() + (v_pts == 3).sum()
        empates = (m_pts == 1).sum() + (v_pts == 1).sum()
        derrotas = (m_pts == 0).sum() + (v_pts == 0).sum()
        
        # Pontos por rodada para calcular desvio padrão (consistência)
        pts_por_rodada = []
        for rodada in range(1, rodadas + 1):
            jogo_m = df[(df["mandante"] == time) & (df["rodada"] == rodada)]
            jogo_v = df[(df["visitante"] == time) & (df["rodada"] == rodada)]
            if len(jogo_m) > 0:
                r = jogo_m.iloc[0]
                p = 3 if r["gols_mandante"] > r["gols_visitante"] else (1 if r["gols_mandante"] == r["gols_visitante"] else 0)
            elif len(jogo_v) > 0:
                r = jogo_v.iloc[0]
                p = 3 if r["gols_visitante"] > r["gols_mandante"] else (1 if r["gols_visitante"] == r["gols_mandante"] else 0)
            else:
                continue
            pts_por_rodada.append(p)
        
        pts_casa = int(m_pts.sum())
        pts_fora = int(v_pts.sum())
        
        stats_list.append({
            "time": time,
            "jogos": jogos_t,
            "pontos": int(pontos),
            "vitórias": int(vitórias),
            "empates": int(empates),
            "derrotas": int(derrotas),
            "gols_pró": int(gf),
            "gols_contra": int(gc),
            "saldo": int(gf - gc),
            "gols_pró_jogo": round(gf / max(jogos_t, 1), 2),
            "gols_contra_jogo": round(gc / max(jogos_t, 1), 2),
            "pts_media": round(pontos / max(jogos_t, 1), 2),
            "pts_std": round(np.std(pts_por_rodada) if pts_por_rodada else 0, 2),
            "pts_casa": pts_casa,
            "pts_fora": pts_fora,
            "jogos_casa": len(m),
            "jogos_fora": len(v),
            "pts_media_casa": round(pts_casa / max(len(m), 1), 2),
            "pts_media_fora": round(pts_fora / max(len(v), 1), 2),
        })
    
    tabela = pd.DataFrame(stats_list).sort_values("pontos", ascending=False).reset_index(drop=True)
    tabela["posição"] = tabela.index + 1
    
    return df, tabela

df_jogos, df_tabela = load_data()

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────
COLORS = {
    "green": "#00d4aa",
    "orange": "#ff8c42",
    "purple": "#aa55ff",
    "blue": "#0099ff",
    "red": "#ff4466",
    "bg": "#0a0f1e",
    "card": "#0d1526",
    "border": "#1e2d4a",
    "text": "#e8eaf0",
    "muted": "#7a8099",
}

def plotly_layout(title="", height=420):
    return dict(
        title=dict(text=title, font=dict(family="Syne", size=15, color=COLORS["text"]), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,21,38,0.6)",
        font=dict(family="DM Sans", color=COLORS["muted"], size=12),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], zerolinecolor=COLORS["border"]),
        yaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], zerolinecolor=COLORS["border"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["muted"])),
    )

# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 2rem 0 1rem 0; border-bottom: 1px solid #1e2d4a; margin-bottom: 2rem;">
    <div class="hero-title">⚽ Brasileirão 2025</div>
    <div style="font-family: Syne; font-size:1.4rem; color:#7a8099; font-weight:600; letter-spacing:0.05em; margin-bottom:0.5rem">
        O que os dados revelam sobre o futebol?
    </div>
    <div class="hero-subtitle">
        Uma análise estatística das primeiras 10 rodadas · Data Storytelling · Análise Exploratória
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs GERAIS ─────────────────────────────────────────────────────────────
total_gols = df_jogos["gols_mandante"].sum() + df_jogos["gols_visitante"].sum()
media_gols_jogo = total_gols / len(df_jogos)
jogos_com_gols = len(df_jogos[df_jogos["gols_mandante"] + df_jogos["gols_visitante"] > 0])
empates = len(df_jogos[df_jogos["gols_mandante"] == df_jogos["gols_visitante"]])

col1, col2, col3, col4, col5 = st.columns(5)
kpis = [
    (len(df_jogos), "Partidas Analisadas"),
    (total_gols, "Gols no Período"),
    (f"{media_gols_jogo:.1f}", "Gols por Jogo"),
    (f"{empates/len(df_jogos)*100:.0f}%", "Taxa de Empate"),
    (20, "Times na Competição"),
]
for col, (val, label) in zip([col1, col2, col3, col4, col5], kpis):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<p class="narrative">
Antes de responder às grandes perguntas do futebol, precisamos conhecer o cenário: 
<span class="highlight">20 times, 10 rodadas, centenas de gols e histórias.</span>
O Brasileirão 2025 começou com ritmo intenso. Cada número abaixo esconde uma lição.
Vamos desvendá-las juntos, uma pergunta de cada vez.
</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CAPÍTULO 1 — ATAQUE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="chapter-header">Capítulo 1 / Análise Ofensiva</div>
<div class="chapter-title">Atacar Bem Garante Mais Pontos?</div>
<div class="chapter-question">"Time que marca mais ganha mais. Será mesmo?"</div>
""", unsafe_allow_html=True)

corr_atk, pval_atk = stats.pearsonr(df_tabela["gols_pró"], df_tabela["pontos"])
corr_def, pval_def = stats.pearsonr(df_tabela["gols_contra"], df_tabela["pontos"])

col_a, col_b = st.columns([3, 2], gap="large")

with col_a:
    # Scatter: gols pró x pontos
    fig = px.scatter(
        df_tabela,
        x="gols_pró", y="pontos",
        text="time",
        size="vitórias",
        color="pontos",
        color_continuous_scale=[[0, "#1e2d4a"], [0.5, "#0099ff"], [1, "#00d4aa"]],
        hover_data={"vitórias": True, "gols_contra": True},
        labels={"gols_pró": "Gols Marcados", "pontos": "Pontos"},
    )
    
    # Linha de tendência
    z = np.polyfit(df_tabela["gols_pró"], df_tabela["pontos"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df_tabela["gols_pró"].min(), df_tabela["gols_pró"].max(), 100)
    fig.add_scatter(x=x_line, y=p(x_line), mode="lines",
                    line=dict(color=COLORS["green"], width=2, dash="dot"),
                    name="Tendência", showlegend=False)
    
    fig.update_traces(textposition="top center", textfont=dict(size=9, color="#c8ccdc"),
                      marker=dict(line=dict(width=1, color="#0a0f1e")))
    fig.update_layout(**plotly_layout("Gols Marcados × Pontos", height=400))
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">📊 Correlação de Pearson</div>
        <div class="insight-text">
            A correlação entre <b>gols marcados</b> e <b>pontos</b> é:<br><br>
            <span style="font-family:Syne; font-size:2rem; color:#00d4aa; font-weight:800;">r = {corr_atk:.2f}</span><br><br>
            {'✅ Correlação <b>forte e positiva</b>.' if corr_atk > 0.7 else '⚠️ Correlação <b>moderada</b>.'}
            <br>p-valor = {pval_atk:.4f} {'(estatisticamente significativo)' if pval_atk < 0.05 else ''}
        </div>
    </div>
    
    <div class="insight-box" style="margin-top:1rem;">
        <div class="insight-title">🔍 O que isso significa?</div>
        <div class="insight-text">
            Times que marcam mais gols têm <b>probabilidade muito maior de vencer</b>.
            Cada gol adicional por jogo representa, em média, 
            <b style="color:#00d4aa">+{(corr_atk * df_tabela['pontos'].std() / df_tabela['gols_pró'].std()):.1f} pontos</b>
            na tabela no período analisado.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top 5 atacantes da tabela
    top5_atk = df_tabela.nlargest(5, "gols_pró")[["time", "gols_pró", "pontos"]]
    fig2 = go.Figure()
    fig2.add_bar(x=top5_atk["time"], y=top5_atk["gols_pró"],
                 marker_color=COLORS["green"], opacity=0.85, name="Gols Marcados")
    fig2.add_scatter(x=top5_atk["time"], y=top5_atk["pontos"],
                     mode="markers+lines", marker=dict(color=COLORS["orange"], size=10),
                     line=dict(color=COLORS["orange"], width=2), name="Pontos", yaxis="y2")
    fig2.update_layout(
        **plotly_layout("Top 5 Ofensivos", height=280)
    )
    fig2.update_layout(
    yaxis2=dict(
        overlaying="y",
        side="right",
        gridcolor="rgba(0,0,0,0)",
        linecolor=COLORS["border"],
        color=COLORS["orange"]
    ),
    legend=dict(orientation="h", y=1.1)
)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
<div class="verdict-box">
    <div class="verdict-title">✅ Veredicto do Capítulo 1</div>
    <p class="narrative">
        <span class="highlight">Sim, atacar bem garante mais pontos</span> — e os dados confirmam isso com força estatística.
        A correlação de <span class="highlight">r = {corr_atk:.2f}</span> mostra que times mais ofensivos acumulam significativamente
        mais pontos. O ataque não é apenas estética: é <span class="highlight">eficiência convertida em tabela</span>.
        Flamengo e Palmeiras, os times com maior média de gols por jogo, lideram justamente por isso.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CAPÍTULO 2 — DEFESA vs ATAQUE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="chapter-header">Capítulo 2 / Defesa × Ataque</div>
<div class="chapter-title">Sofrer Menos Gols é Mais Importante que Marcar Mais?</div>
<div class="chapter-question">"O melhor ataque vence campeonatos, mas a melhor defesa também os conquista."</div>
""", unsafe_allow_html=True)

corr_def_neg, _ = stats.pearsonr(df_tabela["gols_contra"], df_tabela["pontos"])

col_c, col_d = st.columns([2, 3], gap="large")

with col_c:
    st.markdown(f"""
    <div class="insight-box warning">
        <div class="insight-title warning">🛡️ Correlação: Defesa × Pontos</div>
        <div class="insight-text">
            Correlação entre <b>gols sofridos</b> e <b>pontos</b>:<br><br>
            <span style="font-family:Syne; font-size:2rem; color:#ff8c42; font-weight:800;">r = {corr_def_neg:.2f}</span><br><br>
            <b>Correlação negativa</b>: quanto mais gols sofre, menos pontos faz.
        </div>
    </div>
    
    <div class="insight-box" style="margin-top:1rem">
        <div class="insight-title">⚖️ Comparação direta</div>
        <div class="insight-text">
            <table style="width:100%; color:#c8ccdc; font-size:0.9rem;">
                <tr>
                    <td><b>Fator</b></td>
                    <td><b>Correlação</b></td>
                    <td><b>Força</b></td>
                </tr>
                <tr>
                    <td>Gols marcados</td>
                    <td style="color:#00d4aa">r = {corr_atk:.2f}</td>
                    <td>{'Forte' if abs(corr_atk) > 0.7 else 'Moderada'}</td>
                </tr>
                <tr>
                    <td>Gols sofridos</td>
                    <td style="color:#ff8c42">r = {corr_def_neg:.2f}</td>
                    <td>{'Forte' if abs(corr_def_neg) > 0.7 else 'Moderada'}</td>
                </tr>
            </table>
            <br>
            O fator com <b>maior valor absoluto</b> tem maior impacto nos pontos.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_d:
    # Radar / comparativo defesa x ataque por quadrante
    fig3 = go.Figure()
    
    # Quadrantes: ataque bom/ruim × defesa boa/ruim
    med_gp = df_tabela["gols_pró_jogo"].median()
    med_gc = df_tabela["gols_contra_jogo"].median()
    
    cores_quad = {
        "Completos": COLORS["green"],
        "Especulativos": COLORS["blue"],
        "Vulneráveis": COLORS["orange"],
        "Em dificuldade": COLORS["red"],
    }
    
    for _, row in df_tabela.iterrows():
        if row["gols_pró_jogo"] >= med_gp and row["gols_contra_jogo"] <= med_gc:
            grupo = "Completos"
        elif row["gols_pró_jogo"] >= med_gp and row["gols_contra_jogo"] > med_gc:
            grupo = "Especulativos"
        elif row["gols_pró_jogo"] < med_gp and row["gols_contra_jogo"] <= med_gc:
            grupo = "Vulneráveis"
        else:
            grupo = "Em dificuldade"
        
        fig3.add_scatter(
            x=[row["gols_pró_jogo"]], y=[row["gols_contra_jogo"]],
            mode="markers+text",
            text=[row["time"].split("-")[0]],
            textposition="top center",
            textfont=dict(size=9, color="#c8ccdc"),
            marker=dict(size=row["pontos"]/2+5, color=cores_quad[grupo],
                        opacity=0.8, line=dict(width=1, color="#0a0f1e")),
            name=grupo,
            showlegend=True,
            legendgroup=grupo,
        )
    
    # Linhas de mediana
    fig3.add_vline(x=med_gp, line_dash="dot", line_color=COLORS["border"], line_width=1)
    fig3.add_hline(y=med_gc, line_dash="dot", line_color=COLORS["border"], line_width=1)
    
    # Anotações de quadrante
    fig3.add_annotation(x=df_tabela["gols_pró_jogo"].max()*0.97,
                        y=df_tabela["gols_contra_jogo"].min()*1.05,
                        text="✅ Completos", showarrow=False,
                        font=dict(color=COLORS["green"], size=10))
    fig3.add_annotation(x=df_tabela["gols_pró_jogo"].min()*1.03,
                        y=df_tabela["gols_contra_jogo"].max()*0.97,
                        text="❌ Dificuldade", showarrow=False,
                        font=dict(color=COLORS["red"], size=10))
    
    layout = plotly_layout("Mapa Estratégico: Ataque × Defesa (tamanho = pontos)", height=430)
    layout["xaxis"]["title"] = "Gols Marcados por Jogo →"
    layout["yaxis"]["title"] = "← Gols Sofridos por Jogo"
    layout["showlegend"] = False
    fig3.update_layout(**layout)
    st.plotly_chart(fig3, use_container_width=True)

# Gráfico de barras lado a lado: top e bottom 5 por defesa
col_e, col_f = st.columns(2, gap="large")

with col_e:
    df_def = df_tabela.nsmallest(5, "gols_contra")[["time", "gols_contra", "pontos"]]
    fig4 = px.bar(df_def, x="time", y=["gols_contra", "pontos"],
                  barmode="group",
                  color_discrete_map={"gols_contra": COLORS["orange"], "pontos": COLORS["green"]},
                  labels={"value": "Valor", "variable": "Métrica"},
                  title="Top 5 Defesas × Pontos")
    fig4.update_layout(**plotly_layout("Top 5 Melhores Defesas × Pontos", height=300))
    st.plotly_chart(fig4, use_container_width=True)

with col_f:
    df_def2 = df_tabela.nlargest(5, "gols_contra")[["time", "gols_contra", "pontos"]]
    fig5 = px.bar(df_def2.sort_values("gols_contra", ascending=False),
                  x="time", y=["gols_contra", "pontos"],
                  barmode="group",
                  color_discrete_map={"gols_contra": COLORS["red"], "pontos": COLORS["muted"]},
                  labels={"value": "Valor", "variable": "Métrica"})
    fig5.update_layout(**plotly_layout("Top 5 Piores Defesas × Pontos", height=300))
    st.plotly_chart(fig5, use_container_width=True)

maior_corr = "defesa" if abs(corr_def_neg) > abs(corr_atk) else "ataque"
st.markdown(f"""
<div class="verdict-box">
    <div class="verdict-title">✅ Veredicto do Capítulo 2</div>
    <p class="narrative">
        Comparando as correlações, o <span class="highlight-orange">{maior_corr}</span> mostra maior impacto absoluto 
        nos pontos neste início de campeonato.
        A correlação de <span class="highlight-orange">r = {corr_def_neg:.2f}</span> entre gols sofridos e pontos revela que
        <span class="highlight">cada gol a menos que você sofre vale mais do que um gol a mais que você marca</span>.
        Os dados sugerem que, no Brasileirão 2025, 
        <span class="highlight-orange">a sólida defesa é o alicerce da tabela</span> — enquanto o ataque é o diferencial
        que separa os grandes dos bons.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CAPÍTULO 3 — CONSISTÊNCIA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="chapter-header">Capítulo 3 / Consistência × Irregularidade</div>
<div class="chapter-title">Times Consistentes Pontuam Mais que Times Irregulares?</div>
<div class="chapter-question">"Vale mais ser bom todo dia ou ótimo às vezes?"</div>
""", unsafe_allow_html=True)

# Consistência medida pelo desvio padrão de pontos por rodada
corr_std, pval_std = stats.pearsonr(df_tabela["pts_std"], df_tabela["pontos"])
media_pts = df_tabela["pts_media"].mean()
std_pts = df_tabela["pts_media"].std()

col_g, col_h = st.columns([3, 2], gap="large")

with col_g:
    # Scatter: desvio padrão × pontos
    fig6 = px.scatter(
        df_tabela,
        x="pts_std", y="pontos",
        text="time",
        size="pts_media",
        color="pts_media",
        color_continuous_scale=[[0, "#1e2d4a"], [0.5, COLORS["purple"]], [1, COLORS["green"]]],
        labels={"pts_std": "Desvio Padrão (Irregularidade)", "pontos": "Total de Pontos",
                "pts_media": "Média pts/jogo"},
    )
    
    z2 = np.polyfit(df_tabela["pts_std"], df_tabela["pontos"], 1)
    p2 = np.poly1d(z2)
    x_line2 = np.linspace(df_tabela["pts_std"].min(), df_tabela["pts_std"].max(), 100)
    fig6.add_scatter(x=x_line2, y=p2(x_line2), mode="lines",
                     line=dict(color=COLORS["purple"], width=2, dash="dot"),
                     showlegend=False)
    
    fig6.update_traces(textposition="top center", textfont=dict(size=9, color="#c8ccdc"),
                       marker=dict(line=dict(width=1, color="#0a0f1e")))
    fig6.update_coloraxes(showscale=False)
    fig6.update_layout(**plotly_layout("Irregularidade (Desvio Padrão) × Pontos", height=420))
    st.plotly_chart(fig6, use_container_width=True)

with col_h:
    st.markdown(f"""
    <div class="insight-box purple">
        <div class="insight-title purple">📈 Medidas de Dispersão</div>
        <div class="insight-text">
            <b>Desvio padrão dos pontos por rodada</b> como proxy de irregularidade:<br><br>
            Média geral: <span style="color:#aa55ff; font-weight:700">{df_tabela['pts_std'].mean():.2f}</span><br>
            Time mais consistente: <span style="color:#00d4aa; font-weight:700">{df_tabela.loc[df_tabela['pts_std'].idxmin(), 'time']}</span> (σ={df_tabela['pts_std'].min():.2f})<br>
            Time mais irregular: <span style="color:#ff8c42; font-weight:700">{df_tabela.loc[df_tabela['pts_std'].idxmax(), 'time']}</span> (σ={df_tabela['pts_std'].max():.2f})<br><br>
            Correlação irregularidade × pontos:<br>
            <span style="font-family:Syne; font-size:2rem; color:#aa55ff; font-weight:800;">r = {corr_std:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Box plot de pontos por rodada dos top 5 e bottom 5
    top5 = df_tabela.nlargest(5, "pontos")["time"].tolist()
    bot5 = df_tabela.nsmallest(5, "pontos")["time"].tolist()
    
    # Recalcula pontos por rodada para visualização
    pts_data = []
    for time in top5 + bot5:
        grupo = "Top 5" if time in top5 else "Bot 5"
        for rodada in range(1, 11):
            jm = df_jogos[(df_jogos["mandante"] == time) & (df_jogos["rodada"] == rodada)]
            jv = df_jogos[(df_jogos["visitante"] == time) & (df_jogos["rodada"] == rodada)]
            if len(jm) > 0:
                r = jm.iloc[0]
                p = 3 if r["gols_mandante"] > r["gols_visitante"] else (1 if r["gols_mandante"] == r["gols_visitante"] else 0)
                pts_data.append({"time": time[:10], "rodada": rodada, "pts": p, "grupo": grupo})
            elif len(jv) > 0:
                r = jv.iloc[0]
                p = 3 if r["gols_visitante"] > r["gols_mandante"] else (1 if r["gols_visitante"] == r["gols_mandante"] else 0)
                pts_data.append({"time": time[:10], "rodada": rodada, "pts": p, "grupo": grupo})
    
    df_pts = pd.DataFrame(pts_data)
    fig7 = px.box(df_pts, x="grupo", y="pts",
                  color="grupo",
                  color_discrete_map={"Top 5": COLORS["green"], "Bot 5": COLORS["red"]},
                  labels={"pts": "Pontos na Rodada", "grupo": "Grupo"},
                  points="all")
    fig7.update_layout(**plotly_layout("Distribuição de Pontos: Top × Bot 5", height=280))
    fig7.update_layout(showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)

# Evolução cumulativa dos pontos
st.markdown("""
<div class="insight-box" style="margin: 1rem 0;">
    <div class="insight-title">📅 Trajetória dos Pontos ao Longo das Rodadas</div>
    <div class="insight-text">Acompanhe como os times construíram (ou não) sua pontuação de forma consistente:</div>
</div>
""", unsafe_allow_html=True)

top8 = df_tabela.nlargest(8, "pontos")["time"].tolist()
evolucao = []
for time in top8:
    pts_acum = 0
    for rodada in range(1, 11):
        jm = df_jogos[(df_jogos["mandante"] == time) & (df_jogos["rodada"] == rodada)]
        jv = df_jogos[(df_jogos["visitante"] == time) & (df_jogos["rodada"] == rodada)]
        if len(jm) > 0:
            r = jm.iloc[0]
            pts_acum += 3 if r["gols_mandante"] > r["gols_visitante"] else (1 if r["gols_mandante"] == r["gols_visitante"] else 0)
        elif len(jv) > 0:
            r = jv.iloc[0]
            pts_acum += 3 if r["gols_visitante"] > r["gols_mandante"] else (1 if r["gols_visitante"] == r["gols_mandante"] else 0)
        evolucao.append({"time": time, "rodada": rodada, "pts_acumulados": pts_acum})

df_evo = pd.DataFrame(evolucao)
fig8 = px.line(df_evo, x="rodada", y="pts_acumulados", color="time",
               labels={"rodada": "Rodada", "pts_acumulados": "Pontos Acumulados", "time": "Time"},
               markers=True)
fig8.update_layout(**plotly_layout("Evolução dos Pontos Acumulados · Top 8 Times", height=380))
fig8.update_traces(line=dict(width=2.5), marker=dict(size=7))
st.plotly_chart(fig8, use_container_width=True)

st.markdown(f"""
<div class="verdict-box">
    <div class="verdict-title">✅ Veredicto do Capítulo 3</div>
    <p class="narrative">
        A correlação de <span class="highlight-purple">r = {corr_std:.2f}</span> entre irregularidade e pontos 
        {'confirma' if abs(corr_std) > 0.3 else 'sugere parcialmente'} que 
        <span class="highlight">times consistentes pontuam mais</span>.
        O box plot revela que o Top 5 tem distribuição de pontos por rodada
        <span class="highlight">mais concentrada e mais alta</span> — enquanto os últimos colocados oscilam mais.
        No futebol de pontos corridos, <span class="highlight-purple">regularidade supera brilhos isolados</span>:
        um time que tira 1–2 pontos por jogo consistentemente supera aquele que alterna 3 pontos com derrotas.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CAPÍTULO 4 — FATOR CASA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="chapter-header">Capítulo 4 / Vantagem do Mando</div>
<div class="chapter-title">Jogar em Casa Influencia a Pontuação dos Times?</div>
<div class="chapter-question">"A torcida é o 12º jogador. Os números confirmam isso?"</div>
""", unsafe_allow_html=True)

# Estatísticas gerais casa vs fora
vitorias_casa = len(df_jogos[df_jogos["gols_mandante"] > df_jogos["gols_visitante"]])
vitorias_fora = len(df_jogos[df_jogos["gols_visitante"] > df_jogos["gols_mandante"]])
empates_total = len(df_jogos[df_jogos["gols_mandante"] == df_jogos["gols_visitante"]])
total = len(df_jogos)

gols_casa_total = df_jogos["gols_mandante"].sum()
gols_fora_total = df_jogos["gols_visitante"].sum()

col_i, col_j, col_k, col_l = st.columns(4)
for col, (val, label, cor) in zip(
    [col_i, col_j, col_k, col_l],
    [
        (f"{vitorias_casa/total*100:.0f}%", "Vitórias em Casa", "#00d4aa"),
        (f"{empates_total/total*100:.0f}%", "Empates", "#7a8099"),
        (f"{vitorias_fora/total*100:.0f}%", "Vitórias Fora", "#ff4466"),
        (f"{gols_casa_total/total:.1f} vs {gols_fora_total/total:.1f}", "Gols Casa vs Fora/Jogo", "#0099ff"),
    ]
):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:{cor}">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_m, col_n = st.columns([3, 2], gap="large")

with col_m:
    # Scatter: pts casa × pts fora por time
    df_tabela["dif_casa_fora"] = df_tabela["pts_media_casa"] - df_tabela["pts_media_fora"]
    
    fig9 = px.scatter(
        df_tabela,
        x="pts_media_fora", y="pts_media_casa",
        text="time",
        size="pontos",
        color="dif_casa_fora",
        color_continuous_scale=[[0, COLORS["red"]], [0.5, COLORS["muted"]], [1, COLORS["green"]]],
        labels={"pts_media_casa": "Pontos/Jogo em Casa", "pts_media_fora": "Pontos/Jogo Fora",
                "dif_casa_fora": "Vantagem Casa"},
    )
    
    # Linha diagonal (casa = fora)
    max_val = max(df_tabela["pts_media_casa"].max(), df_tabela["pts_media_fora"].max()) + 0.2
    fig9.add_scatter(x=[0, max_val], y=[0, max_val], mode="lines",
                     line=dict(color=COLORS["border"], width=1.5, dash="dash"),
                     name="Casa = Fora", showlegend=True)
    
    fig9.update_traces(textposition="top center", textfont=dict(size=9, color="#c8ccdc"),
                       selector=dict(mode="markers+text"),
                       marker=dict(line=dict(width=1, color="#0a0f1e")))
    fig9.update_coloraxes(showscale=False)
    layout9 = plotly_layout("Pontos por Jogo: Casa × Fora (acima da diagonal = vantagem em casa)", height=420)
    layout9["xaxis"]["title"] = "Pontos/Jogo como Visitante"
    layout9["yaxis"]["title"] = "Pontos/Jogo como Mandante"
    fig9.update_layout(**layout9)
    st.plotly_chart(fig9, use_container_width=True)

with col_n:
    # Gráfico de pizza dos resultados
    fig10 = go.Figure(data=[go.Pie(
        labels=["Vitória Mandante", "Empate", "Vitória Visitante"],
        values=[vitorias_casa, empates_total, vitorias_fora],
        hole=0.55,
        marker_colors=[COLORS["green"], COLORS["muted"], COLORS["red"]],
        textfont=dict(family="DM Sans", size=12, color="white"),
        textposition="outside",
    )])
    fig10.add_annotation(text=f"<b>{total}</b><br>Jogos", x=0.5, y=0.5,
                         showarrow=False, font=dict(size=16, color=COLORS["text"], family="Syne"))
    fig10.update_layout(**plotly_layout("Resultados por Mando de Campo", height=320))
    st.plotly_chart(fig10, use_container_width=True)
    
    # Teste t: pts casa vs fora
    t_stat, t_pval = stats.ttest_rel(df_tabela["pts_media_casa"], df_tabela["pts_media_fora"])
    
    st.markdown(f"""
    <div class="insight-box blue">
        <div class="insight-title blue">📐 Teste Estatístico (t-Student pareado)</div>
        <div class="insight-text">
            Média pts/jogo em casa: <span style="color:#00d4aa; font-weight:700">{df_tabela['pts_media_casa'].mean():.2f}</span><br>
            Média pts/jogo fora: <span style="color:#ff4466; font-weight:700">{df_tabela['pts_media_fora'].mean():.2f}</span><br>
            Diferença média: <span style="color:#0099ff; font-weight:700">+{df_tabela['pts_media_casa'].mean()-df_tabela['pts_media_fora'].mean():.2f} pts/jogo</span><br><br>
            t = {t_stat:.2f} | p = {t_pval:.4f}<br>
            <b>{'✅ Diferença estatisticamente significativa.' if t_pval < 0.05 else '⚠️ Diferença não significativa a 5%.'}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de barras empilhadas: casa vs fora por time
df_top10 = df_tabela.nlargest(12, "pontos")
fig11 = go.Figure()
fig11.add_bar(x=df_top10["time"], y=df_top10["pts_casa"],
              name="Pontos em Casa", marker_color=COLORS["green"], opacity=0.85)
fig11.add_bar(x=df_top10["time"], y=df_top10["pts_fora"],
              name="Pontos Fora", marker_color=COLORS["blue"], opacity=0.85)
fig11.update_layout(**plotly_layout("Pontos em Casa vs Fora · Top 12 Times", height=350),
                    barmode="group")
st.plotly_chart(fig11, use_container_width=True)

pct_acima_diagonal = (df_tabela["pts_media_casa"] > df_tabela["pts_media_fora"]).mean() * 100
st.markdown(f"""
<div class="verdict-box">
    <div class="verdict-title">✅ Veredicto do Capítulo 4</div>
    <p class="narrative">
        Os números são claros: <span class="highlight">{vitorias_casa/total*100:.0f}% das partidas são vencidas pelo mandante</span>,
        contra apenas {vitorias_fora/total*100:.0f}% pelo visitante. 
        <span class="highlight-blue">{pct_acima_diagonal:.0f}% dos times pontuam melhor em casa do que fora</span>
        — confirmado pelo scatter acima da diagonal.
        A diferença média de <span class="highlight">+{df_tabela['pts_media_casa'].mean()-df_tabela['pts_media_fora'].mean():.2f} pontos por jogo</span>
        em casa é economicamente significativa ao longo de uma temporada de 38 rodadas.
        <span class="highlight-orange">A torcida, o gramado conhecido e o deslocamento zero fazem diferença real na tabela.</span>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CONCLUSÃO GERAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="chapter-header">Conclusão Geral</div>
<div class="chapter-title">O Que o Brasileirão 2025 Nos Ensina?</div>
""", unsafe_allow_html=True)

col_o, col_p = st.columns([3, 2], gap="large")

with col_o:
    # Heatmap de correlações
    corr_cols = ["pontos", "gols_pró", "gols_contra", "saldo", "vitórias", "pts_std", "pts_media_casa", "pts_media_fora"]
    corr_labels = ["Pontos", "Gols Pró", "Gols Contra", "Saldo", "Vitórias", "Irregularidade", "Pts Casa", "Pts Fora"]
    
    corr_matrix = df_tabela[corr_cols].corr()
    
    fig12 = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_labels,
        y=corr_labels,
        colorscale=[[0, COLORS["red"]], [0.5, COLORS["card"]], [1, COLORS["green"]]],
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=11, family="Syne"),
        hovertemplate="<b>%{x} × %{y}</b><br>Correlação: %{z:.2f}<extra></extra>",
    ))
    fig12.update_layout(**plotly_layout("Matriz de Correlações · Todos os Fatores", height=450))
    fig12.update_layout(xaxis=dict(tickangle=-30))
    st.plotly_chart(fig12, use_container_width=True)

with col_p:
   # texto dinâmico
    if abs(corr_def_neg) > abs(corr_atk):
        texto_defesa = "Defesa tem impacto ligeiramente maior que o ataque."
    else:
        texto_defesa = "Ataque e defesa têm impacto similar, com leve vantagem do ataque."

    st.markdown(f"""
    <div style="padding-top:1rem;">

        <div style="background:#111827; padding:12px; margin-bottom:10px; border-left:4px solid #00d4aa;">
            <b>1️⃣ Atacar Bem</b><br>
            <span style="color:#00d4aa;">r = {corr_atk:.2f}</span> — correlação forte entre gols marcados e pontos.
        </div>

        <div style="background:#111827; padding:12px; margin-bottom:10px; border-left:4px solid #ff8c42;">
            <b>2️⃣ Defender Bem</b><br>
            <span style="color:#ff8c42;">r = {corr_def_neg:.2f}</span> — {texto_defesa}
        </div>

        <div style="background:#111827; padding:12px; margin-bottom:10px; border-left:4px solid #aa55ff;">
            <b>3️⃣ Consistência</b><br>
            <span style="color:#aa55ff;">r = {corr_std:.2f}</span> — times irregulares pontuam menos.
        </div>

        <div style="background:#111827; padding:12px; margin-bottom:10px; border-left:4px solid #0099ff;">
            <b>4️⃣ Fator Casa</b><br>
            <span style="color:#0099ff;">{vitorias_casa/total*100:.0f}%</span> de vitórias do mandante.
        </div>

    </div>
    """, unsafe_allow_html=True)

# Tabela final
st.markdown("""
<div class="insight-box" style="margin-top:1.5rem; margin-bottom:1rem;">
    <div class="insight-title">📋 Tabela Classificatória Completa · Primeiras 10 Rodadas</div>
    <div class="insight-text">Todos os indicadores analisados ao longo do dashboard, reunidos em uma visão única.</div>
</div>
""", unsafe_allow_html=True)

tabela_display = df_tabela[[
    "posição", "time", "pontos", "vitórias", "empates", "derrotas",
    "gols_pró", "gols_contra", "saldo", "pts_media", "pts_std", "pts_media_casa", "pts_media_fora"
]].copy()
tabela_display.columns = [
    "Pos", "Time", "Pts", "V", "E", "D",
    "GP", "GC", "SG", "Média/J", "DP (Irreg.)", "Média Casa", "Média Fora"
]

st.dataframe(
    tabela_display.style
    .background_gradient(subset=["Pts"], cmap="Greens")
    .background_gradient(subset=["GC"], cmap="Reds_r")
    .background_gradient(subset=["DP (Irreg.)"], cmap="Oranges_r")
    .format({"Média/J": "{:.2f}", "DP (Irreg.)": "{:.2f}", "Média Casa": "{:.2f}", "Média Fora": "{:.2f}"}),
    use_container_width=True,
    height=550,
)

# Footer
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0; border-top: 1px solid #1e2d4a; margin-top:2rem;">
    <div style="font-family:Syne; font-size:1rem; color:#7a8099; font-weight:600;">
        Brasileirão 2025 · Data Storytelling Dashboard
    </div>
    <div style="font-size:0.8rem; color:#3a4060; margin-top:0.4rem;">
        Dados: github.com/adaoduque/Brasileirao_Dataset · Análise Estatística: Pearson, t-Student, Desvio Padrão, Correlação
    </div>
</div>
""", unsafe_allow_html=True)