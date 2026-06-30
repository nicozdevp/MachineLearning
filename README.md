# Predicción de Precios de Viviendas con Machine Learning

---

## Descripción

Este proyecto desarrolla un análisis de datos sobre el mercado inmobiliario utilizando un dataset real de propiedades en Bangladesh. El objetivo es identificar los factores que influyen en el precio de las viviendas y preparar la información para la construcción de un modelo predictivo basado en Machine Learning.

---

## Fuente de datos

El dataset utilizado proviene de Kaggle:

https://www.kaggle.com/datasets/durjoychandrapaul/house-price-bangladesh

Este conjunto de datos contiene propiedades de distintas ciudades como Dhaka, Chattogram, Cumilla, Narayanganj y Gazipur, incluyendo variables como número de habitaciones, baños, superficie y precio. ([Kaggle][1])

---

## Variables principales

El dataset incluye las siguientes características relevantes:

* **Bedrooms**: número de habitaciones
* **Bathrooms**: número de baños
* **Floor_no**: número de piso
* **Floor_area**: superficie en pies cuadrados
* **City**: ciudad de la propiedad
* **Location**: ubicación específica
* **Occupancy_status**: estado de ocupación
* **Price_in_taka**: precio de la propiedad

Estas variables permiten analizar el comportamiento del mercado y construir modelos de predicción de precios. 

---

## Objetivo

Desarrollar un modelo de análisis que permita:

* Identificar los factores que afectan el precio de las viviendas
* Analizar la relación entre variables mediante correlación
* Preparar los datos para su uso en Machine Learning
* Predecir el valor de una propiedad según sus características

---

## Metodología

El proyecto sigue la metodología **CRISP-DM**:

1. **Business Understanding**
   Definición del problema: predicción de precios inmobiliarios.

2. **Data Understanding**
   Exploración del dataset y análisis de variables.

3. **Data Preparation**

   * Eliminación de variables irrelevantes (ej: `Title`)
   * Tratamiento de outliers
   * Estandarización de datos
   * Limpieza de valores

4. **Modeling **
   Preparación del dataset para modelos predictivos.

5. **Evaluation **
   Uso de matriz de correlación y heatmap para analizar relaciones.

6. **Training**
   * Regresión Lineal Múltiple como modelo base
   * Árbol de Decisión Regresor como modelo avanzado
   * Árbol de Decisión Clasificador sobre categorías de precio
   * Naive Bayes (GaussianNB) como modelo probabilístico de clasificación

7. **Deployment**
   Expansión del dataset mediante web scraping desde bdhousing.com (+1,972 filas).
---

## Análisis realizado

* Limpieza y depuración del dataset
* Eliminación de columnas no relevantes
* Detección y tratamiento de outliers
* Estandarización de variables numéricas
* Construcción de matriz de correlación
* Visualización de datos con heatmap
* Predicción con modelos de regresión y clasificación

---

## Modelos predictivos

### Regresión (predicción de precio exacto en Takas)

Se implementaron dos modelos de regresión para predecir el valor numérico de cada propiedad. El dataset se dividió en 80% entrenamiento y 20% prueba (`random_state=42`).

#### Regresión Lineal Múltiple

| Métrica | Valor |
|---|---|
| R² (Coeficiente de determinación) | 0.1909 |
| MAE (Error absoluto medio) | ৳28,466,440 Takas |
| MSE (Error cuadrático medio) | ৳810,123,160,710,525 Takas² |
| RMSE (Raíz del error cuadrático) | ৳28,462,662 Takas |

El bajo R² confirma que el mercado inmobiliario no sigue una relación lineal. La ubicación geográfica tiene un impacto no lineal que este modelo no puede capturar.

#### Árbol de Decisión Regresor (`max_depth=10`)

| Métrica | Valor |
|---|---|
| R² (Coeficiente de determinación) | 0.8025 |
| MAE (Error absoluto medio) | ৳4,173,490 Takas |
| MSE (Error cuadrático medio) | ৳441,445,328,710,320 Takas² |
| RMSE (Raíz del error cuadrático) | ৳14,062,934 Takas |

El Árbol de Decisión superó ampliamente a la Regresión Lineal al poder crear reglas de corte por zona geográfica, mejorando el R² de 19% a 80%.

---

### Clasificación (predicción de categoría de precio)

Para aplicar métricas de clasificación, el precio continuo fue transformado en 3 categorías basadas en los percentiles 25 y 75 del dataset:

| Categoría | Rango en Takas |
|---|---|
| Bajo | < 4,900,000 |
| Medio | 4,900,000 — 11,000,000 |
| Alto | > 11,000,000 |

Se implementaron dos modelos de clasificación y se compararon sus resultados.

#### Árbol de Decisión Clasificador (`max_depth=10`)

| Métrica | Valor |
|---|---|
| Accuracy | 0.8499 |
| Precisión | 0.8525 |
| Recall | 0.8499 |
| F1-Score | 0.8492 |

#### Naive Bayes (GaussianNB)

Se utilizó GaussianNB junto con los datos estandarizados (`StandardScaler`) para mejorar la compatibilidad con el supuesto gaussiano del modelo.

| Métrica | Valor |
|---|---|
| Accuracy | 0.6624 |
| Precisión | 0.6987 |
| Recall | 0.6624 |
| F1-Score | 0.6352 |

**Análisis por categoría (Naive Bayes):**

| Categoría | Precisión | Recall | F1 |
|---|---|---|---|
| Bajo | 0.72 | 0.57 | 0.64 |
| Medio | 0.63 | 0.89 | 0.74 |
| Alto | 0.83 | 0.28 | 0.42 |

El modelo presenta un sesgo marcado hacia la clase Medio (la más frecuente). Solo detecta el 28% de las propiedades de precio Alto, clasificando 122 de 186 propiedades caras como Medio. Esto se debe a que el supuesto de independencia entre variables viola la naturaleza del mercado inmobiliario, donde el precio depende de la combinación de ubicación y características físicas.

#### Comparación de modelos de clasificación

| Modelo | Accuracy | F1-Score |
|---|---|---|
| Árbol de Decisión | **0.8499** | **0.8492** |
| Naive Bayes | 0.6624 | 0.6352 |

El Árbol de Decisión supera al Naive Bayes en ~18 puntos porcentuales por su capacidad de crear reglas geográficas específicas sin asumir independencia entre variables.

---

## Métricas implementadas

### Métricas de Regresión
| Métrica | Descripción |
|---|---|
| **R²** | Proporción de varianza del precio explicada por el modelo |
| **MAE** | Promedio del error absoluto en Takas |
| **MSE** | Promedio del error al cuadrado (penaliza errores grandes) |
| **RMSE** | Raíz del MSE, en las mismas unidades que el precio |

### Métricas de Clasificación
| Métrica | Descripción |
|---|---|
| **Accuracy** | Porcentaje total de predicciones correctas |
| **Precisión** | De las predicciones de una clase, cuántas fueron correctas |
| **Recall** | De los casos reales de una clase, cuántos fueron detectados |
| **F1-Score** | Media armónica entre Precisión y Recall |
| **Matriz de Confusión** | Tabla de aciertos y errores por categoría |

---

## Errores durante el proceso
* Cantidad de nulos en distintas columnas.
* Binary Code mal ejecutado en variable categorica.
* Bajo porcentaje de predicción del modelo de regresión lineal simple.
* Violación del supuesto gaussiano en Naive Bayes por columnas binarias del encoding de Location.
* Pérdida accidental de filas del CSV original durante la deduplicación del scraping (corregido mediante backup generado en el análisis).

---

## Expansión del Dataset mediante Web Scraping

Con el objetivo de enriquecer el dataset original y mejorar la representatividad del modelo, se realizó un proceso de web scraping para obtener nuevas propiedades inmobiliarias desde una fuente externa.

### Fuente de datos adicional

**[bdhousing.com](https://www.bdhousing.com)** — Mayor portal inmobiliario de Bangladesh con más de 150,000 listings. Se eligió esta fuente por:

* No utiliza protección Cloudflare, lo que permite hacer requests directos sin navegador
* Estructura HTML estática y consistente, fácil de parsear
* Cubre exactamente las mismas ciudades del dataset original

### Herramientas utilizadas

* **cloudscraper** — Emula headers de navegador real a nivel de TLS para evitar bloqueos básicos
* **BeautifulSoup4** — Parseo y extracción de elementos HTML
* **Pandas** — Integración y deduplicación con el CSV original

### Método de extracción

Se desarrolló el script `scraper_bikroy.py` que realiza el siguiente proceso:

1. Recorre 50 páginas por cada ciudad (250 páginas en total)
2. Por cada página extrae: Título, Precio, Ubicación, Habitaciones, Baños y Área
3. Convierte los precios del formato bengalí (`৳ 2.99 Cr.` / `৳ 80 Lac`) a enteros en Takas
4. Filtra propiedades sin precio (no aptas para el modelo)
5. Deduplica contra el CSV original usando el Título como clave única
6. Agrega solo filas nuevas sin modificar los datos originales

### Selectores CSS utilizados (estructura de bdhousing.com)

| Campo | Selector |
|---|---|
| Tarjeta contenedora | `div.flex-row` |
| Título | `h1.title.fix_title` |
| Precio | `label.control-label1.new` |
| Ubicación | `p.location` |
| Habitaciones | `div.listing-info.bedroom > span.number` |
| Baños | `div.listing-info.bath > span.number` |
| Área (sqft) | `div.listing-info.size > span.number` |

### Resultado del scraping

| Métrica | Valor |
|---|---|
| Dataset original (Kaggle) | 3,865 filas |
| Filas nuevas agregadas | 1,972 filas |
| **Dataset final** | **5,837 filas** |

**Distribución final por ciudad:**

| Ciudad | Filas |
|---|---|
| Chattogram | 1,960 |
| Dhaka | 1,681 |
| Narayanganj | 904 |
| Gazipur | 664 |
| Cumilla | 628 |
| **Total** | **5,837** |

### Consideraciones

* El campo `Floor_no` no está disponible en el listado de bdhousing, se imputa con `None` y el pipeline del notebook lo completa con el valor por defecto `1`
* El campo `Occupancy_status` se asigna como `vacant` por defecto
* El campo `Title` en las filas originales del Kaggle fue reconstruido como vacío al restaurar desde el backup generado durante el análisis

---

## Tecnologías utilizadas

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Cloudscraper
* BeautifulSoup4
* Google Colab

---

## Estructura del proyecto

```
MachineLearning-MineriadeDatos/
├── MachineLearning_MineriadeDatos.ipynb   ← Notebook principal con todo el análisis
├── scraper_bikroy.py                      ← Script de web scraping (bdhousing.com)
├── house_price_bd.csv                     ← Dataset (original Kaggle + scraping)
├── looker_data/                           ← Exports CSV para Looker Studio
│   ├── datos_procesados.csv
│   ├── estadisticas_ciudad.csv
│   ├── predicciones_regresion.csv
│   ├── metricas_regresion.csv
│   ├── predicciones_clasificacion.csv
│   ├── metricas_clasificacion.csv
│   ├── matriz_confusion.csv
│   └── distribucion_categorias.csv
├── dashboard_inmobiliario.html            ← Dashboard interactivo con los datos ya explotados
└── README.md
```

---

## Dashboard interactivo (datos explotados)

Para comunicar los resultados del análisis de forma visual, se construyó un dashboard HTML autocontenido: **[`dashboard_inmobiliario.html`](dashboard_inmobiliario.html)**. Se puede abrir directamente en cualquier navegador, sin necesidad de instalar nada.

El dashboard toma los datos ya procesados por el notebook (limpieza, outliers, predicciones y métricas) y los presenta en un formato ejecutivo, pensado para que cualquier persona — no solo quien programó el modelo — pueda entender los hallazgos de un vistazo.

**Contenido del dashboard:**

* **Filtro por ciudad**, para explorar el mercado de Dhaka, Chattogram, Cumilla, Narayanganj y Gazipur por separado
* **KPIs generales** del dataset (5.381 propiedades analizadas)
* **Precio promedio por ciudad** — confirma que Dhaka, la capital, lidera el valor del mercado
* **Distribución de propiedades por rango de precio** (Bajo / Medio / Alto), según los percentiles 25 y 75
* **Precio frente a superficie construida** (scatter plot) — muestra que el tamaño influye, pero no determina el precio: la ubicación introduce saltos que el área por sí sola no explica
* **Comparación de modelos de clasificación** (Árbol de Decisión vs. Naive Bayes)
* **Comparación de modelos de regresión** (Regresión Lineal vs. Árbol de Decisión Regresor)
* **Veredicto final**: el Árbol de Decisión es el modelo que mejor performa tanto en clasificación como en regresión, por su capacidad de generar reglas de corte según la zona geográfica

### Reporte complementario en Looker Studio

Además del dashboard HTML, los datos exportados a `looker_data/` fueron utilizados para construir un reporte en **Google Looker Studio (Data Studio)**, disponible en:

🔗 [Ver reporte en Looker Studio](https://datastudio.google.com/reporting/3016b38e-17e5-4591-9b36-9e0b6c7ca9fa)

Este reporte permite explorar de forma interactiva las estadísticas por ciudad, la matriz de confusión y las métricas de los modelos de regresión y clasificación, complementando la visualización ofrecida por el dashboard HTML.

---

## Acerca de este README

Este archivo documenta el trabajo completo del proyecto: desde la fuente de datos y la metodología CRISP-DM aplicada, pasando por la limpieza y expansión del dataset mediante web scraping, hasta los modelos de Machine Learning entrenados (regresión y clasificación) y sus métricas de evaluación. También enlaza los dos artefactos visuales generados a partir de esos resultados: el dashboard HTML local y el reporte en Looker Studio.

---


