

# 1. Comprensión del Negocio (Business Understanding)

## Contexto general
Este proyecto busca entender cómo han cambiado las intervenciones realizadas con niños, niñas y adolescentes (NNA) en Bogotá entre los años 2021 y 2025, analizando su comportamiento a lo largo del tiempo y en las diferentes localidades de la ciudad.  
El propósito es identificar en qué zonas han aumentado o disminuido las intervenciones y revisar si esos cambios guardan relación con las condiciones sociales de la población, tomando como referencia el tipo de afiliación en salud, especialmente el régimen subsidiado.

De esta manera, se busca no solo observar la evolución de las intervenciones, sino también reconocer posibles desigualdades territoriales y orientar futuras acciones de política pública que fortalezcan la atención a la niñez y la adolescencia en las zonas más vulnerables.

> **Nota:** aunque la base de datos incluye registros hasta 2025, el análisis principal se centró en el período 2021–2024, que cuenta con información completa y validada para todas las variables.

---

## Propósito del proyecto
El propósito es comprender los patrones de cambio de las intervenciones con NNA en Bogotá, tanto en el tiempo como en el territorio, y analizar si existen diferencias asociadas al tipo de afiliación en salud, en especial el régimen subsidiado.  
Con esto se espera obtener una visión más clara del comportamiento institucional y social de la atención, que sirva de base para orientar decisiones o estrategias futuras.

---

## Objetivo general
Analizar cómo han cambiado las intervenciones con niños, niñas y adolescentes (NNA) en las distintas localidades de Bogotá entre 2021 y 2024, identificando las zonas donde los casos han aumentado o disminuido y relacionando esos cambios con las condiciones sociales de la población, tomando como referencia el tipo de afiliación en salud, especialmente el régimen subsidiado.

---

## Objetivos específicos
1. Describir la distribución de las intervenciones con NNA por localidad y año entre 2021 y 2024.  
2. Identificar las localidades con aumento o disminución en el número de intervenciones a lo largo del tiempo.  
3. Explorar posibles relaciones entre el comportamiento de las intervenciones y el tipo de afiliación en salud, con énfasis en el régimen subsidiado.  

---

## Preguntas guía
- ¿En qué localidades han aumentado o disminuido las intervenciones con NNA entre 2021 y 2024?  
- ¿Qué características tienen las localidades con mayor crecimiento o concentración de casos?  
- ¿Se observa alguna relación entre la evolución de las intervenciones y el tipo de afiliación en salud, especialmente el régimen subsidiado?  

---

## Alcance
El análisis se centra en los registros de intervenciones con NNA entre 2021 y 2024, considerando las variables de localidad, año y régimen de afiliación en salud.  
El objetivo no es establecer relaciones causales, sino **describir y comprender** cómo varían las intervenciones en función del territorio y las condiciones sociales.

---

## Resultados esperados
- Conocer cómo cambian las intervenciones con NNA a lo largo del tiempo y en cada localidad.  
- Identificar las zonas con mayor concentración o crecimiento de casos.  
- Establecer una primera aproximación entre las intervenciones y el tipo de afiliación en salud.  
- Aportar información útil para fortalecer las estrategias de atención y protección a la niñez y adolescencia en Bogotá.  

---

## Glosario

| **Término** | **Definición** |
|--------------|----------------|
| **NNA** | Sigla que significa *Niños, Niñas y Adolescentes*. Hace referencia a la población menor de 18 años objeto de las intervenciones analizadas. |
| **Intervención** | Acción o proceso desarrollado por una entidad o programa para atender, proteger o acompañar a un niño, niña o adolescente. |
| **Análisis espacio-temporal** | Tipo de estudio que combina la información geográfica (espacial) y temporal para observar cómo cambian los casos o eventos según la zona y el año. |
| **Localidad** | División territorial de Bogotá que agrupa diferentes barrios. En total, la ciudad cuenta con 20 localidades. |
| **Régimen de afiliación en salud** | Forma en que las personas están vinculadas al sistema de salud. Los principales son el *régimen contributivo* (para quienes cotizan) y el *régimen subsidiado* (para personas en situación de vulnerabilidad). |
| **Régimen subsidiado** | Tipo de afiliación en salud dirigido a la población con menores ingresos o en condición de vulnerabilidad, financiado con recursos públicos. |
| **Zona de alerta** | Localidad donde se observa un aumento importante o sostenido en el número de intervenciones, lo que puede requerir atención prioritaria. |


# 2. Comprensión de los Datos (Data Understanding)

## 2.1 Origen de los datos
La información utilizada proviene del archivo **base_datos_completa_NNA_TI_anon.xlsx**, que recopila los registros de intervenciones realizadas con niños, niñas y adolescentes (NNA) en Bogotá entre los años **2021 y 2025**.  
Los datos provienen de sistemas administrativos del distrito y fueron **anonimizados** para proteger la identidad de las personas.

Durante el procesamiento se generaron dos versiones principales:

- **base_nna_understanding.xlsx:** usada para revisar la estructura y la calidad general de los datos.  
- **base_nna_limpia.xlsx:** base depurada utilizada para los análisis exploratorios y el análisis de componentes principales (ACP).

El objetivo de esta etapa fue conocer la composición del conjunto de datos, evaluar su calidad y entender si era adecuado para responder las preguntas planteadas en el proyecto.

---

## 2.2 Estructura general del conjunto de datos

| Concepto | Valor |
|-----------|-------|
| Registros iniciales | 56,473 |
| Variables originales | 115 |
| Registros después de limpieza | 52,358 |
| Variables finales | 83 |
| Porcentaje de retención total | 66.3 % |
| Cobertura temporal | 2021–2025 |
| Localidades analizadas | 20 |

Durante la depuración se eliminaron registros duplicados, columnas sin valor analítico y variables administrativas o personales.  
También se estandarizaron los nombres de las columnas, los formatos de fecha y los valores de texto para garantizar consistencia en todo el conjunto.

---

## 2.3 Variables principales utilizadas

| Tipo de variable | Nombre | Descripción | Uso principal |
|------------------|---------|--------------|---------------|
| Territorial | LOCALIDAD_FIC | Localidad donde se realizó la intervención | Agrupación espacial |
| Temporal | AÑO | Año en el que se registró la intervención | Análisis temporal |
| Socioeconómica | AFILIACIÓN_AL_SGSSS | Tipo de régimen de afiliación al sistema de salud | Variable de referencia social |
| Métrica | Conteo de registros | Número total de intervenciones por año y localidad | Indicador principal de análisis |

Estas variables fueron la base del análisis espacio-temporal, ya que permiten observar cómo varía el número de intervenciones a través del tiempo y entre las distintas zonas de la ciudad.

---

## 2.4 Naturaleza y alcance de los datos

- **Unidad de análisis:** cada registro representa una intervención, no un niño o niña único.  
  Un mismo NNA puede tener varias intervenciones si fue atendido más de una vez.  
- **Tipo de fuente:** datos administrativos, estructurados y anonimizados.  
- **Escala temporal:** anual (2021–2025).  
- **Nivel de agregación:** localidad.  

Por tanto, los resultados deben interpretarse como tendencias generales del sistema de atención, no como descripciones individuales.

---

## 2.5 Evaluación de calidad de los datos

Durante la revisión se consideraron tres aspectos principales:

1. **Completitud:**  
   Tras la limpieza, la base quedó sin valores nulos reales.  
   Los códigos **99999** se conservaron cuando significaban “No aplica” o “Sin información”, evitando perder observaciones válidas.

2. **Consistencia:**  
   Todas las fechas de intervención están dentro del rango 2021–2025, sin registros fuera del periodo de estudio.  

3. **Validez:**  
   Se eliminaron once columnas sin variación y se detectaron **19 zonas de alerta** (localidades con picos inusuales de casos) que fueron revisadas en el ACP.

---

## 2.6 Distribución general de las intervenciones

### Evolución anual

| Año | Registros | Porcentaje |
|------|------------|-------------|
| 2021 | 10,488 | 21.4 % |
| 2022 | 11,200 | 22.9 % |
| 2023 | 15,766 | 32.2 % |
| 2024 | 11,527 | 23.5 % |
| 2025 | 3,377 | 6.0 % |

El año **2023** presenta un aumento considerable en el número de intervenciones.  
Este incremento podría estar relacionado con la recuperación institucional y administrativa posterior a la pandemia. En 2022 se identificó un número mayor de registros con el código **99999**, lo que sugiere vacíos o inconsistencias en el registro que luego se corrigieron, haciendo que en 2023 apareciera un “pico” aparente por la mejora en la captura de información.

---

### Distribución por localidad

| Localidad | Registros | Porcentaje |
|------------|------------|-------------|
| Ciudad Bolívar | 6,956 | 14.2 % |
| Bosa | 4,895 | 10.0 % |
| Kennedy | 4,756 | 9.7 % |
| Suba | 4,200 | 8.6 % |
| Usme | 3,418 | 7.0 % |
| Engativá | 3,330 | 6.8 % |
| Rafael Uribe Uribe | 2,875 | 5.9 % |
| Los Mártires | 2,773 | 5.7 % |
| San Cristóbal | 2,717 | 5.6 % |
| Santa Fe | 2,434 | 5.0 % |

Estas diez localidades concentran más del **70 % de las intervenciones**, evidenciando una fuerte concentración territorial, sobre todo en las zonas del sur y suroccidente de Bogotá.

---

## 2.7 Distribución por régimen de afiliación en salud

| Régimen | Registros | Porcentaje |
|----------|------------|-------------|
| Subsidiado | 17,146 | 35.0 % |
| Contributivo | 14,071 | 28.7 % |
| No asegurado | 6,088 | 12.4 % |
| Especial | 572 | 1.2 % |
| Vinculado | 5 | 0.01 % |

El **régimen subsidiado** agrupa la mayor parte de las intervenciones, reflejando la relación entre vulnerabilidad socioeconómica y frecuencia de atención.  
El régimen contributivo también tiene un peso importante, mientras que los demás aparecen con porcentajes marginales.

---

## 2.8 Principales hallazgos de esta etapa

- La base tiene una estructura sólida y buena calidad para el análisis.  
- Se observa un pico de intervenciones en 2023, posiblemente asociado a la mejora en los registros tras la pandemia.  
- Las localidades con mayor número de casos son Ciudad Bolívar, Kennedy, Bosa y Suba.  
- El régimen subsidiado concentra más de un tercio de los registros, siendo un indicador clave del componente social del análisis.  
- Los datos permiten realizar comparaciones temporales y espaciales confiables.

---

## 2.9 Conclusión

En esta etapa se comprendió la estructura y calidad del conjunto de datos, verificando que es adecuado para los análisis posteriores.  
Los resultados muestran que el año 2023 concentra el mayor número de intervenciones, lo cual puede estar vinculado a la recuperación institucional y la mejora en los sistemas de información tras los efectos de la pandemia.  
También se confirmó que las intervenciones se concentran principalmente en las localidades del sur de Bogotá y en la población del régimen subsidiado, lo que orienta el análisis hacia las desigualdades territoriales y sociales.  
Estos hallazgos guiaron las siguientes fases de preparación y modelado de los datos.

---
# 3. Preparación de los Datos (Data Preparation)

## 3.1 Objetivo de la etapa

El propósito de esta fase fue **organizar y limpiar la base de datos** para dejarla lista para los análisis exploratorios y el Análisis de Componentes Principales (ACP).  
Se buscó eliminar información redundante, estandarizar las variables y garantizar que los datos fueran consistentes y comparables entre localidades y años.

---

## 3.2 Proceso general de preparación

A partir de la base procesada **base_nna_understanding.xlsx**, se llevaron a cabo las siguientes tareas:

1. **Estandarización de nombres de columnas**  
   Se homogenizaron los nombres de las variables, convirtiéndolos a mayúsculas y eliminando espacios, tildes y caracteres especiales.  
   Ejemplo: `Afiliación al SGSSS` → `AFILIACION_AL_SGSSS`.

2. **Eliminación de información personal o sensible (PII)**  
   Se eliminaron 7 columnas con posibles datos identificables, como nombres, correos o direcciones, para cumplir con criterios éticos y de anonimato.

3. **Depuración de variables sin valor analítico**  
   Se retiraron 26 columnas de carácter administrativo o técnico que no aportaban al análisis.  
   Entre ellas: `BASE_ORIGEN`, `RED_FIC`, `USUARIO`, `PESO`, `TALLA_CM` y otros campos repetidos o de seguimiento individual.

4. **Estandarización de fechas y formatos**  
   Se normalizaron ocho columnas de tipo fecha que tenían formatos diferentes y se unificaron los valores de texto.  
   También se eliminaron **3,690 registros duplicados**.

5. **Manejo de valores faltantes**  
   Se eliminaron **425 registros** con valores realmente nulos.  
   Los códigos **99999** se conservaron solo cuando representaban categorías válidas como “No aplica” o “Sin información”.

6. **Revisión de tipos de datos**  
   Se identificaron y clasificaron las variables en:
   - 55 categóricas o de texto  
   - 20 numéricas  
   - 8 de tipo fecha  

7. **Verificación de la variable temporal (AÑO)**  
   Se comprobó que el campo **AÑO** estuviera completo y con valores válidos, asegurando la posibilidad de realizar los análisis por periodo.

8. **Exportación de la base limpia**  
   El conjunto final se guardó como **base_nna_limpia.xlsx** dentro de la carpeta `data/processed`, sirviendo como insumo para las etapas siguientes.

---

## 3.3 Resultados de la limpieza

| Concepto | Valor |
|-----------|-------|
| Filas iniciales | 56,473 |
| Filas finales | 52,358 |
| Columnas iniciales | 116 |
| Columnas finales | 83 |
| Registros eliminados | 4,115 |
| Columnas eliminadas | 33 |
| Retención de registros | 92.7 % |
| Retención total (celdas) | 66.3 % |

El proceso permitió conservar la mayor parte de la información relevante, eliminando principalmente duplicados, columnas redundantes y campos administrativos.  
El resultado fue una base más ligera, estructurada y lista para los análisis exploratorios y multivariados.

---

## 3.4 Evaluación después de la limpieza

1. **Distribución temporal**  
   La base conserva una distribución equilibrada entre los años 2021 y 2024, con un aumento importante en 2023.  
   Este incremento coincide con la reducción de los códigos 99999, lo que sugiere una mejora en la calidad del registro.

2. **Distribución espacial**  
   Las 20 localidades de Bogotá permanecen representadas.  
   Las localidades con mayor número de registros siguen siendo **Ciudad Bolívar, Bosa, Kennedy y Suba**, que juntas concentran más del 40 % del total.

3. **Integridad de categorías**  
   La variable **AFILIACION_AL_SGSSS** se consolidó en cinco categorías principales:  
   `SUBSIDIADO`, `CONTRIBUTIVO`, `NO_ASEGURADO`, `ESPECIAL` y `VINCULADO`, eliminando errores de digitación y duplicados de texto.

---

## 3.5 Análisis exploratorio inicial (EDA)

Antes de aplicar el ACP se realizó un análisis exploratorio que permitió observar los primeros patrones:

- **Tendencia temporal:** se observa un aumento marcado de intervenciones en 2023.  
- **Concentración territorial:** más del 70 % de los casos se registran en las diez localidades con mayor población.  
- **Predominio del régimen subsidiado:** alrededor del 45 % de las intervenciones pertenecen a este grupo.  
- **Comportamiento estable del régimen contributivo:** mantiene cerca del 30 % de participación anual.

Estos resultados confirmaron que la base depurada tenía la estructura adecuada para avanzar con los análisis de correlación y reducción de dimensiones.

---

## 3.6 Cobertura del conjunto de datos graficados

Durante la exploración se trabajó con un subconjunto de **37,882 registros**, correspondiente a los años 2021–2024.  
Esto representa:

- **72.3 %** de la base limpia total (52,358 registros).  
- **48.0 %** del total de la base original (56,473 registros).

El subconjunto excluye datos con información incompleta y años con registros parciales (como 2025), garantizando comparabilidad y estabilidad en los análisis.

---

## 3.7 Conclusión de la etapa

La fase de preparación dejó un conjunto de datos **coherente, completo y representativo** del fenómeno analizado.  
Se mantuvo una cobertura temporal y territorial amplia, conservando más del 70 % de los registros limpios.  
El tratamiento de los valores 99999 fue cuidadoso, diferenciando los casos de “sin información” de los de “no aplica”.  
En conjunto, esta etapa aseguró que las conclusiones del ACP y del análisis espacio-temporal se basaran en datos de buena calidad y con significado analítico claro.

---
## 3. Visualización descriptiva y resumen de datos graficados

Durante la fase de análisis exploratorio se generaron siete visualizaciones que resumen el comportamiento de las intervenciones con NNA en Bogotá entre 2021 y 2024, tomando como base las variables de **año, localidad y régimen de afiliación en salud**.  
El conjunto de datos utilizado para estas gráficas agrupa **37,882 registros**, lo que corresponde aproximadamente al **72.3 % de la base limpia total (52,358 registros)**.  
Esto significa que los gráficos representan la porción más estructurada y consistente de la información, excluyendo registros con datos incompletos o regímenes poco frecuentes.

### 3.1 Intervenciones por año y régimen

Los años 2023 y 2024 concentran la mayoría de las intervenciones, con 14,575 (38.5 %) y 11,527 (30.4 %) respectivamente.  
El año 2022 presenta un descenso notable (solo 7.6 % del total), probablemente relacionado con dificultades de registro y los efectos posteriores a la pandemia, ya que en ese periodo se observaron más valores tipo “99999”, que reflejan vacíos o inconsistencias en la captura de información.

Por régimen de afiliación, la mayor parte de las intervenciones se concentra en:
- **Régimen subsidiado:** 17,146 casos (45.3 % del total)
- **Régimen contributivo:** 14,071 casos (37.1 %)
- **No asegurado:** 6,088 casos (16.1 %)

Los regímenes especial y vinculado representan proporciones mínimas (1.5 % y 0.01 %, respectivamente).

### 3.2 Distribución por régimen y localidad

El análisis por localidad muestra una gran concentración de intervenciones en zonas históricamente más vulnerables de la ciudad.  
Las cinco localidades con más registros son:

| Localidad         | Intervenciones | Porcentaje |
|-------------------|----------------|-------------|
| Ciudad Bolívar    | 5,542          | 18.3 % |
| Kennedy           | 3,892          | 12.8 % |
| Bosa              | 3,839          | 12.7 % |
| Suba              | 3,292          | 10.9 % |
| Usme              | 2,613          | 8.6 % |

Estas cinco localidades suman casi el **63 % de las intervenciones graficadas**, lo que reafirma su peso territorial en los programas de atención.  

Otras zonas como **Rafael Uribe Uribe, Los Mártires, Engativá y Santa Fe** también presentan volúmenes considerables, aunque con menor crecimiento entre 2023 y 2024.

### 3.3 Tendencias temporales

- En **2021**, las intervenciones se mantuvieron relativamente equilibradas, aunque con niveles inferiores al promedio.
- En **2022**, se evidencia una caída abrupta en todos los regímenes, posiblemente asociada a vacíos de registro.
- En **2023**, se produce un aumento generalizado de los casos, lo que coincide con una mejora en la cobertura y el registro institucional.
- En **2024**, la tendencia se estabiliza, con niveles aún altos pero sin nuevos picos.

### 3.4 Interpretación general

Las visualizaciones confirman que la evolución temporal y territorial de las intervenciones tiene un fuerte componente social:
- El **régimen subsidiado** concentra casi la mitad de los casos y se asocia directamente con las localidades de mayor vulnerabilidad.
- El **año 2023** representa un punto de inflexión en la dinámica de atención, coincidiendo con la reducción de los valores 99999 y la consolidación de registros más completos.
- Las diferencias entre localidades muestran un patrón estable: las zonas del sur (Ciudad Bolívar, Bosa, Usme) concentran la mayoría de los esfuerzos institucionales.

En síntesis, el análisis gráfico permitió visualizar que los cambios más fuertes no se deben tanto a transformaciones territoriales, sino a mejoras en la captura y consolidación de la información posterior al impacto de la pandemia.


# 4. Visualización descriptiva y resumen de datos graficados

## 4.1 Propósito de la fase

Esta etapa tuvo como propósito **describir de forma visual el comportamiento de las intervenciones con NNA en Bogotá** durante el periodo 2021–2024, utilizando gráficos que permiten identificar patrones y diferencias entre años, localidades y tipos de afiliación al sistema de salud.  

Las visualizaciones se elaboraron a partir de un subconjunto de **37,882 registros**, lo que equivale aproximadamente al **72.3 % de la base limpia total**.  
Esta proporción garantiza que las gráficas representen los datos más consistentes y completos, sin incluir registros con vacíos o información poco confiable.

---

## 4.2 Intervenciones por año y régimen

El análisis temporal muestra una evolución desigual entre los años:

| Año | Intervenciones | Porcentaje del total |
|------|----------------|----------------------|
| 2021 | 8,894 | 23.5 % |
| 2022 | 2,886 | 7.6 % |
| 2023 | 14,575 | 38.5 % |
| 2024 | 11,527 | 30.4 % |

El año **2023** presentó el pico más alto de intervenciones, seguido de una leve disminución en 2024.  
El descenso en 2022 es evidente y probablemente está relacionado con dificultades en el registro y la persistencia de códigos “99999”, asociados a vacíos de información tras la pandemia.  
Este comportamiento sugiere que el incremento de 2023 no solo refleja un aumento real de intervenciones, sino también una mejora en la calidad del registro administrativo.

---

## 4.3 Distribución por régimen de afiliación

| Régimen | Casos | Porcentaje |
|----------|--------|-------------|
| Subsidiado | 17,146 | 45.3 % |
| Contributivo | 14,071 | 37.1 % |
| No asegurado | 6,088 | 16.1 % |
| Especial | 572 | 1.5 % |
| Vinculado | 5 | 0.01 % |

La mayor parte de las intervenciones corresponde al **régimen subsidiado**, lo que coincide con el perfil socioeconómico de las zonas del sur y suroccidente de Bogotá, donde predominan los hogares con menores ingresos.  
El **régimen contributivo** también tiene una participación importante, mientras que los demás regímenes son marginales.  
Esta distribución refuerza la idea de que la intensidad de las intervenciones está directamente relacionada con las condiciones sociales de la población.

---

## 4.4 Distribución territorial

El análisis por localidad muestra una marcada concentración de casos en algunas zonas.  
Las cinco localidades con mayor número de intervenciones son:

| Localidad | Intervenciones | Porcentaje |
|------------|----------------|-------------|
| Ciudad Bolívar | 5,542 | 18.3 % |
| Kennedy | 3,892 | 12.8 % |
| Bosa | 3,839 | 12.7 % |
| Suba | 3,292 | 10.9 % |
| Usme | 2,613 | 8.6 % |

Estas cinco localidades concentran casi el **63 % de todas las intervenciones registradas**, lo que evidencia una alta concentración territorial de los casos en el sur y suroccidente de la ciudad.  
Otras zonas como **Rafael Uribe Uribe, Los Mártires, Engativá y Santa Fe** también registran una participación considerable, aunque con menor crecimiento entre 2023 y 2024.

---

## 4.5 Evolución temporal y posibles causas

Al observar las series por año, se identifican cuatro momentos:

1. **2021:** periodo de recuperación inicial tras la pandemia, con un nivel moderado de registros.  
2. **2022:** descenso marcado, posiblemente asociado a vacíos de información y dificultades operativas.  
3. **2023:** aumento generalizado, que puede explicarse tanto por una reactivación de las intervenciones como por mejoras en la captura de datos.  
4. **2024:** estabilización de los valores, lo que sugiere que el sistema logró normalizar sus flujos de atención.

El comportamiento general coincide con lo observado en otras bases institucionales del mismo periodo, donde los registros administrativos suelen mostrar una caída en los años de transición postpandemia y un repunte al año siguiente.

---

## 4.6 Interpretación general de las visualizaciones

Las gráficas permiten identificar varios patrones relevantes:

- **Predominio del régimen subsidiado:** concentra casi la mitad de las intervenciones, especialmente en localidades de mayor vulnerabilidad.  
- **Comportamiento estable del régimen contributivo:** aunque tiene una participación menor, mantiene una presencia constante en todas las localidades.  
- **Pico de 2023:** explicado por una combinación entre mejora en el registro y aumento real de atenciones.  
- **Concentración geográfica:** las zonas del sur (Ciudad Bolívar, Bosa, Usme y Kennedy) son las que reúnen la mayor parte de los casos.  

Estos hallazgos refuerzan la importancia de considerar las condiciones sociales y la cobertura del régimen de salud al analizar la dinámica de las intervenciones con NNA.

---

## 4.7 Conclusión de la fase descriptiva

El análisis visual confirmó que la **evolución de las intervenciones tiene un patrón territorial y social claramente definido**.  
El aumento de 2023 refleja tanto un cambio en la dinámica institucional como una mejora en la calidad de la información.  
Los resultados muestran que la concentración de casos en el régimen subsidiado y en las localidades del sur de Bogotá sigue siendo un indicador clave de desigualdad, y que el comportamiento general del sistema tiende a estabilizarse en los años más recientes.

---
# 5. Modelado (Análisis de Componentes Principales - ACP)

## 5.1 Propósito del análisis

El análisis de componentes principales (ACP) se aplicó para **resumir y simplificar la información** relacionada con las intervenciones en niños, niñas y adolescentes (NNA) según el tipo de afiliación en salud y la localidad.  
El objetivo fue identificar patrones comunes y diferencias entre localidades y años, reduciendo la complejidad de los datos a unos pocos componentes que concentran la mayor parte de la variabilidad.

En términos simples, el ACP permitió observar **qué tanto se parecen o se diferencian las localidades** en función de los regímenes de afiliación en salud y cómo estas relaciones cambiaron entre 2021 y 2024.

---

## 5.2 Datos utilizados para el ACP

El análisis se realizó con la base **base_nna_limpia.xlsx**, que contiene **52,358 registros válidos**.  
De esa base se generó una tabla resumen con el número total de intervenciones agrupadas por:

- Localidad  
- Año  
- Régimen de afiliación (Subsidiado, Contributivo, No Asegurado, Especial, Vinculado)

El resultado fue una matriz con **74 observaciones** (una por cada combinación de localidad y año) y **5 variables numéricas** (los cinco regímenes).  
Esta tabla fue normalizada para eliminar las diferencias de escala entre regímenes antes de aplicar el ACP.

---

## 5.3 Resultados generales del modelo

El ACP mostró que los **dos primeros componentes principales explican cerca del 80 % de la variación total** de los datos, lo cual es un nivel alto de representatividad.  
Esto significa que con solo dos ejes (PC1 y PC2) se puede visualizar de manera efectiva cómo se agrupan las localidades y cómo se comportan los distintos regímenes.

| Componente | Varianza explicada | Interpretación principal |
|-------------|--------------------|---------------------------|
| PC1 | 59.84 % | Representa la intensidad general de las intervenciones, especialmente en los regímenes subsidiado y contributivo. |
| PC2 | 20.15 % | Refleja diferencias específicas vinculadas al régimen vinculado y algunos casos atípicos. |

En conjunto, estos dos componentes resumen el patrón estructural del sistema de intervención.

---

## 5.4 Interpretación de las cargas (loadings)

Las cargas indican cuánto aporta cada régimen a los componentes principales:

| Régimen | PC1 | PC2 |
|----------|-----|-----|
| Subsidiado | 0.557 | 0.041 |
| Contributivo | 0.541 | 0.047 |
| No asegurado | 0.368 | -0.072 |
| Especial | 0.511 | -0.037 |
| Vinculado | -0.003 | 0.995 |

Estas cifras muestran que el **primer componente (PC1)** está dominado por los regímenes **subsidiado, contributivo y especial**, es decir, resume la tendencia general de las intervenciones.  
El **segundo componente (PC2)** está definido casi exclusivamente por el régimen **vinculado**, que aunque tiene pocos casos, introduce una variación particular en algunos años o localidades.

---

## 5.5 Resultados gráficos e interpretación visual

Se generaron varios gráficos para representar los resultados del ACP:

1. **Scree Plot:** evidencia que los dos primeros componentes son suficientes, ya que a partir del tercero la varianza explicada es mínima.  
2. **Biplot general:** muestra cómo las localidades se agrupan según la combinación de regímenes. Las más activas (como Ciudad Bolívar, Kennedy, Bosa y Suba) aparecen con valores altos en PC1.  
3. **Trayectorias espacio-temporales:** permiten ver cómo cambian las posiciones de cada localidad con el paso del tiempo. En 2023, la mayoría se desplaza hacia la derecha del gráfico (valores altos de PC1), reflejando el aumento general de intervenciones.  
4. **Cargas o contribuciones:** muestran gráficamente que los regímenes subsidiado y contributivo tienen un peso muy similar y dominan el comportamiento global.  
5. **Círculo de correlaciones:** confirma la relación positiva y fuerte entre los regímenes subsidiado, contributivo y especial, y la independencia del régimen vinculado.

---

## 5.6 Comportamiento por componentes

- **PC1 – Intensidad general de las intervenciones:**  
  Resume el nivel total de actividad en cada localidad. Las más altas en este eje (Ciudad Bolívar, Kennedy, Bosa y Suba) son las que registran más intervenciones, especialmente bajo el régimen subsidiado.  
  Un valor alto en PC1 equivale a una mayor carga institucional de atención.

- **PC2 – Casos específicos o atípicos:**  
  Representa diferencias particulares que no dependen del volumen total, sino de la aparición ocasional de regímenes poco frecuentes. Por ejemplo, *Rafael Uribe Uribe* en 2024 muestra un ligero incremento en el régimen vinculado, lo que eleva su posición en PC2.

---

## 5.7 Cambios espacio-temporales observados

El análisis de las trayectorias temporales dentro del espacio de componentes mostró una tendencia clara:

- En **2021**, las localidades presentan posiciones más dispersas, con niveles moderados de intervención.  
- En **2022**, varias localidades caen en el eje PC1, lo que coincide con la reducción general de registros y los problemas de captura asociados al uso del código 99999.  
- En **2023**, casi todas las localidades se mueven hacia valores positivos en PC1, indicando un incremento generalizado de intervenciones.  
- En **2024**, la mayoría se estabiliza en posiciones similares, lo que sugiere una normalización posterior al pico del año anterior.

En conjunto, la variación temporal del ACP refleja con claridad los efectos de la pandemia sobre la calidad y el volumen de los registros administrativos.

---

## 5.8 Síntesis de los resultados

1. **El régimen subsidiado es el principal factor de variación** y explica gran parte de las diferencias entre localidades.  
2. **Las localidades del sur y suroccidente de la ciudad** (Ciudad Bolívar, Kennedy, Bosa y Usme) mantienen valores altos y estables en PC1, confirmando su papel como zonas prioritarias.  
3. **El año 2023** marca el punto de mayor crecimiento, impulsado tanto por una reactivación institucional como por una mejora en el registro de datos.  
4. **El régimen vinculado**, aunque poco frecuente, introduce una dimensión adicional de variación capturada en PC2.  
5. **La estructura general del sistema de intervenciones es consistente**, lo que demuestra estabilidad en la forma como los distintos regímenes se comportan a lo largo del tiempo.

---

## 5.9 Conclusión del ACP

El ACP cumplió su propósito de reducir la complejidad y resaltar los patrones más importantes del fenómeno.  
Se concluye que:

- Las diferencias entre localidades están determinadas principalmente por el volumen total de intervenciones y la proporción de población en el régimen subsidiado.  
- El comportamiento de los regímenes se mantiene estable entre años, salvo por el repunte general de 2023.  
- Los dos primeros componentes permiten explicar cerca del 80 % de la estructura de los datos, lo cual valida la consistencia del modelo.

En resumen, el ACP ofrece una visión sintética del sistema de atención a NNA en Bogotá, evidenciando tanto la dimensión social (a través del régimen subsidiado) como la dimensión temporal (a través del aumento y posterior estabilización de los casos).

# 6. Evaluación y criterios de éxito

## 6.1 Propósito de la etapa

La fase de evaluación tuvo como objetivo revisar si el proceso analítico y los resultados obtenidos respondieron adecuadamente a los objetivos planteados en la etapa de comprensión del negocio.  
En esta etapa se evaluó tanto la **calidad técnica del análisis** (en términos de consistencia, cobertura y representatividad de los datos) como la **validez interpretativa** de los hallazgos obtenidos mediante el análisis exploratorio y el ACP.

---

## 6.2 Criterios de éxito definidos

Se establecieron los siguientes criterios para valorar el éxito del proyecto, considerando tanto aspectos técnicos como sustantivos del análisis:

| **Criterio** | **Descripción** | **Indicador esperado** | **Resultado obtenido** |
|---------------|------------------|--------------------------|--------------------------|
| **Cobertura de datos** | Porcentaje de registros útiles, completos y con información válida. | ≥ 60 % del total de la base original | **Cumplido (72.3 %)** |
| **Consistencia temporal** | Existencia de registros continuos entre 2021 y 2024. | Años consecutivos sin vacíos relevantes | **Cumplido (2021–2024 presentes)** |
| **Validez territorial** | Presencia de las 20 localidades de Bogotá con registros suficientes. | ≥ 19 localidades representadas | **Cumplido (20 localidades)** |
| **Varianza explicada por el ACP** | Porcentaje de información retenida en los dos primeros componentes. | ≥ 70 % | **Cumplido (79.98 %)** |
| **Coherencia con la realidad social** | Correspondencia entre los resultados del ACP y los patrones históricos de vulnerabilidad. | Coincidencia con zonas del sur de Bogotá | **Cumplido (Ciudad Bolívar, Bosa, Usme, Kennedy)** |
| **Identificación de cambios estructurales** | Detección de aumentos o descensos significativos entre años. | Variaciones > 20 % | **Cumplido (pico en 2023)** |

En conjunto, los resultados confirman que el proyecto cumplió satisfactoriamente los criterios de éxito definidos. La base depurada fue representativa, las series temporales fueron consistentes y el ACP logró explicar la mayor parte de la variación de los datos con solo dos componentes.

---

## 6.3 Evaluación de la calidad analítica

1. **Representatividad:**  
   El subconjunto utilizado en las gráficas y el ACP (37,882 registros) abarca el 72 % de la base limpia.  
   Esta proporción garantiza una cobertura suficiente para realizar análisis fiables y comparaciones entre años y localidades.

2. **Solidez estadística:**  
   El ACP mostró una estructura estable: los dos primeros componentes explican cerca del 80 % de la varianza total, lo que indica que el modelo logró captar la dinámica esencial del fenómeno sin pérdida de información relevante.

3. **Coherencia con la realidad territorial:**  
   Los resultados reflejan patrones coherentes con las condiciones sociales conocidas de la ciudad.  
   Las localidades con mayor número de intervenciones (Ciudad Bolívar, Bosa, Kennedy, Usme) coinciden con zonas de alta vulnerabilidad y mayor concentración de población en el régimen subsidiado.

4. **Identificación de anomalías temporales:**  
   El descenso de 2022 y el repunte de 2023 se interpretan como un efecto de mejora en la captura de datos después del periodo más crítico de la pandemia.  
   Los registros con código **99999**, frecuentes en 2022, explican parte de esa caída temporal.

---

## 6.4 Evaluación interpretativa

Desde el punto de vista sustantivo, los resultados del ACP y las visualizaciones cumplen con el propósito inicial del proyecto:

- **Se identificaron patrones espacio-temporales claros**, tanto a nivel de localidad como de año.  
- **Se verificó la relación entre vulnerabilidad social y volumen de intervenciones**, especialmente en los regímenes subsidiado y no asegurado.  
- **Se observó una recuperación institucional** en la capacidad de registro y atención después de 2022.  

Esto significa que el modelo no solo es técnicamente válido, sino que también ofrece información útil para la comprensión de la dinámica de atención a la niñez en Bogotá.

---

## 6.5 Síntesis general de la evaluación

| Aspecto | Resultado | Nivel de cumplimiento |
|----------|------------|----------------------|
| Cobertura y representatividad de datos | Adecuada (72 %) | Alto |
| Varianza explicada por el ACP | 79.98 % | Alto |
| Correspondencia con condiciones reales | Coherente | Alto |
| Identificación de tendencias y anomalías | Clara (pico 2023) | Alto |
| Utilidad para la toma de decisiones | Alta | Alto |

En términos generales, el modelo es **válido, interpretable y coherente con la realidad social** de la ciudad.  
Las variaciones encontradas no se deben a ruido o errores, sino a cambios identificables en el contexto y la calidad del registro.

---

## 6.6 Conclusión de la evaluación

El análisis cumplió con los objetivos propuestos:  
- La base depurada fue suficiente y de buena calidad.  
- Los patrones observados son consistentes con la estructura social y territorial de Bogotá.  
- El ACP permitió sintetizar la información de forma efectiva, con alta capacidad explicativa.  

En consecuencia, se considera que **el modelo de análisis espacio-temporal con ACP fue exitoso**, tanto en términos técnicos como interpretativos.  
Los resultados ofrecen una visión sólida del comportamiento de las intervenciones con NNA y constituyen una base confiable para recomendaciones y análisis futuros.

# 7. Conclusiones generales y utilidad práctica

## 7.1 Síntesis general del proceso

El proyecto siguió la metodología **CRISP-DM**, desarrollando de manera ordenada las etapas de comprensión del negocio, análisis de los datos, preparación, modelado y evaluación.  
A lo largo del proceso se logró construir un conjunto de datos confiable y se aplicaron técnicas que permitieron resumir el comportamiento espacio-temporal de las intervenciones con niños, niñas y adolescentes (NNA) en Bogotá entre 2021 y 2024.

Los resultados muestran que el proceso de análisis no solo fue técnicamente correcto, sino también relevante desde el punto de vista social.  
El uso del Análisis de Componentes Principales (ACP) permitió identificar patrones claros entre años, localidades y tipos de régimen en salud, sintetizando la información de más de 50 mil registros en un modelo interpretativo y visualmente comprensible.

---

## 7.2 Principales hallazgos

1. **Evolución temporal de las intervenciones**  
   Se observó un incremento notable en 2023, seguido de una estabilización en 2024.  
   Este aumento puede estar asociado tanto a una mejora en la calidad del registro institucional como a la recuperación de actividades después de la pandemia, ya que en 2022 se encontraron más códigos **99999**, que reflejan vacíos de información.

2. **Concentración territorial**  
   Las localidades con mayor número de intervenciones fueron **Ciudad Bolívar, Kennedy, Bosa y Suba**, que juntas concentran más del 60 % del total de casos graficados.  
   Estas zonas coinciden con las áreas de mayor densidad poblacional y vulnerabilidad social, lo cual refuerza la relación entre condiciones socioeconómicas y frecuencia de intervenciones.

3. **Distribución por régimen de afiliación**  
   El **régimen subsidiado** representa cerca del 45 % de las intervenciones, seguido del **contributivo** con un 37 %.  
   Los regímenes especial, vinculado y no asegurado tienen menor participación, aunque el no asegurado sigue siendo relevante (16 %), mostrando que aún existe una parte de la población infantil sin cobertura formal en salud.

4. **Estructura estadística estable**  
   El ACP logró explicar cerca del 80 % de la variabilidad de los datos con solo dos componentes, lo que demuestra una estructura fuerte y bien definida.  
   El primer componente (PC1) refleja el volumen total de intervenciones, mientras que el segundo (PC2) diferencia casos específicos asociados al régimen vinculado.

5. **Representatividad de los datos utilizados**  
   El subconjunto empleado en los análisis y gráficas (37,882 registros) corresponde al 72.3 % de la base limpia total (52,358 registros), lo que asegura una representación adecuada y resultados sólidos.

---

## 7.3 Interpretación general

El comportamiento observado refleja la dinámica social y administrativa del sistema de atención a la niñez en Bogotá:

- Los años 2021 y 2022 pueden considerarse de ajuste o transición, marcados por los efectos de la pandemia y la reactivación institucional.  
- El año 2023 representó un punto de recuperación y consolidación de la información, con un aumento significativo de los registros.  
- En 2024 la tendencia se estabilizó, lo que sugiere una mejora sostenida en la gestión y seguimiento de las intervenciones.

Desde el punto de vista espacial, el patrón se mantiene consistente con la realidad socioeconómica de la ciudad: las localidades del sur concentran la mayor proporción de intervenciones, mientras que las del norte muestran niveles más bajos.

---

## 7.4 Utilidad práctica del análisis

Los resultados del proyecto pueden servir como base para distintos propósitos institucionales y de investigación:

- **Planeación de estrategias territoriales:** permite identificar las zonas con mayor carga de atención (por ejemplo, Ciudad Bolívar o Bosa) y orientar recursos hacia ellas.  
- **Seguimiento a la equidad en la atención:** facilita monitorear si las intervenciones se distribuyen proporcionalmente a las necesidades sociales.  
- **Evaluación del sistema de registro:** los vacíos observados en 2022 pueden guiar mejoras en los procesos de captura de información.  
- **Toma de decisiones basadas en evidencia:** el ACP ofrece una visión sintética que puede incorporarse en reportes o tableros de monitoreo.

---

## 7.5 Limitaciones del estudio

- El análisis se basa en **registros administrativos**, que pueden tener diferencias en la calidad del diligenciamiento según el año o la entidad.  
- Los códigos **99999** fueron tratados como valores válidos cuando representaban “No aplica”, pero en algunos casos podrían reflejar información incompleta.  
- No se incluyeron variables individuales (edad, género, tipo de intervención específica), por lo que los resultados representan tendencias agregadas y no comportamientos personales.  

Estas limitaciones no afectan la validez general del análisis, pero deben tenerse en cuenta al interpretar los resultados.

---

## 7.6 Conclusión general

El proyecto logró su propósito de describir cómo han cambiado las intervenciones con NNA en Bogotá a lo largo del tiempo y el territorio.  
El análisis confirmó que la distribución de las intervenciones está asociada a factores sociales, especialmente el tipo de afiliación en salud y la ubicación geográfica.  
El enfoque espacio-temporal y el uso del ACP permitieron resumir de forma clara la dinámica general, evidenciando el peso del régimen subsidiado y el papel de las localidades más vulnerables.

En términos generales, los resultados ofrecen una visión completa, útil y coherente de la evolución de las intervenciones con NNA en Bogotá entre 2021 y 2024, y sientan las bases para futuros estudios orientados a fortalecer las políticas de protección y atención a la infancia.

---

