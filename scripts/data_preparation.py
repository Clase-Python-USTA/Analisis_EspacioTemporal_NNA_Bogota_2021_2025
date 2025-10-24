# ============================================================
# DATA PREPARATION - Proyecto NNA Bogotá (2021–2025)
# Limpieza, transformación y preparación de datos
# ============================================================

import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from dotenv import load_dotenv
import warnings
import json

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

# ============================================================
# CONFIGURACIÓN DE RUTAS - BASE CON COLUMNA 'AÑO'
# ============================================================

load_dotenv()

# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Ruta directa al archivo procesado desde Data Understanding
file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "base_nna_understanding.xlsx"
)

# Carpetas de salida para esta fase
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
PREP_REPORTS_DIR = os.path.join(BASE_DIR, "reports", "preparation")
PREP_FIGURES_DIR = os.path.join(PREP_REPORTS_DIR, "figures")
CLEANED_DATA_FILE = os.path.join(PROCESSED_DIR, "base_nna_limpia.xlsx")
PREP_LOG_FILE = os.path.join(PREP_REPORTS_DIR, "preparation_log.txt")

# Crear carpetas si no existen
for path in [PROCESSED_DIR, PREP_REPORTS_DIR, PREP_FIGURES_DIR]:
    os.makedirs(path, exist_ok=True)

# Inicializar log
log_entries = []

def log(message):
    """Registra mensaje en consola y en el log"""
    print(message)
    log_entries.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

print(f"\n📂 Archivo de entrada (procesado con columna 'AÑO'):\n{file_path}")


# ============================================================
# PASO 1: CONFIGURACIÓN Y CARGA DE DATOS
# ============================================================

def paso1_cargar_datos():
    """Carga inicial de datos con validación de la columna 'AÑO'"""
    log("\n PASO 1: Configuración y carga de datos")
    log("-"*70)

    ext = os.path.splitext(file_path)[-1].lower()
    log(f" Cargando archivo: {os.path.basename(file_path)}")

    if ext in ['.xlsx', '.xls']:
        try:
            xls = pd.ExcelFile(file_path)
            sheet = 'BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1]
            df = pd.read_excel(file_path, sheet_name=sheet)
            log(f"   ✓ Hoja cargada: {sheet}")
        except PermissionError:
            log("   ⚠️ Archivo en uso. Intentando lectura alternativa...")
            import shutil
            import tempfile

            temp_file = os.path.join(tempfile.gettempdir(), f"temp_{os.path.basename(file_path)}")
            try:
                shutil.copy2(file_path, temp_file)
                xls = pd.ExcelFile(temp_file)
                sheet = 'BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1]
                df = pd.read_excel(temp_file, sheet_name=sheet)
                os.remove(temp_file)
                log(f"   ✓ Hoja cargada (modo alternativo): {sheet}")
            except Exception as e:
                log(f"   ❌ Error: No se puede acceder al archivo")
                raise PermissionError(
                    f"\n\n{'='*70}\n"
                    f"ERROR: El archivo está abierto en otro programa\n"
                    f"{'='*70}\n"
                    f"SOLUCIONES:\n"
                    f"1. Cierra Microsoft Excel completamente\n"
                    f"2. Verifica en Administrador de Tareas que no haya Excel.exe corriendo\n"
                    f"3. Espera unos segundos y vuelve a ejecutar el script\n"
                    f"4. Si persiste, reinicia tu computadora\n"
                    f"{'='*70}\n"
                ) from e

    elif ext == '.csv':
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
        log("   ✓ CSV cargado correctamente")
    else:
        raise ValueError("Formato no compatible (solo .xlsx, .xls o .csv)")

    # Información básica
    log(f"   Dimensiones: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    log(f"   Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # ============================================================
    # VALIDAR QUE EXISTA LA COLUMNA 'AÑO'
    # ============================================================
    if 'AÑO' not in df.columns:
        log("   ⚠️ La columna 'AÑO' no fue encontrada en la base.")
        log("   ➜ Intentando extraer 'AÑO' desde la columna 'Fecha_intervencion'...")

        # Intentar crearla si existe la columna de fecha
        fecha_col = [col for col in df.columns if 'fecha' in col.lower()]
        if fecha_col:
            try:
                df['AÑO'] = pd.to_datetime(df[fecha_col[0]], errors='coerce').dt.year
                log(f"   ✓ Columna 'AÑO' creada a partir de '{fecha_col[0]}'")
            except Exception as e:
                log(f"   ❌ Error al crear columna 'AÑO': {e}")
        else:
            log("   ❌ No se encontró ninguna columna con nombre parecido a 'Fecha_intervencion'")
    else:
        log("   ✓ Columna 'AÑO' detectada correctamente en la base")

    # ============================================================
    # CARGAR CONFIGURACIÓN DESDE DATA UNDERSTANDING (si existe)
    # ============================================================
    understanding_config = os.path.join(BASE_DIR, "reports", "understanding", "config_understanding.json")
    global CODIGOS_VALIDOS

    if os.path.exists(understanding_config):
        with open(understanding_config, "r", encoding="utf-8") as f:
            config = json.load(f)
        CODIGOS_VALIDOS = config.get("codigos_validos", ["99999"])
        log(f"   ✓ Configuración importada desde: config_understanding.json")
        log(f"     Códigos válidos reconocidos: {CODIGOS_VALIDOS}")
    else:
        CODIGOS_VALIDOS = ["99999"]
        log("   ⚠️ No se encontró configuración de Understanding. Se usará 99999 por defecto.")

    return df

# ============================================================
# PASO 2: ESTANDARIZACIÓN DE NOMBRES DE COLUMNAS
# ============================================================

def paso2_estandarizar_columnas(df): 
    """Limpia y estandariza nombres de columnas""" 
    log("\n PASO 2: Estandarización de nombres de columnas") 
    log("-"*70) 
    
    original_cols = df.columns.tolist() 
    
    # Limpieza y normalización
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[^\w_]', '', regex=True)
        .str.upper()
    )
    
    # Eliminar guiones bajos duplicados
    df.columns = df.columns.str.replace(r'_+', '_', regex=True).str.strip('_')
    
    # Mapeo de cambios
    cambios = {orig: nuevo for orig, nuevo in zip(original_cols, df.columns) if orig != nuevo} 
    
    log(f" Columnas estandarizadas: {len(df.columns)} variables")
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
        'NOMBRE', 'APELLIDO', 'DOCUMENTO', 'CEDULA', 'IDENTIFICACION',
        'CORREO', 'EMAIL', 'MAIL',
        'RESPONSABLE', 'ACUDIENTE', 'TUTOR'
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
# PASO 3B: ELIMINACIÓN DE VARIABLES ADMINISTRATIVAS Y NO RELEVANTES
# ============================================================

def paso3b_eliminar_administrativas(df):
    """Elimina variables administrativas, de contacto y seguimiento individual que no aportan al análisis territorial/temporal"""
    log("\n PASO 3B: Eliminación de variables administrativas y no relevantes")
    log("-"*70)
    
    # Lista completa de columnas a eliminar (usando patrones parciales)
    admin_patterns = [
        # Variables administrativas
        'USUARIO', 'BASE_ORIGEN', 'RED_FIC', 'NOMBRE_EAPB', 
        
        # Información de contacto
        'TELEFONO', 'CORREO', 'DIRECCION_DE_LA_VIVIENDA', 'DIRECCION_DEL_TRABAJO',
        
        # Información muy granular
        'NUMERO_DE_MANZANA_DEL_CUIDADO', 'MANZANA_DEL_CUIDADO', 'NOMBRE_DE_LA_UT',
        
        # Variables de seguimiento individual
        'FECHA_SEGUIMIENTO_CIERRE', 'NNA_DESVINCULADO_DE_LA_ACTIVIDAD_LABORAL',
        'INTERVENCION_DE_NINO_NINA_O_ADOLESCENTE_QUE_TERMINA_EL_PROCESO',
        
        # Alertas individuales
        'ALERTAS_EN_NUTRICION', 'ALERTAS_PSICOSOCIALES', 'ALERTAS_SALUD_BUCAL',
        'ALERTAS_INFANCIA', 'ALERTAS_EN_MUJERES',
        
        # Variables clínicas individuales
        'ETAPA_DE_GESTACION', 'PESO', 'TALLA_CM', 'CLASIFICACION_NUTRICIONAL',
        'REQUIERE_ASESORIA_DE_NUTRICION', 'CATEGORIAS_DE_LA_DISCAPACIDAD',
        'CONDICIONES_CRONICAS',
        
        # Acompañamientos (perfiles individuales)
        'ACOMPANAMIENTO_1_PERFIL', 'ACOMPANAMIENTO_2_PERFIL',
        'ACOMPANAMIENTO_3_PERFIL', 'ACOMPANAMIENTO_4_PERFIL',
        
        # Temas tratados (demasiado específicos)
        'TEMAS_TRATADOS', 'IEC'
    ]
    
    # Identificar columnas que coincidan con los patrones
    cols_admin = []
    for col in df.columns:
        for pattern in admin_patterns:
            if pattern in col:
                cols_admin.append(col)
                break  # Una vez encontrada, no seguir buscando
    
    # Eliminar duplicados de la lista
    cols_admin = list(set(cols_admin))
    
    # Verificar qué columnas realmente existen antes de eliminar
    cols_existentes = [col for col in cols_admin if col in df.columns]
    
    if cols_existentes:
        df = df.drop(columns=cols_existentes)
        log(f" Variables administrativas eliminadas: {len(cols_existentes)}")
        log(f"\n   Categorías eliminadas:")
        
        # Agrupar por tipo para mejor visualización
        tipos = {
            'Administrativas': ['USUARIO', 'BASE_ORIGEN', 'RED_FIC', 'NOMBRE_EAPB', 'NOMBRE_DE_LA_UT'],
            'Contacto': ['TELEFONO', 'CORREO', 'DIRECCION'],
            'Geográficas granulares': ['MANZANA', 'NUMERO_DE_MANZANA'],
            'Seguimiento individual': ['FECHA_SEGUIMIENTO', 'NNA_DESVINCULADO', 'INTERVENCION'],
            'Alertas': ['ALERTAS'],
            'Clínicas': ['PESO', 'TALLA', 'NUTRICIONAL', 'GESTACION', 'DISCAPACIDAD', 'CRONICAS'],
            'Acompañamientos': ['ACOMPANAMIENTO'],
            'Intervención específica': ['TEMAS_TRATADOS', 'IEC']
        }
        
        for tipo, keywords in tipos.items():
            cols_tipo = [c for c in cols_existentes if any(kw in c for kw in keywords)]
            if cols_tipo:
                log(f"\n   {tipo} ({len(cols_tipo)}):")
                for col in sorted(cols_tipo):
                    log(f"      • {col}")
    else:
        log(" No se encontraron variables administrativas para eliminar")
    
    log(f"\n Columnas restantes: {len(df.columns)}")
    
    return df


# ============================================================
# PASO 4: LIMPIEZA DE INCONSISTENCIAS
# ============================================================

def paso4_limpiar_inconsistencias(df):
    """Limpieza general sin alterar los códigos válidos (como 99999)"""
    log("\n PASO 4: Limpieza de inconsistencias")
    log("-"*70)

    text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    log(f"   Columnas de texto detectadas: {len(text_cols)}")

    for col in text_cols:
        df[col] = df[col].apply(
            lambda x: re.sub(r'\s+', ' ', x.strip()) if isinstance(x, str) else x
        )
        df[col] = df[col].replace(
            ['nan', 'None', 'NULL', '', 'N/A', 'NA', 'n/a', 'na'], np.nan
        )

    # Limpieza de fechas
    date_cols = [c for c in df.columns if 'FECHA' in c.upper()]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            log(f"   ✓ Fecha estandarizada: {col}")
        except Exception:
            log(f"   ⚠ No se pudo convertir: {col}")

    # Eliminar duplicados completos
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        log(f"   ✓ Duplicados eliminados: {duplicates}")
    else:
        log("   ✓ No se encontraron duplicados completos")

    # Normalizar variables categóricas
    cat_estandar = {
        'SI': ['Si', 'sí', 'Sí', 'si', 'S', 's', 1],
        'NO': ['No', 'no', 'N', 'n', 0]
    }

    for col in text_cols:
        if df[col].nunique(dropna=True) < 25:
            for val, variants in cat_estandar.items():
                df[col] = df[col].replace(variants, val)

    log("   ✓ Limpieza de inconsistencias completada (manteniendo códigos válidos)")
    return df


# ============================================================
# PASO 5: MANEJO DE VALORES FALTANTES (elimina filas con "n/a", "na", etc.)
# ============================================================

def paso5_manejar_faltantes(df):
    """Elimina filas que contienen valores tipo 'n/a', 'na', 'null', '', etc., pero conserva 99999"""
    log("\n PASO 5: Manejo de valores faltantes (eliminando filas con valores tipo nulo)")
    log("-"*70)

    tables_dir = os.path.join(PREP_REPORTS_DIR, 'tables')
    figures_dir = os.path.join(PREP_REPORTS_DIR, 'figures')
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # ---------------------------
    # 1️⃣ Reemplazar variantes textuales de nulos por NaN
    # ---------------------------
    patrones_nulos = ['n/a', 'N/A', 'na', 'NA', 'Na', 'nan', 'Nan', 'None', 'NULL', 'null', '']
    
    text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    for col in text_cols:
        df[col] = df[col].replace(patrones_nulos, np.nan)

    log(f"   ✓ Limpieza textual aplicada a {len(text_cols)} columnas de texto")

    # ---------------------------
    # 2️⃣ Eliminar filas que contienen algún NaN real
    # ---------------------------
    filas_antes = len(df)
    df = df.dropna(how='any')  # elimina toda fila que tenga al menos un NaN real
    filas_despues = len(df)
    filas_eliminadas = filas_antes - filas_despues

    log(f"   ✓ Filas eliminadas por contener valores tipo nulo: {filas_eliminadas:,}")

    # ---------------------------
    # 3️⃣ Calcular completitud global (sin tocar los 99999)
    # ---------------------------
    total_celdas = len(df) * len(df.columns)
    total_nulos = int(df.isnull().sum().sum())
    porcentaje_valido = ((total_celdas - total_nulos) / total_celdas) * 100

    log(f"   🔹 Porcentaje global de datos válidos (sin nulos reales ni 'n/a'): {porcentaje_valido:.2f}%")
    log("   ✓ Limpieza completada (manteniendo códigos 99999)")

    # ---------------------------
    # 4️⃣ Reporte y gráfico
    # ---------------------------
    reporte_nulos = pd.DataFrame({
        'Variable': df.columns,
        'Nulos': df.isnull().sum().values,
        'Porcentaje': (df.isnull().sum() / len(df) * 100).round(3)
    }).sort_values('Porcentaje', ascending=False)

    reporte_nulos.to_excel(os.path.join(tables_dir, 'reporte_nulos.xlsx'), index=False)
    log("   ✓ Reporte de nulos reales generado")

    plt.figure(figsize=(10, 5))
    sns.histplot(reporte_nulos['Porcentaje'].clip(0, 100), bins=30)
    plt.title("Distribución de % de valores faltantes después de eliminar filas con 'n/a'")
    plt.xlabel("% valores faltantes")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'faltantes_distribucion.png'))
    plt.close()
    log("   ✓ Gráfico de distribución guardado")

    return df



# ============================================================
# PASO 6: ANÁLISIS EXPLORATORIO INICIAL
# ============================================================

def paso6_eda_inicial(df):
    """Análisis exploratorio de datos limpiados"""
    log("\n PASO 6: Análisis exploratorio inicial (EDA)")
    log("-"*70)
    
    # Estadísticas numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        stats = df[num_cols].describe().T
        stats.to_excel(os.path.join(PREP_REPORTS_DIR, "estadisticas_descriptivas.xlsx"))
        log(f"   ✓ Estadísticas descriptivas guardadas ({len(num_cols)} variables)")
    
    # Distribuciones categóricas
    cat_cols = df.select_dtypes(include=['object']).columns[:10]
    
    for col in cat_cols:
        if df[col].nunique() < 50:
            freq = df[col].value_counts().head(15)
            
            plt.figure(figsize=(10, 6))
            freq.plot(kind='barh', color='steelblue')
            plt.title(f"Distribución de {col}")
            plt.xlabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(os.path.join(PREP_FIGURES_DIR, f"dist_{col}.png"), dpi=150)
            plt.close()
    
    log(f"   ✓ Distribuciones categóricas generadas")
    
    # Análisis temporal
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
    
    return df


# ============================================================
# PASO 7: EXPORTACIÓN DE BASE FINAL
# ============================================================

# ============================================================
# PASO 7: EXPORTACIÓN DE BASE FINAL (con porcentaje global)
# ============================================================

def paso7_exportar_datos(df):
    """Exporta base de datos limpia y calcula el porcentaje global de retención"""
    log("\n PASO 7: Exportación de la base final")
    log("-"*70)

    # Guardar base en Excel y CSV
    df.to_excel(CLEANED_DATA_FILE, index=False, engine='openpyxl')
    log(f" Base limpia exportada a Excel")

    csv_file = CLEANED_DATA_FILE.replace('.xlsx', '.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    log(f" Base limpia exportada a CSV")

    # Calcular dimensiones finales
    filas_finales = df.shape[0]
    columnas_finales = df.shape[1]

    # Recuperar dimensiones iniciales (guardadas al inicio)
    try:
        filas_iniciales = FILAS_INICIALES
        columnas_iniciales = COLUMNAS_INICIALES
    except NameError:
        filas_iniciales = filas_finales
        columnas_iniciales = columnas_finales

    # Cálculos
    celdas_iniciales = filas_iniciales * columnas_iniciales
    celdas_finales = filas_finales * columnas_finales
    porcentaje_global = (celdas_finales / celdas_iniciales) * 100
    filas_eliminadas = filas_iniciales - filas_finales
    columnas_eliminadas = columnas_iniciales - columnas_finales

    # Log detallado
    log("\n 📊 RESULTADO FINAL DE LA BASE")
    log("----------------------------------------------------------------------")
    log(f"   • Filas iniciales:     {filas_iniciales:,}")
    log(f"   • Columnas iniciales:  {columnas_iniciales}")
    log(f"   • Filas finales:       {filas_finales:,}")
    log(f"   • Columnas finales:    {columnas_finales}")
    log(f"   • Filas eliminadas:    {filas_eliminadas:,}")
    log(f"   • Columnas eliminadas: {columnas_eliminadas}")
    log(f"\n   • Celdas iniciales:    {celdas_iniciales:,}")
    log(f"   • Celdas finales:      {celdas_finales:,}")
    log(f"   • 🔹 Porcentaje total de la base retenida: {porcentaje_global:.2f}%")
    log("----------------------------------------------------------------------")

    # Crear resumen JSON con toda la info
    resumen = {
        "fecha_procesamiento": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "dimensiones_iniciales": {
            "filas": int(filas_iniciales),
            "columnas": int(columnas_iniciales)
        },
        "dimensiones_finales": {
            "filas": int(filas_finales),
            "columnas": int(columnas_finales)
        },
        "transformacion": {
            "filas_eliminadas": int(filas_eliminadas),
            "columnas_eliminadas": int(columnas_eliminadas),
            "porcentaje_retencion_filas": round((filas_finales / filas_iniciales) * 100, 2),
            "porcentaje_retencion_columnas": round((columnas_finales / columnas_iniciales) * 100, 2),
            "porcentaje_retencion_global": round(porcentaje_global, 2)
        },
        "archivo_salida": os.path.basename(CLEANED_DATA_FILE),
        "tamaño_mb": float((df.memory_usage(deep=True).sum() / 1024**2).round(2))
    }

    with open(os.path.join(PREP_REPORTS_DIR, "resumen_final.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    log(f" Resumen final generado con porcentaje global de retención ({porcentaje_global:.2f}%)")

    return df

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Ejecuta todo el proceso de preparación"""
    inicio = datetime.now()
    
    # Variables globales para tracking
    global FILAS_INICIALES, COLUMNAS_INICIALES
    
    try:
        df = paso1_cargar_datos()
        
        # Guardar dimensiones originales
        FILAS_INICIALES = df.shape[0]
        COLUMNAS_INICIALES = df.shape[1]
        
        df = paso2_estandarizar_columnas(df)
        df = paso3_eliminar_pii(df)
        df = paso3b_eliminar_administrativas(df)  # ← NUEVO PASO
        df = paso4_limpiar_inconsistencias(df)
        df = paso5_manejar_faltantes(df)
        df = paso6_eda_inicial(df)
        df = paso7_exportar_datos(df)
        
        duracion = (datetime.now() - inicio).total_seconds()
        
        # Calcular porcentajes de retención
        filas_finales = df.shape[0]
        columnas_finales = df.shape[1]
        
        porcentaje_filas = (filas_finales / FILAS_INICIALES) * 100
        porcentaje_columnas = (columnas_finales / COLUMNAS_INICIALES) * 100
        
        filas_eliminadas = FILAS_INICIALES - filas_finales
        columnas_eliminadas = COLUMNAS_INICIALES - columnas_finales
        
        log("\n" + "="*70)
        log(" DATA PREPARATION COMPLETADO CON ÉXITO")
        log("="*70)
        log(f"\n 📊 RESUMEN DE TRANSFORMACIÓN:")
        log("-"*70)
        log(f"\n   FILAS (registros):")
        log(f"      • Iniciales:    {FILAS_INICIALES:>10,}")
        log(f"      • Finales:      {filas_finales:>10,}")
        log(f"      • Eliminadas:   {filas_eliminadas:>10,}")
        log(f"      • Retención:    {porcentaje_filas:>10.2f}%")
        log(f"\n   COLUMNAS (variables):")
        log(f"      • Iniciales:    {COLUMNAS_INICIALES:>10}")
        log(f"      • Finales:      {columnas_finales:>10}")
        log(f"      • Eliminadas:   {columnas_eliminadas:>10}")
        log(f"      • Retención:    {porcentaje_columnas:>10.2f}%")
        log(f"\n   DATOS TOTALES:")
        log(f"      • Celdas iniciales: {FILAS_INICIALES * COLUMNAS_INICIALES:>12,}")
        log(f"      • Celdas finales:   {filas_finales * columnas_finales:>12,}")
        log(f"      • Retención global: {((filas_finales * columnas_finales) / (FILAS_INICIALES * COLUMNAS_INICIALES)) * 100:>11.2f}%")
        log(f"\n   TIEMPO:")
        log(f"      • Ejecución:    {duracion:>10.2f} segundos")
        log(f"\n 📁 Archivos generados:")
        log(f"      • Base limpia: {os.path.basename(CLEANED_DATA_FILE)}")
        log(f"      • Reportes: {os.path.basename(PREP_REPORTS_DIR)}/")
        log("\n" + "="*70)
        
    except Exception as e:
        log(f"\n ERROR: {str(e)}") 
        import traceback
        traceback.print_exc()
    
    finally:
        with open(PREP_LOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(log_entries))
        log(f"\n📄 Log guardado en: {PREP_LOG_FILE}") 


if __name__ == "__main__":
    main()

    # ============================================================
# BLOQUE FINAL - RESUMEN GLOBAL CONSOLIDADO (solo texto)
# ============================================================

def resumen_global(df):
    """Genera un resumen textual con todos los resultados clave obtenidos"""
    print("\n" + "="*80)
    print("🔹 RESUMEN GLOBAL - DATA PREPARATION NNA BOGOTÁ (2021–2025)")
    print("="*80)

    # Dimensiones
    filas, columnas = df.shape
    print(f"\n📊 Dimensiones finales de la base limpia:")
    print(f"   • Filas: {filas:,}")
    print(f"   • Columnas: {columnas}")

    # Tipos de datos
    tipos = df.dtypes.value_counts()
    print(f"\n🔍 Tipos de datos:")
    for tipo, count in tipos.items():
        print(f"   • {tipo}: {count}")

    # Porcentaje de nulos global
    total_celdas = len(df) * len(df.columns)
    total_nulos = int(df.isnull().sum().sum())
    porcentaje_valido = ((total_celdas - total_nulos) / total_celdas) * 100
    print(f"\n💧 Calidad de datos:")
    print(f"   • Celdas totales: {total_celdas:,}")
    print(f"   • Celdas nulas: {total_nulos:,}")
    print(f"   • Porcentaje de datos válidos: {porcentaje_valido:.2f}%")

    # Estadísticas básicas de variables numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        desc = df[num_cols].describe().T[['mean', 'std', 'min', 'max']].round(2)
        print("\n📈 Variables numéricas (resumen):")
        print(desc.head(10).to_string())
    else:
        print("\n📈 No se detectaron variables numéricas.")

    # Variables categóricas con más frecuencia
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        print("\n🔠 Variables categóricas (frecuencias más altas):")
        for col in cat_cols[:5]:
            print(f"\n   ▪ {col}:")
            print(df[col].value_counts(dropna=False).head(3).to_string())
    else:
        print("\n🔠 No se detectaron variables categóricas.")

    # Años de intervención
    if 'AÑO' in df.columns:
        print("\n🕒 Distribución por año de intervención:")
        print(df['AÑO'].value_counts().sort_index().to_string())
    else:
        print("\n🕒 No se encontró la columna 'AÑO' para distribución temporal.")

    # Tamaño del archivo exportado
    size_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"\n💾 Tamaño aproximado de la base final en memoria: {size_mb:.2f} MB")

    print("\n✅ FIN DEL RESUMEN GLOBAL")
    print("="*80)
    print()


# ============================================================
# EJECUCIÓN DEL BLOQUE FINAL
# ============================================================
if __name__ == "__main__":
    main()
    
    try:
        # Si main() crea df y no lo devuelve, puedes volver a cargarlo
        df_final = pd.read_excel(CLEANED_DATA_FILE, engine='openpyxl')
        resumen_global(df_final)
    except Exception as e:
        print(f"\n⚠️ No se pudo generar el resumen global automáticamente: {e}")
