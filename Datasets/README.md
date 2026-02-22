---

# Interpretable SQLi Detection: Lightweight Decision Trees with SHAP-XAI

This repository contains the implementation of a lightweight machine learning framework for SQL Injection (SQLi) detection. The project focuses on balancing high-speed inference (~0.3ms) with transparency using **SHAP (SHapley Additive exPlanations)**.

---

## 📊 Dataset Architecture

The model is trained on a robust, hybrid dataset comprising **200,000+ samples**. The data is sourced from two established public repositories and one custom-engineered synthetic dataset included in this repository named as synthetic_sqli_dataset.csv and the Hybrid dataset that was used to train the model named as sqli_mixed_70_30.csv

### Dataset Sources

| ID | Source | Type | Access Link |
| --- | --- | --- | --- |
| **D1** | M. Sajid | Real-world SQLi | [Kaggle Repository](https://www.kaggle.com/datasets/sajid576/sql-injection-dataset) |
| **D2** | A. Khaldi | Real-world SQLi  | [Kaggle Repository](https://www.kaggle.com/datasets/ayahkhaldi/sql-injection-dataset) |
| **D3** | Author | Malicious+Benigh Payloads | Check synthetic_sqli_dataset.csv here in Datasets dir |
| **D4** | Author | Malicious+Benigh Payloads | Check sqli_mixed_70_30.csv here in Datasets dir |


---
