# ECU911 Predictor — Análisis y Modelo de Predicción de Emergencias (2021–2025)

**Autor:** Brandon Minta  
**Programa:** MSc Data Science – Montebello Academy  
**Despliegue interactivo:**  
 [ECU911 Predictor (Streamlit)](https://app-practice-app-bqyspxatorm2maqiylkuy7.streamlit.app/)

---

## Descripción del proyecto

Este proyecto desarrolla un modelo estadístico para **predecir el número esperado de emergencias diarias** en cada provincia del Ecuador, utilizando datos abiertos del **Servicio Integrado de Seguridad ECU911** (2021–2025).

A partir de más de **4.7 millones de registros**, se realiza un análisis exploratorio, se detectan patrones temporales y espaciales, y se entrena un modelo **GLM (Generalized Linear Model)** con distribución **Negative Binomial**, implementado y desplegado mediante **Streamlit**.

---

## Objetivos

1. Analizar la distribución temporal y geográfica de las emergencias en Ecuador (2021–2025).  
2. Identificar patrones relacionados con población, fines de semana y feriados.  
3. Construir un modelo predictivo ajustado por tamaño poblacional.  
4. Desplegar una interfaz interactiva para explorar predicciones por provincia y rango de fechas.

---

##  Hallazgos principales

- Se observó una **alta correlación entre el tamaño poblacional y el número de emergencias**, por lo que se introdujo un **offset logarítmico de población** (`log(pop)`) para modelar **tasas de ocurrencia**, no conteos brutos.  
- Los **fines de semana (viernes–domingo)** presentan un incremento sostenido de emergencias (~20 % más que días laborables).  
- Los **feriados** generan solo picos esporádicos, menos significativos que el efecto de fin de semana.  
- Provincias como **Pichincha** y **Guayas** concentran la mayor carga operativa absoluta, mientras que provincias andinas y amazónicas destacan al ajustar por población (incidencias por 100k habitantes).  
- Se confirma **sobredispersión** en los datos → justifica el uso del modelo **Negative Binomial GLM** sobre Poisson o regresión lineal.

---

##  Modelo seleccionado

**Generalized Linear Model – Negative Binomial**

\[
\log(E[Y]) = \beta_0 + \beta_1X_1 + \dots + \beta_kX_k + \log(\text{población})
\]

- `Y`: número de emergencias diarias por provincia  
- `X`: variables explicativas (día de semana, feriado, año, estacionalidad, etc.)  
- `offset`: log(población) → ajusta por el tamaño poblacional  

### Ventajas
Adecuado para datos de conteo sobredispersos  
Mantiene interpretabilidad (coeficientes, significancia)  
Evita sobreajuste (RMSE similar entre train y test)  
Permite estimar tasas ajustadas por población  

---

## Métricas de desempeño

| Métrica        | Train | Test | Interpretación |
|----------------|-------|------|----------------|
| **RMSE**       | 97.7  | 95.5 | Error medio absoluto (en conteos reales) |
| **nRMSE**      | –     | 0.256 | Error relativo ≈ 25 % |
| **Pseudo R²**  | –     | 0.09  | Típico en datos de conteo sobredispersos |

El modelo presenta **buen equilibrio** entre ajuste e interpretabilidad, sin indicios de sobreajuste.

---

## ⚙️ Estructura de la aplicación

### `app.py`
Aplicación Streamlit que permite:
- Seleccionar una **provincia** y un **rango de fechas**.  
- Ejecutar la función `predecir_incidentes()` para generar estimaciones diarias.  
- Mostrar resultados y totales estimados en tiempo real.

### `modelo_neg_binomial.pkl`
Modelo entrenado con `statsmodels` (GLM Negative Binomial).

### `data/poblacion_provincias_ecuador_2022.csv`
Fuente de datos de población por provincia (INEC 2022).

---

## Librerías principales

| Librería | Propósito |
|-----------|------------|
| **Streamlit** | Interfaz web interactiva |
| **Pandas** | Manipulación de datos tabulares |
| **NumPy** | Cálculo numérico y funciones trigonométricas |
| **Statsmodels** | Entrenamiento y predicción del modelo GLM |
| **Patsy** | Construcción de matrices de diseño a partir de fórmulas (`C(provincia) + ...`) |
| **Matplotlib / Seaborn** | Visualización y análisis exploratorio |
| **Pickle** | Serialización y carga del modelo entrenado |

---
