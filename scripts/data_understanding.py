# ============================================================
# DATA UNDERSTANDING - Proyecto NNA Bogotá (2021–2025)
# Versión extendida con análisis espacio-temporal
# ============================================================

import os # manejo de rutas y directorios.
import pandas as pd # manipulación de datos.
import numpy as np # manipulación numérica.
import hashlib # funciones hash para anonimización.
import matplotlib.pyplot as plt # visualización.
import seaborn as sns # visualización avanzada.
from dotenv import load_dotenv # carga de variables de entorno.
from datetime import datetime # manejo de fechas.
import warnings # manejo de advertencias.
import json # manejo de archivos JSON.

warnings.filterwarnings('ignore')# Ignorar advertencias innecesarias
sns.set_style("whitegrid")# Estilo de gráficos


"""
============================================================
RESUMEN EJECUTIVO DEL SCRIPT - DATA UNDERSTANDING
Proyecto: NNA Bogotá (2021-2025)
============================================================

 PROPÓSITO GENERAL:
Este script automatiza la fase de "Data Understanding" (Comprensión de Datos) 
de la metodología CRISP-DM para analizar intervenciones con Niños, Niñas y 
Adolescentes en Bogotá durante 2021-2025.

 OBJETIVOS PRINCIPALES:
1. Cargar y explorar datos de intervenciones con NNA
2. Analizar tendencias espacio-temporales por localidad
3. Identificar zonas de alerta con cambios significativos (>20%)
4. Estudiar la relación con el régimen de afiliación en salud (subsidiado)
5. Generar reportes automáticos y visualizaciones

============================================================
 ESTRUCTURA DEL SCRIPT (11 PASOS)
============================================================

1️  CONFIGURACIÓN INICIAL
   • Carga variables de entorno (.env)
   • Define rutas de entrada/salida
   • Crea estructura de carpetas automáticamente

2️  CARGA DE DATOS
   • Lee archivos Excel (.xlsx, .xls) o CSV
   • Detecta automáticamente hojas y separadores
   • Muestra dimensiones del dataset

3️  LIMPIEZA Y NORMALIZACIÓN
   • Estandariza nombres de columnas (mayúsculas, sin espacios)
   • Verifica anonimización (elimina datos personales si existen)
   • Guarda mapeo de nombres originales → normalizados

4️  DETECCIÓN TEMPORAL
   • Identifica columnas de fecha/año
   • Extrae año de fechas automáticamente
   • Detecta rango temporal disponible (2021-2025)

5️  DICCIONARIO DE DATOS
   • Documenta todas las variables del dataset
   • Clasifica por tipo: numéricas, categóricas, identificadores, etc.
   • Calcula: nulos, únicos, cardinalidad, primer valor
   • Exporta a Excel y CSV

6️  VERIFICACIÓN DE CALIDAD
   • Detecta duplicados completos
   • Identifica columnas constantes o casi vacías (>90% nulos)
   • Encuentra columnas con alta cardinalidad
   • Calcula métricas: % nulos, memoria usada
   • Genera reporte JSON de calidad

7️ ANÁLISIS EXPLORATORIO
   • Frecuencias de variables categóricas (Top 20)
   • Estadísticas descriptivas de numéricas
   • Genera gráficos de barras e histogramas
   • Limita a primeras 15 categóricas y 10 numéricas
8️  ANÁLISIS ESPACIO-TEMPORAL  (NUEVO - Objetivo principal)
   • Agrupa intervenciones por localidad y año
   • Calcula tendencias: aumento/disminución por localidad
   • Identifica zonas de alerta con cambios >20%
   • Genera:
     - Tabla pivote localidad × año
     - Gráfico de evolución temporal (Top 10 localidades)
     - Mapa de calor de intervenciones

9️  ANÁLISIS RÉGIMEN DE SALUD (NUEVO - Objetivo específico 3)
   • Distribuye intervenciones por tipo de afiliación (subsidiado, contributivo)
   • Cruza localidad × régimen de salud (porcentajes)
   • Identifica Top 10 localidades con mayor % subsidiado
   • Genera gráficos:
     - Distribución general de regímenes
     - Barras apiladas por localidad

10 CRUCES DE VARIABLES
   • Localidad × Tipo de intervención
   • Año × Tipo de intervención
   • Motivo × Servicio (si existen)
   • Exporta matrices y mapas de calor

10.1 VISUALIZACIONES GENERALES
   • Valores faltantes (Top 20)
   • Matriz de correlación de variables numéricas

1️0.2 DOCUMENTACIÓN MARKDOWN
   • Genera reporte completo siguiendo CRISP-DM:
     - 2.1 Collect Initial Data
     - 2.2 Describe Data
     - 2.3 Explore Data
     - 2.4 Verify Data Quality
   • Incluye tablas de zonas de alerta
   • Lista archivos generados

============================================================
 ARCHIVOS DE SALIDA GENERADOS
============================================================

 reports/tables/
├── diccionario_datos.xlsx        # Documentación completa de variables
├── column_mapping.json            # Mapeo de nombres originales
├── quality_report.json            # Reporte de calidad JSON
├── quality_summary.csv            # Resumen de calidad CSV
├── distribucion_localidad_año.csv # Datos espacio-temporales
├── matriz_localidad_año.xlsx     # Tabla pivote
├── tendencias_por_localidad.xlsx # Cambios y tendencias
├── zonas_alerta.csv              #  Localidades con cambios >20%
├── distribucion_regimen_salud.csv
├── regimen_por_localidad_porcentaje.xlsx
├── top_localidades_subsidiado.csv
├── cruce_localidad_tipo_intervencion.xlsx
├── cruce_año_tipo_intervencion.xlsx
├── estadisticas_numericas.xlsx
└── frecuencia_*.csv (múltiples)  # Frecuencias por variable

 reports/figures/temporal/
└── evolucion_temporal_top10.png  # Serie temporal por localidad

 reports/figures/spatial/
├── heatmap_localidad_año.png     # Mapa de calor
├── top_subsidiado_localidades.png
└── regimen_por_localidad_stacked.png

 reports/figures/exploratory/
├── missing_values.png             # Valores faltantes
├── correlation_matrix.png         # Correlaciones
├── distribucion_regimen.png
├── cruce_localidad_tipo.png
├── dist_*.png (múltiples)        # Distribuciones categóricas
└── hist_*.png (múltiples)        # Histogramas numéricas

 reports/
└── data_summary.md                #  Reporte Markdown completo

============================================================
 FUNCIONES PRINCIPALES
============================================================

load_data()              → Carga Excel/CSV con detección automática
clean_columns()          → Normaliza nombres de columnas
anonymize()              → Verifica y elimina datos personales
detect_temporal_columns()→ Detecta y extrae variables temporales
generate_dictionary()    → Genera diccionario de datos
clasificar_variable()    → Clasifica variables por tipo
verify_quality()         → Verifica calidad del dataset
exploratory_analysis()   → EDA de categóricas y numéricas
analyze_spatiotemporal() → Análisis espacio-temporal (CORE)
analyze_health_regime()  → Análisis régimen subsidiado
cross_analysis()         → Cruces de variables clave
plot_missing()           → Gráfico de valores faltantes
plot_correlation()       → Matriz de correlación
generate_summary_md()    → Genera reporte Markdown
main()                   → Flujo principal (orquestador)

============================================================
 CONFIGURACIÓN REQUERIDA
============================================================

1. Archivo .env con:
   DATA_FILE=data/raw/base_datos_completa_NNA_TI_anon.xlsx

2. Librerías necesarias:
   - pandas, numpy (manipulación de datos)
   - matplotlib, seaborn (visualización)
   - python-dotenv (variables de entorno)
   - openpyxl (lectura/escritura Excel)

3. Estructura de carpetas (se crea automáticamente):
   - data/raw/ (entrada)
   - reports/tables/ (tablas)
   - reports/figures/ (gráficos)

============================================================
 CARACTERÍSTICAS ESPECIALES
============================================================

Detección automática de formatos (Excel/CSV)
Manejo de datos ya anonimizados (no re-encripta)
Clasificación inteligente de variables
Identificación automática de zonas de alerta
Análisis temporal con detección de tendencias
Cruces automáticos de variables relacionadas
Exportación múltiple (Excel, CSV, JSON, PNG, MD)
Reportes siguiendo metodología CRISP-DM
Manejo robusto de errores
Log completo en consola

============================================================
 INDICADORES CLAVE CALCULADOS
============================================================

- Cambio absoluto: diferencia entre año final e inicial
- Cambio porcentual: ((final - inicial) / (inicial + 1)) * 100
- Tendencia: clasificación cualitativa del cambio
  - Aumento fuerte: >20%
  - Aumento moderado: 5-20%
  - Estable: -5% a 5%
  - Disminución moderada: -20% a -5%
  - Disminución fuerte: <-20%

- Zonas de alerta: localidades con |cambio| > 20%

============================================================
 RESPONDE A LOS OBJETIVOS DEL PROYECTO
============================================================

Objetivo 1:  Describir distribución por localidad y año
Objetivo 2:  Identificar localidades con aumento/disminución
Objetivo 3:  Relacionar con régimen de afiliación (subsidiado)

Preguntas guía:
 ¿Dónde aumentaron/disminuyeron las intervenciones?
 ¿Qué características tienen las localidades con mayor crecimiento?
 ¿Existe relación entre intervenciones y régimen subsidiado?


============================================================
 AUTOR Y VERSIÓN
============================================================

Proyecto: Análisis NNA Bogotá (2021-2025)
Metodología: CRISP-DM
Fase: Data Understanding
Versión: 2.0 (con análisis espacio-temporal).Karen Suarez
Fecha: Octubre 2025

============================================================
"""

# ============================================================
# 1. CONFIGURACIÓN DE RUTAS
# ============================================================

load_dotenv() # Cargar variables de entorno desde .env

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # Directorio base del proyecto
DATA_FILE = os.getenv("DATA_FILE")# Ruta del archivo de datos desde .env

if not DATA_FILE: # Verificar que la variable exista
    raise ValueError(" No se encontró la variable DATA_FILE en el archivo .env") #  Error si no existe

file_path = os.path.join(BASE_DIR, DATA_FILE)# Ruta completa del archivo de datos

if not os.path.exists(file_path):# Verificar que el archivo exista
    raise FileNotFoundError(f"❌ No se encontró el archivo: {file_path}")# Error si no existe

# Estructura de carpetas
REPORTS_DIR = os.path.join(BASE_DIR, "reports")# Carpeta principal de reportes
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")# Carpeta de figuras
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")# Carpeta de tablas
TEMPORAL_DIR = os.path.join(FIGURES_DIR, "temporal")# Carpeta de figuras temporales
SPATIAL_DIR = os.path.join(FIGURES_DIR, "spatial")# Carpeta de figuras espaciales
EXPLORATORY_DIR = os.path.join(FIGURES_DIR, "exploratory")# Carpeta de figuras exploratorias
SUMMARY_FILE = os.path.join(REPORTS_DIR, "data_summary.md")# Resumen en Markdown
ALERT_ZONES_FILE = os.path.join(TABLES_DIR, "zonas_alerta.csv")# Zonas de alerta

for path in [REPORTS_DIR, FIGURES_DIR, TABLES_DIR, TEMPORAL_DIR, SPATIAL_DIR, EXPLORATORY_DIR]:# Crear carpetas si no existen
    os.makedirs(path, exist_ok=True)# Crear carpetas si no existen

print(f" Estructura de carpetas creada en: {REPORTS_DIR}")    


# ============================================================
# 2. CARGA DE DATOS CON DETECCIÓN AUTOMÁTICA
# ============================================================

def load_data(file_path):
    """Carga datos desde Excel o CSV con detección automática""" # Carga datos desde Excel o CSV con detección automática
    ext = os.path.splitext(file_path)[-1].lower() # Extensión del archivo
    
    print(f" Cargando archivo: {os.path.basename(file_path)}") # Cargando archivo
    
    if ext in ['.xlsx', '.xls']:# Archivo Excel
        xls = pd.ExcelFile(file_path)# Cargar archivo Excel
        print(f"   Hojas disponibles: {xls.sheet_names}")# Listar hojas disponibles
        sheet = 'BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1]# Seleccionar hoja 'BD' 
        df = pd.read_excel(file_path, sheet_name=sheet)# Cargar hoja seleccionada
        print(f"   ✓ Cargada hoja: {sheet}")# Confirmar hoja cargada
    elif ext == '.csv':
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')# Cargar CSV con detección automática de separador
        print(f"   ✓ CSV cargado con detección automática de separador")# Confirmar carga CSV
    else:
        raise ValueError("❌ Formato no compatible. Usa .csv, .xlsx o .xls")# Error si formato no compatible
    
    print(f"✅ Datos cargados: {df.shape[0]:,} filas × {df.shape[1]} columnas")# Confirmar dimensiones
    return df# Retornar DataFrame


# ============================================================
# 3. LIMPIEZA Y NORMALIZACIÓN
# ============================================================

def clean_columns(df):
    """Limpia y normaliza nombres de columnas"""
    original_cols = df.columns.tolist()# Guardar nombres originales de columnas 
    
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
        .str.upper()
    )# Normalizar nombres de columnas 
    
    col_mapping = dict(zip(original_cols, df.columns))# Mapeo de nombres originales a normalizados
    with open(os.path.join(TABLES_DIR, "column_mapping.json"), "w", encoding="utf-8") as f: # Guardar mapeo en JSON 
        json.dump(col_mapping, f, indent=2, ensure_ascii=False) # Guardar mapeo en JSON 
    
    print(f" Columnas normalizadas: {len(df.columns)} variables")# Confirmar normalización
    return df # Retornar DataFrame


def anonymize(df):
    """Anonimiza datos personales mediante hash irreversible"""
    import hashlib
    
    sensitive_cols = {
        'telefono': ['TELÉFONO', 'TELEFONO', 'TEL'],
        'correo': ['CORREO', 'EMAIL', 'MAIL'],
        'direccion': ['DIRECCIÓN', 'DIRECCION', 'DIR'],
        'nombre_eapb': ['NOMBRE_EAPB', 'EAPB'],
        'barrio': ['BARRIO', 'VEREDA']  # Solo si es muy específico
    }
    
    def hash_value(value):
        """Genera hash SHA256 irreversible"""
        if pd.isna(value) or value == '99999':
            return value
        return hashlib.sha256(str(value).encode()).hexdigest()[:16]
    
    anonimizadas = []
    
    for categoria, keywords in sensitive_cols.items():
        for col in df.columns:
            if any(kw in col.upper() for kw in keywords):
                if col in df.columns:
                    df[col] = df[col].apply(hash_value)
                    anonimizadas.append(col)
                    print(f"   ✓ Anonimizada: {col}")
    
    # ELIMINAR columnas de acudiente si existen
    acudiente_cols = [c for c in df.columns if 'ACUDIENTE' in c.upper() and 'NOMBRE' in c.upper()]
    if acudiente_cols:
        df.drop(columns=acudiente_cols, inplace=True)
        print(f"    Eliminadas: {acudiente_cols}")
    
    print(f"\n Anonimización completada: {len(anonimizadas)} columnas procesadas")
    return df


# ============================================================
# 4. DETECCIÓN AUTOMÁTICA DE VARIABLES TEMPORALES
# ============================================================

def detect_temporal_columns(df): 
    """Detecta y procesa columnas de fecha/año (sin tratar 99999 como fecha)."""
    temporal_info = {}
    date_candidates = [c for c in df.columns if any(x in c.upper() for x in ['FECHA', 'DATE', 'AÑO', 'ANO', 'YEAR', 'MES', 'MONTH'])]

    for col in date_candidates:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            temporal_info[col] = 'datetime'
        elif df[col].dtype == 'object':
            try:
                # No intentar convertir valores tipo '99999'
                df[col] = pd.to_datetime(df[col].replace('99999', np.nan), errors='coerce')
                temporal_info[col] = 'datetime_converted'
            except:
                pass

    # Extraer año si hay columnas de fecha válidas
    for col in temporal_info.keys():
        if 'AÑO' not in df.columns and 'YEAR' not in df.columns:
            df['AÑO'] = df[col].dt.year
            print(f"   ✓ Columna 'AÑO' extraída de {col}")

    # Validar rango de años 2021–2025
    if 'AÑO' in df.columns:
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce')
        df.loc[(df['AÑO'] < 2021) | (df['AÑO'] > 2025), 'AÑO'] = np.nan
        years = df['AÑO'].dropna().unique()
        print(f" Años detectados válidos: {sorted([int(y) for y in years])}")
        temporal_info['years_available'] = sorted([int(y) for y in years])
    else:
        print("  No se detectó columna de año válida")

    return df, temporal_info


# ============================================================
# 5. DICCIONARIO DE DATOS AMPLIADO (Versión ajustada a NNA)
# ============================================================

def clasificar_variable(row, total_rows):
    """
    Clasifica una variable según su tipo y cardinalidad.
    """
    tipo = str(row['Tipo_dato']).lower()
    cardinalidad = row['Cardinalidad']
    n_unicos = row['Valores_únicos']
    nombre = str(row['Variable']).upper()

    # Identificadores típicos
    if 'ID' in nombre or 'IDENTIFICADOR' in nombre or 'DOCUMENTO' in nombre:
        return 'Identificador'
    # Fechas
    if 'FECHA' in nombre or 'DATE' in nombre or 'AÑO' in nombre or 'YEAR' in nombre or 'MES' in nombre or 'MONTH' in nombre:
        return 'Temporal'
    # Numéricas
    if tipo in ['int64', 'float64', 'int32', 'float32']:
        if n_unicos < 10:
            return 'Numérica discreta'
        else:
            return 'Numérica continua'
    # Categóricas
    if tipo in ['object', 'category']:
        if n_unicos < 30:
            return 'Categórica'
        elif cardinalidad > 80:
            return 'Texto libre / alta cardinalidad'
        else:
            return 'Categórica'
    # Booleanas
    if tipo in ['bool']:
        return 'Booleana'
    return 'Otro'

def generate_dictionary(df):
    """Genera diccionario completo de datos sin tratar '99999' como nulo."""

    # --- Solo cuentan como nulos los valores verdaderamente faltantes ---
    def contar_nulos_reales(col):
        """Cuenta únicamente los NaN reales."""
        return col.isna().sum()

    # --- Limpieza del primer valor mostrado ---
    def limpiar_valor(v):
        """Devuelve None solo si es NaN, deja '99999' tal cual."""
        if pd.isna(v):
            return None
        return str(v).strip()

    # --- Calcular nulos y estadísticas básicas ---
    valores_nulos = [contar_nulos_reales(df[col]) for col in df.columns]

    dic = pd.DataFrame({
        "Variable": df.columns,
        "Tipo_dato": df.dtypes.values,
        "Valores_nulos": valores_nulos,
        "Porcentaje_nulos": (np.array(valores_nulos) / len(df) * 100).round(2),
        "Valores_únicos": df.nunique().values,
        "Cardinalidad": (df.nunique().values / len(df) * 100).round(2),
        "Primer_valor": [limpiar_valor(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else None for col in df.columns]
    })

    # Clasificación de variables
    dic['Clasificación'] = dic.apply(lambda row: clasificar_variable(row, len(df)), axis=1)

    # Guardar resultados
    dic.to_excel(os.path.join(TABLES_DIR, "diccionario_datos.xlsx"), index=False)
    dic.to_csv(os.path.join(TABLES_DIR, "diccionario_datos.csv"), index=False)

    print(f"📘 Diccionario de datos generado correctamente ({len(dic)} variables).")
    print("   '99999' se considera un valor válido (No Aplica), no un dato faltante.")
    return dic


# ============================================================
# 6. VERIFICACIÓN DE CALIDAD DE DATOS
# ============================================================

# ============================================================
# 6. VERIFICACIÓN DE CALIDAD DE DATOS (versión sin excluir “99999”)
# ============================================================

def verify_quality(df):
    """Análisis exhaustivo de calidad de datos sin tratar '99999' como nulo,
    y genera reportes separados para valores nulos y valores '99999'."""
    
    df_check = df.copy()

    def es_nulo_real(x):
        return pd.isna(x)

    # --- Métricas generales ---
    total_filas = len(df_check)
    total_columnas = df_check.shape[1]
    filas_duplicadas = df_check.duplicated().sum()
    porcentaje_duplicados = round((filas_duplicadas / total_filas) * 100, 2)
    promedio_nulos = round(
        np.mean([col.map(es_nulo_real).mean() for _, col in df_check.items()]) * 100, 2
    )
    columnas_constantes = len([c for c in df_check.columns if df_check[c].nunique() == 1])
    columnas_casi_vacias = len(
        [c for c in df_check.columns if df_check[c].map(es_nulo_real).mean() > 0.9]
    )
    memoria_mb = round(df_check.memory_usage(deep=True).sum() / 1024**2, 2)

    # --- Columnas problemáticas ---
    problematic = []
    for col in df_check.columns:
        issues = []
        if df_check[col].nunique() == 1:
            issues.append("constante")
        if df_check[col].map(es_nulo_real).mean() > 0.9:
            issues.append("casi_vacía")
        if df_check[col].nunique() > len(df_check) * 0.95 and df_check[col].dtype == 'object':
            issues.append("alta_cardinalidad")
        if issues:
            problematic.append({"columna": col, "problemas": issues})

    # --- 🔹 NUEVO: reporte de nulos reales ---
    nulos_df = pd.DataFrame({
        "Variable": df_check.columns,
        "Valores_nulos_reales": [df_check[c].isna().sum() for c in df_check.columns],
        "Porcentaje_nulos_reales": [
            (df_check[c].isna().sum() / total_filas * 100).round(2) for c in df_check.columns
        ]
    })
    nulos_df = nulos_df[nulos_df["Valores_nulos_reales"] > 0]
    nulos_path = os.path.join(TABLES_DIR, "reporte_nulos.xlsx")
    nulos_df.to_excel(nulos_path, index=False)

    # --- 🔹 NUEVO: reporte de valores '99999' ---
    rep_99999 = pd.DataFrame({
        "Variable": df_check.columns,
        "Cantidad_99999": [(df_check[c] == 99999).sum() + (df_check[c] == '99999').sum() for c in df_check.columns],
        "Porcentaje_99999": [
            (((df_check[c] == 99999).sum() + (df_check[c] == '99999').sum()) / total_filas * 100).round(2)
            for c in df_check.columns
        ]
    })
    rep_99999 = rep_99999[rep_99999["Cantidad_99999"] > 0]
    rep_99999_path = os.path.join(TABLES_DIR, "reporte_99999.xlsx")
    rep_99999.to_excel(rep_99999_path, index=False)

    # --- Guardar resumen general ---
    quality = {
        "total_filas": int(total_filas),
        "total_columnas": int(total_columnas),
        "filas_duplicadas": int(filas_duplicadas),
        "porcentaje_duplicados": float(porcentaje_duplicados),
        "promedio_nulos": float(promedio_nulos),
        "columnas_constantes": int(columnas_constantes),
        "columnas_casi_vacias": int(columnas_casi_vacias),
        "memoria_mb": float(memoria_mb),
        "columnas_problemáticas": problematic
    }

    with open(os.path.join(TABLES_DIR, "quality_report.json"), "w", encoding="utf-8") as f:
        json.dump(quality, f, indent=2, ensure_ascii=False)

    pd.Series({k: v for k, v in quality.items() if not isinstance(v, list)}).to_csv(
        os.path.join(TABLES_DIR, "quality_summary.csv")
    )

    print(f" Calidad verificada: {quality['filas_duplicadas']} duplicados, {quality['columnas_constantes']} columnas constantes")
    print("   Nota: los valores '99999' se mantienen como válidos (no se cuentan como nulos).")
    print(f"   Se generaron archivos:\n    • {nulos_path}\n    • {rep_99999_path}")
    return quality


# ============================================================
# 7. ANÁLISIS EXPLORATORIO AMPLIADO
# ============================================================

def exploratory_analysis(df, dic):
    """Análisis exploratorio completo de todas las variables"""
    print("\n Iniciando análisis exploratorio ampliado...") # Iniciando análisis exploratorio ampliado
    
    cat_vars = dic[dic['Clasificación'].str.contains('Categórica', na=False)]['Variable'].tolist() # Variables categóricas
    
    for var in cat_vars[:15]:
        if var in df.columns:
            freq = df[var].value_counts().head(20) # Frecuencia de valores
            freq.to_csv(os.path.join(TABLES_DIR, f"frecuencia_{var}.csv")) # Guardar frecuencia en CSV
            
            if len(freq) > 0:
                plt.figure(figsize=(10, 6)) # Gráfico de barras horizontales
                freq.plot(kind='barh', color='steelblue') # Gráfico de barras horizontales
                plt.title(f"Distribución de {var}")# Título del gráfico
                plt.xlabel("Frecuencia")# Etiqueta del eje X
                plt.tight_layout()# Ajuste del diseño
                plt.savefig(os.path.join(EXPLORATORY_DIR, f"dist_{var}.png"), dpi=150) # Guardar figura
                plt.close() # Cerrar figura
    
    num_vars = df.select_dtypes(include=[np.number]).columns.tolist() # Variables numéricas
    if num_vars:
        stats = df[num_vars].describe().T # Estadísticas descriptivas
        stats.to_excel(os.path.join(TABLES_DIR, "estadisticas_numericas.xlsx")) # Guardar estadísticas en Excel
        
        for var in num_vars[:10]:# Limitar a las primeras 10 variables numéricas
            if df[var].notna().sum() > 0:# Solo si hay datos no nulos
                plt.figure(figsize=(8, 5))# Histograma
                df[var].hist(bins=30, color='coral', edgecolor='black')# Histograma
                plt.title(f"Distribución de {var}")# Título del gráfico
                plt.xlabel(var)# Etiqueta del eje X
                plt.ylabel("Frecuencia")# Etiqueta del eje Y
                plt.tight_layout() # Ajuste del diseño
                plt.savefig(os.path.join(EXPLORATORY_DIR, f"hist_{var}.png"), dpi=150)# Guardar figura
                plt.close() # Cerrar figura
    
    print(f" Análisis exploratorio: {len(cat_vars)} categóricas, {len(num_vars)} numéricas") # Resumen del análisis

# ============================================================
# 8. ANÁLISIS ESPACIO-TEMPORAL (robusto y mantiene 99999)
# ============================================================

def analyze_spatiotemporal(df):
    """Análisis espacial y temporal según objetivos del proyecto"""
    print("\n Iniciando análisis espacio-temporal...")

    results = {}

    # Buscar columna de localidad
    loc_col = next((c for c in df.columns if 'LOCALIDAD' in c), None)
    if not loc_col:
        print("  ⚠️ No se encontró columna de localidad.")
        return results

    # Verificar que exista columna de año
    if 'AÑO' not in df.columns:
        print("  ⚠️ No se encontró columna de año para análisis temporal.")
        return results

    # Asegurar que el año sea numérico
    df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce')

    # Eliminar filas sin año válido (manteniendo los 99999)
    df_temp = df[df['AÑO'].notna()].copy()
    if df_temp.empty:
        print("  ⚠️ No hay registros con año válido para analizar.")
        return results

    # Agrupar intervenciones por localidad y año
    distribucion = (
        df_temp.groupby([loc_col, 'AÑO'])
        .size()
        .reset_index(name='Intervenciones')
    )

    if distribucion.empty:
        print("  ⚠️ No se encontraron combinaciones válidas de localidad y año.")
        return results

    distribucion.to_csv(os.path.join(TABLES_DIR, "distribucion_localidad_año.csv"), index=False)

    # Tabla pivote (localidad × año)
    pivot = distribucion.pivot(index=loc_col, columns='AÑO', values='Intervenciones').fillna(0)
    pivot.to_excel(os.path.join(TABLES_DIR, "matriz_localidad_año.xlsx"))

    # Calcular totales y promedios
    pivot['Total'] = pivot.sum(axis=1)
    años_disponibles = [c for c in pivot.columns if isinstance(c, (int, float, np.integer, np.floating))]
    pivot['Promedio_anual'] = pivot['Total'] / max(1, len(años_disponibles))

    # Calcular cambios solo si hay al menos 2 años
    if len(años_disponibles) >= 2:
        año_ini = int(min(años_disponibles))
        año_fin = int(max(años_disponibles))

        pivot['Cambio_absoluto'] = pivot[año_fin] - pivot[año_ini]
        pivot['Cambio_porcentual'] = ((pivot[año_fin] - pivot[año_ini]) /
                                      (pivot[año_ini] + 1) * 100).round(2)

        pivot['Tendencia'] = pivot['Cambio_porcentual'].apply(
            lambda x: 'Aumento fuerte' if x > 20 else
                      ('Aumento moderado' if x > 5 else
                       ('Estable' if x > -5 else
                        ('Disminución moderada' if x > -20 else 'Disminución fuerte')))
        )

        pivot.to_excel(os.path.join(TABLES_DIR, "tendencias_por_localidad.xlsx"))

        # Identificar zonas de alerta
        alertas = pivot[abs(pivot['Cambio_porcentual']) > 20].sort_values('Cambio_porcentual', ascending=False)
        alertas.to_csv(ALERT_ZONES_FILE)
        print(f"    {len(alertas)} zonas de alerta identificadas")
        results['zonas_alerta'] = alertas
    else:
        print("  ⚠️ No hay suficientes años distintos para calcular tendencias.")

    # Gráfico de evolución temporal (solo si hay datos)
    top_localidades = pivot.nlargest(10, 'Total').index
    if años_disponibles and len(top_localidades) > 0:
        plt.figure(figsize=(14, 8))
        for loc in top_localidades:
            valores = pivot.loc[loc, años_disponibles]
            plt.plot(años_disponibles, valores, marker='o', label=loc, linewidth=2)

        plt.title("Evolución temporal de intervenciones - Top 10 localidades", fontsize=14, fontweight='bold')
        plt.xlabel("Año", fontsize=12)
        plt.ylabel("Número de intervenciones", fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(TEMPORAL_DIR, "evolucion_temporal_top10.png"), dpi=150, bbox_inches='tight')
        plt.close()

    # Gráfico de mapa de calor
    if años_disponibles and not pivot[años_disponibles].empty:
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            pivot[años_disponibles].head(15),
            annot=True, fmt='.0f', cmap='YlOrRd',
            cbar_kws={'label': 'Intervenciones'}
        )
        plt.title("Mapa de calor: Intervenciones por localidad y año", fontsize=14, fontweight='bold')
        plt.ylabel("Localidad", fontsize=12)
        plt.xlabel("Año", fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(SPATIAL_DIR, "heatmap_localidad_año.png"), dpi=150)
        plt.close()
    else:
        print("  ⚠️ No se generó el mapa de calor (sin datos válidos para graficar).")

    print(" Análisis espacio-temporal completado")
    results['distribucion'] = distribucion
    results['pivot'] = pivot

    return results


# ============================================================
# 9. ANÁLISIS DE RÉGIMEN SUBSIDIADO (NUEVO)
# ============================================================

def analyze_health_regime(df):
    """Análisis del régimen de salud (Objetivo específico 3)"""
    print("\n Analizando régimen de afiliación en salud...")# Analizando régimen de afiliación en salud
    
    afiliacion_col = None
    for col in df.columns:
        if 'AFILIACIÓN' in col or 'AFILIACION' in col or 'SGSSS' in col or 'REGIMEN' in col: # Buscar columna relacionada
            afiliacion_col = col
            break # Detener búsqueda al encontrar la primera coincidencia
    
    if not afiliacion_col:
        print(" No se encontró columna de régimen de salud") # Advertencia si no se encuentra
        return {} # Retornar resultados vacíos
    
    regimen_dist = df[afiliacion_col].value_counts() # Distribución del régimen de salud
    regimen_dist.to_csv(os.path.join(TABLES_DIR, "distribucion_regimen_salud.csv")) # Guardar distribución en CSV
    
    plt.figure(figsize=(10, 6)) # Gráfico de barras del régimen de salud
    regimen_dist.plot(kind='bar', color=['#2ecc71', '#e74c3c', '#3498db', '#95a5a6'])# Gráfico de barras del régimen de salud
    plt.title("Distribución por régimen de afiliación en salud", fontsize=14, fontweight='bold') # Título del gráfico
    plt.xlabel("Tipo de régimen", fontsize=12)
    plt.ylabel("Número de intervenciones", fontsize=12)
    plt.xticks(rotation=45, ha='right')# Rotar etiquetas del eje X
    plt.tight_layout()# Ajuste del diseño
    plt.savefig(os.path.join(EXPLORATORY_DIR, "distribucion_regimen.png"), dpi=150) # Guardar figura
    plt.close() # Cerrar figura
    
    loc_col = next((c for c in df.columns if 'LOCALIDAD' in c), None) # Columna de localidad
    
    if loc_col:
        cruce = pd.crosstab(df[loc_col], df[afiliacion_col], normalize='index') * 100 # Porcentaje por localidad
        cruce.to_excel(os.path.join(TABLES_DIR, "regimen_por_localidad_porcentaje.xlsx")) # Guardar cruce en Excel
        
        if 'SUBSIDIADO' in cruce.columns or any('SUBSID' in str(col) for col in cruce.columns):# Buscar columna relacionada con subsidiado
            subsid_col = next((c for c in cruce.columns if 'SUBSID' in str(c)), None) # Columna de subsidiado
            if subsid_col:
                top_subsidiado = cruce[subsid_col].sort_values(ascending=False).head(10) # Top 10 localidades con mayor % subsidiado
                top_subsidiado.to_csv(os.path.join(TABLES_DIR, "top_localidades_subsidiado.csv"))
                
                plt.figure(figsize=(10, 7))# Gráfico de barras horizontales para top 10 subsidiado
                top_subsidiado.plot(kind='barh', color='#e67e22')# Gráfico de barras horizontales para top 10 subsidiado
                plt.title("Top 10 localidades con mayor % régimen subsidiado", fontsize=14, fontweight='bold')# Título del gráfico
                plt.xlabel("Porcentaje (%)", fontsize=12)
                plt.ylabel("Localidad", fontsize=12)
                plt.tight_layout()# Ajuste del diseño
                plt.savefig(os.path.join(SPATIAL_DIR, "top_subsidiado_localidades.png"), dpi=150)# Guardar figura
                plt.close()# Cerrar figura
        
        plt.figure(figsize=(14, 8))# Gráfico de barras apiladas por localidad
        cruce.head(15).plot(kind='barh', stacked=True, colormap='Set3', figsize=(14, 8))# Gráfico de barras apiladas por localidad
        plt.title("Composición de régimen de salud por localidad (Top 15)", fontsize=14, fontweight='bold')# Título del gráfico
        plt.xlabel("Porcentaje (%)", fontsize=12)
        plt.ylabel("Localidad", fontsize=12)
        plt.legend(title='Régimen', bbox_to_anchor=(1.05, 1), loc='upper left') # Leyenda fuera del gráfico
        plt.tight_layout()
        plt.savefig(os.path.join(SPATIAL_DIR, "regimen_por_localidad_stacked.png"), dpi=150, bbox_inches='tight')# Guardar figura
        plt.close()# Cerrar figura
    
    print(" Análisis de régimen de salud completado")# Confirmar finalización
    return {'distribucion': regimen_dist}# Retornar resultados


# ============================================================
# 10. CRUCES DE VARIABLES CLAVE
# ============================================================

def cross_analysis(df):
    """Análisis de cruces entre variables importantes"""
    print("\n🔗 Generando cruces de variables...")
    
    loc_col = next((c for c in df.columns if 'LOCALIDAD' in c), None)# Columna de localidad
    tipo_col = next((c for c in df.columns if 'TIPO' in c and 'INTERVENCION' in c), None)# Columna de tipo de intervención
    motivo_col = next((c for c in df.columns if 'MOTIVO' in c), None)# Columna de motivo
    servicio_col = next((c for c in df.columns if 'SERVICIO' in c), None)# Columna de servicio
    
    cruces_generados = 0 # Contador de cruces generados
    
    if loc_col and tipo_col:# Cruce localidad × tipo de intervención
        cruce = pd.crosstab(df[loc_col], df[tipo_col])# Cruce localidad × tipo de intervención
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_localidad_tipo_intervencion.xlsx"))# Guardar cruce en Excel
        cruces_generados += 1# Incrementar contador
        
        plt.figure(figsize=(12, 8))# Mapa de calor del cruce
        sns.heatmap(cruce.head(15), annot=True, fmt='d', cmap='Blues')# Mapa de calor del cruce
        plt.title("Cruce: Localidad × Tipo de intervención", fontsize=14, fontweight='bold')# Título del gráfico
        plt.tight_layout()# Ajuste del diseño
        plt.savefig(os.path.join(EXPLORATORY_DIR, "cruce_localidad_tipo.png"), dpi=150)# Guardar figura
        plt.close()
    
    if motivo_col and servicio_col:
        cruce = pd.crosstab(df[motivo_col], df[servicio_col])# Cruce motivo × servicio
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_motivo_servicio.xlsx"))# Guardar cruce en Excel
        cruces_generados += 1# Incrementar contador
    
    if 'AÑO' in df.columns and tipo_col:# Cruce año × tipo de intervención
        cruce = pd.crosstab(df['AÑO'], df[tipo_col])# Cruce año × tipo de intervención
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_año_tipo_intervencion.xlsx"))# Guardar cruce en Excel
        cruces_generados += 1
    
    print(f" {cruces_generados} cruces de variables generados")# Confirmar número de cruces generados


# ============================================================
# 11. VISUALIZACIONES GENERALES
# ============================================================

def plot_missing(df):
    """Gráfico de valores faltantes"""# Gráfico de valores faltantes
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False).head(20)# Top 20 variables con más nulos
    
    if len(missing) > 0:# Solo si hay variables con nulos
        plt.figure(figsize=(10, 8))# Gráfico de barras horizontales
        sns.barplot(x=missing.values, y=missing.index, palette='Reds_r')# Gráfico de barras horizontales
        plt.title("Porcentaje de valores faltantes (Top 20)", fontsize=14, fontweight='bold')# Título del gráfico
        plt.xlabel("Porcentaje (%)", fontsize=12)# Etiqueta del eje X
        plt.ylabel("Variable", fontsize=12)# Etiqueta del eje Y
        plt.tight_layout()
        plt.savefig(os.path.join(EXPLORATORY_DIR, "missing_values.png"), dpi=150)# Guardar figura
        plt.close()# Cerrar figura


def plot_correlation(df):
    """Matriz de correlación de variables numéricas"""
    numeric_df = df.select_dtypes(include=[np.number])# DataFrame solo con variables numéricas
    
    if numeric_df.shape[1] > 1:# Solo si hay más de una variable numérica
        corr = numeric_df.corr()# Matriz de correlación
        
        plt.figure(figsize=(12, 10))# Gráfico de mapa de calor
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})# Gráfico de mapa de calor
        plt.title("Matriz de correlación - Variables numéricas", fontsize=14, fontweight='bold')# Título del gráfico
        plt.tight_layout()# Ajuste del diseño
        plt.savefig(os.path.join(EXPLORATORY_DIR, "correlation_matrix.png"), dpi=150)# Guardar figura
        plt.close()


# ============================================================
# 12. DOCUMENTACIÓN MARKDOWN COMPLETA
# ============================================================

def generate_summary_md(df, quality, dic, temporal_info, spatial_results):
    """Genera reporte completo en Markdown"""
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:# Abrir archivo Markdown para escribir
        f.write("# 📊 Data Understanding - Proyecto NNA Bogotá (2021-2025)\n\n")
        f.write(f"**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")# Fecha de generación
        f.write("---\n\n")# Separador
        
        f.write("## 2.1. Collect Initial Data\n\n")# Sección de recopilación de datos
        f.write("La base de datos contiene registros de intervenciones con niños, niñas y adolescentes (NNA) ")# Descripción del dataset
        f.write("en las localidades de Bogotá durante el período 2021-2025.\n\n")# Descripción del dataset
        f.write(f"- **Archivo origen:** `{os.path.basename(file_path)}`\n")# Archivo origen
        f.write(f"- **Filas:** {quality['total_filas']:,}\n")# Filas
        f.write(f"- **Columnas:** {quality['total_columnas']}\n")# Columnas
        f.write(f"- **Tamaño:** {quality['memoria_mb']} MB\n\n")# Tamaño
        
        if temporal_info.get('years_available'):# Años disponibles
            f.write(f"- **Años disponibles:** {', '.join(map(str, temporal_info['years_available']))}\n\n")# Años disponibles
        
        f.write("## 2.2. Describe Data\n\n")# Sección de descripción de datos
        f.write("### Calidad de datos\n\n")# Sección de calidad de datos
        f.write(f"- Filas duplicadas: **{quality['filas_duplicadas']}** ({quality['porcentaje_duplicados']}%)\n")# Filas duplicadas
        f.write(f"- Promedio de valores nulos: **{quality['promedio_nulos']}%**\n")# Promedio de nulos
        f.write(f"- Columnas constantes: **{quality['columnas_constantes']}**\n")# Columnas constantes
        f.write(f"- Columnas casi vacías (>90% nulos): **{quality['columnas_casi_vacias']}**\n\n")# Columnas casi vacías
        
        f.write("### Clasificación de variables\n\n")# Sección de clasificación de variables
        clasificacion = dic['Clasificación'].value_counts()# Conteo por tipo
        for tipo, count in clasificacion.items():# Conteo por tipo
            f.write(f"- {tipo}: **{count}** variables\n")# Conteo por tipo
        f.write("\n")# Nueva línea
        
        if quality.get('columnas_problemáticas'):# Columnas problemáticas
            f.write("###  Columnas problemáticas detectadas\n\n")# Columnas problemáticas detectadas
            for item in quality['columnas_problemáticas'][:10]:# Limitar a las primeras 10 problemáticas
                f.write(f"- `{item['columna']}`: {', '.join(item['problemas'])}\n")# Listar problemáticas
            f.write("\n")
        
        f.write("## 2.3. Explore Data\n\n")
        f.write("### Análisis espacio-temporal\n\n")
        
        if spatial_results.get('zonas_alerta') is not None and len(spatial_results['zonas_alerta']) > 0:
            f.write(f"**Zonas de alerta identificadas:** {len(spatial_results['zonas_alerta'])}\n\n")
            f.write("Localidades con cambios significativos (>20%):\n\n")# Localidades con cambios significativos (>20%):
            f.write("| Localidad | Cambio % |\n")# Tabla de cambios
            f.write("|-----------|----------|\n")# Encabezado de la tabla
            for idx, row in spatial_results['zonas_alerta'].head(10).iterrows():# Limitar a las primeras 10
                f.write(f"| {idx} | {row['Cambio_porcentual']:.1f}% |\n")
            f.write("\n")
        
        f.write("### Distribución geográfica\n\n")
        f.write("Se generaron análisis detallados de:\n")
        f.write("- Distribución de intervenciones por localidad y año\n")
        f.write("- Evolución temporal de las principales localidades\n")# Evolución temporal de las principales localidades
        f.write("- Identificación de tendencias (aumento/disminución)\n")# Identificación de tendencias (aumento/disminución)
        f.write("- Relación con régimen de afiliación en salud\n\n")# Relación con régimen de afiliación en salud
        
        f.write("## 2.4. Verify Data Quality\n\n")
        f.write("### Verificaciones realizadas\n\n")#
        f.write(" **Completitud:** Análisis de valores faltantes por variable\n\n")
        f.write(" **Consistencia:** Detección de duplicados y valores constantes\n\n")
        f.write(" **Validez:** Identificación de columnas con alta cardinalidad\n\n")
        f.write(" **Unicidad:** Verificación de identificadores únicos\n\n")
        
        f.write("##  Archivos generados\n\n")
        f.write("### Tablas\n")
        f.write("- `diccionario_datos.xlsx` - Descripción completa de variables\n")
        f.write("- `distribucion_localidad_año.csv` - Datos espacio-temporales\n")
        f.write("- `tendencias_por_localidad.xlsx` - Análisis de cambios\n")
        f.write("- `zonas_alerta.csv` - Localidades con cambios significativos\n")
        f.write("- `regimen_por_localidad_porcentaje.xlsx` - Distribución de afiliación\n")
        f.write("- `quality_report.json` - Reporte completo de calidad\n\n")
        
        f.write("### Figuras\n")
        f.write("- **Temporales:** Evolución de intervenciones por año\n")
        f.write("- **Espaciales:** Mapas de calor y distribuciones por localidad\n")
        f.write("- **Exploratorias:** Distribuciones, correlaciones y valores faltantes\n\n")
        
        f.write("---\n\n")
        f.write(f"**Ruta de reportes:** `{REPORTS_DIR}`\n")
    
    print(" Reporte Markdown generado correctamente")


# ============================================================
# 13. FLUJO PRINCIPAL
# ============================================================

def main():
    """Flujo principal de Data Understanding"""
    print("="*70)
    print(" DATA UNDERSTANDING - PROYECTO NNA BOGOTÁ (2021-2025)")
    print("="*70)
    print()
    
    # 1. Carga de datos
    print(" PASO 1: Carga de datos")
    print("-"*70)
    df = load_data(file_path)# Cargar datos
    print()
    
    # 2. Limpieza y normalización
    print(" PASO 2: Limpieza y normalización") 
    print("-"*70) # Limpieza y normalización
    df = clean_columns(df)
    df = anonymize(df)
    print()
    
    # 3. Detección temporal
    print(" PASO 3: Detección de variables temporales")
    print("-"*70)
    df, temporal_info = detect_temporal_columns(df)
    print()
    
    # 4. Diccionario de datos
    print(" PASO 4: Generación de diccionario de datos")
    print("-"*70)
    dic = generate_dictionary(df)
    print()
    
    # 5. Verificación de calidad
    print("  PASO 5: Verificación de calidad")# Verificación de calidad
    print("-"*70)
    quality = verify_quality(df)
    print()
    
    # 6. Análisis exploratorio
    print(" PASO 6: Análisis exploratorio")
    print("-"*70)
    exploratory_analysis(df, dic)
    print()
    
    # 7. Análisis espacio-temporal
    print("  PASO 7: Análisis espacio-temporal") 
    print("-"*70)
    spatial_results = analyze_spatiotemporal(df)
    print()
    
    # 8. Análisis de régimen de salud
    print(" PASO 8: Análisis de régimen de salud")
    print("-"*70)
    analyze_health_regime(df)
    print()
    
    # 9. Cruces de variables
    print("PASO 9: Cruces de variables clave")#
    print("-"*70)#
    cross_analysis(df)
    print()
    
    # 10. Visualizaciones generales
    print("📊 PASO 10: Visualizaciones generales")
    print("-"*70)#
    plot_missing(df)
    plot_correlation(df)
    print(" Visualizaciones generales completadas")
    print()
    
    # 11. Documentación final
    print(" PASO 11: Generación de documentación")
    print("-"*70)
    generate_summary_md(df, quality, dic, temporal_info, spatial_results)
    print()
    
    # Resumen final
    print("="*70)
    print(" DATA UNDERSTANDING COMPLETADO CON ÉXITO")
    print("="*70)
    print()
    print(f" Resumen:")
    print(f"   • Filas procesadas: {df.shape[0]:,}")
    print(f"   • Columnas analizadas: {df.shape[1]}")
    print(f"   • Duplicados detectados: {quality['filas_duplicadas']}")
    print(f"   • Calidad promedio: {100 - quality['promedio_nulos']:.1f}%")
    print()
    print(f" Archivos generados en:")
    print(f"   • Reportes: {REPORTS_DIR}")
    print(f"   • Tablas: {TABLES_DIR}")# Tablas
    print(f"   • Figuras: {FIGURES_DIR}")# Figuras
    print()
    print(f" Resumen completo disponible en:")
    print(f"   {SUMMARY_FILE}") 
    print()
    print("="*70)


if __name__ == "__main__": # Punto de entrada del script
    try:
        main()# Ejecutar flujo principal
    except Exception as e:
        print(f"\n ERROR: {str(e)}")# Capturar cualquier error inesperado
        import traceback # Importar módulo traceback
        traceback.print_exc() # Imprimir traceback del error

# ============================================================
# FIN DEL SCRIPT
# ============================================================