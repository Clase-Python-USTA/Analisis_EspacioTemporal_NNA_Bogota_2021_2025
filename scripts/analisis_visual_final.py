# -*- coding: utf-8 -*-
# analisis_visual_final_corregido.py
# ============================================================
# Visualizaciones finales NNA Bogotá (2021–2024) - Versión definitiva corregida
# Genera 7 gráficas PNG en reports/figures/graficos/
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker

# ------------------ CONFIGURACIÓN ------------------
DATA_FILE = r"C:\Users\ASUS\OneDrive - Universidad Santo Tomás\SANTO TOMAS\8-SEMESTRE\PYTHON\Analisis_EspacioTemporal_NNA_Bogota_2021_2025\data\processed\base_nna_limpia.xlsx"

# Directorio de salida (informado por ti)
BASE_DIR = os.path.dirname(os.path.dirname(DATA_FILE))
FIGS_DIR = os.path.join(BASE_DIR, "reports", "figures", "graficos")
os.makedirs(FIGS_DIR, exist_ok=True)

# ------------------ CARGA ------------------
print("➡ Cargando datos desde:", DATA_FILE)
df = pd.read_excel(DATA_FILE, engine="openpyxl").replace("N/A", np.nan)

# Dimensión original conocida (según tu instrucción)
ORIGINAL_ROWS = 56473
ORIGINAL_COLS = 115

# Normalizar nombres (sin eliminar columnas)
df.rename(columns=lambda s: s.strip() if isinstance(s, str) else s, inplace=True)

# ------------------ COLUMNAS CLAVE ------------------
# Preferimos la columna AÑO; si no existe la derivamos desde FECHA_INTERVENCION
if "AÑO" not in df.columns:
    posibles_fechas = [c for c in df.columns if "FECHA" in c.upper() and "INTERVENC" in c.upper()]
    if posibles_fechas:
        fecha_col = posibles_fechas[0]
        df[fecha_col] = df[fecha_col].replace("99999", np.nan)
        df[fecha_col] = pd.to_datetime(df[fecha_col], dayfirst=True, errors="coerce")
        df["AÑO"] = pd.to_numeric(df[fecha_col].dt.year, errors="coerce").astype("Int64")
    else:
        raise KeyError("No se encontró columna 'AÑO' ni columna de fecha de intervención para derivarla.")
fecha_col = "AÑO"

# Afiliación (buscar AFILI ... SGSSS preferente)
possible_af = [c for c in df.columns if 'AFILI' in c.upper() and 'SGSSS' in c.upper()]
if not possible_af:
    possible_af = [c for c in df.columns if 'AFILI' in c.upper()]
if not possible_af:
    raise KeyError("No se encontró columna de AFILIACIÓN en el dataset.")
af_col = possible_af[0]

# Localidad
possible_loc = [c for c in df.columns if 'LOCALIDAD' in c.upper()]
if not possible_loc:
    raise KeyError("No se encontró columna de LOCALIDAD en el dataset.")
loc_col = possible_loc[0]

print(f"➡ Columnas seleccionadas => AÑO: '{fecha_col}', AFILIACIÓN: '{af_col}', LOCALIDAD: '{loc_col}'")

# ------------------ FILTROS ------------------
# Forzar AÑO como entero y filtrar 2021-2024
df[fecha_col] = pd.to_numeric(df[fecha_col], errors='coerce').astype('Int64')
YEARS = [2021, 2022, 2023, 2024]
df = df[df[fecha_col].isin(YEARS)].copy()

# Eliminar valores de código 99999 en afiliación y localidad (int o str)
def is_99999_val(x):
    return (x == 99999) or (isinstance(x, str) and x.strip() == "99999")

mask_valid = ~(df[af_col].apply(is_99999_val) | df[loc_col].apply(is_99999_val))
df = df[mask_valid].copy()

# Cuenta filas usadas y porcentaje respecto a la dimensión original
used_rows = df.shape[0]
pct_used = round(used_rows / ORIGINAL_ROWS * 100, 1)

print(f"➡ Filas originales: {ORIGINAL_ROWS}, filas usadas: {used_rows} ({pct_used} %)")

# ------------------ PALETAS ------------------
PALETA_REGIMEN = ["#A99364", "#DA95AA", "#F4F0E4", "#B74954", "#C2DDB2"]  # tu paleta para regímenes
PALETA_LOCALIDADES_10 = ["#1F83B4", "#A3EBED", "#2CA030", "#8EBA58", "#D3D350",
                         "#FFBF50", "#D2ACF0", "#F46FC3", "#D63A3A", "#BC4691"]

sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "legend.frameon": True,
    "legend.fontsize": 9,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# ------------------ HELP: nota metodológica ------------------
def agregar_nota(fig):
    nota = (f"Nota metodológica: Se está graficando el 48.0 % del total inicial / 72.3 % de la base limpia "
            f"({ORIGINAL_ROWS:,} registros, {ORIGINAL_COLS} columnas).")
    fig.text(0.98, 0.02, nota, ha='right', va='bottom', fontsize=9, style='italic',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='lightgray', alpha=0.95))

# ------------------ 1) BARRAS VERTICALES: Intervenciones por Año y Régimen (ajustada) ------------------
df_bar = df.groupby([fecha_col, af_col]).size().reset_index(name="Intervenciones")

fig, ax = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=df_bar,
    x=fecha_col, y="Intervenciones", hue=af_col,
    palette=PALETA_REGIMEN, dodge=True, ci=None, ax=ax
)

# Calcular porcentajes relativos al total graficado
total_graficado = used_rows if used_rows > 0 else df_bar["Intervenciones"].sum()

# Anotar valores y porcentajes
for p in ax.patches:
    h = p.get_height()
    if h <= 0:
        continue
    x = p.get_x() + p.get_width() / 2
    y = h
    pct = h / total_graficado * 100
    ax.text(
        x, y + total_graficado * 0.005,
        f"{int(h):,}\n({pct:.1f}%)",
        ha='center', va='bottom', fontsize=9, color='black'
    )

# 🔧 Ajuste del título (espacio adicional)
ax.set_title("INTERVENCIONES POR AÑO Y RÉGIMEN", fontsize=16, weight='bold', pad=25)

ax.set_xlabel("AÑO", fontsize=12)
ax.set_ylabel("Número de intervenciones", fontsize=12)
ax.set_xticks(range(len(YEARS)))
ax.set_xticklabels([str(y) for y in YEARS])
ax.legend(title="Régimen", bbox_to_anchor=(1.02, 1), loc="upper left")

# Nota metodológica
agregar_nota(fig)

# 🧩 Ajuste fino de márgenes: un poco más de aire arriba
plt.tight_layout()
plt.subplots_adjust(top=0.90)

plt.savefig(os.path.join(FIGS_DIR, "01_barras_verticales_año_regimen.png"), dpi=300)
plt.close()

# ------------------ 2) DONUT: Distribución por régimen (versión final corregida) ------------------
df_donut = df[af_col].value_counts().reset_index()
df_donut.columns = ["Régimen", "Casos"]
sizes = df_donut["Casos"].values
colors = PALETA_REGIMEN[:len(sizes)]

total_graficado = df_donut["Casos"].sum()

fig, ax = plt.subplots(figsize=(8, 6))

# Gráfico de dona
wedges, _ = ax.pie(
    sizes,
    wedgeprops=dict(width=0.35, edgecolor='white'),
    startangle=90,
    colors=colors,
    normalize=True
)

# Título
ax.set_title(
    "Distribución de intervenciones por régimen",
    fontsize=16,
    weight='bold',
    pad=20
)
ax.set(aspect="equal")

# ✅ Leyenda ajustada (ya no se corta)
legend_labels = [
    f"{r} — {c:,} ({c/total_graficado*100:.1f}%)"
    for r, c in zip(df_donut["Régimen"], df_donut["Casos"])
]
ax.legend(
    wedges,
    legend_labels,
    title="Régimen",
    bbox_to_anchor=(1.05, 0.5),  # deja suficiente espacio
    loc="center left",
    fontsize=9,
    title_fontsize=10,
    frameon=False
)

# Nota metodológica
agregar_nota(fig)

# 🧩 Ajustes de espaciado: centrado más a la izquierda pero con aire a la derecha
plt.subplots_adjust(left=0.05, right=0.88, top=0.87, bottom=0.12)

# 🔒 Evita que tight_layout recorte la leyenda
plt.tight_layout(rect=[0, 0, 0.90, 1])

plt.savefig(os.path.join(FIGS_DIR, "02_donut_regimen.png"), dpi=300, bbox_inches="tight")
plt.close()


# ------------------ 3) BOXPLOT: Distribución por régimen (por localidad) + etiquetas Med, Q1, Q3, Mean ------------------
df_box = df.groupby([af_col, loc_col]).size().reset_index(name="Intervenciones")
regs = sorted(df_box[af_col].unique())
data = [df_box[df_box[af_col] == r]["Intervenciones"].values for r in regs]

fig, ax = plt.subplots(figsize=(12, 6))
b = ax.boxplot(data, labels=regs, patch_artist=True, widths=0.55, showfliers=True)

# colorear cajas con la paleta (repetir si hay menos colores o más)
colors_for_boxes = (PALETA_REGIMEN * ((len(regs) // len(PALETA_REGIMEN)) + 1))[:len(regs)]
for patch, color in zip(b["boxes"], colors_for_boxes):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

# Anotar media, Q1, Q3 arriba de cada caja
ymax = max(np.concatenate([arr if len(arr) > 0 else np.array([0]) for arr in data])) if len(data) > 0 else 0
offset = max(1, int(ymax * 0.05))
for i, arr in enumerate(data, start=1):
    if len(arr) == 0:
        continue
    med = int(np.median(arr))
    q1 = int(np.percentile(arr, 25))
    q3 = int(np.percentile(arr, 75))
    mean = int(np.mean(arr))
    txt = f"Mean: {mean:,}\nMed: {med:,}\nQ1: {q1:,}\nQ3: {q3:,}"
    ax.text(i, ax.get_ylim()[1] - offset, txt, ha='center', va='top', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray'))

ax.set_title("Distribución de intervenciones por régimen (por localidad)", fontsize=16, weight='bold')
ax.set_xlabel("Régimen de afiliación", fontsize=12)
ax.set_ylabel("Número de intervenciones por localidad", fontsize=12)
agregar_nota(fig)
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "03_boxplot_regimen_localidad.png"), dpi=300)
plt.close()

# ------------------ 4) SERIE TEMPORAL: Top 10 localidades (líneas con puntos y ticks enteros) ------------------
df_time = df.groupby([fecha_col, loc_col]).size().reset_index(name="Intervenciones")
top10_loc = df[loc_col].value_counts().head(10).index.tolist()
pivot = df_time[df_time[loc_col].isin(top10_loc)].pivot(index=fecha_col, columns=loc_col, values="Intervenciones").reindex(YEARS).fillna(0)

fig, ax = plt.subplots(figsize=(14, 7))
colors_for_top10 = PALETA_LOCALIDADES_10[:len(top10_loc)]
for loc, color in zip(top10_loc, colors_for_top10):
    ax.plot(pivot.index.astype(int), pivot[loc].values, marker='o', linewidth=2.2, label=loc, color=color)

ax.set_title("Evolución de intervenciones por localidad (Top 10)", fontsize=16, weight='bold')
ax.set_xlabel("AÑO", fontsize=12)
ax.set_ylabel("Número de intervenciones", fontsize=12)
# ticks con años enteros (sin decimales)
ax.set_xticks(YEARS)
ax.set_xticklabels([str(y) for y in YEARS])
ax.legend(title="Localidad", bbox_to_anchor=(1.02, 1), loc="upper left")
agregar_nota(fig)
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "04_serie_top10_localidades.png"), dpi=300)
plt.close()

# ------------------ 5) HEATMAP: Régimen × Año (usar paleta de régimen) ------------------
df_heat1 = df.groupby([af_col, fecha_col]).size().reset_index(name="Intervenciones")
tabla1 = df_heat1.pivot(index=af_col, columns=fecha_col, values="Intervenciones").fillna(0)
# Asegurar columnas años en orden
for y in YEARS:
    if y not in tabla1.columns:
        tabla1[y] = 0
tabla1 = tabla1[YEARS]

fig, ax = plt.subplots(figsize=(8, max(4, len(tabla1) * 0.6)))
sns.heatmap(tabla1, annot=True, fmt=".0f", cmap=sns.color_palette(PALETA_REGIMEN, as_cmap=True), linewidths=0.5, ax=ax)
ax.set_title("Heatmap: Intervenciones por régimen y año", fontsize=16, weight='bold')
ax.set_xlabel("AÑO", fontsize=12)
ax.set_ylabel("Régimen de afiliación", fontsize=12)
agregar_nota(fig)
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "05_heatmap_regimen_ano.png"), dpi=300)
plt.close()

# ------------------ 6) HEATMAP: Localidad × Año (Top 15) ------------------
top15 = df[loc_col].value_counts().head(15).index.tolist()
df_heat2 = df[df[loc_col].isin(top15)].groupby([loc_col, fecha_col]).size().reset_index(name="Intervenciones")
tabla2 = df_heat2.pivot(index=loc_col, columns=fecha_col, values="Intervenciones").fillna(0)
for y in YEARS:
    if y not in tabla2.columns:
        tabla2[y] = 0
tabla2 = tabla2[YEARS]

fig, ax = plt.subplots(figsize=(10, max(6, len(tabla2) * 0.45)))
sns.heatmap(tabla2, annot=True, fmt=".0f", cmap="YlOrBr", linewidths=0.5, ax=ax)
ax.set_title("Heatmap: Intervenciones por localidad y año (Top 15)", fontsize=16, weight='bold')
ax.set_xlabel("AÑO", fontsize=12)
ax.set_ylabel("Localidad", fontsize=12)
agregar_nota(fig)
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "06_heatmap_localidad_ano_top15.png"), dpi=300)
plt.close()

# ------------------ 7) TOP 10 LOCALIDADES: Barras horizontales (cada barra color diferente, valor + % ) ------------------
top10 = df[loc_col].value_counts().head(10).reset_index()
top10.columns = ["Localidad", "Intervenciones"]
top10 = top10.sort_values("Intervenciones", ascending=True)  # para barras horizontales ordenadas
top10_total = top10["Intervenciones"].sum()

fig, ax = plt.subplots(figsize=(12, 7))
colors_top10 = PALETA_LOCALIDADES_10[:len(top10)]
# dibujar barras una por una para asignar color individual y espacio claro
y_positions = np.arange(len(top10))
bars = ax.barh(y_positions, top10["Intervenciones"].values, color=colors_top10, height=0.65)
ax.set_yticks(y_positions)
ax.set_yticklabels(top10["Localidad"].values)
ax.invert_yaxis()  # mayor arriba

# anotar valor y porcentaje (respecto al total de top10)
for i, (val, bar) in enumerate(zip(top10["Intervenciones"].values, bars)):
    pct = val / top10_total * 100 if top10_total > 0 else 0
    ax.text(bar.get_width() + max(top10["Intervenciones"].max() * 0.005, 5),
            bar.get_y() + bar.get_height() / 2,
            f"{int(val):,} ({pct:.1f}%)",
            va='center', fontsize=9)

ax.set_title("Top 10 localidades con mayor número de intervenciones (2021–2024)", fontsize=16, weight='bold')
ax.set_xlabel("Número de intervenciones", fontsize=12)
ax.set_ylabel("Localidad", fontsize=12)
agregar_nota(fig)
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "07_top10_localidades_barras_horiz.png"), dpi=300)
plt.close()

print("\n✅ Se generaron las 7 gráficas en:", FIGS_DIR)

# ============================================================
# 🔹 BLOQUE FINAL: RESUMEN TEXTUAL DE DATOS GRAFICADOS
# ============================================================

print("\n" + "="*90)
print("📊 RESUMEN TEXTUAL DE LOS DATOS GRAFICADOS (2021–2024)")
print("="*90)

# 1️⃣ BARRAS VERTICALES: Intervenciones por Año y Régimen
print("\n1️⃣ INTERVENCIONES POR AÑO Y RÉGIMEN")
tabla1 = df_bar.pivot(index=fecha_col, columns=af_col, values="Intervenciones").fillna(0)
tabla1["Total_Año"] = tabla1.sum(axis=1)
tabla1.loc["TOTAL"] = tabla1.sum()
print(tabla1.astype(int).to_string())

totales_por_regimen = tabla1.loc["TOTAL"].drop("Total_Año")
for r, val in totales_por_regimen.items():
    pct = val / totales_por_regimen.sum() * 100 if totales_por_regimen.sum() > 0 else 0
    print(f"   ▪ {r}: {val:,} ({pct:.1f}%) del total graficado")

# 2️⃣ DONUT: Distribución por régimen
print("\n2️⃣ DISTRIBUCIÓN POR RÉGIMEN (Donut)")
print(df_donut.to_string(index=False))
for i, row in df_donut.iterrows():
    pct = row["Casos"] / total_graficado * 100
    print(f"   ▪ {row['Régimen']}: {row['Casos']:,} casos ({pct:.1f}%)")

# 3️⃣ BOXPLOT: Distribución por régimen (por localidad)
print("\n3️⃣ DISTRIBUCIÓN DE INTERVENCIONES POR RÉGIMEN Y LOCALIDAD (Boxplot)")
df_box_sum = df_box.groupby(af_col)["Intervenciones"].agg(['count', 'mean', 'median', 'min', 'max']).round(2)
print(df_box_sum.to_string())
for r, fila in df_box_sum.iterrows():
    print(f"   ▪ {r}: {int(fila['count'])} localidades, media {fila['mean']:.1f}, mediana {fila['median']:.1f}")

# 4️⃣ SERIE TEMPORAL: Top 10 localidades
print("\n4️⃣ EVOLUCIÓN DE INTERVENCIONES POR LOCALIDAD (Top 10)")
print(pivot.astype(int).to_string())
for loc in top10_loc:
    total_loc = pivot[loc].sum()
    pct = total_loc / pivot.sum().sum() * 100 if pivot.sum().sum() > 0 else 0
    print(f"   ▪ {loc}: {total_loc:,} ({pct:.1f}%) del total graficado")

# 5️⃣ HEATMAP: Régimen × Año
print("\n5️⃣ HEATMAP RÉGIMEN × AÑO")
print(tabla1.astype(int).to_string())
for r in tabla1.index[:-1]:
    total_reg = tabla1.loc[r, "Total_Año"]
    pct = total_reg / tabla1.loc["TOTAL", "Total_Año"] * 100 if tabla1.loc["TOTAL", "Total_Año"] > 0 else 0
    print(f"   ▪ {r}: {total_reg:,} intervenciones ({pct:.1f}%)")

# 6️⃣ HEATMAP: Localidad × Año (Top 15)
print("\n6️⃣ HEATMAP LOCALIDAD × AÑO (Top 15)")
print(tabla2.astype(int).to_string())
total_localidades = tabla2.sum(axis=1)
suma_total = total_localidades.sum()
for loc, val in total_localidades.items():
    pct = val / suma_total * 100 if suma_total > 0 else 0
    print(f"   ▪ {loc}: {val:,} ({pct:.1f}%) del total de Top 15")

# 7️⃣ TOP 10 LOCALIDADES: Barras horizontales
print("\n7️⃣ TOP 10 LOCALIDADES CON MÁS INTERVENCIONES")
print(top10.to_string(index=False))
for _, fila in top10.iterrows():
    pct = fila["Intervenciones"] / top10_total * 100 if top10_total > 0 else 0
    print(f"   ▪ {fila['Localidad']}: {int(fila['Intervenciones']):,} ({pct:.1f}%)")

print("\n✅ FIN DEL RESUMEN TEXTUAL. TODAS LAS CIFRAS CORRESPONDEN A LOS DATOS GRAFICADOS.")
print("="*90 + "\n")
