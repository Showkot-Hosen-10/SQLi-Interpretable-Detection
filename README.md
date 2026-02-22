

---

# Interpretable SQL Injection Detection: Lightweight Decision Trees with SHAP-Enhanced Deployment

This repository contains the official implementation of the research paper: **"Interpretable SQL Injection Detection: Lightweight Decision Trees with SHAP-Enhanced Deployment."**

The project addresses the computational bottleneck of Deep Learning (DL) in web security by utilizing a high-performance **111-parameter Decision Tree** model, integrated with **SHAP (SHapley Additive exPlanations)** for real-time transparency in Security Operations Centers (SOC).

---

## 🔬 Research Overview

Traditional Deep Learning models for SQLi detection often exceed 45K parameters, leading to high latency in resource-constrained web environments. This implementation achieves:

* **Accuracy:** 98.31% on balanced hybrid datasets.
* **Latency:** ~0.3ms per query (production-grade).
* **Interpretability:** Query-level feature attribution via SHAP TreeExplainer.
* **Lightweight Design:** Only 111 model parameters compared to 46,000+ in standard DNNs.

---

## 🏗️ System Architecture

The pipeline consists of three core layers:

1. **Feature Engineering:** TF-IDF vectorization (max_features=15,000) to capture semantic SQL tokens.
2. **Detection Engine:** Optimized Decision Tree Classifier trained on 200K hybrid samples.
3. **Explainability Layer:** SHAP integration providing real-time "Red-Flag" token identification.
4. **Deployment Layer:** Flask-based Web Interface with SQLite-backed SOC alerting.

---

## 📁 Repository Structure

```text
├── SQLi Web App Project/
│   ├── app.py                # Flask Production Server
│   ├── sqli_detector_model.joblib               # Serialized (.joblib) DT & TF-IDF Vectorizer
│   ├── sqli_explainer.joblib            # CSS/JS for SOC Dashboard
│   ├──sqli_vectorizer.zip            # HTML Interfaces (User & Admin)
│   ├── requirements.txt      # Dependency Specification
│   └── Test Payloads.md         # SQLite Backend for Alert Logging
    └── Datasets Links.md              # Reference links to Kaggle sources

```

---

## 🚀 Reproducibility Guide

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Showkot-Hosen-10/ML-Based-Cyberdefence.git
cd "ML-Based-Cyberdefence/SQLi Web App Project"

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Launching the System

```bash
python app.py

```

* **User Gateway:** `http://localhost:5000`
* **SOC Dashboard:** `http://localhost:5000/admin`

### 3. Verification Credentials

| Role | Username | Password |
| --- | --- | --- |
| **Admin/SOC Analyst** | `admin` | `admin123` |
| **End User** | `student` | `student123` |

---

## 📊 Evaluation Results

The model was validated against 15 unique real-world attack vectors, including Tautology, Union-based, and Time-Delay attacks.

| Metric | Decision Tree (Proposed) | DNN (Baseline) |
| --- | --- | --- |
| **Accuracy** | **98.0%** | 48% (Overfit/Poor Convergence) |
| **Parameters** | **111** | 46,849 |
| **Training Time** | **43ms** | 10s |
| **Inference Latency** | **0.001ms** | 0.133ms |

---

## 🛡️ Interpretability Case Study

When a payload like `1' OR 1=1 --` is detected, the SHAP engine decomposes the prediction:

* **Trigger Token `--**`: Contributes **+0.535** to the malicious score.
* **Trigger Token `OR**`: Contributes **+0.122** to the malicious score.
This allows security teams to verify the "logic" behind the alert instantly.

---

## 📜 Citation

If you use this code or research in your work, please cite:

```bibtex
@inproceedings{blind2025sqli,
  author={blind_author},
  title={Interpretable SQL Injection Detection: Lightweight Decision Trees with SHAP-Enhanced Deployment},
  year={2025},
  note={Under Peer Review}
}

```



