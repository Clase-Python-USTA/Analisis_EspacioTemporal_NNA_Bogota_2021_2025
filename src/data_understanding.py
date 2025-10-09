# ============================================================
# DATA UNDERSTANDING - Proyecto NNA Bogotá (2021–2025)
# ============================================================

import os
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. CONFIGURACIÓN DE RUTAS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # raíz del proyecto
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")

# Crear carpetas si no existen
for path in [REPORTS_DIR, FIGURES_DIR, TABLES_DIR]:
    os.makedirs(path, exist_ok=True)


# ============================================================
# 2. FUNCIÓN DE CARGA AUTOMÁTICA
# ============================================================

def load_data(file_path):
    """Carga un Excel o CSV detectando hoja o separador automáticamente."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext in ['.xlsx', '.xls']:
        xls = pd.ExcelFile(file_path)
        print(f"Hojas disponibles: {xls.sheet_names}")
        df = pd.read_excel(file_path, sheet_name='BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1])
    elif ext in ['.csv']:
        df = pd.read_csv(file_path, sep=None, engine='python')
    else:
        raise ValueError("Formato no compatible. Usa .csv o .xlsx")

    print(f"✅ Archivo cargado: {df.shape[0]} filas × {df.shape[1]} columnas.")
    return df


# ============================================================
# 3. LIMPIEZA Y ANONIMIZACIÓN
# ============================================================

def clean_columns(df):
    """Limpia nombres de columnas."""
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
        .str.upper()
    )
    return df


def anonymize(df):
    """Elimina columnas sensibles y anonimiza ID."""
    sensitive_cols = [
        'USUARIO', 'DIRECCIÓN_DE_LA_VIVIENDA', 'CORREO_1', 'CORREO_2',
        'TELÉFONO_1', 'TELÉFONO_2', 'NOMBRE_EAPB', 'NOMBRE_EAPB1'
    ]
    df = df.drop(columns=[c for c in sensitive_cols if c in df.columns], errors='ignore')

    if 'ID_FIC' in df.columns:
        df['ID_FIC'] = df['ID_FIC'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

    print("✅ Columnas sensibles eliminadas y datos anonimizados.")
    return df


# ============================================================
# 4. DICCIONARIO DE DATOS
# ============================================================

def generate_dictionary(df):
    """Genera diccionario con tipo, nulos y valores únicos."""
    dic = pd.DataFrame({
        "Tipo_de_dato": df.dtypes,
        "Valores_nulos": df.isnull().sum(),
        "Porcentaje_nulos": (df.isnull().sum() / len(df)) * 100,
        "Valores_únicos": df.nunique()
    })
    dic.to_excel(os.path.join(TABLES_DIR, "diccionario_datos.xlsx"))
    print("📘 Diccionario de datos guardado.")
    return dic


# ============================================================
# 5. CHEQUEO DE CALIDAD
# ============================================================

def quality_report(df):
    """Detecta duplicados y columnas problemáticas."""
    constantes = [c for c in df.columns if df[c].nunique() == 1]
    duplicados = df.duplicated().sum()
    muchas_categorias = [c for c in df.columns if df[c].dtype == 'object' and df[c].nunique() > 50]

    resumen = {
        "columnas_constantes": len(constantes),
        "filas_duplicadas": duplicados,
        "columnas_con_muchas_categorias": len(muchas_categorias)
    }

    pd.Series(resumen).to_csv(os.path.join(TABLES_DIR, "quality_report.csv"))
    print("🧾 Reporte de calidad generado.")
    return resumen


# ============================================================
# 6. EXPLORACIÓN Y RESÚMENES
# ============================================================

def summarize_data(df):
    """Crea resúmenes estadísticos básicos."""
    num_summary = df.describe().T
    cat_summary = df.select_dtypes('object').describe().T

    num_summary.to_csv(os.path.join(TABLES_DIR, "resumen_numerico.csv"))
    cat_summary.to_csv(os.path.join(TABLES_DIR, "resumen_categorico.csv"))
    print("📊 Resúmenes estadísticos guardados.")
    return num_summary, cat_summary


# ============================================================
# 7. VISUALIZACIONES
# ============================================================

def plot_missing(df):
    """Gráfico de porcentaje de valores faltantes."""
    missing = df.isnull().mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing.head(15), y=missing.head(15).index)
    plt.title("Porcentaje de valores faltantes (Top 15)")
    plt.xlabel("Porcentaje")
    plt.ylabel("Variable")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "missing_values.png"))
    plt.close()


def plot_correlation(df):
    """Matriz de correlaciones."""
    corr = df.select_dtypes('number').corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap='coolwarm', center=0)
    plt.title("Matriz de correlaciones numéricas")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "correlation_matrix.png"))
    plt.close()


# ============================================================
# 8. EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    print("🚀 Iniciando proceso de Data Understanding...")

    file_path = os.path.join(DATA_DIR, "raw", "base_datos_completa_NNA_TI_anon.xlsx")
    df = load_data(file_path)
    df = clean_columns(df)
    df = anonymize(df)

    dic = generate_dictionary(df)
    quality = quality_report(df)
    summarize_data(df)

    plot_missing(df)
    plot_correlation(df)

    print("\n✅ Data Understanding completado con éxito.")
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    print(f"Reportes guardados en: {REPORTS_DIR}")


# ============================================================
# 9. EJECUCIÓN DESDE TERMINAL
# ============================================================

if __name__ == "__main__":
    main()
