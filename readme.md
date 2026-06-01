# AIRA - Air Quality Prediction System

## Overview

AIRA (Air Quality Prediction System) is a hybrid machine learning system designed to predict future Air Quality Index (AQI) values using historical air pollution data and real-time environmental measurements.

The system combines:

* Long Short-Term Memory (LSTM) for time-series AQI forecasting.
* Extreme Gradient Boosting (XGBoost) for residual error correction.
* OpenAQ API for real-time air quality monitoring.
* FastAPI backend for prediction services.
* React dashboard for visualization and user interaction.
* Docker for local deployment.

This project was developed as part of the Digital Data Analysis and Processing course.

---

## Problem Statement

Air quality directly impacts public health and environmental sustainability. Accurate AQI prediction allows authorities and communities to take preventive actions before air pollution reaches dangerous levels.

Traditional forecasting methods often struggle to capture complex temporal patterns. To address this issue, AIRA implements a hybrid architecture that combines deep learning and ensemble learning techniques.

---

## Dataset

Dataset:

**Air Quality Data in India (2015–2020)**

Source:
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india

Main variables:

* PM2.5
* PM10
* NO
* NO2
* NOx
* NH3
* CO
* SO2
* O3
* AQI

Target Variable:

* AQI (Air Quality Index)

---

## Hybrid Model Architecture

### Stage 1 — LSTM AQI Forecasting

The LSTM model is trained using historical air quality observations and sliding window sequences.

Input:

* Historical pollutant measurements
* Time-series sequences

Output:

* Predicted AQI at t+1

---

### Stage 2 — XGBoost Residual Correction

After generating AQI predictions from the LSTM model, XGBoost is trained to predict residual errors.

Residual Formula:

Residual = AQI_actual − AQI_LSTM

Input Features:

* Pollutant measurements
* Temporal features
* LSTM AQI prediction

Output:

* Predicted residual value

---

### Final Prediction

AQI_final = AQI_LSTM + Residual_XGBoost

This approach allows the XGBoost model to learn systematic errors that remain after LSTM forecasting.

---

## System Architecture

OpenAQ API

↓

Realtime Data Collection

↓

Preprocessing Pipeline

↓

Frozen LSTM Model

↓

Residual XGBoost Model

↓

AQI Final Prediction

↓

AQI Category Mapping

↓

FastAPI Backend

↓

React Dashboard

---

## Technology Stack

### Machine Learning

* Python
* TensorFlow / Keras
* XGBoost
* Scikit-Learn
* Pandas
* NumPy

### Backend

* FastAPI
* Uvicorn

### Frontend

* React
* HTML
* CSS
* JavaScript

### Deployment

* Docker
* Docker Compose

### Data Source

* OpenAQ API

---

## Repository Structure

```text
airPredictions/
├── data/
├── notebooks/
├── src/
├── frontend/
├── models/
├── docs/
├── reports/
├── tests/
├── docker/
├── README.md
└── docker-compose.yml
```

Detailed folder descriptions can be found in the project documentation.

---

## Dashboard Features

* Real-time AQI monitoring
* Hybrid AQI prediction
* AQI category visualization
* Historical AQI trends
* Air quality alerts
* Model information display

---

## Current Limitations

* Model is trained on historical Indian air quality data.
* Model is frozen and does not perform online learning.
* Potential data drift may occur when using real-time OpenAQ data.
* Prediction quality depends on OpenAQ data availability.

---