# ============================================================
# SCRIPT: LISTAR REPORTES Y FIGURAS GENERADAS
# Proyecto NNA Bogotá (2021–2025)
# ============================================================

import os
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
FINAL_FIG_DIR = os.path.join(FIGURES_DIR, "final")

# ============================================================
# Función para listar archivos de un directorio
# ============================================================

def listar_archivos(directorio, extensiones=None):
    archivos = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if not extensiones or file.lower().endswith(tuple(extensiones)):
                ruta_relativa = os.path.relpath(os.path.join(root, file), BASE_DIR)
                archivos.append({
                    "Archivo": file,
                    "Ruta relativa": ruta_relativa.replace("\\", "/"),
                    "Ubicación": os.path.basename(root),
                    "Fecha_modificación": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).strftime("%Y-%m-%d %H:%M")
                })
    return archivos

# ============================================================
# Recolectar reportes por tipo
# ============================================================

reportes_excel = listar_archivos(TABLES_DIR, [".xlsx", ".xls"])
reportes_csv = listar_archivos(TABLES_DIR, [".csv"])
reportes_json = listar_archivos(TABLES_DIR, [".json"])
figuras_png = listar_archivos(FIGURES_DIR, [".png"])
reportes_md = listar_archivos(REPORTS_DIR, [".md"])

# ============================================================
# Consolidar todo en un solo DataFrame
# ============================================================

todos_reportes = (
    pd.DataFrame(reportes_excel + reportes_csv + reportes_json + figuras_png + reportes_md)
    .sort_values(by=["Ubicación", "Archivo"])
    .reset_index(drop=True)
)

# ============================================================
# Guardar el resumen como Excel y Markdown
# ============================================================

output_excel = os.path.join(REPORTS_DIR, "resumen_archivos_generados.xlsx")
output_md = os.path.join(REPORTS_DIR, "resumen_archivos_generados.md")

todos_reportes.to_excel(output_excel, index=False)

# Exportar versión Markdown
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# 📂 Resumen de archivos generados - Proyecto NNA Bogotá (2021–2025)\n\n")
    f.write(f"**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("| Archivo | Ubicación | Fecha modificación | Ruta relativa |\n")
    f.write("|----------|------------|--------------------|----------------|\n")
    for _, row in todos_reportes.iterrows():
        f.write(f"| {row['Archivo']} | {row['Ubicación']} | {row['Fecha_modificación']} | `{row['Ruta relativa']}` |\n")

print("✅ Resumen generado correctamente.")
print(f"📁 Archivo Excel: {output_excel}")
print(f"📄 Archivo Markdown: {output_md}")
print(f"🖼️ Total de elementos listados: {len(todos_reportes)}")
