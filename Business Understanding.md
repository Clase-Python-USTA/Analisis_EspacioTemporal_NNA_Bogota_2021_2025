

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


#  2. Data Understanding)

## Descripción general de la base de datos
La base de datos utilizada corresponde a los registros de **intervenciones con niños, niñas y adolescentes (NNA)** realizadas en Bogotá entre los años **2021 y 2025**.  
Contiene información sobre las intervenciones ejecutadas en diferentes **localidades de la ciudad**, junto con variables que permiten conocer el **tipo de afiliación en salud** y otras características asociadas a cada caso.  

Esta base fue construida con información institucional anónima y tiene como propósito analizar los cambios en la atención o intervención con la población NNA desde una perspectiva **espacio-temporal y social**.  

---

## Variables principales
A continuación se describen las variables más importantes incluidas en el análisis:

| **Variable** | **Descripción** |
|---------------|----------------|
| **Año** | Año en el que se realizó la intervención (rango: 2021–2025). |
| **Mes** *(si aplica)* | Permite observar variaciones más detalladas dentro de cada año. |
| **Localidad** | División territorial de Bogotá donde ocurrió la intervención. Es clave para el análisis espacial. |
| **Tipo de intervención** | Clasifica la acción o atención realizada con el NNA. |
| **Régimen de afiliación en salud** | Indica si el NNA pertenece al régimen contributivo, subsidiado u otro tipo de afiliación. |
| **Sexo** | Variable de apoyo para análisis demográficos. |
| **Edad** | Edad del NNA al momento de la intervención. |
| **Número de intervenciones** | Representa el conteo total de registros o casos por localidad y año. |

---

## Observaciones iniciales
- Los datos abarcan un **periodo de cinco años (2021–2025)**, lo que permite analizar **tendencias en el tiempo**.  
- La variable **localidad** permitirá observar la **distribución territorial** de las intervenciones.  
- La información sobre **régimen de afiliación** es fundamental para explorar **diferencias sociales** y aproximar posibles relaciones entre vulnerabilidad y número de intervenciones.  
- Es posible que existan valores faltantes o inconsistencias (por ejemplo, registros sin localidad o sin tipo de régimen), que deberán revisarse durante la etapa de preparación de los datos.  

---

## Posibles transformaciones
Para facilitar el análisis, se planea:
- Agrupar los datos por **localidad y año**.  
- Calcular indicadores como **variación porcentual** de intervenciones entre años.  
- Crear una variable que refleje la **proporción de casos según el régimen subsidiado**.  
- Generar visualizaciones iniciales (tablas, gráficos y mapas) para entender los patrones generales.  

---

## Propósito del análisis exploratorio
El análisis exploratorio permitirá:
- Detectar **patrones de crecimiento o disminución** en las intervenciones por localidad.  
- Identificar **zonas de concentración o alerta**.  
- Comprender **cómo se distribuyen las intervenciones según el régimen de afiliación**, especialmente el subsidiado.  
- Reconocer **posibles errores o vacíos** en los datos antes de pasar a la siguiente fase de preparación.  

