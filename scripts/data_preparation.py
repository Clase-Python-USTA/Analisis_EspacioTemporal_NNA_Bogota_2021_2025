# ============================================================
# DATA PREPARATION - Proyecto NNA Bogotá (2021–2025)
# Limpieza, transformación y preparación de datos
# ============================================================

import os # Manipulación de rutas
import pandas as pd # Manipulación de datos
import numpy as np # Cálculos numéricos
import re # Expresiones regulares
import matplotlib.pyplot as plt # Visualización
import seaborn as sns # Visualización avanzada
from datetime import datetime # Manejo de fechas
from dotenv import load_dotenv # Carga variables entorno
import warnings     # Manejo de warnings
import json # Manejo de JSON

# Configuración del entorno
warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("="*70)
print(" DATA PREPARATION - PROYECTO NNA BOGOTÁ (2021-2025)")
print("="*70)
print()

"""
============================================================
RESUMEN EJECUTIVO - DATA PREPARATION
Proyecto: NNA Bogotá (2021-2025)
============================================================

 PROPÓSITO:
    Limpia, transforma y prepara los datos para análisis posterior.
    Convierte datos brutos en datos listos para modelado.

 OBJETIVO PRINCIPAL:
    Preparar una base de datos limpia, consistente y sin información
    personal, lista para análisis espacio-temporal.

============================================================
 ESTRUCTURA DEL PROCESO (7 PASOS)
============================================================

PASO 1: CARGA DE DATOS
--------
- Detecta formato del archivo (Excel/CSV)
- Carga hoja 'BD' si existe, si no, la última hoja
- Reporta dimensiones y memoria utilizada
- Validación inicial del archivo

PASO 2: ESTANDARIZACIÓN DE COLUMNAS
--------
- Limpia nombres de columnas:
  - Elimina espacios y caracteres especiales
  - Convierte todo a MAYÚSCULAS
  - Reemplaza espacios por guiones bajos (_)
  - Ejemplo: "Nombre Columna!" → "NOMBRE_COLUMNA"
- Guarda mapeo de cambios en JSON para trazabilidad
- Elimina guiones bajos duplicados

PASO 3: ELIMINACIÓN DE INFORMACIÓN PERSONAL (PII)
--------
- Identifica y elimina columnas con datos personales:
  - Nombres, apellidos, documentos
  - Teléfonos, correos, direcciones
  - Información de acudientes
  - Nombres de EPS/EAPB
- EXCEPCIONES: Mantiene columnas como:
  - NUMERO_DE_MANZANA_DEL_CUIDADO
  - NUMERO_DE_FICHA_ANTERIOR
- Reporta columnas eliminadas

PASO 4: LIMPIEZA DE INCONSISTENCIAS
--------
- Limpia texto en columnas categóricas:
  - Elimina espacios extra
  - Convierte 'nan', 'None', '' a NaN real
- Estandariza fechas a formato datetime
- Elimina registros duplicados completos
- Estandariza valores categóricos:
  - 'Si', 'si', 's', '1' → 'SI'
  - 'No', 'no', 'n', '0' → 'NO'
  - NOTA: Mantiene '99999' como código válido del sistema

PASO 5: MANEJO DE VALORES FALTANTES
--------
- Calcula % de nulos por columna
- Genera reporte de nulos en Excel
- Identifica columnas con >90% nulos (casi vacías)
- Imputa valores en categóricas (<50% nulos):
  - Rellena con 'No especificado'
- Genera gráfico de Top 20 variables con más nulos
- NO elimina automáticamente columnas vacías (solo reporta)

PASO 6: ANÁLISIS EXPLORATORIO INICIAL (EDA)
--------
- Estadísticas descriptivas de variables numéricas:
  - Media, mediana, desviación estándar, etc.
  - Exporta a Excel
- Distribuciones de variables categóricas:
  - Gráficos de barras para primeras 10 variables
  - Solo si tienen <50 categorías únicas
- Análisis temporal:
  - Si existe columna AÑO o FECHA_INTERVENCION
  - Genera gráfico de distribución anual
  - Crea columna AÑO si no existe

PASO 7: EXPORTACIÓN DE BASE FINAL
--------
- Exporta datos limpios a:
  - Excel: base_nna_limpia.xlsx
  - CSV: base_nna_limpia.csv (con UTF-8-BOM)
- Genera resumen final en JSON con:
  - Fecha de procesamiento
  - Dimensiones finales (filas × columnas)
  - Tamaño en MB
  - Nombre del archivo
- Guarda log completo del proceso

============================================================
 ARCHIVOS DE SALIDA
============================================================

 data/processed/
├── base_nna_limpia.xlsx          #  Base principal limpia (Excel)
└── base_nna_limpia.csv           # Base limpia en CSV

 reports/preparation/
├── preparation_log.txt           # Log detallado del proceso
├── mapeo_columnas.json           # Mapeo de nombres originales → limpios
├── reporte_nulos.xlsx            # Análisis de valores faltantes
├── estadisticas_descriptivas.xlsx # Stats de variables numéricas
└── resumen_final.json            # Resumen ejecutivo

 reports/preparation/figures/
├── valores_faltantes.png         # Top 20 variables con nulos
├── distribucion_anual.png        # Intervenciones por año
└── dist_*.png                    # Distribuciones de categóricas

============================================================
 DECISIONES CLAVE DE LIMPIEZA
============================================================
 SE MANTIENEN:
- Códigos '99999' (son parte del sistema, NO son missing)
- Columnas NUMERO_DE_MANZANA, NUMERO_DE_FICHA
- Todas las columnas con <90% de nulos

 SE ELIMINAN:
- Información personal: nombres, teléfonos, correos, direcciones
- Duplicados completos (filas idénticas)
- Caracteres especiales en nombres de columnas

 SE TRANSFORMAN:
- Fechas → datetime
- Texto → limpio sin espacios extra
- Categorías → estandarizadas (SI/NO/99999)
- Columnas → MAYÚSCULAS con guiones bajos

============================================================
 CONFIGURACIÓN
============================================================

Variables de entorno (.env):
- DATA_FILE: Ruta del archivo de datos original

Librerías requeridas:
- pandas, numpy: Manipulación de datos
- matplotlib, seaborn: Visualización
- python-dotenv: Variables de entorno
- openpyxl: Lectura/escritura Excel

============================================================
 RESULTADO FINAL
============================================================

Se obtiene una base de datos:
✓ Sin información personal (RGPD compliant)
✓ Con columnas estandarizadas
✓ Sin duplicados
✓ Con fechas en formato correcto
✓ Con categorías estandarizadas
✓ Lista para análisis espacio-temporal

La base limpia queda en:
 data/processed/base_nna_limpia.xlsx

============================================================
"""



# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.getenv("DATA_FILE")

if not DATA_FILE:
    raise ValueError(" No se encontró la variable DATA_FILE en el archivo .env")

file_path = os.path.join(BASE_DIR, DATA_FILE)

# Carpetas de salida
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed") 
PREP_REPORTS_DIR = os.path.join(BASE_DIR, "reports", "preparation") 
PREP_FIGURES_DIR = os.path.join(PREP_REPORTS_DIR, "figures") 
CLEANED_DATA_FILE = os.path.join(PROCESSED_DIR, "base_nna_limpia.xlsx") 
PREP_LOG_FILE = os.path.join(PREP_REPORTS_DIR, "preparation_log.txt") #

for path in [PROCESSED_DIR, PREP_REPORTS_DIR, PREP_FIGURES_DIR]:
    os.makedirs(path, exist_ok=True)#

# Iniciar log
log_entries = []

def log(message):
    """Registra mensaje en consola y en log"""
    print(message)
    log_entries.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


# ============================================================
# PASO 1: CONFIGURACIÓN Y CARGA DE DATOS
# ============================================================

def paso1_cargar_datos():
    """Carga inicial de datos"""
    log("\n PASO 1: Configuración y carga de datos")
    log("-"*70)
    
    ext = os.path.splitext(file_path)[-1].lower() # Extensión del archivo
    
    log(f" Cargando archivo: {os.path.basename(file_path)}")
    
    if ext in ['.xlsx', '.xls']:
        xls = pd.ExcelFile(file_path) #
        log(f"   Hojas disponibles: {xls.sheet_names}") 
        sheet = 'BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1] 
        df = pd.read_excel(file_path, sheet_name=sheet) 
        log(f"   ✓ Cargada hoja: {sheet}") 
    elif ext == '.csv':
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8') 
        log(f"   ✓ CSV cargado") 
    else:
        raise ValueError(" Formato no compatible") 
    
    log(f" Datos cargados: {df.shape[0]:,} filas × {df.shape[1]} columnas") 
    log(f"   Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB") 
    
    return df 


# ============================================================
# PASO 2: ESTANDARIZACIÓN DE NOMBRES DE COLUMNAS
# ============================================================

def paso2_estandarizar_columnas(df): 
    """Limpia y estandariza nombres de columnas""" 
    log("\n  PASO 2: Estandarización de nombres de columnas") 
    log("-"*70) 
    
    original_cols = df.columns.tolist() 
    
    # Limpieza y normalización
    df.columns = (
        df.columns
        .str.strip()                          # Eliminar espacios
        .str.replace(r'\s+', '_', regex=True) # Espacios a guiones bajos
        .str.replace(r'[^\w_]', '', regex=True) # Eliminar caracteres especiales
        .str.upper()                          # Todo en mayúsculas
    )
    
    # Eliminar guiones bajos duplicados
    df.columns = df.columns.str.replace(r'_+', '_', regex=True).str.strip('_') #
    
    # Mapeo de cambios
    cambios = {orig: nuevo for orig, nuevo in zip(original_cols, df.columns) if orig != nuevo} 
    
    log(f" Columnas estandarizadas: {len(df.columns)} variables")#
    log(f"   Columnas modificadas: {len(cambios)}")
    
    # Guardar mapeo
    with open(os.path.join(PREP_REPORTS_DIR, "mapeo_columnas.json"), "w", encoding="utf-8") as f:
        json.dump(cambios, f, indent=2, ensure_ascii=False) 
    
    return df


# ============================================================
# PASO 3: ELIMINACIÓN DE INFORMACIÓN PERSONAL (PII)
# ============================================================

def paso3_eliminar_pii(df):
    """Elimina información personal identificable"""
    log("\n PASO 3: Eliminación de información personal (PII)")
    log("-"*70) 
    
    # Columnas con información personal
    pii_patterns = [
        'USUARIO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO', 'CEDULA', 'IDENTIFICACION',
        'DIRECCION', 'DIRECCION', 'DOMICILIO', 'RESIDENCIA',
        'CORREO', 'EMAIL', 'MAIL',
        'TELEFONO', 'CELULAR', 'MOVIL', 'CONTACTO',
        'RESPONSABLE', 'ACUDIENTE', 'TUTOR',
        'NOMBRE_EAPB', 'EPS'
    ]
    
    # Identificar columnas PII
    cols_pii = []
    for col in df.columns:
        if any(pattern in col for pattern in pii_patterns):
            # Excepciones: columnas que contienen "NUMERO" pero no son personales
            if 'NUMERO_DE_MANZANA' in col or 'NUMERO_DE_FICHA' in col:
                continue
            cols_pii.append(col)
    
    # Eliminar columnas PII
    if cols_pii:
        df = df.drop(columns=cols_pii)
        log(f" Columnas PII eliminadas: {len(cols_pii)}")
        for col in cols_pii:
            log(f"   • {col}")
    else:
        log(" No se encontraron columnas PII adicionales (archivo ya anonimizado)")
    
    return df


# ============================================================
# PASO 4: LIMPIEZA DE INCONSISTENCIAS
# ============================================================

def paso4_limpiar_inconsistencias(df):
    """Limpia inconsistencias en los datos"""
    log("\n PASO 4: Limpieza de inconsistencias")
    log("-"*70)
    
    inconsistencias_corregidas = 0
    
    # 4.1 Limpiar texto en columnas categóricas
    text_cols = df.select_dtypes(include=['object']).columns
    
    for col in text_cols:
        # Eliminar espacios extra y convertir a string
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
        
        # Reemplazar valores como 'nan', 'None', '' por NaN real
        df[col] = df[col].replace(['nan', 'None', '', 'null', 'NULL', 'NA'], np.nan)
    
    log(f"   ✓ Texto limpiado en {len(text_cols)} columnas")
    
    # 4.2 Estandarizar fechas
    date_cols = [c for c in df.columns if 'FECHA' in c]
    for col in date_cols:
        if df[col].dtype != 'datetime64[ns]':
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                log(f"   ✓ Fecha estandarizada: {col}")
            except:
                log(f"     No se pudo convertir: {col}")
    
    # 4.3 Eliminar duplicados completos
    duplicados_antes = df.duplicated().sum()
    if duplicados_antes > 0:
        df = df.drop_duplicates()
        log(f"   ✓ Duplicados eliminados: {duplicados_antes}")
    else:
        log(f"   ✓ No se encontraron duplicados completos")
    
    # 4.4 Estandarizar categorías comunes
    categorias_estandar = {
        'SI': ['Si', 'si', 'SI', 'sí', 'Sí', 's', 'S', '1', 1],
        'NO': ['No', 'no', 'NO', 'n', 'N', '0', 0],
        '99999': ['99999', '99.999', 'No aplica', 'NO APLICA', 'N/A', 'NA']
    }
    
    for col in text_cols:
        if df[col].nunique() < 20:  # Solo para columnas con pocas categorías
            for estandar, variantes in categorias_estandar.items():
                df[col] = df[col].replace(variantes, estandar)
    
    log(f" Limpieza de inconsistencias completada")
    
    return df


# ============================================================
# PASO 5: MANEJO DE VALORES FALTANTES
# ============================================================

def paso5_manejar_faltantes(df):
    """Analiza y maneja valores faltantes"""
    log("\n⚙️  PASO 5: Manejo de valores faltantes")
    log("-"*70)
    
    # Calcular porcentaje de nulos por columna
    nulos = df.isnull().sum()
    pct_nulos = (nulos / len(df) * 100).round(2)
    
    reporte_nulos = pd.DataFrame({
        'Variable': df.columns,
        'Nulos': nulos.values,
        'Porcentaje': pct_nulos.values
    }).sort_values('Porcentaje', ascending=False)
    
    reporte_nulos.to_excel(os.path.join(PREP_REPORTS_DIR, "reporte_nulos.xlsx"), index=False)
    
    # Columnas con muchos nulos (>90%)
    cols_muy_nulas = reporte_nulos[reporte_nulos['Porcentaje'] > 90]['Variable'].tolist()
    
    if cols_muy_nulas:
        log(f"     Columnas con >90% nulos: {len(cols_muy_nulas)}")
        log(f"   Considerar eliminar: {', '.join(cols_muy_nulas[:5])}...")
        
        # Opcional: eliminar columnas casi vacías
        # df = df.drop(columns=cols_muy_nulas)
        # log(f"   ✓ Eliminadas {len(cols_muy_nulas)} columnas casi vacías")
    
    # Imputación de valores para columnas clave
    # Ejemplo: rellenar categóricas con "No especificado"
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0 and df[col].isnull().sum() / len(df) < 0.5:
            df[col] = df[col].fillna('No especificado')
    
    # Gráfico de valores faltantes
    top_nulos = reporte_nulos.head(20)
    if top_nulos['Porcentaje'].max() > 0:
        plt.figure(figsize=(10, 8))
        plt.barh(top_nulos['Variable'], top_nulos['Porcentaje'], color='coral')
        plt.xlabel('Porcentaje de valores faltantes (%)')
        plt.title('Top 20 variables con mayor porcentaje de valores faltantes')
        plt.tight_layout()
        plt.savefig(os.path.join(PREP_FIGURES_DIR, "valores_faltantes.png"), dpi=150)
        plt.close()
        log(f"   ✓ Gráfico de valores faltantes guardado")
    
    log(f" Análisis de valores faltantes completado")
    log(f"   Promedio general de nulos: {pct_nulos.mean():.2f}%")
    
    return df


# ============================================================
# PASO 6: ANÁLISIS EXPLORATORIO INICIAL (EDA)
# ============================================================

def paso6_eda_inicial(df):
    """Análisis exploratorio de datos limpiados"""
    log("\n PASO 6: Análisis exploratorio inicial (EDA)")
    log("-"*70)
    
    # Resumen estadístico de numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        stats = df[num_cols].describe().T
        stats.to_excel(os.path.join(PREP_REPORTS_DIR, "estadisticas_descriptivas.xlsx"))
        log(f"   ✓ Estadísticas descriptivas guardadas ({len(num_cols)} variables numéricas)")
    
    # Distribución de variables categóricas clave
    cat_cols = df.select_dtypes(include=['object']).columns[:10]  # Primeras 10
    
    for col in cat_cols:
        if df[col].nunique() < 50:  # Solo si tiene pocas categorías
            freq = df[col].value_counts().head(15)
            
            plt.figure(figsize=(10, 6))
            freq.plot(kind='barh', color='steelblue')
            plt.title(f"Distribución de {col}")
            plt.xlabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(os.path.join(PREP_FIGURES_DIR, f"dist_{col}.png"), dpi=150)
            plt.close()
    
    log(f"   ✓ Distribuciones generadas para variables categóricas")
    
    # Análisis temporal si existe columna de año
    if 'AÑO' in df.columns or 'FECHA_INTERVENCION' in df.columns:
        if 'AÑO' not in df.columns and 'FECHA_INTERVENCION' in df.columns:
            df['AÑO'] = pd.to_datetime(df['FECHA_INTERVENCION']).dt.year
        
        if 'AÑO' in df.columns:
            dist_anual = df['AÑO'].value_counts().sort_index()
            
            plt.figure(figsize=(10, 6))
            dist_anual.plot(kind='bar', color='mediumseagreen')
            plt.title("Distribución de intervenciones por año")
            plt.xlabel("Año")
            plt.ylabel("Número de intervenciones")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.savefig(os.path.join(PREP_FIGURES_DIR, "distribucion_anual.png"), dpi=150)
            plt.close()
            log(f"   ✓ Distribución temporal generada")
    
    log(f" Análisis exploratorio inicial completado")
    
    return df


# ============================================================
# PASO 7: EXPORTACIÓN DE BASE FINAL
# ============================================================

def paso7_exportar_datos(df):
    """Exporta base de datos limpia"""
    log("\n PASO 7: Exportación de la base final")
    log("-"*70)
    
    # Exportar a Excel
    df.to_excel(CLEANED_DATA_FILE, index=False, engine='openpyxl')
    log(f" Base limpia exportada a: {CLEANED_DATA_FILE}")
    
    # También en CSV
    csv_file = CLEANED_DATA_FILE.replace('.xlsx', '.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    log(f" Base limpia exportada a: {csv_file}")
    
    # Generar resumen final
    resumen = {
        "fecha_procesamiento": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "filas_finales": int(df.shape[0]),
        "columnas_finales": int(df.shape[1]),
        "archivo_salida": os.path.basename(CLEANED_DATA_FILE),
        "tamaño_mb": float((df.memory_usage(deep=True).sum() / 1024**2).round(2))
    }
    
    with open(os.path.join(PREP_REPORTS_DIR, "resumen_final.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    
    log(f" Resumen final generado")
    
    return df


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta todo el proceso de preparación"""
    inicio = datetime.now()
    
    try:
        # Ejecutar pasos
        df = paso1_cargar_datos()
        df = paso2_estandarizar_columnas(df)
        df = paso3_eliminar_pii(df)
        df = paso4_limpiar_inconsistencias(df)
        df = paso5_manejar_faltantes(df)
        df = paso6_eda_inicial(df)
        df = paso7_exportar_datos(df)
        
        # Resumen final
        duracion = (datetime.now() - inicio).total_seconds() 
        
        log("\n" + "="*70)
        log(" DATA PREPARATION COMPLETADO CON ÉXITO")
        log("="*70)
        log(f"\n Resumen final:")
        log(f"   • Filas en base limpia: {df.shape[0]:,}")
        log(f"   • Columnas en base limpia: {df.shape[1]}")
        log(f"   • Tiempo de ejecución: {duracion:.2f} segundos")
        log(f"\n Archivos generados:")
        log(f"   • Base limpia: {CLEANED_DATA_FILE}")
        log(f"   • Reportes: {PREP_REPORTS_DIR}")
        log(f"   • Figuras: {PREP_FIGURES_DIR}")
        log("\n" + "="*70)
        
    except Exception as e:
        log(f"\n ERROR: {str(e)}") 
        import traceback
        traceback.print_exc()
    
    finally:
        # Guardar log
        with open(PREP_LOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(log_entries))
        log(f"\n📄 Log guardado en: {PREP_LOG_FILE}") 


if __name__ == "__main__":
    main()

# ============================================================
# FIN DEL SCRIPT
# ============================================================