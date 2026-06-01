#!/bin/bash

# Script to create all 21 issues in YosuaTriantara/airPredictions repository

REPO="YosuaTriantara/airPredictions"

# Issue 2: Define Residual XGBoost Features
gh issue create -R "$REPO" \
  --title "Define Residual XGBoost Features" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** S

**Description:**
Menentukan fitur input untuk XGBoost residual model.

**Candidate Features:**
- PM2.5
- PM10
- NO
- NO2
- NOx
- NH3
- CO
- SO2
- O3
- hour
- day
- month
- weekday
- AQI_LSTM_prediction

**Deliverables:**
- notebooks/22_residual_feature_selection.ipynb
- docs/residual_features.md
- data/processed/residual_feature_columns.json

**Definition of Done:**
- Daftar fitur residual final tersedia.
- residual hanya digunakan sebagai target.
- AQI_actual tidak digunakan sebagai fitur.
- AQI_LSTM_prediction digunakan sebagai augmented feature."

# Issue 3: Analyze Residual Distribution
gh issue create -R "$REPO" \
  --title "Analyze Residual Distribution" \
  --body "**Component:** Residual XGBoost
**Priority:** P1
**Sprint:** Sprint 1
**Effort:** S

**Description:**
Menganalisis distribusi residual LSTM untuk mengetahui apakah XGBoost layak digunakan sebagai koreksi error.

**Deliverables:**
- notebooks/23_residual_distribution_analysis.ipynb
- reports/residual_distribution_report.md

**Definition of Done:**
- Distribusi residual divisualisasikan.
- Mean residual dihitung.
- Standard deviation residual dihitung.
- Pola overprediction/underprediction LSTM dijelaskan."

# Issue 4: Train Baseline XGBoost Residual Model
gh issue create -R "$REPO" \
  --title "Train Baseline XGBoost Residual Model" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** M

**Description:**
Melatih baseline XGBoost untuk memprediksi residual error LSTM.

**Target**
residual

**Deliverables:**
- notebooks/24_xgboost_residual_baseline_training.ipynb
- models/xgboost/baseline_xgb_residual_model.pkl

**Definition of Done:**
- Model XGBoost berhasil dilatih.
- Target training adalah residual.
- Model baseline tersimpan.
- Training berjalan tanpa error."

# Issue 5: Evaluate Baseline Residual Model
gh issue create -R "$REPO" \
  --title "Evaluate Baseline Residual Model" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** M

**Description:**
Mengevaluasi kemampuan XGBoost dalam memprediksi residual.

**Metrics:**
- MAE residual
- RMSE residual
- R² residual

**Deliverables:**
- notebooks/25_xgboost_residual_baseline_evaluation.ipynb
- reports/xgb_residual_baseline_evaluation.md

**Definition of Done:**
- Metric residual tersedia.
- Predicted residual dibandingkan dengan actual residual.
- Visualisasi residual actual vs predicted dibuat."

# Issue 6: Tune XGBoost Residual Hyperparameters
gh issue create -R "$REPO" \
  --title "Tune XGBoost Residual Hyperparameters" \
  --body "**Component:** Residual XGBoost
**Priority:** P1
**Sprint:** Sprint 1
**Effort:** L

**Description:**
Melakukan tuning terbatas pada model XGBoost residual.

**Parameters:**
- n_estimators
- max_depth
- learning_rate
- subsample
- colsample_bytree
- reg_lambda
- reg_alpha

**Deliverables:**
- notebooks/26_xgboost_residual_tuning.ipynb
- reports/xgb_residual_tuning_results.csv
- reports/xgb_residual_tuning_summary.md

**Definition of Done:**
- Minimal 3 kombinasi parameter diuji.
- Konfigurasi terbaik dipilih.
- Hasil tuning terdokumentasi."

# Issue 7: Train Final XGBoost Residual Model
gh issue create -R "$REPO" \
  --title "Train Final XGBoost Residual Model" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** M

**Description:**
Melatih model XGBoost residual final menggunakan konfigurasi terbaik.

**Deliverables:**
- notebooks/27_xgboost_residual_final_training.ipynb
- models/xgboost/final_xgb_residual_model.pkl

**Definition of Done:**
- Model final berhasil dilatih.
- Model tersimpan dalam format .pkl.
- Konfigurasi final terdokumentasi."

# Issue 8: Freeze XGBoost Residual Model
gh issue create -R "$REPO" \
  --title "Freeze XGBoost Residual Model" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** S

**Description:**
Membekukan model XGBoost final agar dapat digunakan dalam pipeline inferensi.

**Deliverables:**
- models/xgboost/frozen_xgb_residual_model.pkl
- models/xgboost/xgb_residual_metadata.json

**Definition of Done:**
- Frozen model tersedia.
- Metadata berisi feature columns, metric, dan training date.
- Model dapat di-load ulang."

# Issue 9: Calculate Final Hybrid AQI Prediction
gh issue create -R "$REPO" \
  --title "Calculate Final Hybrid AQI Prediction" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** M

**Description:**
Menghitung hasil akhir prediksi AQI setelah koreksi residual.

**Formula:**
AQI_final = AQI_LSTM_prediction + Residual_XGBoost_prediction

**Deliverables:**
- notebooks/28_calculate_hybrid_prediction.ipynb
- data/processed/hybrid_test_predictions.csv

**Definition of Done:**
- Prediksi residual XGBoost tersedia.
- AQI_final berhasil dihitung.
- AQI_final dapat dibandingkan dengan AQI_actual."

# Issue 10: Evaluate Hybrid Model Performance
gh issue create -R "$REPO" \
  --title "Evaluate Hybrid Model Performance" \
  --body "**Component:** Residual XGBoost
**Priority:** P0
**Sprint:** Sprint 1
**Effort:** M

**Description:**
Membandingkan performa LSTM saja dengan LSTM + XGBoost residual correction.

**Comparison:**
- LSTM only
- vs
- LSTM + XGBoost Residual

**Metrics:**
- MAE
- RMSE
- R²

**Deliverables:**
- notebooks/29_hybrid_model_evaluation.ipynb
- reports/hybrid_model_evaluation.md
- reports/figures/hybrid_actual_vs_prediction.png

**Definition of Done:**
- Metric LSTM only tersedia.
- Metric hybrid tersedia.
- Improvement atau penurunan performa dijelaskan.
- Grafik actual vs prediction tersedia."

# Issue 11: Create AQI Category Mapping
gh issue create -R "$REPO" \
  --title "Create AQI Category Mapping" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Membuat fungsi mapping dari AQI numerik final menjadi kategori kualitas udara.

**Categories:**
- Good
- Satisfactory
- Moderate
- Poor
- Very Poor
- Severe

**Deliverables:**
- notebooks/30_aqi_category_mapping_validation.ipynb
- src/inference/aqi_category_mapper.py

**Definition of Done:**
- Fungsi mapping tersedia.
- Setiap range AQI memiliki kategori.
- Output kategori konsisten.
- Fungsi bisa digunakan oleh backend."

# Issue 12: Validate Hybrid Output with AQI Category
gh issue create -R "$REPO" \
  --title "Validate Hybrid Output with AQI Category" \
  --body "**Component:** Inference Pipeline
**Priority:** P1
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Memastikan output numerik AQI final dapat dikonversi menjadi kategori kualitas udara.

**Deliverables:**
- notebooks/31_hybrid_category_validation.ipynb
- reports/hybrid_category_distribution.md

**Definition of Done:**
- Distribusi kategori hasil hybrid tersedia.
- Tidak ada AQI final yang gagal dikategorikan.
- Contoh output numerik dan kategori ditampilkan."

# Issue 13: Research OpenAQ API Response Format
gh issue create -R "$REPO" \
  --title "Research OpenAQ API Response Format" \
  --body "**Component:** OpenAQ Integration
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Mempelajari struktur response OpenAQ API dan kesesuaiannya dengan fitur model.

**Deliverables:**
- docs/openaq_response_structure.md
- docs/openaq_parameter_mapping.md

**Definition of Done:**
- Struktur response API terdokumentasi.
- Parameter polutan OpenAQ teridentifikasi.
- Perbedaan nama parameter dengan dataset training dicatat."

# Issue 14: Implement OpenAQ Data Fetching
gh issue create -R "$REPO" \
  --title "Implement OpenAQ Data Fetching" \
  --body "**Component:** OpenAQ Integration
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** M

**Description:**
Membuat service untuk mengambil data kualitas udara realtime dari OpenAQ API.

**Deliverables:**
- src/services/openaq_service.py
- notebooks/32_openaq_fetching_test.ipynb

**Definition of Done:**
- Data berhasil diambil dari OpenAQ.
- Lokasi/kota dapat dijadikan parameter.
- Response API tersimpan sebagai sample.
- Error response ditangani."

# Issue 15: Validate OpenAQ API Response
gh issue create -R "$REPO" \
  --title "Validate OpenAQ API Response" \
  --body "**Component:** OpenAQ Integration
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Memvalidasi response OpenAQ sebelum masuk ke preprocessing realtime.

**Deliverables:**
- src/services/openaq_validator.py
- notebooks/33_openaq_response_validation.ipynb

**Definition of Done:**
- Response kosong dapat ditangani.
- Missing parameter dapat ditangani.
- Format timestamp tervalidasi.
- Error message jelas."

# Issue 16: Map OpenAQ Parameters to Model Features
gh issue create -R "$REPO" \
  --title "Map OpenAQ Parameters to Model Features" \
  --body "**Component:** OpenAQ Integration
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** M

**Description:**
Memetakan parameter dari OpenAQ agar sesuai dengan feature columns model.

**Deliverables:**
- src/services/openaq_parameter_mapper.py
- docs/openaq_to_model_feature_mapping.md

**Definition of Done:**
- Nama parameter OpenAQ berhasil dimapping.
- Fitur yang tidak tersedia terdokumentasi.
- Strategi fallback untuk fitur kosong dijelaskan.
- Output sesuai feature_columns.json."

# Issue 17: Document Data Drift Limitation
gh issue create -R "$REPO" \
  --title "Document Data Drift Limitation" \
  --body "**Component:** Documentation
**Priority:** P1
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Mendokumentasikan keterbatasan penggunaan model frozen yang dilatih pada data India 2015–2020 terhadap data realtime OpenAQ.

**Deliverables:**
- docs/data_drift_limitation.md

**Definition of Done:**
- Risiko data drift dijelaskan.
- Risiko spatial generalization dijelaskan.
- Sistem dijelaskan sebagai benchmark/PoC.
- Batasan model ditulis dengan jelas."

# Issue 18: Build Realtime Preprocessing Pipeline
gh issue create -R "$REPO" \
  --title "Build Realtime Preprocessing Pipeline" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** L

**Description:**
Membuat preprocessing untuk data realtime agar formatnya sama dengan data training.

**Deliverables:**
- src/inference/realtime_preprocessor.py

**Definition of Done:**
- Input realtime dapat diubah menjadi fitur model.
- Scaler frozen digunakan.
- Output siap masuk ke LSTM.
- Tidak melakukan fit scaler ulang."

# Issue 19: Build LSTM Inference Service
gh issue create -R "$REPO" \
  --title "Build LSTM Inference Service" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** M

**Description:**
Membuat service untuk melakukan prediksi AQI awal menggunakan frozen LSTM.

**Deliverables:**
- src/inference/lstm_inference_service.py

**Definition of Done:**
- Frozen LSTM berhasil di-load.
- Input sequence valid.
- Output berupa AQI_LSTM_prediction.
- Error input shape ditangani."

# Issue 20: Build XGBoost Residual Inference Service
gh issue create -R "$REPO" \
  --title "Build XGBoost Residual Inference Service" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** M

**Description:**
Membuat service untuk memprediksi residual correction menggunakan frozen XGBoost.

**Deliverables:**
- src/inference/xgb_residual_service.py

**Definition of Done:**
- Frozen XGBoost berhasil di-load.
- Input fitur residual valid.
- Output berupa Residual_XGBoost_prediction.
- Feature order sesuai metadata."

# Issue 21: Build Hybrid Prediction Pipeline
gh issue create -R "$REPO" \
  --title "Build Hybrid Prediction Pipeline" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** L

**Description:**
Menggabungkan preprocessing, LSTM, XGBoost residual, dan AQI category mapping dalam satu pipeline inferensi.

**Flow**
Realtime data
↓
Preprocessing
↓
LSTM prediction
↓
XGBoost residual prediction
↓
AQI_final
↓
AQI category

**Deliverables:**
- src/inference/prediction_pipeline.py

**Definition of Done:**
- Pipeline menghasilkan AQI_LSTM_prediction.
- Pipeline menghasilkan Residual_XGBoost_prediction.
- Pipeline menghasilkan AQI_final.
- Pipeline menghasilkan AQI_category.
- Pipeline dapat dipanggil oleh backend API."

# Issue 22: Format Prediction Response JSON
gh issue create -R "$REPO" \
  --title "Format Prediction Response JSON" \
  --body "**Component:** Inference Pipeline
**Priority:** P0
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Membuat format response standar untuk frontend dashboard.

**Example Output**
\`\`\`json
{
  \"location\": \"Delhi\",
  \"timestamp\": \"2026-06-01T10:00:00\",
  \"aqi_lstm_prediction\": 145.3,
  \"residual_correction\": 8.7,
  \"aqi_final\": 154.0,
  \"aqi_category\": \"Moderate\",
  \"model_version\": \"hybrid-lstm-xgb-v1\"
}
\`\`\`

**Deliverables:**
- src/inference/response_formatter.py
- docs/prediction_response_format.md

**Definition of Done:**
- Response JSON konsisten.
- Field utama tersedia.
- Response siap dikonsumsi frontend."

# Issue 23: Build Alert Logic
gh issue create -R "$REPO" \
  --title "Build Alert Logic" \
  --body "**Component:** Inference Pipeline
**Priority:** P1
**Sprint:** Sprint 2
**Effort:** S

**Description:**
Membuat logika alert berdasarkan AQI final dan kategori kualitas udara.

**Trigger**
- Poor
- Very Poor
- Severe

**Deliverables:**
- src/inference/alert_engine.py

**Definition of Done:**
- Alert muncul untuk kategori berbahaya.
- Tidak muncul untuk kategori aman.
- Pesan rekomendasi tersedia.
- Output alert masuk ke response JSON."

echo "✅ All 21 issues created successfully!"
