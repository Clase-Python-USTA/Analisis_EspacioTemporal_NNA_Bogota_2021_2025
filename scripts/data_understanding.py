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
    """Verificación de anonimización - El archivo ya viene anonimizado del origen"""
    
    # Solo verificar si existen columnas personales sensibles y eliminarlas
    # (probablemente ya no existen en el archivo anonimizado)
    sensitive_cols = [
        'USUARIO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO', 
        'DIRECCIÓN', 'DIRECCION', 'CORREO', 'EMAIL', 
        'TELÉFONO', 'TELEFONO', 'CELULAR',
        'NOMBRE_EAPB', 'RESPONSABLE', 'ACUDIENTE'
    ]# Columnas sensibles a eliminar si existen 
    
    removed = [c for c in sensitive_cols if c in df.columns] # Columnas realmente presentes en el DataFrame
    if removed: # Si hay columnas sensibles presentes
        df.drop(columns=removed, inplace=True, errors='ignore')# Eliminar columnas sensibles
    
    #  IMPORTANTE: NO ENCRIPTAMOS NADA
    # El archivo fuente ya está completamente anonimizado
    # Todas las columnas se mantienen tal como están
    
    print(f" Verificación completada: {len(removed)} columnas eliminadas") # Confirmar eliminación
    print(f"     El archivo fuente ya está COMPLETAMENTE ANONIMIZADO") # Confirmar anonimización
    print(f"   ✓ TODAS las variables se mantienen intactas para análisis") # Confirmar mantenimiento de variables
    print(f"   ✓ Los valores como '824e28643eaef519' son datos ya anonimizados del origen") # Confirmar mantenimiento de variables
    
    return df # Retornar DataFrame


# ============================================================
# 4. DETECCIÓN AUTOMÁTICA DE VARIABLES TEMPORALES
# ============================================================

def detect_temporal_columns(df): 
    """Detecta y procesa columnas de fecha/año""" # Detecta y procesa columnas de fecha/año
    temporal_info = {} # Diccionario para almacenar información temporal
    
    date_candidates = [c for c in df.columns if any(x in c for x in ['FECHA', 'DATE', 'AÑO', 'ANO', 'YEAR', 'MES', 'MONTH'])] # Candidatas a columnas de fecha/año
    
    for col in date_candidates: # Intentar convertir a datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]): # Ya es datetime
            temporal_info[col] = 'datetime'# Confirmar tipo datetime
        elif df[col].dtype == 'object':# Intentar conversión
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')# Convertir a datetime
                temporal_info[col] = 'datetime_converted'# Confirmar conversión exitosa
            except:# Ignorar errores
                pass
    
    for col in temporal_info.keys(): # Extraer año si es datetime
        if 'AÑO' not in df.columns and 'YEAR' not in df.columns: # Solo si no existe ya
            df['AÑO'] = df[col].dt.year # Extraer año
            print(f"   ✓ Columna 'AÑO' extraída de {col}") # Confirmar extracción
    
    year_cols = [c for c in df.columns if c in ['AÑO', 'ANO', 'YEAR', 'ANIO']] # Columnas que podrían ser año
    if year_cols:
        df['AÑO'] = pd.to_numeric(df[year_cols[0]], errors='coerce') # Convertir a numérico
    
    if 'AÑO' in df.columns:# Si existe columna de año
        years = df['AÑO'].dropna().unique()# Años únicos
        print(f"✅ Años detectados: {sorted([int(y) for y in years if not np.isnan(y)])}")# Mostrar años detectados
        temporal_info['years_available'] = sorted([int(y) for y in years if not np.isnan(y)])# Guardar años disponibles
    else:
        print("⚠️  No se detectó columna de año")# Advertencia si no se detecta
    
    return df, temporal_info# Retornar DataFrame y info temporal


# ============================================================
# 5. DICCIONARIO DE DATOS AMPLIADO
# ============================================================

def generate_dictionary(df):
    """Genera diccionario completo de datos""" # Genera diccionario completo de datos
    dic = pd.DataFrame({
        "Variable": df.columns, # Nombres de variables
        "Tipo_dato": df.dtypes.values,# Tipos de datos
        "Valores_nulos": df.isnull().sum().values,# Valores nulos
        "Porcentaje_nulos": (df.isnull().sum() / len(df) * 100).round(2).values,# Porcentaje de nulos
        "Valores_únicos": df.nunique().values,# Valores únicos
        "Cardinalidad": df.nunique().values / len(df) * 100,# Cardinalidad
        "Primer_valor": [df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None for col in df.columns]# Primer valor no nulo
    })# Crear DataFrame del diccionario
    
    dic['Clasificación'] = dic.apply(lambda row: clasificar_variable(row, len(df)), axis=1)# Clasificar variables
    
    dic.to_excel(os.path.join(TABLES_DIR, "diccionario_datos.xlsx"), index=False)# Guardar en Excel
    dic.to_csv(os.path.join(TABLES_DIR, "diccionario_datos.csv"), index=False)# Guardar en CSV
    
    print(f" Diccionario de datos generado: {len(dic)} variables documentadas")# Confirmar generación 
    return dic# Retornar diccionario


def clasificar_variable(row, n_rows):
    """Clasifica tipo de variable según sus características"""
    if row['Porcentaje_nulos'] > 90:# Más del 90% nulos
        return 'Casi_vacía'# Casi vacía
    elif row['Valores_únicos'] == 1:# Solo un valor único
        return 'Constante'
    elif row['Valores_únicos'] == n_rows:# Todos los valores únicos
        return 'Identificador'# Identificador
    elif row['Valores_únicos'] <= 10:# Hasta 10 valores únicos
        return 'Categórica_baja'# Categórica baja
    elif row['Valores_únicos'] <= 50:# Hasta 50 valores únicos
        return 'Categórica_media'# Categórica media
    elif row['Cardinalidad'] > 90:# Más del 90% de cardinalidad
        return 'Alta_cardinalidad'# Alta cardinalidad
    elif 'int' in str(row['Tipo_dato']) or 'float' in str(row['Tipo_dato']):
        return 'Numérica'
    else:
        return 'Categórica_alta'# Categórica alta


# ============================================================
# 6. VERIFICACIÓN DE CALIDAD DE DATOS
# ============================================================

def verify_quality(df):
    """Análisis exhaustivo de calidad de datos"""
    quality = {
        "total_filas": int(df.shape[0]),# Total de filas
        "total_columnas": int(df.shape[1]),# Total de columnas
        "filas_duplicadas": int(df.duplicated().sum()),# Filas duplicadas
        "porcentaje_duplicados": float((df.duplicated().sum() / len(df) * 100).round(2)),# Porcentaje de duplicados
        "promedio_nulos": float((df.isnull().mean().mean() * 100).round(2)),# Promedio de nulos
        "columnas_constantes": int(len([c for c in df.columns if df[c].nunique() == 1])),# Columnas constantes
        "columnas_casi_vacias": int(len([c for c in df.columns if df[c].isnull().sum() / len(df) > 0.9])),# Columnas casi vacías
        "memoria_mb": float((df.memory_usage(deep=True).sum() / 1024**2).round(2))# Memoria usada en MB
    }# Crear reporte de calidad
    
    problematic = []# Lista de columnas problemáticas
    for col in df.columns:# Revisar cada columna
        issues = []# Problemas detectados
        if df[col].nunique() == 1:# Columna constante
            issues.append("constante")# Columna constante
        if df[col].isnull().sum() / len(df) > 0.9:# Columna casi vacía
            issues.append("casi_vacía")
        if df[col].nunique() > len(df) * 0.95 and df[col].dtype == 'object':
            issues.append("alta_cardinalidad")
        if issues:
            problematic.append({"columna": col, "problemas": issues})
    
    quality['columnas_problemáticas'] = problematic
    
    with open(os.path.join(TABLES_DIR, "quality_report.json"), "w", encoding="utf-8") as f:
        json.dump(quality, f, indent=2, ensure_ascii=False)
    
    pd.Series({k: v for k, v in quality.items() if not isinstance(v, list)}).to_csv(
        os.path.join(TABLES_DIR, "quality_summary.csv")
    )# Guardar resumen en CSV
    
    print(f"✅ Calidad verificada: {quality['filas_duplicadas']} duplicados, {quality['columnas_constantes']} columnas constantes")
    return quality


# ============================================================
# 7. ANÁLISIS EXPLORATORIO AMPLIADO
# ============================================================

def exploratory_analysis(df, dic):
    """Análisis exploratorio completo de todas las variables"""
    print("\n🔍 Iniciando análisis exploratorio ampliado...")
    
    cat_vars = dic[dic['Clasificación'].str.contains('Categórica', na=False)]['Variable'].tolist()
    
    for var in cat_vars[:15]:
        if var in df.columns:
            freq = df[var].value_counts().head(20)
            freq.to_csv(os.path.join(TABLES_DIR, f"frecuencia_{var}.csv"))
            
            if len(freq) > 0:
                plt.figure(figsize=(10, 6))
                freq.plot(kind='barh', color='steelblue')
                plt.title(f"Distribución de {var}")
                plt.xlabel("Frecuencia")
                plt.tight_layout()
                plt.savefig(os.path.join(EXPLORATORY_DIR, f"dist_{var}.png"), dpi=150)
                plt.close()
    
    num_vars = df.select_dtypes(include=[np.number]).columns.tolist() 
    if num_vars:
        stats = df[num_vars].describe().T
        stats.to_excel(os.path.join(TABLES_DIR, "estadisticas_numericas.xlsx"))
        
        for var in num_vars[:10]:
            if df[var].notna().sum() > 0:
                plt.figure(figsize=(8, 5))
                df[var].hist(bins=30, color='coral', edgecolor='black')
                plt.title(f"Distribución de {var}")
                plt.xlabel(var)
                plt.ylabel("Frecuencia")
                plt.tight_layout()
                plt.savefig(os.path.join(EXPLORATORY_DIR, f"hist_{var}.png"), dpi=150)
                plt.close()
    
    print(f"✅ Análisis exploratorio: {len(cat_vars)} categóricas, {len(num_vars)} numéricas")


# ============================================================
# 8. ANÁLISIS ESPACIO-TEMPORAL (NUEVO)
# ============================================================

def analyze_spatiotemporal(df):
    """Análisis espacial y temporal según objetivos del proyecto"""
    print("\n📊 Iniciando análisis espacio-temporal...")
    
    results = {}
    
    loc_col = None
    for col in df.columns:
        if 'LOCALIDAD' in col:
            loc_col = col
            break
    
    if not loc_col or 'AÑO' not in df.columns:
        print("⚠️  No se encontraron columnas de localidad o año necesarias")
        return results
    
    distribucion = df.groupby([loc_col, 'AÑO']).size().reset_index(name='Intervenciones')
    distribucion.to_csv(os.path.join(TABLES_DIR, "distribucion_localidad_año.csv"), index=False)
    
    pivot = distribucion.pivot(index=loc_col, columns='AÑO', values='Intervenciones').fillna(0)
    pivot.to_excel(os.path.join(TABLES_DIR, "matriz_localidad_año.xlsx"))
    
    pivot['Total'] = pivot.sum(axis=1)
    pivot['Promedio_anual'] = pivot['Total'] / len(pivot.columns)
    
    if len(pivot.columns) >= 3:
        años = [col for col in pivot.columns if isinstance(col, (int, np.integer))]
        if len(años) >= 2:
            pivot['Cambio_absoluto'] = pivot[max(años)] - pivot[min(años)]
            pivot['Cambio_porcentual'] = ((pivot[max(años)] - pivot[min(años)]) / (pivot[min(años)] + 1) * 100).round(2)
            pivot['Tendencia'] = pivot['Cambio_porcentual'].apply(
                lambda x: 'Aumento fuerte' if x > 20 else ('Aumento moderado' if x > 5 else ('Estable' if x > -5 else ('Disminución moderada' if x > -20 else 'Disminución fuerte')))
            )
    
    pivot.to_excel(os.path.join(TABLES_DIR, "tendencias_por_localidad.xlsx"))
    
    if 'Cambio_porcentual' in pivot.columns:
        alertas = pivot[abs(pivot['Cambio_porcentual']) > 20].sort_values('Cambio_porcentual', ascending=False)
        alertas.to_csv(ALERT_ZONES_FILE)
        print(f"   ⚠️  {len(alertas)} zonas de alerta identificadas")
        results['zonas_alerta'] = alertas
    
    top_localidades = pivot.nlargest(10, 'Total').index
    
    plt.figure(figsize=(14, 8))
    años_disponibles = [col for col in pivot.columns if isinstance(col, (int, np.integer))]
    
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
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot[años_disponibles].head(15), annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Intervenciones'})
    plt.title("Mapa de calor: Intervenciones por localidad y año", fontsize=14, fontweight='bold')
    plt.ylabel("Localidad", fontsize=12)
    plt.xlabel("Año", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(SPATIAL_DIR, "heatmap_localidad_año.png"), dpi=150)
    plt.close()
    
    print(f"✅ Análisis espacio-temporal completado")
    results['distribucion'] = distribucion
    results['pivot'] = pivot
    
    return results


# ============================================================
# 9. ANÁLISIS DE RÉGIMEN SUBSIDIADO (NUEVO)
# ============================================================

def analyze_health_regime(df):
    """Análisis del régimen de salud (Objetivo específico 3)"""
    print("\n💊 Analizando régimen de afiliación en salud...")
    
    afiliacion_col = None
    for col in df.columns:
        if 'AFILIACIÓN' in col or 'AFILIACION' in col or 'SGSSS' in col or 'REGIMEN' in col:
            afiliacion_col = col
            break
    
    if not afiliacion_col:
        print("⚠️  No se encontró columna de régimen de salud")
        return {}
    
    regimen_dist = df[afiliacion_col].value_counts()
    regimen_dist.to_csv(os.path.join(TABLES_DIR, "distribucion_regimen_salud.csv"))
    
    plt.figure(figsize=(10, 6))
    regimen_dist.plot(kind='bar', color=['#2ecc71', '#e74c3c', '#3498db', '#95a5a6'])
    plt.title("Distribución por régimen de afiliación en salud", fontsize=14, fontweight='bold')
    plt.xlabel("Tipo de régimen", fontsize=12)
    plt.ylabel("Número de intervenciones", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(EXPLORATORY_DIR, "distribucion_regimen.png"), dpi=150)
    plt.close()
    
    loc_col = next((c for c in df.columns if 'LOCALIDAD' in c), None)
    
    if loc_col:
        cruce = pd.crosstab(df[loc_col], df[afiliacion_col], normalize='index') * 100
        cruce.to_excel(os.path.join(TABLES_DIR, "regimen_por_localidad_porcentaje.xlsx"))
        
        if 'SUBSIDIADO' in cruce.columns or any('SUBSID' in str(col) for col in cruce.columns):
            subsid_col = next((c for c in cruce.columns if 'SUBSID' in str(c)), None)
            if subsid_col:
                top_subsidiado = cruce[subsid_col].sort_values(ascending=False).head(10)
                top_subsidiado.to_csv(os.path.join(TABLES_DIR, "top_localidades_subsidiado.csv"))
                
                plt.figure(figsize=(10, 7))
                top_subsidiado.plot(kind='barh', color='#e67e22')
                plt.title("Top 10 localidades con mayor % régimen subsidiado", fontsize=14, fontweight='bold')
                plt.xlabel("Porcentaje (%)", fontsize=12)
                plt.ylabel("Localidad", fontsize=12)
                plt.tight_layout()
                plt.savefig(os.path.join(SPATIAL_DIR, "top_subsidiado_localidades.png"), dpi=150)
                plt.close()
        
        plt.figure(figsize=(14, 8))
        cruce.head(15).plot(kind='barh', stacked=True, colormap='Set3', figsize=(14, 8))
        plt.title("Composición de régimen de salud por localidad (Top 15)", fontsize=14, fontweight='bold')
        plt.xlabel("Porcentaje (%)", fontsize=12)
        plt.ylabel("Localidad", fontsize=12)
        plt.legend(title='Régimen', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(SPATIAL_DIR, "regimen_por_localidad_stacked.png"), dpi=150, bbox_inches='tight')
        plt.close()
    
    print("✅ Análisis de régimen de salud completado")
    return {'distribucion': regimen_dist}


# ============================================================
# 10. CRUCES DE VARIABLES CLAVE
# ============================================================

def cross_analysis(df):
    """Análisis de cruces entre variables importantes"""
    print("\n🔗 Generando cruces de variables...")
    
    loc_col = next((c for c in df.columns if 'LOCALIDAD' in c), None)
    tipo_col = next((c for c in df.columns if 'TIPO' in c and 'INTERVENCION' in c), None)
    motivo_col = next((c for c in df.columns if 'MOTIVO' in c), None)
    servicio_col = next((c for c in df.columns if 'SERVICIO' in c), None)
    
    cruces_generados = 0
    
    if loc_col and tipo_col:
        cruce = pd.crosstab(df[loc_col], df[tipo_col])
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_localidad_tipo_intervencion.xlsx"))
        cruces_generados += 1
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(cruce.head(15), annot=True, fmt='d', cmap='Blues')
        plt.title("Cruce: Localidad × Tipo de intervención", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(EXPLORATORY_DIR, "cruce_localidad_tipo.png"), dpi=150)
        plt.close()
    
    if motivo_col and servicio_col:
        cruce = pd.crosstab(df[motivo_col], df[servicio_col])
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_motivo_servicio.xlsx"))
        cruces_generados += 1
    
    if 'AÑO' in df.columns and tipo_col:
        cruce = pd.crosstab(df['AÑO'], df[tipo_col])
        cruce.to_excel(os.path.join(TABLES_DIR, "cruce_año_tipo_intervencion.xlsx"))
        cruces_generados += 1
    
    print(f"✅ {cruces_generados} cruces de variables generados")


# ============================================================
# 11. VISUALIZACIONES GENERALES
# ============================================================

def plot_missing(df):
    """Gráfico de valores faltantes"""
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False).head(20)
    
    if len(missing) > 0:
        plt.figure(figsize=(10, 8))
        sns.barplot(x=missing.values, y=missing.index, palette='Reds_r')
        plt.title("Porcentaje de valores faltantes (Top 20)", fontsize=14, fontweight='bold')
        plt.xlabel("Porcentaje (%)", fontsize=12)
        plt.ylabel("Variable", fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(EXPLORATORY_DIR, "missing_values.png"), dpi=150)
        plt.close()


def plot_correlation(df):
    """Matriz de correlación de variables numéricas"""
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.shape[1] > 1:
        corr = numeric_df.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title("Matriz de correlación - Variables numéricas", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(EXPLORATORY_DIR, "correlation_matrix.png"), dpi=150)
        plt.close()


# ============================================================
# 12. DOCUMENTACIÓN MARKDOWN COMPLETA
# ============================================================

def generate_summary_md(df, quality, dic, temporal_info, spatial_results):
    """Genera reporte completo en Markdown"""
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("# 📊 Data Understanding - Proyecto NNA Bogotá (2021-2025)\n\n")
        f.write(f"**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## 2.1. Collect Initial Data\n\n")
        f.write("La base de datos contiene registros de intervenciones con niños, niñas y adolescentes (NNA) ")
        f.write("en las localidades de Bogotá durante el período 2021-2025.\n\n")
        f.write(f"- **Archivo origen:** `{os.path.basename(file_path)}`\n")
        f.write(f"- **Filas:** {quality['total_filas']:,}\n")
        f.write(f"- **Columnas:** {quality['total_columnas']}\n")
        f.write(f"- **Tamaño:** {quality['memoria_mb']} MB\n\n")
        
        if temporal_info.get('years_available'):
            f.write(f"- **Años disponibles:** {', '.join(map(str, temporal_info['years_available']))}\n\n")
        
        f.write("## 2.2. Describe Data\n\n")
        f.write("### Calidad de datos\n\n")
        f.write(f"- Filas duplicadas: **{quality['filas_duplicadas']}** ({quality['porcentaje_duplicados']}%)\n")
        f.write(f"- Promedio de valores nulos: **{quality['promedio_nulos']}%**\n")
        f.write(f"- Columnas constantes: **{quality['columnas_constantes']}**\n")
        f.write(f"- Columnas casi vacías (>90% nulos): **{quality['columnas_casi_vacias']}**\n\n")
        
        f.write("### Clasificación de variables\n\n")
        clasificacion = dic['Clasificación'].value_counts()
        for tipo, count in clasificacion.items():
            f.write(f"- {tipo}: **{count}** variables\n")
        f.write("\n")
        
        if quality.get('columnas_problemáticas'):
            f.write("### ⚠️ Columnas problemáticas detectadas\n\n")
            for item in quality['columnas_problemáticas'][:10]:
                f.write(f"- `{item['columna']}`: {', '.join(item['problemas'])}\n")
            f.write("\n")
        
        f.write("## 2.3. Explore Data\n\n")
        f.write("### Análisis espacio-temporal\n\n")
        
        if spatial_results.get('zonas_alerta') is not None and len(spatial_results['zonas_alerta']) > 0:
            f.write(f"**Zonas de alerta identificadas:** {len(spatial_results['zonas_alerta'])}\n\n")
            f.write("Localidades con cambios significativos (>20%):\n\n")
            f.write("| Localidad | Cambio % |\n")
            f.write("|-----------|----------|\n")
            for idx, row in spatial_results['zonas_alerta'].head(10).iterrows():
                f.write(f"| {idx} | {row['Cambio_porcentual']:.1f}% |\n")
            f.write("\n")
        
        f.write("### Distribución geográfica\n\n")
        f.write("Se generaron análisis detallados de:\n")
        f.write("- Distribución de intervenciones por localidad y año\n")
        f.write("- Evolución temporal de las principales localidades\n")
        f.write("- Identificación de tendencias (aumento/disminución)\n")
        f.write("- Relación con régimen de afiliación en salud\n\n")
        
        f.write("## 2.4. Verify Data Quality\n\n")
        f.write("### Verificaciones realizadas\n\n")
        f.write("✅ **Completitud:** Análisis de valores faltantes por variable\n\n")
        f.write("✅ **Consistencia:** Detección de duplicados y valores constantes\n\n")
        f.write("✅ **Validez:** Identificación de columnas con alta cardinalidad\n\n")
        f.write("✅ **Unicidad:** Verificación de identificadores únicos\n\n")
        
        f.write("## 📁 Archivos generados\n\n")
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
    
    print("✅ Reporte Markdown generado correctamente")


# ============================================================
# 13. FLUJO PRINCIPAL
# ============================================================

def main():
    """Flujo principal de Data Understanding"""
    print("="*70)
    print("🚀 DATA UNDERSTANDING - PROYECTO NNA BOGOTÁ (2021-2025)")
    print("="*70)
    print()
    
    # 1. Carga de datos
    print("📥 PASO 1: Carga de datos")
    print("-"*70)
    df = load_data(file_path)
    print()
    
    # 2. Limpieza y normalización
    print("🧹 PASO 2: Limpieza y normalización")
    print("-"*70)
    df = clean_columns(df)
    df = anonymize(df)
    print()
    
    # 3. Detección temporal
    print("📅 PASO 3: Detección de variables temporales")
    print("-"*70)
    df, temporal_info = detect_temporal_columns(df)
    print()
    
    # 4. Diccionario de datos
    print("📖 PASO 4: Generación de diccionario de datos")
    print("-"*70)
    dic = generate_dictionary(df)
    print()
    
    # 5. Verificación de calidad
    print("✔️  PASO 5: Verificación de calidad")
    print("-"*70)
    quality = verify_quality(df)
    print()
    
    # 6. Análisis exploratorio
    print("🔍 PASO 6: Análisis exploratorio")
    print("-"*70)
    exploratory_analysis(df, dic)
    print()
    
    # 7. Análisis espacio-temporal
    print("🗺️  PASO 7: Análisis espacio-temporal")
    print("-"*70)
    spatial_results = analyze_spatiotemporal(df)
    print()
    
    # 8. Análisis de régimen de salud
    print("💊 PASO 8: Análisis de régimen de salud")
    print("-"*70)
    analyze_health_regime(df)
    print()
    
    # 9. Cruces de variables
    print("🔗 PASO 9: Cruces de variables clave")
    print("-"*70)
    cross_analysis(df)
    print()
    
    # 10. Visualizaciones generales
    print("📊 PASO 10: Visualizaciones generales")
    print("-"*70)
    plot_missing(df)
    plot_correlation(df)
    print("✅ Visualizaciones generales completadas")
    print()
    
    # 11. Documentación final
    print("📝 PASO 11: Generación de documentación")
    print("-"*70)
    generate_summary_md(df, quality, dic, temporal_info, spatial_results)
    print()
    
    # Resumen final
    print("="*70)
    print("✅ DATA UNDERSTANDING COMPLETADO CON ÉXITO")
    print("="*70)
    print()
    print(f"📊 Resumen:")
    print(f"   • Filas procesadas: {df.shape[0]:,}")
    print(f"   • Columnas analizadas: {df.shape[1]}")
    print(f"   • Duplicados detectados: {quality['filas_duplicadas']}")
    print(f"   • Calidad promedio: {100 - quality['promedio_nulos']:.1f}%")
    print()
    print(f"📁 Archivos generados en:")
    print(f"   • Reportes: {REPORTS_DIR}")
    print(f"   • Tablas: {TABLES_DIR}")
    print(f"   • Figuras: {FIGURES_DIR}")
    print()
    print(f"📄 Resumen completo disponible en:")
    print(f"   {SUMMARY_FILE}")
    print()
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# ============================================================
# FIN DEL SCRIPT
# ============================================================