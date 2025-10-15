#  Data Understanding - Proyecto NNA Bogotá (2021-2025)

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
