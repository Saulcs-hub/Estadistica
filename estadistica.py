"""
Proyecto de Aula - Fase 2
Análisis del Comportamiento del Usuario y Consumo de Recursos en Dispositivos Móviles
Universidad Autónoma de Bucaramanga - Estadística

Ejecutar con:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Configuración general ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Dispositivos Móviles · UNAB",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta de colores UNAB (gris institucional + azul oscuro) ─────────────────
COLOR_PRIMARY   = "#1B3A6B"   # azul UNAB
COLOR_SECONDARY = "#4A90D9"   # azul claro
COLOR_ACCENT    = "#E8A020"   # dorado
COLOR_BG        = "#F4F6FA"
PALETTE_OS      = {"Android": "#34A853", "iOS": "#1B3A6B"}
PALETTE_CLASS   = ["#D0E8FF", "#90C4F0", "#4A90D9", "#1F5FA6", "#0D2D5E"]

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* fondo general */
  .stApp {{ background-color: {COLOR_BG}; }}

  /* sidebar */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, {COLOR_PRIMARY} 0%, #0D2245 100%);
  }}
  [data-testid="stSidebar"] * {{ color: white !important; }}
  [data-testid="stSidebar"] .stRadio label {{ color: white !important; }}

  /* métricas */
  [data-testid="metric-container"] {{
      background: white;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,.08);
      border-left: 4px solid {COLOR_PRIMARY};
  }}

  /* títulos de sección */
  .section-title {{
      color: {COLOR_PRIMARY};
      font-size: 1.5rem;
      font-weight: 700;
      border-bottom: 3px solid {COLOR_ACCENT};
      padding-bottom: 6px;
      margin-bottom: 18px;
  }}

  /* tarjeta de hallazgo */
  .insight-card {{
      background: white;
      border-radius: 12px;
      padding: 18px 22px;
      box-shadow: 0 2px 10px rgba(0,0,0,.07);
      border-left: 5px solid {COLOR_ACCENT};
      margin-bottom: 14px;
      font-size: .95rem;
      color: #333;
  }}

  /* badge */
  .badge {{
      display: inline-block;
      background: {COLOR_PRIMARY};
      color: white !important;
      border-radius: 20px;
      padding: 3px 12px;
      font-size: .78rem;
      font-weight: 600;
      margin-right: 6px;
  }}

  h1 {{ color: {COLOR_PRIMARY} !important; }}
  h2 {{ color: {COLOR_PRIMARY} !important; }}
  h3 {{ color: {COLOR_PRIMARY} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("user_behavior_dataset.csv")
    df["Grupo_Edad"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 59],
        labels=["18-25", "26-35", "36-45", "46-59"]
    )
    return df

df = load_data()

etiquetas_clase = {
    1: "Uso muy bajo",
    2: "Uso bajo",
    3: "Uso moderado",
    4: "Uso alto",
    5: "Uso muy alto",
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/UNAB_logo.svg/320px-UNAB_logo.svg.png",
             width=140)
    st.markdown("---")
    st.markdown("### 📱 Navegación")
    seccion = st.radio("", [
        "🏠 Inicio",
        "🔍 Exploración del Dataset",
        "🎯 Objetivo 1 · Clasificación",
        "🔋 Objetivo 2 · Batería",
        "📡 Objetivo 3 · Correlación",
        "📊 Matriz de Correlaciones",
    ])
    st.markdown("---")
    st.markdown("**Proyecto de Aula · Fase 2**")
    st.markdown("Estadística · UNAB · 2025")
    st.markdown("---")

    # filtros globales
    st.markdown("### ⚙️ Filtros")
    os_filter = st.multiselect("Sistema Operativo",
                               df["Operating System"].unique(),
                               default=list(df["Operating System"].unique()))
    gender_filter = st.multiselect("Género",
                                   df["Gender"].unique(),
                                   default=list(df["Gender"].unique()))

df_f = df[df["Operating System"].isin(os_filter) & df["Gender"].isin(gender_filter)]


# ═══════════════════════════════════════════════════════════════
# INICIO
# ═══════════════════════════════════════════════════════════════
if seccion == "🏠 Inicio":
    st.title("📱 Análisis del Comportamiento del Usuario")
    st.subheader("Consumo de Recursos en Dispositivos Móviles · UNAB")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Usuarios", f"{len(df_f):,}")
    col2.metric("📱 Dispositivos", df_f["Device Model"].nunique())
    col3.metric("🕐 Pantalla promedio", f"{df_f['Screen On Time (hours/day)'].mean():.1f} h/día")
    col4.metric("🔋 Batería promedio", f"{df_f['Battery Drain (mAh/day)'].mean():.0f} mAh/día")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Distribución por Sistema Operativo</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 4), facecolor="white")
        counts = df_f["Operating System"].value_counts()
        wedges, texts, autotexts = ax.pie(
            counts, labels=counts.index, autopct="%1.1f%%",
            colors=[PALETTE_OS.get(o, COLOR_SECONDARY) for o in counts.index],
            startangle=90, wedgeprops=dict(edgecolor="white", linewidth=2)
        )
        for at in autotexts:
            at.set_fontsize(12); at.set_color("white"); at.set_fontweight("bold")
        ax.set_title("Usuarios por SO", fontsize=13, color=COLOR_PRIMARY, fontweight="bold")
        st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section-title">Distribución por Clase de Comportamiento</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 4), facecolor="white")
        vc = df_f["User Behavior Class"].value_counts().sort_index()
        bars = ax.bar([etiquetas_clase[i] for i in vc.index], vc.values,
                      color=PALETTE_CLASS, edgecolor="white", linewidth=1.5)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(int(bar.get_height())), ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=COLOR_PRIMARY)
        ax.set_xlabel("Clase de Comportamiento", fontsize=10)
        ax.set_ylabel("Número de usuarios", fontsize=10)
        ax.set_title("Usuarios por clase", fontsize=13, color=COLOR_PRIMARY, fontweight="bold")
        ax.tick_params(axis="x", rotation=20)
        ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor("white")
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    st.markdown("---")
    st.markdown('<p class="section-title">Variables del Dataset</p>', unsafe_allow_html=True)
    info = pd.DataFrame({
        "Variable": df.columns[:-1],
        "Tipo": ["Cuantitativa discreta","Cualitativa nominal","Cualitativa nominal",
                 "Cuantitativa discreta","Cuantitativa continua","Cuantitativa discreta",
                 "Cuantitativa discreta","Cuantitativa discreta","Cuantitativa discreta",
                 "Cualitativa nominal","Cuantitativa discreta"],
        "Descripción": [
            "Identificador único del usuario",
            "Modelo del dispositivo",
            "Sistema operativo (Android/iOS)",
            "Minutos diarios usando apps",
            "Horas de pantalla encendida por día",
            "mAh consumidos por día",
            "Número de apps instaladas",
            "MB de datos móviles por día",
            "Edad del usuario",
            "Género del usuario",
            "Clase de intensidad de uso (1–5)",
        ]
    })
    st.dataframe(info, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# EXPLORACIÓN
# ═══════════════════════════════════════════════════════════════
elif seccion == "🔍 Exploración del Dataset":
    st.title("🔍 Exploración del Dataset")
    st.markdown("---")

    st.markdown('<p class="section-title">Estadísticas Descriptivas Globales</p>', unsafe_allow_html=True)
    cols_num = ["App Usage Time (min/day)", "Screen On Time (hours/day)",
                "Battery Drain (mAh/day)", "Number of Apps Installed",
                "Data Usage (MB/day)", "Age"]
    desc = df_f[cols_num].describe().T.round(2)
    desc.columns = ["n","Media","Desv. Est.","Mín","Q1","Mediana","Q3","Máx"]
    st.dataframe(desc.style.background_gradient(cmap="Blues", subset=["Media"]),
                 use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Distribuciones (Histogramas)</p>', unsafe_allow_html=True)

    col_sel = st.selectbox("Selecciona una variable:", cols_num)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), facecolor="white")

    # histograma
    axes[0].hist(df_f[col_sel].dropna(), bins=30, color=COLOR_SECONDARY,
                 edgecolor="white", linewidth=0.8)
    axes[0].axvline(df_f[col_sel].mean(), color=COLOR_ACCENT, linewidth=2,
                    linestyle="--", label=f"Media: {df_f[col_sel].mean():.1f}")
    axes[0].axvline(df_f[col_sel].median(), color=COLOR_PRIMARY, linewidth=2,
                    linestyle="-.", label=f"Mediana: {df_f[col_sel].median():.1f}")
    axes[0].set_title(f"Histograma · {col_sel}", color=COLOR_PRIMARY, fontweight="bold")
    axes[0].legend(fontsize=9)
    axes[0].set_facecolor(COLOR_BG)
    axes[0].spines[["top","right"]].set_visible(False)

    # boxplot por OS
    data_plot = [df_f[df_f["Operating System"]==os][col_sel].dropna()
                 for os in df_f["Operating System"].unique()]
    bp = axes[1].boxplot(data_plot, patch_artist=True, notch=False,
                         labels=df_f["Operating System"].unique())
    colors_bp = [PALETTE_OS.get(o, COLOR_SECONDARY) for o in df_f["Operating System"].unique()]
    for patch, color in zip(bp["boxes"], colors_bp):
        patch.set_facecolor(color); patch.set_alpha(0.7)
    axes[1].set_title(f"Boxplot por SO · {col_sel}", color=COLOR_PRIMARY, fontweight="bold")
    axes[1].set_facecolor(COLOR_BG)
    axes[1].spines[["top","right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")
    st.markdown('<p class="section-title">Vista previa de datos</p>', unsafe_allow_html=True)
    st.dataframe(df_f.head(20), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# OBJETIVO 1 — Clasificación
# ═══════════════════════════════════════════════════════════════
elif seccion == "🎯 Objetivo 1 · Clasificación":
    st.title("🎯 Objetivo 1 · Clasificación por Nivel de Uso")
    st.markdown("""
    <div class="insight-card">
    <span class="badge">Objetivo</span>
    Clasificar a los usuarios según su nivel de intensidad de uso (<b>User Behavior Class</b>)
    basándose en el tiempo de pantalla y uso de aplicaciones.
    </div>
    """, unsafe_allow_html=True)

    ubc = df_f.groupby("User Behavior Class").agg(
        n=("User ID","count"),
        pantalla_media=("Screen On Time (hours/day)","mean"),
        pantalla_std=("Screen On Time (hours/day)","std"),
        apps_media=("App Usage Time (min/day)","mean"),
        apps_std=("App Usage Time (min/day)","std"),
    ).round(2)

    # tabla resumen
    st.markdown('<p class="section-title">Tabla de Resultados por Clase</p>', unsafe_allow_html=True)
    tabla = ubc.copy()
    tabla.index = [f"Clase {i} · {etiquetas_clase[i]}" for i in tabla.index]
    tabla.columns = ["n","Pantalla media (h)","Pantalla std","Apps media (min)","Apps std"]
    st.dataframe(tabla.style.background_gradient(cmap="Blues", subset=["Pantalla media (h)","Apps media (min)"]),
                 use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Tiempo de Pantalla por Clase</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")
        clases = ubc.index
        ax.bar(clases, ubc["pantalla_media"], color=PALETTE_CLASS,
               edgecolor="white", linewidth=1.5, zorder=3)
        ax.errorbar(clases, ubc["pantalla_media"], yerr=ubc["pantalla_std"],
                    fmt="none", color="#333", capsize=5, linewidth=1.5, zorder=4)
        ax.set_xticks(clases)
        ax.set_xticklabels([f"Clase {i}\n{etiquetas_clase[i]}" for i in clases], fontsize=8)
        ax.set_ylabel("Horas/día", fontsize=10)
        ax.set_title("Pantalla encendida por clase", color=COLOR_PRIMARY, fontweight="bold")
        ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3, zorder=0)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section-title">Uso de Apps por Clase</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")
        ax.barh([etiquetas_clase[i] for i in clases], ubc["apps_media"],
                color=PALETTE_CLASS[::-1], edgecolor="white", linewidth=1.5)
        for i, (v, e) in enumerate(zip(ubc["apps_media"], ubc["apps_std"])):
            ax.text(v + 5, i, f"{v:.0f} min", va="center", fontsize=9,
                    color=COLOR_PRIMARY, fontweight="bold")
        ax.set_xlabel("Minutos/día", fontsize=10)
        ax.set_title("Uso de apps por clase", color=COLOR_PRIMARY, fontweight="bold")
        ax.set_facecolor(COLOR_BG); ax.grid(axis="x", alpha=0.3)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    # violín
    st.markdown('<p class="section-title">Distribución Detallada (Violin Plot)</p>', unsafe_allow_html=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor="white")
    for ax, col, label in zip(axes,
        ["Screen On Time (hours/day)", "App Usage Time (min/day)"],
        ["Tiempo de Pantalla (h/día)", "Uso de Apps (min/día)"]):
        data_v = [df_f[df_f["User Behavior Class"]==c][col].dropna() for c in sorted(df_f["User Behavior Class"].unique())]
        parts = ax.violinplot(data_v, positions=range(1,6), showmedians=True, showmeans=False)
        for i, pc in enumerate(parts["bodies"]):
            pc.set_facecolor(PALETTE_CLASS[i]); pc.set_alpha(0.8)
        parts["cmedians"].set_color(COLOR_ACCENT); parts["cmedians"].set_linewidth(2)
        ax.set_xticks(range(1,6))
        ax.set_xticklabels([f"C{i}\n{etiquetas_clase[i]}" for i in range(1,6)], fontsize=8)
        ax.set_ylabel(label, fontsize=10)
        ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3)
        ax.spines[["top","right"]].set_visible(False)
    fig.suptitle("Distribución por clase de comportamiento", color=COLOR_PRIMARY,
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("""
    <div class="insight-card">
    💡 <b>Hallazgo:</b> La progresión entre clases es muy clara y consistente.
    Los usuarios de Clase 5 usan el teléfono <b>~6.8× más</b> que los de Clase 1 en tiempo de pantalla
    y <b>~9× más</b> en uso de aplicaciones. La baja desviación estándar dentro de cada clase
    confirma que esta clasificación es muy precisa.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# OBJETIVO 2 — Batería
# ═══════════════════════════════════════════════════════════════
elif seccion == "🔋 Objetivo 2 · Batería":
    st.title("🔋 Objetivo 2 · Drenaje de Batería: Android vs iOS")
    st.markdown("""
    <div class="insight-card">
    <span class="badge">Objetivo</span>
    Comparar el drenaje de batería promedio entre Android e iOS para identificar
    cuál presenta mayor eficiencia bajo perfiles de uso similares.
    </div>
    """, unsafe_allow_html=True)

    bat = df_f.groupby("Operating System")["Battery Drain (mAh/day)"].agg(
        n="count", Media="mean", Mediana="median",
        Std="std", Min="min", Max="max"
    ).round(2)

    # métricas rápidas
    c1, c2, c3 = st.columns(3)
    android_mean = bat.loc["Android","Media"] if "Android" in bat.index else 0
    ios_mean     = bat.loc["iOS","Media"]     if "iOS"     in bat.index else 0
    c1.metric("🤖 Android media", f"{android_mean:.0f} mAh/día")
    c2.metric("🍎 iOS media",     f"{ios_mean:.0f} mAh/día")
    c3.metric("📏 Diferencia",    f"{abs(ios_mean - android_mean):.0f} mAh/día",
              delta=f"iOS {'consume más' if ios_mean > android_mean else 'consume menos'}",
              delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Tabla Comparativa</p>', unsafe_allow_html=True)
    st.dataframe(bat.style.background_gradient(cmap="Greens", subset=["Media","Mediana"]),
                 use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Comparación de Medias y Medianas</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")
        sistemas = bat.index.tolist()
        x = np.arange(len(sistemas))
        w = 0.35
        bars1 = ax.bar(x - w/2, bat["Media"],   width=w, label="Media",
                       color=[PALETTE_OS.get(s, COLOR_SECONDARY) for s in sistemas],
                       edgecolor="white", alpha=0.9)
        bars2 = ax.bar(x + w/2, bat["Mediana"], width=w, label="Mediana",
                       color=[PALETTE_OS.get(s, COLOR_SECONDARY) for s in sistemas],
                       edgecolor="white", alpha=0.5, hatch="//")
        for bar in list(bars1) + list(bars2):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f"{bar.get_height():.0f}", ha="center", fontsize=9,
                    fontweight="bold", color=COLOR_PRIMARY)
        ax.set_xticks(x); ax.set_xticklabels(sistemas, fontsize=11)
        ax.set_ylabel("mAh/día", fontsize=10)
        ax.set_title("Batería: Media vs Mediana", color=COLOR_PRIMARY, fontweight="bold")
        ax.legend(fontsize=9)
        ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section-title">Boxplot por Sistema Operativo</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")
        data_box = [df_f[df_f["Operating System"]==s]["Battery Drain (mAh/day)"].dropna()
                    for s in sistemas]
        bp = ax.boxplot(data_box, patch_artist=True, labels=sistemas, notch=False,
                        widths=0.5)
        for patch, s in zip(bp["boxes"], sistemas):
            patch.set_facecolor(PALETTE_OS.get(s, COLOR_SECONDARY)); patch.set_alpha(0.75)
        bp["medians"][0].set_color(COLOR_ACCENT) if len(bp["medians"]) > 0 else None
        ax.set_ylabel("mAh/día", fontsize=10)
        ax.set_title("Distribución del drenaje por SO", color=COLOR_PRIMARY, fontweight="bold")
        ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    # batería por clase y SO
    st.markdown('<p class="section-title">Drenaje de Batería por Clase y Sistema Operativo</p>', unsafe_allow_html=True)
    bat_clase = df_f.groupby(["Operating System","User Behavior Class"])["Battery Drain (mAh/day)"].mean().round(1).unstack()
    fig, ax = plt.subplots(figsize=(11, 4), facecolor="white")
    x = np.arange(5); w = 0.35
    for i, (so, color) in enumerate(PALETTE_OS.items()):
        if so in bat_clase.index:
            vals = [bat_clase.loc[so, c] if c in bat_clase.columns else 0 for c in range(1,6)]
            bars = ax.bar(x + i*w, vals, width=w, label=so, color=color,
                          edgecolor="white", alpha=0.85)
    ax.set_xticks(x + w/2)
    ax.set_xticklabels([f"Clase {i}\n{etiquetas_clase[i]}" for i in range(1,6)], fontsize=8)
    ax.set_ylabel("mAh/día", fontsize=10)
    ax.set_title("Batería promedio por clase y SO", color=COLOR_PRIMARY, fontweight="bold")
    ax.legend(fontsize=10); ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3)
    ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("""
    <div class="insight-card">
    💡 <b>Hallazgo:</b> iOS consume en promedio <b>81 mAh/día más</b> que Android (~5.4% más),
    pero la diferencia es pequeña comparada con la altísima variabilidad interna (±819 mAh).
    Al controlar por clase de comportamiento, los patrones son prácticamente idénticos entre SO,
    lo que sugiere que el <b>perfil de uso importa más que el sistema operativo</b>.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# OBJETIVO 3 — Correlación
# ═══════════════════════════════════════════════════════════════
elif seccion == "📡 Objetivo 3 · Correlación":
    st.title("📡 Objetivo 3 · Correlación: Edad vs Consumo de Datos")
    st.markdown("""
    <div class="insight-card">
    <span class="badge">Objetivo</span>
    Evaluar la correlación entre la edad de los usuarios y el volumen de datos móviles
    consumidos mensualmente.
    </div>
    """, unsafe_allow_html=True)

    r = df_f["Age"].corr(df_f["Data Usage (MB/day)"])

    c1, c2, c3 = st.columns(3)
    c1.metric("📐 Correlación de Pearson (r)", f"{r:.4f}")
    c2.metric("📊 R² (varianza explicada)",    f"{r**2*100:.2f}%")
    c3.metric("🔎 Interpretación", "Correlación nula")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Diagrama de Dispersión</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 5), facecolor="white")
        scatter_colors = [PALETTE_OS.get(o, COLOR_SECONDARY)
                          for o in df_f["Operating System"]]
        ax.scatter(df_f["Age"], df_f["Data Usage (MB/day)"],
                   c=scatter_colors, alpha=0.35, s=25, edgecolors="none")
        # línea de tendencia
        m, b = np.polyfit(df_f["Age"].dropna(), df_f["Data Usage (MB/day)"].dropna(), 1)
        x_line = np.linspace(df_f["Age"].min(), df_f["Age"].max(), 100)
        ax.plot(x_line, m*x_line + b, color=COLOR_ACCENT, linewidth=2.5,
                linestyle="--", label=f"Tendencia (r={r:.4f})")
        patches = [mpatches.Patch(color=c, label=s) for s, c in PALETTE_OS.items()
                   if s in df_f["Operating System"].values]
        ax.legend(handles=patches + ax.get_legend_handles_labels()[0][-1:], fontsize=9)
        ax.set_xlabel("Edad (años)", fontsize=11)
        ax.set_ylabel("Consumo de datos (MB/día)", fontsize=11)
        ax.set_title("Edad vs Consumo de Datos", color=COLOR_PRIMARY, fontweight="bold")
        ax.set_facecolor(COLOR_BG); ax.grid(alpha=0.25)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section-title">Consumo por Grupo de Edad</p>', unsafe_allow_html=True)
        edad_stats = df_f.groupby("Grupo_Edad", observed=True)["Data Usage (MB/day)"].agg(
            Media="mean", Mediana="median", Std="std", n="count"
        ).round(2)
        fig, ax = plt.subplots(figsize=(6, 5), facecolor="white")
        grupos = edad_stats.index.astype(str)
        bars = ax.bar(grupos, edad_stats["Media"],
                      color=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, "#2E8B57"],
                      edgecolor="white", linewidth=1.5, zorder=3)
        ax.errorbar(range(len(grupos)), edad_stats["Media"], yerr=edad_stats["Std"],
                    fmt="none", color="#555", capsize=6, linewidth=1.5, zorder=4)
        for bar, n in zip(bars, edad_stats["n"]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                    f"{bar.get_height():.0f}", ha="center", fontsize=10,
                    fontweight="bold", color=COLOR_PRIMARY)
        ax.set_xlabel("Grupo de Edad", fontsize=11)
        ax.set_ylabel("MB/día", fontsize=11)
        ax.set_title("Consumo de datos por grupo etario", color=COLOR_PRIMARY, fontweight="bold")
        ax.set_facecolor(COLOR_BG); ax.grid(axis="y", alpha=0.3, zorder=0)
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    st.markdown('<p class="section-title">Tabla por Grupo de Edad</p>', unsafe_allow_html=True)
    st.dataframe(edad_stats.style.background_gradient(cmap="Blues", subset=["Media"]),
                 use_container_width=True)

    st.markdown("""
    <div class="insight-card">
    💡 <b>Hallazgo:</b> El coeficiente de correlación de Pearson es <b>r = 0.0040</b>,
    prácticamente cero. La edad <b>no predice</b> el consumo de datos móviles. Los promedios
    por grupo de edad son muy similares (848–978 MB/día) y la alta desviación estándar dentro
    de cada grupo confirma que otros factores como la clase de comportamiento explican mejor
    el consumo de datos.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# MATRIZ DE CORRELACIONES
# ═══════════════════════════════════════════════════════════════
elif seccion == "📊 Matriz de Correlaciones":
    st.title("📊 Matriz de Correlaciones")
    st.markdown("Relación lineal entre todas las variables numéricas del dataset.")
    st.markdown("---")

    cols_num = ["App Usage Time (min/day)", "Screen On Time (hours/day)",
                "Battery Drain (mAh/day)", "Number of Apps Installed",
                "Data Usage (MB/day)", "Age"]
    corr = df_f[cols_num].corr().round(4)

    labels_cortos = ["Uso Apps","Pantalla","Batería","N° Apps","Datos","Edad"]

    fig, ax = plt.subplots(figsize=(9, 7), facecolor="white")
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
                vmin=-1, vmax=1, center=0,
                xticklabels=labels_cortos, yticklabels=labels_cortos,
                linewidths=0.5, linecolor="white",
                cbar_kws={"shrink": 0.8}, ax=ax,
                annot_kws={"size": 11, "weight": "bold"})
    ax.set_title("Matriz de Correlaciones de Pearson", color=COLOR_PRIMARY,
                 fontsize=14, fontweight="bold", pad=15)
    ax.tick_params(axis="both", labelsize=10)
    fig.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown("""
    <div class="insight-card">
    🔴 <b>Correlaciones muy fuertes (r > 0.93):</b><br>
    Uso de Apps ↔ Pantalla · Batería · N° Apps · Datos<br>
    Todas las variables de consumo están altamente relacionadas entre sí.
    </div>
    """, unsafe_allow_html=True)
    c2.markdown("""
    <div class="insight-card">
    ⚪ <b>Correlación nula con Edad (r ≈ 0):</b><br>
    La edad no tiene relación lineal con ninguna variable de consumo,
    confirmando el hallazgo del Objetivo 3.
    </div>
    """, unsafe_allow_html=True)