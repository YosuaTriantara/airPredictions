# Repository Structure

This document describes the folder organization used in AIRA.

---

# Root Directory

```text
airPredictions/
```

Contains all source code, notebooks, models, documentation, reports, and deployment files.

---

# data/

```text
data/
├── raw/
├── interim/
├── processed/
└── external/
```

Purpose:

Store datasets used during development.

### raw/

Original dataset files.

Example:

```text
city_day.csv
```

### interim/

Intermediate outputs generated during preprocessing.

### processed/

Cleaned and model-ready datasets.

### external/

External data sources and API samples.

---

# notebooks/

```text
notebooks/
```

Contains exploratory analysis, preprocessing, training, and evaluation notebooks.

Naming Convention:

```text
01_*
02_*
03_*
```

Reserved Numbering:

```text
01-09  Data Engineering
11-19  LSTM
21-29  XGBoost Residual
31-39  Integration & Validation
```

---

# src/

```text
src/
```

Contains production-ready source code.

---

## src/preprocessing/

```text
src/preprocessing/
```

Responsibilities:

* Data cleaning
* Feature engineering
* Scaling
* Sliding window generation

---

## src/models/

```text
src/models/
```

Responsibilities:

* LSTM model definitions
* XGBoost model definitions
* Training utilities

---

## src/services/

```text
src/services/
```

Responsibilities:

* OpenAQ integration
* API validation
* Parameter mapping

---

## src/inference/

```text
src/inference/
```

Responsibilities:

* Realtime preprocessing
* LSTM inference
* XGBoost inference
* AQI category mapping
* Prediction pipeline

---

## src/api/

```text
src/api/
```

Responsibilities:

* REST API routes
* Request schemas
* Logging
* Configuration

---

# frontend/

```text
frontend/
```

Contains React dashboard application.

---

## frontend/pages/

Application pages.

```text
Overview
Prediction
Historical
About
```

---

## frontend/components/

Reusable UI components.

Examples:

```text
AQIStatusCard
AlertBanner
LoadingState
```

---

## frontend/services/

Frontend API integration.

---

# models/

```text
models/
```

Stores frozen models and preprocessing artifacts.

Structure:

```text
models/
├── scalers/
├── lstm/
└── xgboost/
```

---

# reports/

```text
reports/
```

Stores generated outputs.

Examples:

```text
Evaluation Reports
Testing Reports
Figures
Deployment Reports
```

---

# docs/

```text
docs/
```

Contains project documentation.

Examples:

```text
project_structure.md
```

---

# tests/

```text
tests/
```

Contains automated testing scripts.

Examples:

```text
test_model_loading.py
test_prediction_pipeline.py
test_api_predict.py
```

---

# docker/

```text
docker/
```

Contains Docker-related configuration.

Examples:

```text
backend.Dockerfile
frontend.Dockerfile
```

---

# Naming Conventions

Python Files:

```text
snake_case.py
```

Classes:

```python
PascalCase
```

Functions:

```python
snake_case()
```

Variables:

```python
snake_case
```

React Components:

```text
PascalCase.jsx
```

Examples:

```text
AQIStatusCard.jsx
PredictionPage.jsx
```