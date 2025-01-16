# nequi-data-engineer

- [nequi-data-engineer](#nequi-data-engineer)
  - [Paso 1: Alcance del proyecto y captura de datos](#paso-1-alcance-del-proyecto-y-captura-de-datos)
    - [Identificación y recopilación de datos](#identificación-y-recopilación-de-datos)
      - [**1. Users Data (`users_data.csv`)**](#1-users-data-users_datacsv)
      - [**2. Transactions Data (`transactions_data.csv`)**](#2-transactions-data-transactions_datacsv)
      - [**3. Cards Data (`cards_data.csv`)**](#3-cards-data-cards_datacsv)
    - [**Motivación para la selección de estos datos**](#motivación-para-la-selección-de-estos-datos)
    - [Casos de uso final de los datos](#casos-de-uso-final-de-los-datos)
      - [**1. Análisis de comportamiento del cliente**](#1-análisis-de-comportamiento-del-cliente)
      - [**2. Evaluación financiera y detección de riesgos**](#2-evaluación-financiera-y-detección-de-riesgos)
    - [Objetivo](#objetivo)
    - [**Actualización y acceso a los datos**](#actualización-y-acceso-a-los-datos)
  - [Paso 2: Explorar y evaluar los datos (EDA)](#paso-2-explorar-y-evaluar-los-datos-eda)
    - [Resultados de la exploración](#resultados-de-la-exploración)
      - [**1. Tabla `cards_data`**](#1-tabla-cards_data)
      - [**2. Tabla `users_data`**](#2-tabla-users_data)
      - [**3. Tabla `transactions_data`**](#3-tabla-transactions_data)
    - [Pasos necesarios para la limpieza de datos](#pasos-necesarios-para-la-limpieza-de-datos)
      - [**Manejo de valores faltantes**](#manejo-de-valores-faltantes)
      - [**Eliminación de duplicados**](#eliminación-de-duplicados)
      - [**Corrección de errores de formato**](#corrección-de-errores-de-formato)
      - [**Validaciones lógicas**](#validaciones-lógicas)

## Paso 1: Alcance del proyecto y captura de datos

### Identificación y recopilación de datos

Para llevar a cabo este proyecto, se han identificado tres conjuntos de datos clave provenientes de un entorno bancario. Estos datos contienen información relevante sobre usuarios, transacciones y tarjetas, lo que permite abordar diferentes casos de uso relacionados con análisis de comportamiento y evaluación financiera. Los datos fueron obtenidos de la plataforma Kaggle y se pueden encontrar en:

<https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?select=users_data.csv>

Los datos fueron recopilados durante la decada de los 2010.

A continuación, se describen los archivos disponibles:

#### **1. Users Data (`users_data.csv`)**

Este archivo contiene información demográfica y financiera de los clientes. Algunas de las columnas más destacadas incluyen:

- `id`: Identificador único del cliente.
- `current_age`: Edad actual del cliente.
- `retirement_age`: Edad estimada de retiro.
- `yearly_income`: Ingreso anual del cliente.
- `credit_score`: Puntuación crediticia.
- `num_credit_cards`: Número total de tarjetas de crédito asociadas.

**Uso principal:**  
Este archivo brinda información relevante para analizar el perfil financiero de los clientes y realizar segmentaciones basadas en edad, ingresos y comportamiento crediticio.

---

#### **2. Transactions Data (`transactions_data.csv`)**

Este archivo registra las transacciones realizadas por los clientes, incluyendo detalles sobre los montos, ubicación de los comerciantes y posibles errores en las transacciones. Las columnas clave incluyen:

- `id`: Identificador único de la transacción.
- `date`: Fecha de la transacción.
- `client_id`: Identificador del cliente asociado.
- `amount`: Monto de la transacción.
- `merchant_city` y `merchant_state`: Ubicación del comerciante.

**Uso principal:**  
Proporciona información granular para analizar el comportamiento de gasto, patrones de transacción y posibles anomalías o errores.

---

#### **3. Cards Data (`cards_data.csv`)**

Este archivo incluye información sobre las tarjetas de crédito y débito emitidas a los clientes, como límites de crédito y características de seguridad. Entre las columnas más relevantes están:

- `id`: Identificador único de la tarjeta.
- `client_id`: Identificador del cliente asociado.
- `card_type`: Tipo de tarjeta (crédito o débito).
- `credit_limit`: Límite de crédito asignado.
- `card_on_dark_web`: Indicador de si la tarjeta ha sido detectada en mercados ilícitos.

**Uso principal:**  
Ayuda a evaluar el perfil financiero del cliente y detectar posibles riesgos asociados a tarjetas comprometidas.

---

### **Motivación para la selección de estos datos**

La principal motivación para utilizar este conjunto de datos es su relación con posibles procesos dentro de Nequi, ya que se busca utilizar datos relacionados con la banca y transacciones.

**Formato de los datos:**  
Los archivos están en formato CSV y serán almacenados en un bucket de **AWS S3** para facilitar su procesamiento y acceso mediante servicios como **AWS Glue** y **Athena**.

### Casos de uso final de los datos

El propósito de este proyecto es preparar los datos para su integración en casos de uso estratégicos, asegurando que las transformaciones y consolidaciones necesarias se completen hasta el final de la tubería de datos. A continuación, se describen los principales casos de uso finales hacia los cuales se orientará la preparación de los datos:

---

#### **1. Análisis de comportamiento del cliente**

Preparar los datos necesarios para habilitar futuros análisis de comportamiento del cliente. Estos análisis permitirán:

- Facilitar la **segmentación de clientes** basada en datos demográficos y financieros.
- Brindar una base sólida para modelos predictivos de **churn** (deserción de clientes).
- Proveer datos organizados para diseñar **recomendaciones personalizadas** según el historial de consumo.

---

#### **2. Evaluación financiera y detección de riesgos**

Preparar los datos necesarios para que se puedan desarrollar sistemas de monitoreo y evaluación financiera. Esto incluye:

- Consolidar información sobre transacciones para detectar posibles anomalías.
- Centralizar indicadores como `card_on_dark_web` y `credit_score` para la evaluación de riesgos.
- Proveer datos organizados sobre clientes y tarjetas para facilitar el desarrollo de reportes y análisis futuros.

---

### Objetivo

El propósito de este proyecto es la construcción de una tubería de datos que permita:

- La integración y transformación de los datos en un formato coherente y centralizado.
- La entrega de datos listos para ser utilizados en análisis operativos y estratégicos.
- La garantía de que los datos sean accesibles y consistentes a través de recursos como **AWS S3** y consultas en **AWS Athena**.

---

### **Actualización y acceso a los datos**

Se propone una frecuencia de actualización diaria para garantizar que los datos procesados estén actualizados y disponibles para análisis posteriores. El pipeline será diseñado para automatizar este proceso, utilizando herramientas como **AWS Glue** y **DBT**.

## Paso 2: Explorar y evaluar los datos (EDA)

Para realizar la exploración de los datos, se optó por trabajar en un notebook de Jupyter, permitiendo verificar el estado de los datos directamente desde la fuente. El notebook utilizado para el análisis se encuentra disponible en la carpeta **eda**.

### Resultados de la exploración

A continuación, se detallan los hallazgos de la exploración de las tres tablas principales del dataset:

#### **1. Tabla `cards_data`**

- No se encontraron valores nulos en ninguna columna.
- No se detectaron registros duplicados.
- Todas las columnas cumplen con el tipo de dato esperado.
- No se identificaron problemas estructurales o de calidad en esta tabla.

#### **2. Tabla `users_data`**

- Al igual que la tabla `cards_data`, no presenta valores nulos ni duplicados.
- Los datos cumplen con los formatos necesarios, incluyendo los campos numéricos y categóricos.
- La tabla está en condiciones óptimas para continuar con los siguientes pasos del proyecto.

#### **3. Tabla `transactions_data`**

- A pesar del volumen de datos (más de 13 millones de registros), la tabla está en buenas condiciones generales.
- No se encontraron registros duplicados.
- Las columnas relevantes no contienen valores nulos; sin embargo, algunas columnas opcionales presentan valores faltantes permitidos.
- Todas las columnas cumplen con los formatos esperados.

---

### Pasos necesarios para la limpieza de datos

Aunque las tablas presentan una calidad aceptable, se sugieren los siguientes pasos de limpieza para asegurar la consistencia y preparar los datos para su uso en el pipeline:

#### **Manejo de valores faltantes**

- Imputar valores faltantes en columnas numéricas (e.g., rellenar con `0` en caso de ser apropiado).
- Completar valores categóricos faltantes (e.g., `card_type`, `merchant_state`) utilizando una categoría estándar como `"desconocido"`.

#### **Eliminación de duplicados**

- Remover registros duplicados en cada tabla, verificando los identificadores únicos.

#### **Corrección de errores de formato**

- Uniformar las fechas al formato estándar `YYYY-MM-DD` en las tablas `transactions_data` y `cards_data`.
- Validar que los valores numéricos (e.g., `amount`, `credit_score`) no contengan caracteres inválidos.

#### **Validaciones lógicas**

- Asegurar la coherencia entre las columnas `current_age` y `retirement_age` en la tabla `users_data`.

---

Estos son algunos pasos que podrían garantizar que los datos estén completamente preparados para ser utilizados en las siguientes etapas del proyecto. Estos pasos se encuentran representados en los diagramas del siguiente paso.
