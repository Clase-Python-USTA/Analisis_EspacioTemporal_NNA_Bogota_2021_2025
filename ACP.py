# ============================================================
# ANÁLISIS DE COMPONENTES PRINCIPALES ESPACIO-TEMPORAL
# Proyecto: Intervenciones con NNA Bogotá (2021–2024)
# Versión mejorada con normalización robusta y metadata
# ============================================================

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import __version__ as sklearn_version
from datetime import datetime
import warnings
import json
import joblib

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'

print("="*70)
print("📊 ANÁLISIS DE COMPONENTES PRINCIPALES ESPACIO-TEMPORAL")
print("    Proyecto: Intervenciones NNA Bogotá (2021-2024)")
print("="*70)
print()

# ============================================================
# 1. CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = SCRIPT_DIR if os.path.exists(os.path.join(SCRIPT_DIR, "data")) else os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "base_nna_limpia.xlsx")

ACP_DIR = os.path.join(BASE_DIR, "reports", "figures", "ACP")
ACP_TABLES = os.path.join(BASE_DIR, "reports", "tables", "ACP")
ACP_LOG = os.path.join(BASE_DIR, "reports", "ACP_analisis.md")

for path in [ACP_DIR, ACP_TABLES]:
    os.makedirs(path, exist_ok=True)

# Parámetros del análisis
AÑOS_VALIDOS = [2021, 2022, 2023, 2024]
N_COMPONENTS = 2
TOP_N_LABELS = 8  # Para anotaciones en biplot

# Orden deseado de regímenes (si existen)
ORDEN_REGIMENES = ['SUBSIDIADO', 'CONTRIBUTIVO', 'NO_ASEGURADO', 'ESPECIAL', 'VINCULADO']

print(f"📂 Configuración:")
print(f"   • Base de datos: {os.path.basename(DATA_FILE)}")
print(f"   • Años válidos: {AÑOS_VALIDOS}")
print(f"   • Componentes: {N_COMPONENTS}")
print(f"   • Salida: {ACP_DIR}")
print()

# ============================================================
# 2. PALETAS DE COLORES PROFESIONALES
# ============================================================

COLORES_AÑOS = {
    2021: '#0D47A1',  # Azul oscuro
    2022: '#1976D2',  # Azul medio
    2023: '#42A5F5',  # Azul claro
    2024: '#90CAF9'   # Azul muy claro
}

COLORES_LOCALIDADES = [
    '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3',
    '#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#CDDC39',
    '#FFC107', '#FF9800', '#FF5722', '#795548', '#607D8B',
    '#F44336', '#E040FB', '#00E676', '#FFEA00', '#FF6D00'
]

COLORES_REGIMENES = {
    'SUBSIDIADO': '#E53935',
    'CONTRIBUTIVO': '#1E88E5', 
    'NO_ASEGURADO': '#FDD835',
    'ESPECIAL': '#43A047',
    'VINCULADO': '#AB47BC'
}

# ============================================================
# 2. PREPARACIÓN DE DATOS PARA EL ACP (FILTRANDO 99999)
# ============================================================

def preparar_datos_acp(df, col_loc, col_afil, col_año):
    """
    Prepara la base agregada por localidad, año y tipo de afiliación.
    Filtra categorías 99999 o vacías, y genera tabla pivote lista para ACP.
    """
    print("\n======================================================================")
    print("🔧 FASE 2: PREPARACIÓN DE DATOS ESPACIO-TEMPORALES")
    print("======================================================================\n")

    # 🔹 Copia para no alterar el original
    data = df.copy()

    print(f"• Registros iniciales: {len(data):,}")

    # ------------------------------------------------------------
    # 1️⃣ Limpieza básica: eliminar nulos y 99999 en variables clave
    # ------------------------------------------------------------
    data = data.dropna(subset=[col_loc, col_afil, col_año])

    # Convertir a string para evitar problemas con valores mixtos
    data[col_loc] = data[col_loc].astype(str).str.strip()
    data[col_afil] = data[col_afil].astype(str).str.strip()
    data[col_año] = data[col_año].astype(str).str.strip()

    # Filtrar categorías 99999 o equivalentes
    for col in [col_loc, col_afil, col_año]:
        mask_999 = data[col].isin(["99999", "99", "9999", "NA", "NaN", "nan", "N/A", ""])
        if mask_999.any():
            eliminadas = mask_999.sum()
            data = data[~mask_999]
            print(f"   ⚠️ Registros eliminados por '{col}' = 99999 o vacío: {eliminadas:,}")

    print(f"• Registros válidos: {len(data):,}")
    print(f"• Tasa de retención: {100 * len(data) / df.shape[0]:.2f}%\n")

    # ------------------------------------------------------------
    # 2️⃣ Normalizar etiquetas de texto
    # ------------------------------------------------------------
    print("🔄 Normalizando regímenes...")
    data[col_afil] = data[col_afil].str.upper().replace({
        'SUBSIDIADO ': 'SUBSIDIADO',
        'CONTRIBUTIVO ': 'CONTRIBUTIVO',
        'NO ASEGURADO': 'NO_ASEGURADO',
        'NINGUNO': 'NO_ASEGURADO',
        'SIN AFILIACIÓN': 'NO_ASEGURADO',
        'NO ASEGURADO ': 'NO_ASEGURADO',
        'ESPECIAL ': 'ESPECIAL',
        'VINCULADO ': 'VINCULADO',
        '': np.nan
    })

    print("🔄 Normalizando años...")
    data[col_año] = data[col_año].str.extract(r'(\d{4})').astype(float).astype(int)

    # ------------------------------------------------------------
    # 3️⃣ Generar tabla pivote (Localidad × Año × Régimen)
    # ------------------------------------------------------------
    tabla_pivot = (
        data
        .groupby([col_loc, col_año, col_afil])
        .size()
        .reset_index(name='conteo')
        .pivot_table(index=[col_loc, col_año],
                     columns=col_afil,
                     values='conteo',
                     fill_value=0)
        .reset_index()
    )

    print(f"✓ Tabla espacio-temporal creada:")
    print(f"   • Observaciones (Localidad×Año): {len(tabla_pivot):,}")
    print(f"   • Variables (Regímenes): {len(tabla_pivot.columns) - 2}")
    print(f"   • Regímenes detectados: {list(tabla_pivot.columns[2:])}\n")

    return tabla_pivot


# ============================================================
# 3. CARGA Y VALIDACIÓN DE DATOS
# ============================================================

def cargar_datos():
    """Carga y valida la base de datos limpia"""
    print("="*70)
    print("📥 FASE 1: CARGA DE DATOS")
    print("="*70)
    
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"❌ No se encontró: {DATA_FILE}")
    
    df = pd.read_excel(DATA_FILE, engine='openpyxl')
    print(f"\n✓ Base cargada exitosamente")
    print(f"   • Filas totales: {df.shape[0]:,}")
    print(f"   • Columnas totales: {df.shape[1]}")
    print(f"   • Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Buscar columnas clave
    col_localidad = next((c for c in df.columns if 'LOCALIDAD' in c.upper()), None)
    col_afiliacion = next((c for c in df.columns if 'AFILI' in c.upper()), None)
    col_año = 'AÑO' if 'AÑO' in df.columns else None
    
    if not all([col_localidad, col_afiliacion, col_año]):
        raise ValueError("❌ Faltan columnas necesarias (LOCALIDAD, AFILIACIÓN, AÑO)")
    
    print(f"\n✓ Columnas identificadas:")
    print(f"   • Localidad: {col_localidad}")
    print(f"   • Afiliación: {col_afiliacion}")
    print(f"   • Año: {col_año}")
    
    return df, col_localidad, col_afiliacion, col_año

# ============================================================
# 4. NORMALIZACIÓN Y LIMPIEZA DE DATOS
# ============================================================

def normalizar_regimen(valor):
    """Normaliza valores de régimen de afiliación"""
    if pd.isna(valor):
        return np.nan
    
    # Convertir a string y normalizar
    valor_str = str(valor).strip().upper()
    
    # Eliminar prefijos numéricos como "1__", "1- ", "2__"
    valor_str = pd.Series([valor_str]).str.replace(r'^\d+[\W_]*', '', regex=True).iloc[0]
    
    # Eliminar caracteres especiales extra
    valor_str = valor_str.replace('_', ' ').strip()
    
    # Mapeo de variantes comunes
    mapeo = {
        'SUBSIDIADO': ['SUBSIDIADO', 'SUBSID', 'SUB'],
        'CONTRIBUTIVO': ['CONTRIBUTIVO', 'CONTRIB', 'CONT'],
        'NO ASEGURADO': ['NO ASEGURADO', 'NO ASEG', 'SIN AFILIACION', 'NINGUNO'],
        'ESPECIAL': ['ESPECIAL', 'ESP', 'EXCEPCION'],
        'VINCULADO': ['VINCULADO', 'VINC']
    }
    
    for clave, variantes in mapeo.items():
        if any(var in valor_str for var in variantes):
            return clave
    
    return valor_str

# ============================================================
# 5. PREPARACIÓN DE DATOS PARA ACP
# ============================================================

def preparar_datos_acp(df, col_loc, col_afil, col_año):
    """Construye tabla espacio-temporal para ACP con normalización robusta"""
    print("\n" + "="*70)
    print("🔧 FASE 2: PREPARACIÓN DE DATOS ESPACIO-TEMPORALES")
    print("="*70)
    
    # Copiar y renombrar columnas
    df_filtrado = df[[col_loc, col_año, col_afil]].copy()
    df_filtrado.columns = ['Localidad', 'Año', 'Regimen']
    
    print(f"\n• Registros iniciales: {len(df_filtrado):,}")
    
    # ✨ NORMALIZACIÓN ROBUSTA DE RÉGIMEN
    print("\n🔄 Normalizando regímenes...")
    df_filtrado['Regimen'] = df_filtrado['Regimen'].apply(normalizar_regimen)
    
    # ✨ NORMALIZACIÓN Y FILTRADO DE AÑO
    print("🔄 Normalizando años...")
    df_filtrado['Año'] = pd.to_numeric(df_filtrado['Año'], errors='coerce').astype('Int64')
    df_filtrado = df_filtrado[df_filtrado['Año'].isin(AÑOS_VALIDOS)]
    
    # Eliminar valores 99999 y nulos
    df_filtrado = df_filtrado[
        (df_filtrado['Regimen'] != '99999') & 
        (df_filtrado['Regimen'] != 99999) &
        df_filtrado['Regimen'].notna() &
        df_filtrado['Localidad'].notna() &
        df_filtrado['Año'].notna()
    ]
    
    print(f"• Registros válidos: {len(df_filtrado):,}")
    print(f"• Tasa de retención: {len(df_filtrado)/len(df)*100:.2f}%")
    
    # Estadísticas descriptivas
    print(f"\n📊 Distribución temporal:")
    dist_años = df_filtrado['Año'].value_counts().sort_index()
    for año, count in dist_años.items():
        print(f"   • {int(año)}: {count:>8,} intervenciones ({count/len(df_filtrado)*100:>5.2f}%)")
    
    print(f"\n🗺️  Distribución espacial (Top 10):")
    dist_loc = df_filtrado['Localidad'].value_counts().head(10)
    for loc, count in dist_loc.items():
        print(f"   • {loc[:30]:<30}: {count:>7,} ({count/len(df_filtrado)*100:>5.2f}%)")
    
    print(f"\n🏥 Distribución por régimen:")
    dist_reg = df_filtrado['Regimen'].value_counts()
    for reg, count in dist_reg.items():
        print(f"   • {reg:<30}: {count:>7,} ({count/len(df_filtrado)*100:>5.2f}%)")
    
    # Crear tabla de frecuencias
    tabla = (
        df_filtrado
        .groupby(['Localidad', 'Año', 'Regimen'])
        .size()
        .reset_index(name='Intervenciones')
    )
    
    # Pivot: Localidad-Año como filas, Régimen como columnas
    tabla_pivot = tabla.pivot_table(
        index=['Localidad', 'Año'],
        columns='Regimen',
        values='Intervenciones',
        fill_value=0
    )
    
    # ✨ ORDENAR COLUMNAS SEGÚN ORDEN DEFINIDO
    print("\n🔄 Ordenando columnas de regímenes...")
    columnas_actuales = tabla_pivot.columns.tolist()
    columnas_finales = ['Localidad', 'Año']
    
    for reg in ORDEN_REGIMENES:
        # Buscar columna que contenga este régimen
        col_match = next((c for c in columnas_actuales if reg in str(c).upper()), None)
        if col_match:
            columnas_finales.append(col_match)
            tabla_pivot = tabla_pivot.rename(columns={col_match: reg})
        else:
            # Crear columna con ceros si no existe
            tabla_pivot[reg] = 0
            columnas_finales.append(reg)
    
    # Resetear índice y reordenar
    tabla_pivot.reset_index(inplace=True)
    
    # Solo mantener columnas que existen
    columnas_existentes = [c for c in columnas_finales if c in tabla_pivot.columns]
    tabla_pivot = tabla_pivot[columnas_existentes]
    
    # Guardar tabla base
    tabla_pivot.to_excel(
        os.path.join(ACP_TABLES, 'tabla_espacio_temporal.xlsx'),
        index=False
    )
    
    print(f"\n✓ Tabla espacio-temporal creada:")
    print(f"   • Observaciones (Localidad×Año): {tabla_pivot.shape[0]}")
    print(f"   • Variables (Regímenes): {tabla_pivot.shape[1] - 2}")
    print(f"   • Regímenes detectados: {list(tabla_pivot.columns[2:])}")
    
    return tabla_pivot

# ============================================================
# 6. APLICACIÓN DEL ACP
# ============================================================

def aplicar_acp(tabla_pivot, n_components=N_COMPONENTS):
    """Ejecuta el Análisis de Componentes Principales"""
    print("\n" + "="*70)
    print("🔍 FASE 3: ANÁLISIS DE COMPONENTES PRINCIPALES")
    print("="*70)
    
    # Separar variables predictoras
    X = tabla_pivot.drop(columns=['Localidad', 'Año'])
    variables = X.columns.tolist()
    
    print(f"\n• Variables incluidas en el ACP: {len(variables)}")
    for i, var in enumerate(variables, 1):
        print(f"   {i}. {var}")
    
    # Normalizar datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"\n✓ Datos estandarizados (media=0, desviación=1)")
    
    # Aplicar ACP
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    
    # Crear DataFrame con resultados
    df_pca = pd.DataFrame(
        X_pca,
        columns=[f'PC{i+1}' for i in range(n_components)]
    )
    df_pca['Localidad'] = tabla_pivot['Localidad'].values
    df_pca['Año'] = tabla_pivot['Año'].values
    
    # Varianza explicada
    var_exp = pca.explained_variance_ratio_ * 100
    
    print(f"\n📊 VARIANZA EXPLICADA:")
    print("="*70)
    for i, v in enumerate(var_exp, 1):
        print(f"   Componente Principal {i} (PC{i}): {v:>6.2f}%")
    print(f"   {'─'*66}")
    print(f"   TOTAL ACUMULADO:                {var_exp.sum():>6.2f}%")
    print("="*70)
    
    # Eigenvalues
    eigenvalues = pca.explained_variance_
    print(f"\n📈 EIGENVALUES (Valores propios):")
    for i, ev in enumerate(eigenvalues, 1):
        print(f"   PC{i}: {ev:.4f}")
    
    # Cargas de variables (loadings)
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(n_components)],
        index=variables
    )
    
    print(f"\n🔬 CARGAS DE VARIABLES (Loadings):")
    print("="*70)
    print(loadings.round(3).to_string())
    print("="*70)
    
    # Contribución de cada variable
    contrib = (loadings ** 2) * 100
    print(f"\n📊 CONTRIBUCIÓN DE VARIABLES (%):")
    print("="*70)
    print(contrib.round(2).to_string())
    print("="*70)
    
    # ✨ GUARDAR MODELO PCA Y SCALER
    joblib.dump(
        {'pca': pca, 'scaler': scaler, 'variables': variables},
        os.path.join(ACP_TABLES, 'modelo_pca.joblib')
    )
    print(f"\n✓ Modelo PCA guardado para reutilización")
    
    # Guardar resultados
    df_pca.to_excel(os.path.join(ACP_TABLES, 'coordenadas_acp.xlsx'), index=False)
    loadings.to_excel(os.path.join(ACP_TABLES, 'cargas_variables.xlsx'))
    
    # Eigenvalues detallado
    eigenvalues_df = pd.DataFrame({
        'Componente': [f'PC{i+1}' for i in range(len(pca.explained_variance_))],
        'Eigenvalue': pca.explained_variance_,
        'Varianza_%': pca.explained_variance_ratio_ * 100,
        'Varianza_Acumulada_%': np.cumsum(pca.explained_variance_ratio_) * 100
    })
    eigenvalues_df.to_excel(os.path.join(ACP_TABLES, 'eigenvalues.xlsx'), index=False)
    contrib.to_excel(os.path.join(ACP_TABLES, 'contribucion_variables.xlsx'))
    
    print(f"\n✓ Tablas exportadas a: {ACP_TABLES}")
    
    return df_pca, loadings, var_exp, pca, scaler

# ============================================================
# 7. VISUALIZACIONES PROFESIONALES
# ============================================================

def grafico_scree_plot(pca):
    """Gráfico de sedimentación elegante"""
    var_exp = pca.explained_variance_ratio_ * 100
    
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    x = np.arange(1, len(var_exp) + 1)
    
    bars = ax.bar(x, var_exp, color='#1976D2', alpha=0.85, 
                  edgecolor='#0D47A1', linewidth=2, label='Varianza individual')
    
    cumsum = np.cumsum(var_exp)
    line = ax.plot(x, cumsum, color='#D32F2F', marker='o', 
                   markersize=10, linewidth=3, label='Varianza acumulada')
    
    for i, (bar, val) in enumerate(zip(bars, var_exp)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{val:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=11)
    
    for i, (xi, yi) in enumerate(zip(x, cumsum)):
        ax.text(xi, yi + 3, f'{yi:.1f}%', ha='center', va='bottom',
                fontsize=10, color='#D32F2F', fontweight='bold')
    
    ax.set_xlabel('Componente Principal', fontsize=13, fontweight='bold')
    ax.set_ylabel('Varianza Explicada (%)', fontsize=13, fontweight='bold')
    ax.set_title('SCREE PLOT - Varianza Explicada por Componente\nAnálisis Espacio-Temporal NNA Bogotá', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([f'PC{i}' for i in x], fontsize=11)
    ax.legend(fontsize=11, loc='center right', framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(cumsum) + 10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '01_scree_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 01_scree_plot.png")

def grafico_biplot(df_pca, loadings, var_exp):
    """Biplot profesional con anotaciones selectivas"""
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
    
    # ✨ SELECCIONAR TOP N LOCALIDADES PARA ETIQUETAR
    totales_loc = df_pca.groupby('Localidad').size().sort_values(ascending=False)
    top_localidades = totales_loc.head(TOP_N_LABELS).index
    
    # Scatter de observaciones por año
    años_unicos = sorted(df_pca['Año'].unique())
    
    for año in años_unicos:
        subset = df_pca[df_pca['Año'] == año]
        color = COLORES_AÑOS.get(int(año), '#666666')
        ax.scatter(subset['PC1'], subset['PC2'],
                  c=color, label=f'{int(año)}', s=120, 
                  alpha=0.7, edgecolors='black', linewidth=1.5)
    
    # Etiquetar solo top localidades
    for loc in top_localidades:
        subset = df_pca[df_pca['Localidad'] == loc].iloc[-1]  # Último año
        ax.annotate(loc[:15], 
                   xy=(subset['PC1'], subset['PC2']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, weight='bold', alpha=0.8,
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='yellow', alpha=0.6))
    
    # Vectores de variables
    scale_factor = 4
    for i, var in enumerate(loadings.index):
        arrow_x = loadings.iloc[i, 0] * scale_factor
        arrow_y = loadings.iloc[i, 1] * scale_factor
        
        ax.arrow(0, 0, arrow_x, arrow_y,
                head_width=0.2, head_length=0.2,
                fc='#E53935', ec='#B71C1C', 
                alpha=0.8, linewidth=2.5, zorder=5)
        
        ax.text(arrow_x * 1.15, arrow_y * 1.15, var,
               fontsize=12, weight='bold', color='#B71C1C',
               bbox=dict(boxstyle='round,pad=0.5', 
                        facecolor='white', edgecolor='#E53935',
                        alpha=0.9, linewidth=2))
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    ax.set_xlabel(f'PC1 ({var_exp[0]:.1f}% de la varianza)', 
                  fontsize=14, fontweight='bold')
    ax.set_ylabel(f'PC2 ({var_exp[1]:.1f}% de la varianza)', 
                  fontsize=14, fontweight='bold')
    ax.set_title('BIPLOT ESPACIO-TEMPORAL\nLocalidades, Años y Regímenes de Afiliación',
                fontsize=16, weight='bold', pad=20)
    ax.legend(title='AÑO', title_fontsize=12, fontsize=11, 
             bbox_to_anchor=(1.02, 1), loc='upper left',
             framealpha=0.95, edgecolor='black', fancybox=True)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '02_biplot_espaciotemporal.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 02_biplot_espaciotemporal.png")

def grafico_trayectorias(df_pca, var_exp):
    """Evolución temporal con trayectorias - solo localidades con 2+ años"""
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
    
    # ✨ FILTRAR LOCALIDADES CON AL MENOS 2 AÑOS
    localidades_validas = df_pca.groupby('Localidad').filter(lambda x: len(x) >= 2)['Localidad'].unique()
    localidades_validas = sorted(localidades_validas)
    
    print(f"\n   📍 Trayectorias: {len(localidades_validas)} localidades con 2+ años")
    
    for i, loc in enumerate(localidades_validas):
        subset = df_pca[df_pca['Localidad'] == loc].sort_values('Año')
        
        if len(subset) > 1:
            color = COLORES_LOCALIDADES[i % len(COLORES_LOCALIDADES)]
            
            ax.plot(subset['PC1'], subset['PC2'],
                   marker='o', linewidth=2.5, markersize=8,
                   color=color, alpha=0.8, label=loc[:20])
            
            if len(subset) >= 2:
                x_vals = subset['PC1'].values
                y_vals = subset['PC2'].values
                ax.annotate('', xy=(x_vals[-1], y_vals[-1]),
                          xytext=(x_vals[-2], y_vals[-2]),
                          arrowprops=dict(arrowstyle='->', lw=2.5, 
                                        color=color, alpha=0.9))
            
            ax.text(subset['PC1'].iloc[0], subset['PC2'].iloc[0],
                   f"{int(subset['Año'].iloc[0])}", 
                   fontsize=9, ha='center', va='center',
                   bbox=dict(boxstyle='circle', facecolor='white', 
                            edgecolor=color, linewidth=2))
            
            ax.text(subset['PC1'].iloc[-1] + 0.15, subset['PC2'].iloc[-1],
                   loc[:20], fontsize=9, weight='bold',
                   color=color, alpha=0.9)
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    ax.set_xlabel(f'PC1 ({var_exp[0]:.1f}% varianza)', fontsize=14, fontweight='bold')
    ax.set_ylabel(f'PC2 ({var_exp[1]:.1f}% varianza)', fontsize=14, fontweight='bold')
    ax.set_title('TRAYECTORIAS ESPACIO-TEMPORALES POR LOCALIDAD\nEvolución 2021-2024',
                fontsize=16, weight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '03_trayectorias_espaciotemporales.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 03_trayectorias_espaciotemporales.png")

def grafico_loadings(loadings):
    """Gráfico de cargas con colores por signo"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='white')
    
    for i, comp in enumerate(['PC1', 'PC2']):
        cargas = loadings[comp].sort_values()
        colores = ['#D32F2F' if x < 0 else '#1976D2' for x in cargas.values]
        
        bars = axes[i].barh(range(len(cargas)), cargas.values, 
                           color=colores, alpha=0.85, edgecolor='black', linewidth=1.5)
        
        for j, (bar, val) in enumerate(zip(bars, cargas.values)):
            x_pos = val + (0.02 if val > 0 else -0.02)
            ha = 'left' if val > 0 else 'right'
            axes[i].text(x_pos, bar.get_y() + bar.get_height()/2,
                        f'{val:.3f}', ha=ha, va='center',
                        fontweight='bold', fontsize=10)
        
        axes[i].set_yticks(range(len(cargas)))
        axes[i].set_yticklabels(cargas.index, fontsize=11, fontweight='bold')
        axes[i].set_xlabel('Carga (Loading)', fontsize=12, fontweight='bold')
        axes[i].set_title(f'Evolución Temporal en {comp}', 
                         fontsize=13, weight='bold')
        axes[i].set_xlabel('AÑO', fontsize=12, fontweight='bold')
        axes[i].set_ylabel('LOCALIDAD', fontsize=12, fontweight='bold')
        axes[i].tick_params(labelsize=10)
    
    plt.suptitle('MAPAS DE CALOR ESPACIO-TEMPORALES\nCoordenadas por Localidad y Año',
                fontsize=15, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '05_heatmap_espaciotemporal.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 05_heatmap_espaciotemporal.png")

def grafico_circulos_correlacion(loadings):
    """Círculo de correlaciones"""
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    
    circle = plt.Circle((0, 0), 1, color='gray', fill=False, 
                       linewidth=2, linestyle='--', alpha=0.5)
    ax.add_patch(circle)
    
    for i, var in enumerate(loadings.index):
        x, y = loadings.iloc[i, 0], loadings.iloc[i, 1]
        
        ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.05,
                fc='#1976D2', ec='#0D47A1', linewidth=2.5, alpha=0.8)
        
        ax.text(x * 1.15, y * 1.15, var, fontsize=12, weight='bold',
               ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor='#1976D2', alpha=0.9, linewidth=2))
    
    ax.axhline(0, color='black', linewidth=1.5)
    ax.axvline(0, color='black', linewidth=1.5)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel('PC1', fontsize=14, fontweight='bold')
    ax.set_ylabel('PC2', fontsize=14, fontweight='bold')
    ax.set_title('CÍRCULO DE CORRELACIONES\nRelación entre Regímenes y Componentes',
                fontsize=15, weight='bold', pad=20)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '06_circulo_correlaciones.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 06_circulo_correlaciones.png")

# ============================================================
# 8. INTERPRETACIÓN AUTOMÁTICA MEJORADA
# ============================================================

def interpretar_acp(loadings, var_exp, df_pca):
    """Genera interpretación detallada del análisis"""
    print("\n" + "="*70)
    print("🧠 FASE 4: INTERPRETACIÓN AUTOMÁTICA")
    print("="*70)
    
    interpretacion = []
    
    interpretacion.append("# 🧠 INTERPRETACIÓN DEL ACP ESPACIO-TEMPORAL\n")
    interpretacion.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    interpretacion.append("---\n\n")
    
    # Varianza
    interpretacion.append("## 📊 Varianza Explicada\n\n")
    interpretacion.append(f"- **PC1:** {var_exp[0]:.2f}%\n")
    interpretacion.append(f"- **PC2:** {var_exp[1]:.2f}%\n")
    interpretacion.append(f"- **TOTAL:** {var_exp.sum():.2f}%\n\n")
    
    print(f"\n📊 Varianza total capturada: {var_exp.sum():.2f}%")
    
    # Componente 1
    c1_cargas = loadings['PC1'].sort_values(ascending=False)
    var_max_c1 = c1_cargas.idxmax()
    var_min_c1 = c1_cargas.idxmin()
    
    interpretacion.append("## 🔍 Componente Principal 1 (Eje Horizontal)\n\n")
    interpretacion.append(f"**Variable dominante positiva:** {var_max_c1} ({c1_cargas.max():.3f})\n")
    interpretacion.append(f"**Variable dominante negativa:** {var_min_c1} ({c1_cargas.min():.3f})\n\n")
    interpretacion.append("**Interpretación:** Este componente representa el **volumen y tipo predominante** ")
    interpretacion.append("de afiliación. Valores positivos indican mayor presencia del régimen dominante, ")
    interpretacion.append("mientras valores negativos sugieren una composición diferente.\n\n")
    
    print(f"\n🔍 PC1 - Variable más importante: {var_max_c1} (carga: {c1_cargas.max():.3f})")
    
    # Componente 2
    c2_cargas = loadings['PC2'].sort_values(ascending=False)
    var_max_c2 = c2_cargas.idxmax()
    var_min_c2 = c2_cargas.idxmin()
    
    interpretacion.append("## 🔍 Componente Principal 2 (Eje Vertical)\n\n")
    interpretacion.append(f"**Variable dominante positiva:** {var_max_c2} ({c2_cargas.max():.3f})\n")
    interpretacion.append(f"**Variable dominante negativa:** {var_min_c2} ({c2_cargas.min():.3f})\n\n")
    interpretacion.append("**Interpretación:** Este componente diferencia las **estructuras de afiliación**. ")
    interpretacion.append("Captura variaciones en la composición de regímenes no explicadas por el volumen total.\n\n")
    
    print(f"🔍 PC2 - Variable más importante: {var_max_c2} (carga: {c2_cargas.max():.3f})")
    
    # Patrones espaciales
    interpretacion.append("## 🗺️ Patrones Espacio-Temporales\n\n")
    
    loc_max_pc1 = df_pca.loc[df_pca['PC1'].idxmax()]
    loc_min_pc1 = df_pca.loc[df_pca['PC1'].idxmin()]
    loc_max_pc2 = df_pca.loc[df_pca['PC2'].idxmax()]
    loc_min_pc2 = df_pca.loc[df_pca['PC2'].idxmin()]
    
    interpretacion.append("### Localidades destacadas:\n\n")
    interpretacion.append(f"- **Mayor PC1:** {loc_max_pc1['Localidad']} ({int(loc_max_pc1['Año'])}) = {loc_max_pc1['PC1']:.2f}\n")
    interpretacion.append(f"- **Menor PC1:** {loc_min_pc1['Localidad']} ({int(loc_min_pc1['Año'])}) = {loc_min_pc1['PC1']:.2f}\n")
    interpretacion.append(f"- **Mayor PC2:** {loc_max_pc2['Localidad']} ({int(loc_max_pc2['Año'])}) = {loc_max_pc2['PC2']:.2f}\n")
    interpretacion.append(f"- **Menor PC2:** {loc_min_pc2['Localidad']} ({int(loc_min_pc2['Año'])}) = {loc_min_pc2['PC2']:.2f}\n\n")
    
    print(f"\n🗺️ Localidad con mayor PC1: {loc_max_pc1['Localidad']} ({int(loc_max_pc1['Año'])})")
    print(f"🗺️ Localidad con mayor PC2: {loc_max_pc2['Localidad']} ({int(loc_max_pc2['Año'])})")
    
    # Evolución temporal
    interpretacion.append("## 📈 Análisis de Evolución Temporal\n\n")
    
    cambios_pc1 = []
    cambios_pc2 = []
    
    for loc in df_pca['Localidad'].unique():
        subset = df_pca[df_pca['Localidad'] == loc].sort_values('Año')
        if len(subset) > 1:
            cambio_pc1 = subset['PC1'].iloc[-1] - subset['PC1'].iloc[0]
            cambio_pc2 = subset['PC2'].iloc[-1] - subset['PC2'].iloc[0]
            cambios_pc1.append({'Localidad': loc, 'Cambio': cambio_pc1})
            cambios_pc2.append({'Localidad': loc, 'Cambio': cambio_pc2})
    
    if cambios_pc1:
        df_cambios_pc1 = pd.DataFrame(cambios_pc1).sort_values('Cambio', ascending=False)
        df_cambios_pc2 = pd.DataFrame(cambios_pc2).sort_values('Cambio', ascending=False)
        
        interpretacion.append("### Mayores cambios en PC1 (2021→2024):\n\n")
        for i, row in df_cambios_pc1.head(5).iterrows():
            interpretacion.append(f"- {row['Localidad']}: {row['Cambio']:+.2f}\n")
        
        interpretacion.append("\n### Mayores cambios en PC2 (2021→2024):\n\n")
        for i, row in df_cambios_pc2.head(5).iterrows():
            interpretacion.append(f"- {row['Localidad']}: {row['Cambio']:+.2f}\n")
        
        interpretacion.append("\n**Interpretación:** Las localidades con mayores cambios sugieren ")
        interpretacion.append("transformaciones estructurales en la población atendida o en la ")
        interpretacion.append("cobertura de los programas de intervención.\n\n")
        
        print(f"\n📈 Mayor cambio PC1: {df_cambios_pc1.iloc[0]['Localidad']} ({df_cambios_pc1.iloc[0]['Cambio']:+.2f})")
        print(f"📈 Mayor cambio PC2: {df_cambios_pc2.iloc[0]['Localidad']} ({df_cambios_pc2.iloc[0]['Cambio']:+.2f})")
    
    # Cuadrantes
    interpretacion.append("## 🎯 Clasificación por Cuadrantes\n\n")
    
    df_pca['Cuadrante'] = 'Origen'
    df_pca.loc[(df_pca['PC1'] > 0) & (df_pca['PC2'] > 0), 'Cuadrante'] = 'Q1: Alto PC1, Alto PC2'
    df_pca.loc[(df_pca['PC1'] < 0) & (df_pca['PC2'] > 0), 'Cuadrante'] = 'Q2: Bajo PC1, Alto PC2'
    df_pca.loc[(df_pca['PC1'] < 0) & (df_pca['PC2'] < 0), 'Cuadrante'] = 'Q3: Bajo PC1, Bajo PC2'
    df_pca.loc[(df_pca['PC1'] > 0) & (df_pca['PC2'] < 0), 'Cuadrante'] = 'Q4: Alto PC1, Bajo PC2'
    
    dist_cuadrantes = df_pca['Cuadrante'].value_counts()
    
    for cuad, count in dist_cuadrantes.items():
        pct = count / len(df_pca) * 100
        interpretacion.append(f"- **{cuad}:** {count} observaciones ({pct:.1f}%)\n")
    
    interpretacion.append("\n")
    
    print(f"\n🎯 Distribución por cuadrantes:")
    for cuad, count in dist_cuadrantes.items():
        print(f"   • {cuad}: {count} ({count/len(df_pca)*100:.1f}%)")
    
    # Recomendaciones
    interpretacion.append("## 💡 Recomendaciones de Política Pública\n\n")
    interpretacion.append("### Basadas en el análisis espacio-temporal:\n\n")
    interpretacion.append("1. **Focalización territorial:** Priorizar intervenciones en localidades ")
    interpretacion.append("ubicadas en cuadrantes extremos que presentan perfiles diferenciados.\n\n")
    interpretacion.append("2. **Monitoreo dinámico:** Las localidades con trayectorias inestables ")
    interpretacion.append("requieren seguimiento continuo para identificar causas de variabilidad.\n\n")
    interpretacion.append("3. **Equidad en cobertura:** Analizar si localidades con mayor proporción ")
    interpretacion.append("de régimen subsidiado reciben recursos proporcionales a sus necesidades.\n\n")
    interpretacion.append("4. **Intervenciones diferenciadas:** Diseñar estrategias específicas según ")
    interpretacion.append("el perfil espacio-temporal de cada grupo de localidades.\n\n")
    interpretacion.append("5. **Evaluación de impacto:** Usar las trayectorias 2021-2024 para evaluar ")
    interpretacion.append("la efectividad de políticas implementadas en el período.\n\n")
    
    # Limitaciones
    interpretacion.append("## ⚠️ Limitaciones del Análisis\n\n")
    interpretacion.append("- El ACP captura relaciones lineales; patrones no lineales pueden no ser detectados.\n")
    interpretacion.append("- La interpretación asume estabilidad en la composición poblacional.\n")
    interpretacion.append("- Factores externos (pandemia, migraciones) pueden influir en las trayectorias.\n")
    interpretacion.append(f"- El análisis explica el {var_exp.sum():.1f}% de la variabilidad total; ")
    interpretacion.append(f"el {100-var_exp.sum():.1f}% restante no está capturado.\n\n")
    
    # Conclusión
    interpretacion.append("## 📝 Conclusión\n\n")
    interpretacion.append("El ACP espacio-temporal revela patrones sistemáticos en las intervenciones con NNA ")
    interpretacion.append("en Bogotá durante 2021-2024. Los dos primeros componentes capturan información sobre:\n\n")
    interpretacion.append("- **Volumen y tipo de afiliación predominante** (PC1)\n")
    interpretacion.append("- **Estructura diferenciada de regímenes** (PC2)\n\n")
    interpretacion.append("Las trayectorias temporales permiten identificar localidades con cambios significativos ")
    interpretacion.append("que requieren atención especial en la planificación de políticas públicas.\n")
    
    # Guardar
    texto_completo = ''.join(interpretacion)
    with open(ACP_LOG, 'w', encoding='utf-8') as f:
        f.write(texto_completo)
    
    print(f"\n✓ Interpretación completa guardada en: {ACP_LOG}")
    
    return texto_completo

# ============================================================
# 9. EXPORTAR METADATA DEL ANÁLISIS
# ============================================================

def exportar_metadata(df_pca):
    """Guarda metadata completa del análisis para reproducibilidad"""
    metadata = {
        'fecha_ejecucion': datetime.now().isoformat(),
        'python_version': sys.version,
        'librerias': {
            'pandas': pd.__version__,
            'numpy': np.__version__,
            'sklearn': sklearn_version,
            'matplotlib': matplotlib.__version__,
            'seaborn': sns.__version__
        },
        'parametros': {
            'años_analizados': AÑOS_VALIDOS,
            'n_componentes': N_COMPONENTS,
            'top_n_etiquetas': TOP_N_LABELS
        },
        'datos': {
            'observaciones_totales': len(df_pca),
            'localidades_unicas': int(df_pca['Localidad'].nunique()),
            'años_unicos': sorted([int(x) for x in df_pca['Año'].unique()]),
            'periodo': f"{int(df_pca['Año'].min())}-{int(df_pca['Año'].max())}"
        },
        'archivos_generados': {
            'figuras': sorted(os.listdir(ACP_DIR)),
            'tablas': sorted(os.listdir(ACP_TABLES))
        }
    }
    
    with open(os.path.join(ACP_TABLES, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Metadata exportada: metadata.json")
    return metadata
# ============================================================
# 9.6. MAPA DE CALOR ESPACIO-TEMPORAL
# ============================================================

def grafico_mapa_calor_temporal(df_pca):
    """Genera mapas de calor para las coordenadas PC1 y PC2 por localidad y año."""
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor='white')
    
    for i, comp in enumerate(['PC1', 'PC2']):
        pivot = df_pca.pivot(index='Localidad', columns='Año', values=comp)
        
        sns.heatmap(
            pivot, annot=True, fmt=".2f", cmap='RdYlBu_r', center=0,
            linewidths=1, linecolor='white',
            cbar_kws={'label': f'Coordenada {comp}'},
            ax=axes[i]
        )
        
        axes[i].set_title(f'Mapa de calor {comp}\n(Coordenadas por Localidad y Año)',
                          fontsize=14, weight='bold', pad=15)
        axes[i].set_xlabel('Año', fontsize=12, fontweight='bold')
        axes[i].set_ylabel('Localidad', fontsize=12, fontweight='bold')
        axes[i].tick_params(axis='x', rotation=0)
        axes[i].tick_params(axis='y', labelsize=10)
    
    plt.suptitle(
        'MAPAS DE CALOR ESPACIO-TEMPORALES\nComponentes Principales (PC1 y PC2)',
        fontsize=16, weight='bold', y=1.02
    )
    plt.tight_layout()
    
    plt.savefig(os.path.join(ACP_DIR, '05_heatmap_espaciotemporal.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 05_heatmap_espaciotemporal.png")

# ============================================================
# 9. TABLA DE INTERPRETACIÓN ESPACIO-TEMPORAL DETALLADA
# ============================================================

def tabla_interpretacion_espaciotemporal(df_pca, tabla_pivot, ruta_salida):
    """
    Crea una tabla con los cambios por localidad en PC1, PC2 y total de intervenciones.
    """
    print("\n======================================================================")
    print("📊 FASE 5B: TABLA DE INTERPRETACIÓN ESPACIO-TEMPORAL")
    print("======================================================================\n")

    # Asegurarse de que el año sea numérico
    df_pca = df_pca.copy()
    df_pca['Año'] = df_pca['Año'].astype(int)

    # Calcular total de intervenciones (sumando regímenes)
    tabla_pivot['Total_Intervenciones'] = tabla_pivot.iloc[:, 2:].sum(axis=1)

    # Combinar PCA con totales
    merged = pd.merge(df_pca, 
                      tabla_pivot[['Localidad', 'Año', 'Total_Intervenciones']], 
                      on=['Localidad', 'Año'], how='left')

    # Calcular variaciones por localidad
    cambios = []
    for loc, grupo in merged.groupby('Localidad'):
        grupo_ordenado = grupo.sort_values('Año')
        if len(grupo_ordenado) >= 2:
            pc1_ini, pc1_fin = grupo_ordenado['PC1'].iloc[0], grupo_ordenado['PC1'].iloc[-1]
            pc2_ini, pc2_fin = grupo_ordenado['PC2'].iloc[0], grupo_ordenado['PC2'].iloc[-1]
            total_ini, total_fin = grupo_ordenado['Total_Intervenciones'].iloc[0], grupo_ordenado['Total_Intervenciones'].iloc[-1]

            cambios.append({
                'Localidad': loc,
                'PC1_inicial': round(pc1_ini, 2),
                'PC1_final': round(pc1_fin, 2),
                'ΔPC1': round(pc1_fin - pc1_ini, 2),
                'PC2_inicial': round(pc2_ini, 2),
                'PC2_final': round(pc2_fin, 2),
                'ΔPC2': round(pc2_fin - pc2_ini, 2),
                'Intervenciones_iniciales': int(total_ini),
                'Intervenciones_finales': int(total_fin),
                'ΔIntervenciones': int(total_fin - total_ini)
            })

    resumen = pd.DataFrame(cambios)

    # Clasificar tipo de cambio
    resumen['Cambio_PC1'] = np.where(resumen['ΔPC1'] > 0, 'Aumento', 'Disminución')
    resumen['Cambio_PC2'] = np.where(resumen['ΔPC2'] > 0, 'Aumento', 'Disminución')
    resumen['Cambio_Intervenciones'] = np.where(resumen['ΔIntervenciones'] > 0, 'Aumento', 'Disminución')

    # Ordenar por magnitud de cambio en PC1
    resumen = resumen.sort_values(by='ΔPC1', ascending=False).reset_index(drop=True)

    # Exportar tabla
    output_file = os.path.join(ruta_salida, 'tabla_interpretacion_espaciotemporal.xlsx')
    resumen.to_excel(output_file, index=False)
    print(f"✓ Tabla de interpretación guardada: {output_file}\n")

    # Vista previa de las primeras filas
    print("📋 Principales resultados:\n")
    print(resumen.head(10).to_string(index=False))

    return resumen


# ============================================================
# 10. EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta el análisis completo de ACP espacio-temporal"""
    inicio = datetime.now()
    
    try:
        # ====================================================
        # FASE 1: CARGA DE DATOS
        # ====================================================
        df, col_loc, col_afil, col_año = cargar_datos()
        
        # ====================================================
        # FASE 2: PREPARACIÓN Y NORMALIZACIÓN ROBUSTA
        # ====================================================
        tabla_pivot = preparar_datos_acp(df, col_loc, col_afil, col_año)
        
        # ====================================================
        # FASE 3: APLICACIÓN DEL ACP
        # ====================================================
        df_pca, loadings, var_exp, pca, scaler = aplicar_acp(tabla_pivot, n_components=N_COMPONENTS)
        
        # ====================================================
        # FASE 4: GENERACIÓN DE VISUALIZACIONES
        # ====================================================
        print("\n" + "="*70)
        print("📊 FASE 4: GENERACIÓN DE VISUALIZACIONES")
        print("="*70)
        print()
        
        grafico_scree_plot(pca)                     # Varianza explicada
        grafico_biplot(df_pca, loadings, var_exp)   # Biplot espacio-temporal
        grafico_trayectorias(df_pca, var_exp)       # Evolución temporal
        grafico_loadings(loadings)                  # Cargas por régimen
        grafico_mapa_calor_temporal(df_pca)         # Heatmap espacio-temporal
        grafico_circulos_correlacion(loadings)      # Círculo de correlaciones
        
        # ====================================================
        # FASE 5: INTERPRETACIÓN AUTOMÁTICA
        # ====================================================
        interpretacion = interpretar_acp(loadings, var_exp, df_pca)
        
        # ====================================================
        # FASE 6: EXPORTACIÓN DE METADATA
        # ====================================================
        metadata = exportar_metadata(df_pca)
        
        # ====================================================
        # FASE FINAL: RESUMEN Y CIERRE
        # ====================================================
        duracion = (datetime.now() - inicio).total_seconds()
        
        print("\n" + "="*70)
        print("✅ ANÁLISIS COMPLETADO CON ÉXITO")
        print("="*70)
        print(f"\n📊 RESUMEN DE RESULTADOS:")
        print(f"   • Varianza explicada total: {var_exp.sum():.2f}%")
        print(f"   • Observaciones analizadas: {len(df_pca)}")
        print(f"   • Localidades únicas: {df_pca['Localidad'].nunique()}")
        print(f"   • Período temporal: {int(df_pca['Año'].min())}-{int(df_pca['Año'].max())}")
        
        print(f"\n📁 ARCHIVOS GENERADOS:")
        archivos_figuras = sorted(os.listdir(ACP_DIR))
        print(f"   • Figuras ({len(archivos_figuras)}):")
        for archivo in archivos_figuras:
            print(f"      - {archivo}")
        
        archivos_tablas = sorted(os.listdir(ACP_TABLES))
        print(f"\n   • Tablas ({len(archivos_tablas)}):")
        for archivo in archivos_tablas:
            print(f"      - {archivo}")
        
        print(f"\n   • Interpretación guardada en:")
        print(f"      - {os.path.basename(ACP_LOG)}")
        
        print(f"\n⏱️ Tiempo total de ejecución: {duracion:.2f} segundos")
        print("\n" + "="*70)
        print("📂 Ubicación de resultados:")
        print(f"   • Figuras: {ACP_DIR}")
        print(f"   • Tablas:  {ACP_TABLES}")
        print("="*70)
        print("\n🎉 ¡Análisis espacio-temporal completado exitosamente!")
        print("   Todos los resultados están listos para informes y visualización.")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA EJECUCIÓN: {str(e)}")
        import traceback
        traceback.print_exc()

# ============================================================
#  VERIFICAR TABLA PIVOTE (ENTRADA AL ACP)
# ============================================================
df, col_loc, col_afil, col_año = cargar_datos()
tabla_pivot = preparar_datos_acp(df, col_loc, col_afil, col_año)
print(tabla_pivot.head(15))
tabla_pivot.to_excel("reports/tables/ACP/tabla_pivot_verificada.xlsx", index=False)

# ============================================================
#  VISUALIZACIÓN: CAMBIO DE INTERVENCIONES POR LOCALIDAD
# ============================================================
def grafico_cambio_localidades(tabla_pivot):
    """
    Muestra las localidades con mayor aumento o disminución de intervenciones
    entre el primer y último año (por defecto 2021 vs 2024).
    """
    
    print("\n📊 Generando gráfico de cambio de intervenciones por localidad...")
    
    # Asegurar que los años están ordenados correctamente
    años_disponibles = sorted(tabla_pivot['Año'].unique())
    año_ini, año_fin = años_disponibles[0], años_disponibles[-1]
    
    print(f"   Analizando cambio entre {año_ini} y {año_fin}...")
    
    # Sumar todas las columnas de regímenes para obtener total de intervenciones
    tabla_pivot['Total_Intervenciones'] = tabla_pivot.iloc[:, 2:].sum(axis=1)
    
    # Crear tabla comparativa: una fila por localidad con totales en año inicial y final
    resumen = (
        tabla_pivot
        .pivot_table(index='Localidad', columns='Año', values='Total_Intervenciones', fill_value=0)
        .reset_index()
    )
    
    # Calcular cambio absoluto y relativo
    resumen['Cambio_Abs'] = resumen[año_fin] - resumen[año_ini]
    resumen['Cambio_%'] = ((resumen[año_fin] - resumen[año_ini]) / resumen[año_ini].replace(0, np.nan)) * 100
    
    # Top 10 aumentos y disminuciones
    top_aumentos = resumen.sort_values('Cambio_Abs', ascending=False).head(10)
    top_disminuciones = resumen.sort_values('Cambio_Abs', ascending=True).head(10)
    
    # ====== 📊 Gráfico combinado ======
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='white')
    
    # Aumentos
    axes[0].barh(top_aumentos['Localidad'], top_aumentos['Cambio_Abs'],
                 color='#1976D2', alpha=0.85, edgecolor='black')
    axes[0].set_title(f'Top 10 Aumentos de Intervenciones ({año_ini}→{año_fin})',
                      fontsize=13, weight='bold', pad=15)
    axes[0].set_xlabel('Cambio Absoluto', fontsize=11, fontweight='bold')
    for i, (loc, val) in enumerate(zip(top_aumentos['Localidad'], top_aumentos['Cambio_Abs'])):
        axes[0].text(val + 100, i, f"+{int(val):,}", va='center', fontsize=10, fontweight='bold', color='#0D47A1')
    
    # Disminuciones
    axes[1].barh(top_disminuciones['Localidad'], top_disminuciones['Cambio_Abs'],
                 color='#D32F2F', alpha=0.85, edgecolor='black')
    axes[1].set_title(f'Top 10 Disminuciones de Intervenciones ({año_ini}→{año_fin})',
                      fontsize=13, weight='bold', pad=15)
    axes[1].set_xlabel('Cambio Absoluto', fontsize=11, fontweight='bold')
    for i, (loc, val) in enumerate(zip(top_disminuciones['Localidad'], top_disminuciones['Cambio_Abs'])):
        axes[1].text(val - 300, i, f"{int(val):,}", va='center', fontsize=10, fontweight='bold', color='#B71C1C')
    
    plt.suptitle('CAMBIO EN INTERVENCIONES POR LOCALIDAD (2021–2024)',
                 fontsize=15, weight='bold', y=0.94)
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '08_cambio_localidades.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Exportar tabla resumen
    resumen.to_excel(os.path.join(ACP_TABLES, 'cambio_intervenciones_localidades.xlsx'), index=False)
    
    print("   ✓ Gráfico guardado: 08_cambio_localidades.png")
    print("   ✓ Tabla resumen guardada: cambio_intervenciones_localidades.xlsx")

grafico_cambio_localidades(tabla_pivot)


# ============================================================
# ANÁLISIS DE COMPONENTES PRINCIPALES ESPACIO-TEMPORAL
# Proyecto: Intervenciones con NNA Bogotá (2021–2024)
# Versión OPTIMIZADA con visualizaciones profesionales
# ============================================================

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import __version__ as sklearn_version
from datetime import datetime
import warnings
import json
import joblib

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'

print("="*70)
print("📊 ANÁLISIS DE COMPONENTES PRINCIPALES ESPACIO-TEMPORAL")
print("    Proyecto: Intervenciones NNA Bogotá (2021-2024)")
print("="*70)
print()

# ============================================================
# 1. CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = SCRIPT_DIR if os.path.exists(os.path.join(SCRIPT_DIR, "data")) else os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "base_nna_limpia.xlsx")

ACP_DIR = os.path.join(BASE_DIR, "reports", "figures", "ACP")
ACP_TABLES = os.path.join(BASE_DIR, "reports", "tables", "ACP")
ACP_LOG = os.path.join(BASE_DIR, "reports", "ACP_analisis.md")

for path in [ACP_DIR, ACP_TABLES]:
    os.makedirs(path, exist_ok=True)

# Parámetros del análisis
AÑOS_VALIDOS = [2021, 2022, 2023, 2024]
N_COMPONENTS = 2
TOP_N_LABELS = 10

# Orden deseado de regímenes
ORDEN_REGIMENES = ['SUBSIDIADO', 'CONTRIBUTIVO', 'NO_ASEGURADO', 'ESPECIAL', 'VINCULADO']

print(f"📂 Configuración:")
print(f"   • Base de datos: {os.path.basename(DATA_FILE)}")
print(f"   • Años válidos: {AÑOS_VALIDOS}")
print(f"   • Componentes: {N_COMPONENTS}")
print()

# ============================================================
# 2. PALETAS DE COLORES PROFESIONALES
# ============================================================

COLORES_AÑOS = {
    2021: '#1a237e',  # Azul marino
    2022: '#0277bd',  # Azul cielo
    2023: '#00897b',  # Verde azulado
    2024: '#558b2f'   # Verde oliva
}

COLORES_LOCALIDADES = [
    '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3',
    '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39',
    '#ffc107', '#ff9800', '#ff5722', '#795548', '#607d8b',
    '#f44336', '#e040fb', '#00e676', '#ffea00', '#ff6d00'
]

# ============================================================
# 3. CARGA DE DATOS
# ============================================================

def cargar_datos():
    """Carga y valida la base de datos limpia"""
    print("="*70)
    print("📥 FASE 1: CARGA DE DATOS")
    print("="*70)
    
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"❌ No se encontró: {DATA_FILE}")
    
    df = pd.read_excel(DATA_FILE, engine='openpyxl')
    print(f"\n✓ Base cargada exitosamente")
    print(f"   • Filas totales: {df.shape[0]:,}")
    print(f"   • Columnas totales: {df.shape[1]}")
    
    col_localidad = next((c for c in df.columns if 'LOCALIDAD' in c.upper()), None)
    col_afiliacion = next((c for c in df.columns if 'AFILI' in c.upper()), None)
    col_año = 'AÑO' if 'AÑO' in df.columns else None
    
    if not all([col_localidad, col_afiliacion, col_año]):
        raise ValueError("❌ Faltan columnas necesarias")
    
    print(f"\n✓ Columnas identificadas:")
    print(f"   • Localidad: {col_localidad}")
    print(f"   • Afiliación: {col_afiliacion}")
    print(f"   • Año: {col_año}")
    
    return df, col_localidad, col_afiliacion, col_año

# ============================================================
# 4. PREPARACIÓN DE DATOS
# ============================================================

def normalizar_regimen(valor):
    """Normaliza valores de régimen de afiliación"""
    if pd.isna(valor) or str(valor).strip() == '':
        return np.nan
    
    valor_str = str(valor).strip().upper()
    valor_str = pd.Series([valor_str]).str.replace(r'^\d+[\W_]*', '', regex=True).iloc[0]
    valor_str = valor_str.replace('_', ' ').strip()
    
    mapeo = {
        'SUBSIDIADO': ['SUBSIDIADO', 'SUBSID', 'SUB'],
        'CONTRIBUTIVO': ['CONTRIBUTIVO', 'CONTRIB', 'CONT'],
        'NO_ASEGURADO': ['NO ASEGURADO', 'NO ASEG', 'SIN AFILIACION', 'NINGUNO'],
        'ESPECIAL': ['ESPECIAL', 'ESP', 'EXCEPCION'],
        'VINCULADO': ['VINCULADO', 'VINC']
    }
    
    for clave, variantes in mapeo.items():
        if any(var in valor_str for var in variantes):
            return clave
    
    return valor_str if valor_str else np.nan

def preparar_datos_acp(df, col_loc, col_afil, col_año):
    """Construye tabla espacio-temporal para ACP"""
    print("\n" + "="*70)
    print("🔧 FASE 2: PREPARACIÓN DE DATOS ESPACIO-TEMPORALES")
    print("="*70)
    
    df_filtrado = df[[col_loc, col_año, col_afil]].copy()
    df_filtrado.columns = ['Localidad', 'Año', 'Regimen']
    
    print(f"\n• Registros iniciales: {len(df_filtrado):,}")
    
    # Normalización
    df_filtrado['Regimen'] = df_filtrado['Regimen'].apply(normalizar_regimen)
    df_filtrado['Año'] = pd.to_numeric(df_filtrado['Año'], errors='coerce').astype('Int64')
    df_filtrado = df_filtrado[df_filtrado['Año'].isin(AÑOS_VALIDOS)]
    
    # Filtrar valores inválidos
    df_filtrado = df_filtrado[
        (df_filtrado['Regimen'] != '99999') & 
        (df_filtrado['Regimen'] != 99999) &
        df_filtrado['Regimen'].notna() &
        df_filtrado['Localidad'].notna() &
        df_filtrado['Año'].notna()
    ]
    
    print(f"• Registros válidos: {len(df_filtrado):,} ({len(df_filtrado)/len(df)*100:.1f}%)")
    
    # Crear tabla de frecuencias
    tabla = df_filtrado.groupby(['Localidad', 'Año', 'Regimen']).size().reset_index(name='Intervenciones')
    
    # Pivot
    tabla_pivot = tabla.pivot_table(
        index=['Localidad', 'Año'],
        columns='Regimen',
        values='Intervenciones',
        fill_value=0
    )
    
    # Ordenar columnas
    columnas_actuales = tabla_pivot.columns.tolist()
    columnas_finales = []
    
    for reg in ORDEN_REGIMENES:
        col_match = next((c for c in columnas_actuales if reg in str(c).upper()), None)
        if col_match:
            columnas_finales.append(reg)
            tabla_pivot = tabla_pivot.rename(columns={col_match: reg})
    
    tabla_pivot = tabla_pivot[[c for c in columnas_finales if c in tabla_pivot.columns]]
    tabla_pivot.reset_index(inplace=True)
    
    # Guardar con manejo de errores
    try:
        tabla_pivot.to_excel(os.path.join(ACP_TABLES, 'tabla_espacio_temporal.xlsx'), index=False)
    except PermissionError:
        print("   ⚠️ Archivo Excel abierto, guardando como CSV...")
        tabla_pivot.to_csv(os.path.join(ACP_TABLES, 'tabla_espacio_temporal.csv'), index=False)
    
    print(f"\n✓ Tabla creada: {tabla_pivot.shape[0]} observaciones × {tabla_pivot.shape[1]-2} regímenes")
    
    return tabla_pivot

# ============================================================
# 5. APLICACIÓN DEL ACP
# ============================================================

def aplicar_acp(tabla_pivot, n_components=N_COMPONENTS):
    """Ejecuta el ACP"""
    print("\n" + "="*70)
    print("🔍 FASE 3: ANÁLISIS DE COMPONENTES PRINCIPALES")
    print("="*70)
    
    X = tabla_pivot.drop(columns=['Localidad', 'Año'])
    variables = X.columns.tolist()
    
    print(f"\n• Variables en el ACP: {variables}")
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    
    df_pca = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(n_components)])
    df_pca['Localidad'] = tabla_pivot['Localidad'].values
    df_pca['Año'] = tabla_pivot['Año'].values
    
    var_exp = pca.explained_variance_ratio_ * 100
    
    print(f"\n📊 VARIANZA EXPLICADA:")
    print(f"   • PC1: {var_exp[0]:.2f}%")
    print(f"   • PC2: {var_exp[1]:.2f}%")
    print(f"   • TOTAL: {var_exp.sum():.2f}%")
    
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(n_components)],
        index=variables
    )
    
    print(f"\n🔬 CARGAS DE VARIABLES:")
    print(loadings.round(3))
    
    # Guardar resultados
    try:
        joblib.dump({'pca': pca, 'scaler': scaler, 'variables': variables},
                   os.path.join(ACP_TABLES, 'modelo_pca.joblib'))
        df_pca.to_excel(os.path.join(ACP_TABLES, 'coordenadas_acp.xlsx'), index=False)
        loadings.to_excel(os.path.join(ACP_TABLES, 'cargas_variables.xlsx'))
    except PermissionError:
        print("   ⚠️ Archivos abiertos, guardando como CSV...")
        df_pca.to_csv(os.path.join(ACP_TABLES, 'coordenadas_acp.csv'), index=False)
        loadings.to_csv(os.path.join(ACP_TABLES, 'cargas_variables.csv'))
    
    return df_pca, loadings, var_exp, pca, scaler

# ============================================================
# 6. VISUALIZACIONES MEJORADAS
# ============================================================

def grafico_scree_plot(pca):
    """Scree plot profesional"""
    var_exp = pca.explained_variance_ratio_ * 100
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    x = np.arange(1, len(var_exp) + 1)
    
    bars = ax.bar(x, var_exp, color='#1976D2', alpha=0.8, edgecolor='#0D47A1', linewidth=2)
    cumsum = np.cumsum(var_exp)
    ax.plot(x, cumsum, 'o-', color='#D32F2F', linewidth=3, markersize=10)
    
    for bar, val in zip(bars, var_exp):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
    
    for xi, yi in zip(x, cumsum):
        ax.text(xi, yi + 4, f'{yi:.1f}%', ha='center', fontsize=10, 
               color='#D32F2F', fontweight='bold')
    
    ax.set_xlabel('Componente Principal', fontsize=12, fontweight='bold')
    ax.set_ylabel('Varianza Explicada (%)', fontsize=12, fontweight='bold')
    ax.set_title('VARIANZA EXPLICADA POR COMPONENTE\nAnálisis Espacio-Temporal', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f'PC{i}' for i in x])
    ax.grid(True, alpha=0.3)
    ax.legend(['Acumulada', 'Individual'], fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '01_scree_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 01_scree_plot.png")

def grafico_biplot_mejorado(df_pca, loadings, var_exp):
    """Biplot limpio y profesional"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    
    # Puntos por año
    for año in sorted(df_pca['Año'].unique()):
        subset = df_pca[df_pca['Año'] == año]
        color = COLORES_AÑOS.get(int(año), '#666666')
        ax.scatter(subset['PC1'], subset['PC2'], c=color, label=str(int(año)),
                  s=100, alpha=0.6, edgecolors='white', linewidth=1.5)
    
    # Etiquetar top localidades
    totales = df_pca.groupby('Localidad').size().nlargest(TOP_N_LABELS)
    for loc in totales.index:
        punto = df_pca[df_pca['Localidad'] == loc].iloc[-1]
        ax.annotate(loc[:20], xy=(punto['PC1'], punto['PC2']),
                   xytext=(8, 8), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', fc='yellow', alpha=0.7, ec='orange', lw=1.5),
                   arrowprops=dict(arrowstyle='->', lw=1, color='gray'))
    
    # Vectores de regímenes
    scale = 3.5
    for i, var in enumerate(loadings.index):
        x, y = loadings.iloc[i, 0] * scale, loadings.iloc[i, 1] * scale
        ax.arrow(0, 0, x, y, head_width=0.15, head_length=0.15,
                fc='#E53935', ec='#B71C1C', linewidth=2.5, alpha=0.8, zorder=5)
        ax.text(x*1.2, y*1.2, var, fontsize=11, fontweight='bold',
               color='#B71C1C',
               bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='#E53935', lw=2, alpha=0.95))
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    ax.set_xlabel(f'PC1 ({var_exp[0]:.1f}% varianza)', fontsize=13, fontweight='bold')
    ax.set_ylabel(f'PC2 ({var_exp[1]:.1f}% varianza)', fontsize=13, fontweight='bold')
    ax.set_title('BIPLOT ESPACIO-TEMPORAL\nLocalidades y Regímenes de Afiliación',
                fontsize=15, fontweight='bold', pad=15)
    ax.legend(title='AÑO', fontsize=10, title_fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '02_biplot_profesional.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 02_biplot_profesional.png")

def grafico_trayectorias_mejorado(df_pca, var_exp):
    """Trayectorias temporales claras"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    
    # Solo localidades con 2+ años
    locs_validas = df_pca.groupby('Localidad').filter(lambda x: len(x) >= 2)['Localidad'].unique()
    locs_validas = sorted(locs_validas)[:15]  # Top 15
    
    for i, loc in enumerate(locs_validas):
        subset = df_pca[df_pca['Localidad'] == loc].sort_values('Año')
        if len(subset) < 2:
            continue
            
        color = COLORES_LOCALIDADES[i % len(COLORES_LOCALIDADES)]
        
        # Línea
        ax.plot(subset['PC1'], subset['PC2'], 'o-', color=color,
               linewidth=2, markersize=7, alpha=0.7, label=loc[:25])
        
        # Flecha final
        if len(subset) >= 2:
            x_vals, y_vals = subset['PC1'].values, subset['PC2'].values
            ax.annotate('', xy=(x_vals[-1], y_vals[-1]), xytext=(x_vals[-2], y_vals[-2]),
                       arrowprops=dict(arrowstyle='->', lw=2, color=color))
        
        # Año inicial
        ax.text(subset['PC1'].iloc[0], subset['PC2'].iloc[0],
               str(int(subset['Año'].iloc[0])), fontsize=8, ha='center',
               bbox=dict(boxstyle='circle', fc='white', ec=color, lw=1.5))
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    ax.set_xlabel(f'PC1 ({var_exp[0]:.1f}% varianza)', fontsize=13, fontweight='bold')
    ax.set_ylabel(f'PC2 ({var_exp[1]:.1f}% varianza)', fontsize=13, fontweight='bold')
    ax.set_title('TRAYECTORIAS ESPACIO-TEMPORALES\nEvolución 2021-2024 (Top 15 Localidades)',
                fontsize=15, fontweight='bold', pad=15)
    ax.legend(ncol=2, fontsize=9, loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '03_trayectorias_mejoradas.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 03_trayectorias_mejoradas.png")

def grafico_cargas_mejorado(loadings):
    """Gráfico de cargas horizontal"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='white')
    
    for i, comp in enumerate(['PC1', 'PC2']):
        cargas = loadings[comp].sort_values()
        colores = ['#D32F2F' if x < 0 else '#1976D2' for x in cargas.values]
        
        bars = axes[i].barh(range(len(cargas)), cargas.values,
                           color=colores, alpha=0.8, edgecolor='black', linewidth=1)
        
        for j, (bar, val) in enumerate(zip(bars, cargas.values)):
            x_pos = val + (0.03 if val > 0 else -0.03)
            ha = 'left' if val > 0 else 'right'
            axes[i].text(x_pos, bar.get_y() + bar.get_height()/2,
                        f'{val:.3f}', ha=ha, va='center', fontsize=10, fontweight='bold')
        
        axes[i].set_yticks(range(len(cargas)))
        axes[i].set_yticklabels(cargas.index, fontsize=11, fontweight='bold')
        axes[i].set_xlabel('Carga', fontsize=12, fontweight='bold')
        axes[i].set_title(f'Contribución en {comp}', fontsize=13, fontweight='bold')
        axes[i].axvline(0, color='black', linewidth=2)
        axes[i].grid(True, alpha=0.3, axis='x')
    
    plt.suptitle('CARGAS DE LOS REGÍMENES EN LOS COMPONENTES PRINCIPALES',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '04_cargas_regimenes.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 04_cargas_regimenes.png")

def grafico_circulo_correlacion_mejorado(loadings):
    """Círculo de correlaciones profesional"""
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='white')
    
    # Círculo unitario
    circle = plt.Circle((0, 0), 1, fill=False, color='gray', linewidth=2, linestyle='--')
    ax.add_patch(circle)
    
    # Vectores
    for i, var in enumerate(loadings.index):
        x, y = loadings.iloc[i, 0], loadings.iloc[i, 1]
        
        ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.05,
                fc='#1976D2', ec='#0D47A1', linewidth=2.5, alpha=0.8)
        
        ax.text(x*1.15, y*1.15, var, fontsize=11, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='#1976D2', lw=2))
    
    ax.axhline(0, color='black', linewidth=1.5)
    ax.axvline(0, color='black', linewidth=1.5)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel('PC1', fontsize=13, fontweight='bold')
    ax.set_ylabel('PC2', fontsize=13, fontweight='bold')
    ax.set_title('CÍRCULO DE CORRELACIONES\nRelación entre Regímenes y Componentes',
                fontsize=14, fontweight='bold', pad=15)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(ACP_DIR, '05_circulo_correlaciones.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ 05_circulo_correlaciones.png")

# ============================================================
# 7. EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta el análisis completo"""
    inicio = datetime.now()
    
    try:
        # Carga
        df, col_loc, col_afil, col_año = cargar_datos()
        
        # Preparación
        tabla_pivot = preparar_datos_acp(df, col_loc, col_afil, col_año)
        
        # ACP
        df_pca, loadings, var_exp, pca, scaler = aplicar_acp(tabla_pivot)
        
        # Visualizaciones
        print("\n" + "="*70)
        print("📊 FASE 4: GENERACIÓN DE VISUALIZACIONES")
        print("="*70)
        print()
        
        grafico_scree_plot(pca)
        grafico_biplot_mejorado(df_pca, loadings, var_exp)
        grafico_trayectorias_mejorado(df_pca, var_exp)
        grafico_cargas_mejorado(loadings)
        grafico_circulo_correlacion_mejorado(loadings)
        
        # Resumen
        duracion = (datetime.now() - inicio).total_seconds()
        
        print("\n" + "="*70)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*70)
        print(f"\n📊 Varianza explicada: {var_exp.sum():.2f}%")
        print(f"📍 Localidades analizadas: {df_pca['Localidad'].nunique()}")
        print(f"⏱️ Tiempo: {duracion:.1f} segundos")
        print(f"\n📁 Resultados en: {ACP_DIR}")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

# ============================================================
# EJECUCIÓN DIRECTA DEL SCRIPT
# ============================================================

if __name__ == "__main__":
    main()
