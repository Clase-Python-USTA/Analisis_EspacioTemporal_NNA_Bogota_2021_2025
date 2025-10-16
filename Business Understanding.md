

# Business Understanding

## Contexto general
Este proyecto busca entender cómo han cambiado las intervenciones con niños, niñas y adolescentes (NNA) en Bogotá entre los años 2021 y 2025, analizando los cambios en el tiempo y en las diferentes localidades de la ciudad.  
La idea es ver en qué zonas han aumentado o disminuido los casos y revisar si esos cambios tienen alguna relación con las condiciones sociales de la población, usando como referencia el tipo de afiliación en salud, especialmente el régimen subsidiado.  

De esta forma, no solo se observa el comportamiento de las intervenciones, sino también si existen diferencias entre las localidades según su contexto social. Esto puede ayudar a reconocer posibles desigualdades y a identificar zonas donde se deberían fortalecer las acciones o los programas.  

---

## Propósito del proyecto
Comprender los patrones de cambio de las intervenciones con NNA en Bogotá, tanto en el tiempo como en el territorio, y reconocer si existen diferencias relacionadas con el tipo de afiliación en salud, en especial el régimen subsidiado. Con esto se busca obtener una visión más completa que sirva para orientar decisiones o futuras estrategias de intervención.  

---

## Objetivo general
Analizar cómo han cambiado las intervenciones con niños, niñas y adolescentes (NNA) en las diferentes localidades de Bogotá entre 2021 y 2025, identificando las zonas donde los casos han aumentado o disminuido y relacionando esos cambios con las condiciones sociales de la población, tomando como referencia el tipo de afiliación en salud, especialmente el régimen subsidiado.  

---

## Objetivos específicos
1. Describir la distribución de las intervenciones con NNA por localidad y por año entre 2021 y 2025.  
2. Identificar las localidades con aumento o disminución en el número de intervenciones a lo largo del tiempo.  
3. Aproximar una primera relación entre el comportamiento de las intervenciones y el tipo de afiliación en salud, con énfasis en el régimen subsidiado.  

---

## Preguntas guía
- ¿En qué localidades han aumentado o disminuido las intervenciones con NNA entre 2021 y 2025?  
- ¿Qué características tienen las localidades con mayor crecimiento o concentración de casos?  
- ¿Se puede observar alguna relación entre el comportamiento de las intervenciones y el tipo de afiliación en salud, especialmente el régimen subsidiado?  

---

## Alcance
El análisis se centrará en los registros de intervenciones con NNA entre 2021 y 2025, teniendo en cuenta las variables de localidad, año y régimen de afiliación en salud.  
El objetivo no es demostrar una relación causal, sino explorar y describir cómo varían los casos según el territorio y las condiciones sociales.  

---

## Resultados esperados
- Conocer cómo cambian las intervenciones con NNA a lo largo del tiempo y en cada localidad.  
- Identificar las zonas donde hay más concentración o crecimiento de casos.  
- Tener una primera aproximación a la relación entre las intervenciones y el tipo de afiliación en salud.  
- Aportar información útil para fortalecer las estrategias de atención y protección a la niñez y adolescencia en Bogotá.  

---

##  Glosario
A continuación, se presentan los términos clave que se usarán en el análisis:  

| **Término** | **Definición** |
|--------------|----------------|
| **NNA** | Sigla que significa *Niños, Niñas y Adolescentes*. Hace referencia a la población menor de 18 años objeto de las intervenciones analizadas. |
| **Intervención** | Acción o proceso desarrollado por una entidad o programa para atender, proteger o acompañar a un niño, niña o adolescente. |
| **Análisis espacio-temporal** | Tipo de estudio que combina la información geográfica (espacial) y el tiempo (temporal) para identificar cómo cambian los casos o eventos según la zona y el año. |
| **Localidad** | División territorial de Bogotá que agrupa diferentes barrios. En total, la ciudad cuenta con 20 localidades. |
| **Régimen de afiliación en salud** | Forma en que las personas están vinculadas al sistema de salud. Los principales son: *régimen contributivo* (para quienes cotizan) y *régimen subsidiado* (para personas en situación de vulnerabilidad). |
| **Régimen subsidiado** | Tipo de afiliación en salud dirigido a la población con menores ingresos o en condición de vulnerabilidad, financiado con recursos del Estado. |
| **Zona de alerta** | Localidad donde se observa un aumento importante o sostenido en el número de intervenciones, lo que puede requerir atención prioritaria. |


# 2. Data Understanding

## 2.1. Análisis general de la base

Durante esta fase se realizó un proceso sistemático para comprender la estructura, la calidad y las características de la base de datos **“base_datos_completa_NNA_TI_anon.xlsx”**, que contiene **56.473 registros y 115 columnas** en su versión original.  
El análisis se centró en la hoja **BD**, que incluye la información consolidada y anonimizada de las intervenciones con niños, niñas y adolescentes (NNA) en Bogotá entre **2021 y 2025**.

El flujo de procesamiento permitió identificar y documentar variables clave, evaluar la calidad de los datos, detectar valores faltantes y obtener una primera visión descriptiva y espacial de las intervenciones registradas.

---

## 2.2. Estructura y características de los datos

Tras la limpieza inicial y normalización de variables:

| **Indicador** | **Resultado** |
|----------------|----------------|
| Filas procesadas | 56,473 |
| Columnas analizadas | 114 |
| Columnas constantes (sin variación) | 12 |
| Duplicados detectados | 3,690 |
| Tipos de variables | 93 categóricas y 25 numéricas |
| Cobertura temporal | 2021–2025 |
| Hoja analizada | BD |

Se verificó que la base se encuentra **completamente anonimizada**, por lo que no contiene información personal identificable (PII).  

Se construyó un **diccionario de datos** con las 114 variables documentadas, especificando su tipo, descripción y valores posibles, para garantizar la trazabilidad de cada campo en las siguientes fases.

---

## 2.3. Análisis de calidad de los datos

Durante la verificación de calidad se identificaron los siguientes resultados:

| **Indicador** | **Resultado** |
|----------------|----------------|
| Duplicados detectados | 3,690 |
| Columnas constantes | 12 |
| Promedio general de valores faltantes | 4.86% |
| Columnas con más del 90% de nulos | FECHA_DE_LA_ÚLTIMA_INTERVENCIÓN, FECHA1, FECHA, FECHA2 |
| Código especial identificado | 99999 (representa valores “no aplica” o “sin respuesta”) |

Estos resultados indican que la base presenta **un nivel de calidad alto (99.8%)**, con un porcentaje bajo de valores faltantes y sin presencia significativa de errores estructurales.

---

## 2.4. Análisis de valores faltantes

El proceso de evaluación de faltantes generó los siguientes productos:

📄 **Archivos generados:**
- `reporte_nulos.xlsx`: número y porcentaje de valores faltantes por variable.  
- `reporte_99999.xlsx`: frecuencias y proporciones del código “99999”.  
- `valores_faltantes.png`: gráfico de barras con las 20 variables con mayor porcentaje de nulos.  
- `proporcion_faltantes_global.png`: gráfico de pastel con la proporción total de datos completos y faltantes.  

| **Indicador** | **Resultado** |
|----------------|----------------|
| Total de valores faltantes | 274,356 |
| Porcentaje global de faltantes | 4.86% |
| Columnas con >90% de nulos | FECHA_DE_LA_ÚLTIMA_INTERVENCIÓN, FECHA1, FECHA, FECHA2 |
| Promedio general de nulos | 4.86% |
| Código especial detectado | 99999 |

**Interpretación:**  
El 95% de las variables tiene menos del 10% de valores faltantes, lo cual garantiza estabilidad estadística para los análisis.  
Las columnas con mayor proporción de nulos corresponden a **fechas de seguimiento o cierre**, lo que sugiere registros sin segunda intervención o con procesos administrativos inconclusos.

---

## 2.5. Análisis exploratorio inicial (EDA)

Se ejecutó un análisis exploratorio automatizado para las variables numéricas y categóricas:

- **23 variables numéricas:** se calcularon medidas de tendencia central y dispersión.  
- **93 variables categóricas:** se evaluaron frecuencias absolutas y relativas.  
- **Distribución temporal:** se verificó la existencia de intervenciones en todos los años 2021–2025, confirmando la cobertura completa del periodo de estudio.

Este análisis permitió identificar las **tendencias generales** y **zonas de concentración de casos**, las cuales serán examinadas en mayor detalle en el análisis espacio-temporal.

---

## 2.6. Análisis espacio-temporal

A partir de las variables de **localidad** y **año**, se realizó un análisis para identificar **zonas de alerta** y **patrones espaciales de cambio**.  
El modelo detectó **19 zonas de alerta**, es decir, localidades donde se observa un incremento sostenido o una concentración elevada de intervenciones con NNA durante el periodo 2021–2025.

Estas zonas representan áreas prioritarias para el seguimiento de políticas de atención y prevención, especialmente en relación con el régimen subsidiado de salud.

---

## 2.7. Análisis del régimen de salud

El componente social se evaluó mediante la variable **“régimen de afiliación en salud”**, distinguiendo principalmente entre:

- Régimen contributivo  
- Régimen subsidiado  
- Otros (excepción o transición)

Los resultados iniciales muestran una **mayor participación del régimen subsidiado**, lo cual sugiere una **correlación entre vulnerabilidad social y mayor frecuencia de intervenciones**.  
Este hallazgo orientará la siguiente etapa del análisis hacia un enfoque de desigualdad territorial y social.

---

## 2.8. Resultados globales del Data Understanding

| **Aspecto** | **Resultado** |
|--------------|----------------|
| Filas analizadas | 56,473 |
| Columnas | 114 |
| Duplicados detectados | 3,690 |
| Columnas constantes | 12 |
| Calidad promedio de los datos | 99.8% |
| Cobertura temporal | 2021–2025 |
| Zonas de alerta espacial | 19 |
| Promedio de valores faltantes | 4.86% |
| Código especial (99999) | Detectado y documentado |

---

## 2.9. Interpretación general

El proceso de comprensión de datos permitió confirmar que la base institucional cuenta con un **alto nivel de consistencia y completitud**, lo cual garantiza su idoneidad para los análisis estadísticos y espaciales posteriores.  

Se identificaron algunos vacíos en fechas administrativas y casos sin seguimiento, pero estos representan una proporción mínima dentro del conjunto total.  
El análisis exploratorio evidenció una distribución desigual de las intervenciones por localidad, con **mayor concentración en zonas específicas** que coinciden, en varios casos, con territorios donde predomina el **régimen subsidiado**.  

Estos resultados respaldan el propósito del proyecto: analizar las **diferencias espacio-temporales en las intervenciones con NNA en Bogotá** y su relación con las condiciones sociales y de salud de la población.

---



