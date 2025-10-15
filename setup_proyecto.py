"""
============================================================
SCRIPT DE CONFIGURACIÓN AUTOMÁTICA
Proyecto: Análisis NNA Bogotá (2021-2025)
============================================================

Este script crea automáticamente toda la estructura del proyecto:
- Carpetas necesarias
- Archivos de configuración
- Scripts principales
- Documentación

EJECUCIÓN:
    python setup_proyecto.py

============================================================
"""

import os # Para crear carpetas y manejar rutas
import sys # Para interactuar con el sistema

def crear_estructura_carpetas():
    """Crea la estructura de carpetas del proyecto"""
    carpetas = [
        'scripts', # Carpeta para scripts de Python
        'data/raw', # Carpeta para los datos originales
        'reports', # Carpeta general de reportes
        'reports/tables', # Subcarpeta para tablas generadas
        'reports/figures', # Subcarpeta para gráficos
        'reports/figures/temporal', # Gráficos temporales
        'reports/figures/spatial', # Gráficos espaciales
        'reports/figures/exploratory' # Gráficos exploratorios
    ]
    
    print(" Creando estructura de carpetas...")
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)  # Crea la carpeta si no existe
        print(f"   ✓ {carpeta}") # Confirma creación de cada carpeta
    print()

# Función que crea el archivo .env con la ruta de datos
def crear_env():
    """Crea el archivo .env"""
    contenido = """# ============================================================
# ARCHIVO DE CONFIGURACIÓN - Proyecto NNA Bogotá
# ============================================================

# Ruta al archivo de datos (puede ser .xlsx, .xls o .csv)
# IMPORTANTE: Actualiza esta ruta con la ubicación real de tu archivo

# Opción 1: Ruta relativa (recomendada)
DATA_FILE=data/raw/base_datos_completa_NNA_TI_anon.xlsx

# Opción 2: Ruta absoluta (descomenta si la relativa no funciona)
# DATA_FILE=C:/Users/ASUS/OneDrive - Universidad Santo Tomás/SANTO TOMAS/8-SEMESTRE/PYTHON/Analisis_EspacioTemporal_NNA_Bogota_2021_2025/data/raw/base_datos_completa_NNA_TI_anon.xlsx

# ============================================================
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(contenido) # Guarda el contenido en .env
    
    print(" Archivo .env creado") # Confirma creación

# Función que crea el archivo requirements.txt con dependencias necesarias
def crear_requirements():
    """Crea el archivo requirements.txt"""
    contenido = """# ============================================================
# DEPENDENCIAS - Proyecto NNA Bogotá
# ============================================================
# INSTALACIÓN:
# pip install -r requirements.txt
# ============================================================

# Manejo de datos
pandas==2.2.3
numpy==2.3.3

# Visualizaciones
matplotlib==3.9.2
seaborn==0.13.2

# Variables de entorno
python-dotenv==1.0.1

# Análisis adicionales
scipy==1.15.3
scikit-learn==1.5.2
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(contenido) # Escribe las dependencias en el archivo
    
    print(" Archivo requirements.txt creado") # Confirma creación

# Función que crea .gitignore para ignorar archivos no deseados en Github
def crear_gitignore():
    """Crea el archivo .gitignore"""
    contenido = """# ============================================================
# .gitignore - Proyecto NNA Bogotá
# ============================================================

# Archivos de configuración sensibles
.env

# Datos (no subir datos reales)
data/raw/*.xlsx
data/raw/*.xls
data/raw/*.csv
data/processed/

# Reportes generados
reports/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Sistema operativo
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(contenido)# Guarda contenido en .gitignore
    
    print(" Archivo .gitignore creado")# Confirma creación

# Función que crea README.md con información del proyecto
def crear_readme():
    """Crea el archivo README.md"""
    contenido = """#  Data Understanding - Proyecto NNA Bogotá (2021-2025)

Análisis exploratorio completo de intervenciones con Niños, Niñas y Adolescentes en Bogotá, incluyendo análisis espacio-temporal y de contexto social.

##  Características principales

-  **Carga automática** de archivos Excel (.xlsx, .xls) o CSV
-  **Limpieza y normalización** de columnas
-  **Anonimización** de datos sensibles
-  **Diccionario de datos** completo y automático
-  **Análisis exploratorio exhaustivo** de todas las variables
-  **Análisis espacio-temporal** con detección de tendencias
-  **Análisis de régimen de salud** y contexto social
-  **Identificación de zonas de alerta** por cambios significativos
-  **Visualizaciones automáticas** (gráficos, mapas de calor, correlaciones)
-  **Reportes en múltiples formatos** (Excel, CSV, JSON, Markdown)

---

##  Instalación rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar archivo .env (editar con tu ruta de datos)
# Abrir .env y actualizar DATA_FILE

# 3. Ejecutar análisis
python scripts/data_understanding.py
```

---

##  Estructura del proyecto

```
Analisis_EspacioTemporal_NNA_Bogota_2021_2025/
│
├── data/
│   └── raw/                           # Tus archivos de datos
│       └── base_datos_completa_NNA_TI_anon.xlsx
│
├── scripts/
│   └── data_understanding.py          # Script principal
│
├── reports/                           # Se genera automáticamente
│   ├── data_summary.md                # Reporte principal
│   ├── tables/                        # Tablas generadas
│   └── figures/                       # Gráficos generados
│       ├── temporal/
│       ├── spatial/
│       └── exploratory/
│
├── .env                               # Configuración (EDITAR)
├── .gitignore                         # Archivos ignorados por Git
├── requirements.txt                   # Dependencias
└── README.md                          # Este archivo
```

---

## ▶ Uso detallado

### Configuración inicial

1. **Edita el archivo `.env`** y actualiza la ruta de tu archivo de datos:
   ```bash
   DATA_FILE=data/raw/tu_archivo.xlsx
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

**Desde la terminal:**
```bash
python scripts/data_understanding.py
```

**Desde VS Code:**
1. Abre `scripts/data_understanding.py`
2. Presiona `F5` o click en Run ▶

---

##  Resultados generados

### Tablas (Excel/CSV)
- `diccionario_datos.xlsx` - Descripción completa de variables
- `distribucion_localidad_año.csv` - Datos espacio-temporales
- `tendencias_por_localidad.xlsx` - Análisis de cambios
- `zonas_alerta.csv` - Localidades con cambios significativos
- `regimen_por_localidad_porcentaje.xlsx` - Distribución de afiliación
- Y más...

### Visualizaciones (PNG)
- Evolución temporal de intervenciones
- Mapas de calor localidad × año
- Distribución por régimen de salud
- Matrices de correlación
- Histogramas y gráficos de barras
- Y más...

### Reporte
- `data_summary.md` - Documento Markdown con resumen completo

---

##  Objetivos del análisis

1. **Describir** la distribución de intervenciones por localidad y año
2. **Identificar** localidades con aumentos o disminuciones significativas
3. **Relacionar** cambios con el tipo de afiliación en salud

---

##  Solución de problemas

### Error: "No se encontró DATA_FILE"
- Verifica que existe el archivo `.env`
- Asegúrate de que `DATA_FILE` tenga la ruta correcta

### Error: "No se encontró el archivo"
- Verifica la ruta en `.env`
- Prueba con ruta absoluta si la relativa no funciona

### Error: "ModuleNotFoundError"
- Ejecuta: `pip install -r requirements.txt`

---

##  Notas importantes

-  **Privacidad**: El script anonimiza automáticamente datos sensibles
-  **Tiempo**: Archivos grandes pueden tardar varios minutos
-  **Espacio**: Reserva ~500MB para reportes y figuras

---

##  Contacto

Para dudas o problemas, revisar la documentación en el código fuente.

---

**Metodología**: CRISP-DM (Cross-Industry Standard Process for Data Mining)
**Última actualización**: Octubre 2025
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(" Archivo README.md creado")


def crear_data_understanding():
    """Crea el script principal data_understanding.py"""
    # Aquí va el código completo del script data_understanding.py
    contenido = '''# ============================================================
# DATA UNDERSTANDING - Proyecto NNA Bogotá (2021–2025)
# Versión extendida con análisis espacio-temporal
# ============================================================

import os
import pandas as pd
import numpy as np
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from datetime import datetime
import warnings
import json

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")

# ============================================================
# 1. CONFIGURACIÓN DE RUTAS
# ============================================================

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.getenv("DATA_FILE")

if not DATA_FILE:
    raise ValueError(" No se encontró la variable DATA_FILE en el archivo .env")

file_path = os.path.join(BASE_DIR, DATA_FILE)

if not os.path.exists(file_path):
    raise FileNotFoundError(f" No se encontró el archivo: {file_path}")

# Estructura de carpetas
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")
TEMPORAL_DIR = os.path.join(FIGURES_DIR, "temporal")
SPATIAL_DIR = os.path.join(FIGURES_DIR, "spatial")
EXPLORATORY_DIR = os.path.join(FIGURES_DIR, "exploratory")
SUMMARY_FILE = os.path.join(REPORTS_DIR, "data_summary.md")
ALERT_ZONES_FILE = os.path.join(TABLES_DIR, "zonas_alerta.csv")

for path in [REPORTS_DIR, FIGURES_DIR, TABLES_DIR, TEMPORAL_DIR, SPATIAL_DIR, EXPLORATORY_DIR]:
    os.makedirs(path, exist_ok=True)

print(f" Estructura de carpetas creada en: {REPORTS_DIR}")


# ============================================================
# 2. CARGA DE DATOS CON DETECCIÓN AUTOMÁTICA
# ============================================================

def load_data(file_path):
    """Carga datos desde Excel o CSV con detección automática"""
    ext = os.path.splitext(file_path)[-1].lower()
    
    print(f" Cargando archivo: {os.path.basename(file_path)}")
    
    if ext in ['.xlsx', '.xls']:
        xls = pd.ExcelFile(file_path)
        print(f"   Hojas disponibles: {xls.sheet_names}")
        sheet = 'BD' if 'BD' in xls.sheet_names else xls.sheet_names[-1]
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"   ✓ Cargada hoja: {sheet}")
    elif ext == '.csv':
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
        print(f"   ✓ CSV cargado con detección automática de separador")
    else:
        raise ValueError(" Formato no compatible. Usa .csv, .xlsx o .xls")
    
    print(f" Datos cargados: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    return df


# ============================================================
# 3. LIMPIEZA Y NORMALIZACIÓN
# ============================================================

def clean_columns(df):
    """Limpia y normaliza nombres de columnas"""
    original_cols = df.columns.tolist()
    
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace(r'[^\\w]', '', regex=True)
        .str.upper()
    )
    
    col_mapping = dict(zip(original_cols, df.columns))
    with open(os.path.join(TABLES_DIR, "column_mapping.json"), "w", encoding="utf-8") as f:
        json.dump(col_mapping, f, indent=2, ensure_ascii=False)
    
    print(f" Columnas normalizadas: {len(df.columns)} variables")
    return df


def anonymize(df):
    """Anonimiza información sensible"""
    sensitive_cols = [
        'USUARIO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO', 'ID_USUARIO',
        'DIRECCIÓN', 'DIRECCION', 'DIRECCIÓN_DE_LA_VIVIENDA', 'DIRECCION_VIVIENDA',
        'CORREO', 'CORREO_1', 'CORREO_2', 'EMAIL', 'MAIL',
        'TELÉFONO', 'TELEFONO', 'TELÉFONO_1', 'TELÉFONO_2', 'TELEFONO_1', 'TELEFONO_2', 'CELULAR',
        'NOMBRE_EAPB', 'NOMBRE_EAPB1', 'RESPONSABLE', 'ACUDIENTE'
    ]
    
    removed = [c for c in sensitive_cols if c in df.columns]
    df.drop(columns=removed, inplace=True, errors='ignore')
    
    id_cols = [c for c in df.columns if 'ID' in c and c not in ['ID_LOCALIDAD', 'ID_UPZ']]
    for col in id_cols:
        if df[col].dtype == 'object' or pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16] if pd.notna(x) else x)
    
    print(f" Anonimización completa: {len(removed)} columnas eliminadas, {len(id_cols)} IDs encriptados")
    return df


# ============================================================
# 4. DETECCIÓN AUTOMÁTICA DE VARIABLES TEMPORALES
# ============================================================

def detect_temporal_columns(df):
    """Detecta y procesa columnas de fecha/año"""
    temporal_info = {}
    
    date_candidates = [c for c in df.columns if any(x in c for x in ['FECHA', 'DATE', 'AÑO', 'ANO', 'YEAR', 'MES', 'MONTH'])]
    
    for col in date_candidates:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            temporal_info[col] = 'datetime'
        elif df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                temporal_info[col] = 'datetime_converted'
            except:
                pass
    
    for col in temporal_info.keys():
        if 'AÑO' not in df.columns and 'YEAR' not in df.columns:
            df['AÑO'] = df[col].dt.year
            print(f"   ✓ Columna 'AÑO' extraída de {col}")
    
    year_cols = [c for c in df.columns if c in ['AÑO', 'ANO', 'YEAR', 'ANIO']]
    if year_cols:
        df['AÑO'] = pd.to_numeric(df[year_cols[0]], errors='coerce')
    
    if 'AÑO' in df.columns:
        years = df['AÑO'].dropna().unique()
        print(f" Años detectados: {sorted([int(y) for y in years if not np.isnan(y)])}")
        temporal_info['years_available'] = sorted([int(y) for y in years if not np.isnan(y)])
    else:
        print("  No se detectó columna de año")
    
    return df, temporal_info


# [CONTINÚA EN EL SIGUIENTE MENSAJE - El código es muy largo]
# Por limitaciones de espacio, te mostraré cómo crear el archivo completo...
'''
    
    print("  Creando script data_understanding.py...")
    print("   Por favor, copia el código completo del artifact 'data_understanding_nna'")
    print("   y pégalo en: scripts/data_understanding.py")
    print()


def main():
    """Ejecuta la configuración completa del proyecto"""
    print("="*70)
    print(" CONFIGURACIÓN AUTOMÁTICA DEL PROYECTO")
    print("   Análisis NNA Bogotá (2021-2025)")
    print("="*70)
    print()
    
    # Crear estructura
    crear_estructura_carpetas()
    crear_env()
    crear_requirements()
    crear_gitignore()
    crear_readme()
    
    print("="*70)
    print(" CONFIGURACIÓN COMPLETADA")
    print("="*70)
    print()
    print(" PRÓXIMOS PASOS:")
    print()
    print("1.  Copia el código del artifact 'data_understanding_nna' completo")
    print("   y pégalo en: scripts/data_understanding.py")
    print()
    print("2.   Edita el archivo .env y actualiza la ruta de tus datos:")
    print("   DATA_FILE=data/raw/tu_archivo.xlsx")
    print()
    print("3.  Instala las dependencias:")
    print("   pip install -r requirements.txt")
    print()
    print("4.   Ejecuta el análisis:")
    print("   python scripts/data_understanding.py")
    print()
    print("="*70)
    print()
    print(" Archivos creados:")
    print("   ✓ .env")
    print("   ✓ .gitignore") 
    print("   ✓ requirements.txt")
    print("   ✓ README.md")
    print("   ✓ Estructura de carpetas")
    print()
    print("  PENDIENTE: Crear scripts/data_understanding.py")
    print("   (Copia el código del artifact que te compartí)")
    print()


if __name__ == "__main__":
    try:
        main()  # Ejecuta la configuración completa
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()# Muestra traceback completo