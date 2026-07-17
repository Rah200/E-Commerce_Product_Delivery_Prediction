# 📦 E-Commerce Product Delivery Prediction

Predicting whether an e-commerce order will reach the customer **on time or delayed**, using machine learning — turning historical logistics data into an early-warning system that improves customer trust and operational planning.

🔗 **Live App:** [e-commerceappuctdeliveryprediction.streamlit.app](https://e-commerceappuctdeliveryprediction-tsfaaym9e3e4zxo2rt3lar.streamlit.app/)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Business Problem](#-business-problem)
- [Dataset](#-dataset)
- [Project Workflow](#-project-workflow)
- [Exploratory Data Analysis](#-exploratory-data-analysis)
- [Data Preprocessing & Feature Engineering](#-data-preprocessing--feature-engineering)
- [Models Used](#-models-used)
- [Results](#-results)
- [Hyperparameter Tuning](#-hyperparameter-tuning)
- [Feature Importance — Key Business Insight](#-feature-importance--key-business-insight)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Limitations & Future Work](#-limitations--future-work)
- [Author](#-author)

---

## 🧭 Overview

An international e-commerce company specializing in electronics ships thousands of orders daily. Historically, **nearly 60% of orders arrived late** — hurting customer trust and complicating logistics planning.

This project builds, evaluates, and deploys a machine learning model that predicts — from order and shipment attributes alone, before dispatch — whether a given order will reach the customer **on time**. It covers the full pipeline: EDA → preprocessing → model comparison → hyperparameter tuning → business insight → deployment (Streamlit app + Power BI dashboard).

## 🎯 Business Problem

| | |
|---|---|
| **Type** | Binary Classification |
| **Target** | `Reached.on.Time_Y.N` (1 = Delayed, 0 = On Time) |
| **Goal** | Predict delivery timeliness to optimize logistics, improve customer satisfaction, and surface the real drivers of delay |

**Business value:**
- **Delivery Optimization** — identify operational factors driving delay
- **Customer Satisfaction** — set realistic delivery expectations upfront
- **Operational Insight** — better resource allocation across logistics

## 📊 Dataset

- **Rows:** 10,999 historical orders
- **Columns:** 12 (11 features + 1 target)
- **Missing values / duplicates:** None — verified, not assumed

| Category | Features |
|---|---|
| Logistics / Operations | `Warehouse_block`, `Mode_of_Shipment`, `Customer_care_calls`, `Prior_purchases` |
| Product | `Cost_of_the_Product`, `Product_importance`, `Weight_in_gms`, `Discount_offered` |
| Customer | `Customer_rating`, `Gender` |
| Target | `Reached.on.Time_Y.N` |

## 🔄 Project Workflow

```
Data Collection → EDA → Preprocessing → Train/Test Split →
Model Training (4 algorithms) → Evaluation → Hyperparameter Tuning →
Feature Importance → Business Insight → Deployment
```

## 🔍 Exploratory Data Analysis

- **Univariate:** distribution of every numerical and categorical feature independently
- **Bivariate:** each feature compared against delivery status — `Discount_offered` and `Weight_in_gms` show the clearest separation between on-time and delayed orders; `Warehouse_block` and `Mode_of_Shipment` show relatively even delay rates across categories
- **Correlation Analysis:** `Discount_offered` correlates ~+0.40 with delay — the strongest single relationship in the dataset; no severe multicollinearity found among predictors

## 🧹 Data Preprocessing & Feature Engineering

| Step | Decision | Why |
|---|---|---|
| Missing values / duplicates | None found | Verified explicitly — no imputation needed |
| Outliers | **Reviewed, not removed** | High discounts and heavy packages are genuine orders, not errors — they turned out to be the two strongest predictors of delay. Removing them would have erased the exact signal the model needed. Tree-based models are also naturally robust to them. |
| `ID` | Dropped | Row artifact with no predictive meaning, not a real driver |
| `Gender` | Dropped | No causal link to logistics outcomes |
| Categorical encoding | One-Hot Encoding | `Warehouse_block`, `Mode_of_Shipment`, `Product_importance` are nominal — no inherent order, so Label Encoding would wrongly imply ranking |
| Train/test split | 80/20, **stratified** on target | Preserves the ~60/40 delayed/on-time ratio in both sets for fair evaluation (`random_state=42` for reproducibility) |
| Feature scaling | `StandardScaler`, fit on train only | Applied only to Logistic Regression & KNN (distance/gradient-based); Decision Tree & Random Forest don't need it (threshold-based splits) |

## 🤖 Models Used

| Model | Why it was included |
|---|---|
| Logistic Regression | Simple, interpretable linear baseline |
| Decision Tree | Captures non-linear rules and feature interactions |
| Random Forest | Ensemble of trees — robust, less overfit-prone, yields feature importance |
| K-Nearest Neighbors | Non-parametric, no distributional assumptions |

## 📈 Results

Evaluated on a held-out 20% test set (2,200 orders) using Accuracy, Precision, Recall, F1, and ROC-AUC — not accuracy alone, given the moderate class imbalance.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest** | **65.86%** | 76.02% | 62.53% | 68.62% | **73.49%** |
| Decision Tree | 65.73% | 71.09% | **71.74%** | **71.42%** | 64.28% |
| KNN | 64.32% | 71.53% | 66.79% | 69.08% | 70.86% |
| Logistic Regression | 63.86% | 70.89% | 66.95% | 68.86% | 71.68% |

Confirmed via **5-fold stratified cross-validation** — Random Forest was the most stable performer (mean accuracy 65.70%, std dev 1.37%).

> All four models cluster in a 64–66% accuracy band — evidence of real, learnable signal, but also inherent unpredictability not explained by these 11 features alone.

## 🎛️ Hyperparameter Tuning

`GridSearchCV` over Random Forest — 216 parameter combinations × 5 folds = 1,080 fits, optimizing accuracy.

**Best parameters:** `max_depth=10, min_samples_leaf=2, min_samples_split=5, n_estimators=200`

| Metric | Baseline RF | Tuned RF |
|---|---|---|
| Accuracy | 65.86% | **68.23%** |
| Precision | 76.02% | **88.96%** |
| Recall | 62.53% | 53.39% |
| F1 Score | 68.62% | 66.73% |
| ROC-AUC | 73.49% | **74.36%** |

**Honest trade-off:** tuning improved accuracy, precision, and ROC-AUC, but recall dropped — the tuned model is more conservative and misses more true delays than the baseline. Which version to deploy depends on which type of error costs the business more.

## 💡 Feature Importance — Key Business Insight

| Feature | Importance |
|---|---|
| `Discount_offered` | 36.3% |
| `Weight_in_gms` | 34.8% |
| `Cost_of_the_Product` | 10.2% |
| `Prior_purchases` | 6.0% |
| `Customer_care_calls` | 4.0% |
| `Customer_rating` | 2.7% |
| Warehouse / Shipment / Importance (combined) | ~6.0% |

**`Discount_offered` and `Weight_in_gms` alone account for over 70% of the model's decisions** — far more than warehouse or shipment mode. This redirects operational focus toward bulk/discounted-order handling and oversized-package logistics, rather than warehouse-level changes.

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Data & ML:** pandas, numpy, scikit-learn
- **Visualization:** matplotlib, seaborn
- **Deployment:** Streamlit
- **BI / Dashboarding:** Power BI (DAX)
- **Model Persistence:** joblib

## 📁 Project Structure

```
E-Commerce_Product_Delivery_Prediction/
│
├── data/
│   └── E_Commerce.csv                          # Raw dataset
│
├── notebooks/
│   └── e_commerce_product_delivery.ipynb        # Full EDA → modeling → tuning pipeline
│
├── app/
│   └── streamlit_app.py                         # Deployed prediction app
│
├── dashboard/
│   └── Product_Delivery_Timeliness.pbix          # Power BI dashboard
│
├── artifacts/
│   └── model_rf.joblib                           # Persisted tuned Random Forest model
│
├── requirements.txt
└── README.md
```
*(Adjust the tree above to match your actual folder names if they differ.)*

## ⚙️ Installation & Usage

```bash
# Clone the repository
git clone https://github.com/Rah200/E-Commerce_Product_Delivery_Prediction.git
cd E-Commerce_Product_Delivery_Prediction

# Install dependencies
pip install -r requirements.txt

# Run the notebook
jupyter notebook notebooks/e_commerce_product_delivery.ipynb

# Run the Streamlit app locally
streamlit run app/streamlit_app.py
```

Or just try the **[live app](https://e-commerceappuctdeliveryprediction-tsfaaym9e3e4zxo2rt3lar.streamlit.app/)** — no setup required.

## ⚠️ Limitations & Future Work

**Limitations**
- Single historical dataset — generalizability to new regions/seasons untested
- No external factors captured (weather, carrier-specific issues, real-time traffic)
- Accuracy ceiling (~66–68%) suggests missing predictive signal beyond current features

**Future Work**
- Add geographic features and order/expected delivery dates
- Test gradient boosting methods (XGBoost, LightGBM)
- Monitor for prediction drift after deployment; retrain periodically on new data

## 👤 Author

**Rahul Deshpande**
🔗 GitHub: [Rah200](https://github.com/Rah200)
🔗 Live App: [Product Delivery Predictor](https://e-commerceappuctdeliveryprediction-tsfaaym9e3e4zxo2rt3lar.streamlit.app/)

---

*If you found this project useful, consider giving it a ⭐ on GitHub!*
