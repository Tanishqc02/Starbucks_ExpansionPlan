# ☕ Starbucks Global Expansion Strategy Dashboard

## Data-Driven Market Classification & AI-Powered Growth Analysis

---

## 🔗 Live Application
**[ 🚀 VIEW LIVE DASHBOARD ](https://69a5199a-b73c-8013-9b0c-991318afc0e9-fztznsrdweh6zwashue72s.streamlit.app/)**

---

# 📌 1. Business Problem Statement

Starbucks operates in more than 70 countries, but not all markets perform the same way. Some countries are highly saturated with thousands of stores, while others are still emerging with only a few locations.

The core business question of this project is:

> **How can Starbucks expand globally while maximizing revenue and minimizing financial risk?**

To answer this, we analyze global store distribution patterns, ownership models, and geographic concentration using Artificial Intelligence and economic reasoning.

This project helps identify:
*   Which markets are mature and saturated
*   Which markets are growing rapidly
*   Which markets require cautious entry
*   What ownership strategy (Company-Owned vs Licensed) should be used

---

# 🌍 2. Project Overview

This is a full end-to-end Data Science and Business Intelligence project built using:
*   📍 **Geographic Clustering (K-Means)**
*   🧠 **Predictive Modeling (Logistic Regression)**
*   📊 **Exploratory Data Analysis (EDA)**
*   🌐 **Interactive Dashboard (Streamlit)**

The dashboard analyzes **25,000+ Starbucks store records** across **73 countries**.

---

# 📊 3. Economic Concepts Applied

This project connects AI results with real economic theory in simple and practical ways.

## 🔹 Demand vs Supply
*   High store density indicates strong and stable demand.
*   If too many stores exist in one area, growth slows due to **market saturation**.
*   **Example**: The USA has very high store density, meaning demand is strong but growth opportunities are limited.

## 🔹 Revenue Optimization
Starbucks uses different ownership models depending on market stability.
*   **Mature markets** → Company-Owned (higher profit control)
*   **Emerging markets** → Licensed (shared risk, lower capital exposure)
This balances profit maximization with risk management.

## 🔹 Risk Diversification
In uncertain or developing markets, Starbucks reduces financial exposure by partnering with local operators. This protects capital while testing market potential.

## 🔹 Market Saturation
When store density becomes very high, new stores may reduce revenue per store. At this stage, companies focus on:
*   Improving efficiency
*   Increasing digital sales
*   Raising average revenue per store

## 🔹 Pricing Strategy
*   **Premium pricing** in loyal, high-income markets.
*   **Localized pricing** in developing economies.

---

# 🤖 4. AI Techniques Used

## 🔹 K-Means Clustering (Unsupervised Learning)
*   **Purpose**: Automatically segment global markets into strategic hubs.
*   **Features Used**: Latitude, Longitude, Store Density, Ownership Distribution.
*   **Outcome**: Identified 5 global market clusters (Americas, EMEA, East Asia, Southeast Asia, Pacific).

## 🔹 Logistic Regression (Supervised Learning)
*   **Purpose**: Predict optimal expansion strategy.
*   **Model Accuracy**: ~74% validation accuracy.
*   **Inputs**: Geographic coordinates & Cluster information.
*   **Outputs**: Demand Level, Revenue Potential, Risk Profile, Recommended Ownership Strategy.

---

# 📂 5. Dataset Information

*   **Dataset Source (Kaggle)**: [Starbucks Store Location 2023](https://www.kaggle.com/datasets/omarsobhy14/starbucks-store-location-2023)
*   **Total Records**: 25,000+
*   **Contains**: Store Name, Country, City, Ownership Type, Latitude, Longitude.

> [!NOTE]
> Revenue data is not directly included. Revenue potential is inferred from store density and ownership patterns.

---

# 📸 6. Screenshots of Outputs

> [!TIP]
> Add your own screenshots here after running the app!

## 🔹 Global Store Map
![Global Store Map](assets/screenshots/Global%20Store%20Map.png)

## 🔹 Top 10 Countries by Store Count
![Top 10 Countries](assets/screenshots/Top%2010%20Countries%20by%20Store%20Count.png)

## 🔹 Ownership Distribution Chart
![Ownership Distribution](assets/screenshots/Ownership%20Distribution%20Chart.png)

## 🔹 K-Means Cluster Visualization
![Cluster Map](assets/screenshots/K-Means%20Cluster%20Visualization.png)

## 🔹 Risk & Strategy Predictor Output
![Prediction Output](assets/screenshots/Risk%20&%20Strategy%20Predictor%20Output.png)

---

# 🛠 7. Technical Stack

*   Python 3.9+
*   Streamlit (Interactive Dashboard)
*   Pandas (Data Handling)
*   Scikit-Learn (Machine Learning Models)
*   Plotly Express (Visualizations)

---

# ⚙️ 8. Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <your_repository_url>
    cd starbucks-global-expansion-dashboard
    ```
2.  **Install dependencies**:
    ```bash
    pip install streamlit pandas plotly scikit-learn pycountry openpyxl
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py --server.port 8503
    ```
4.  **Open in browser**: [http://localhost:8503](http://localhost:8503)

---

# 🧠 9. What This Project Demonstrates

✔ Data Cleaning & Feature Engineering
✔ Exploratory Data Analysis
✔ Unsupervised Machine Learning (Clustering)
✔ Supervised Machine Learning (Classification)
✔ Business Strategy Interpretation
✔ Interactive Dashboard Deployment

---

# 📌 Final Summary

This project proves that Starbucks expansion is not random. It is **data-driven, risk-aware, revenue-focused, and strategically optimized**. By combining AI techniques with economic reasoning, this dashboard provides a scalable framework for intelligent global expansion strategy.

---

**Author: Rayan**
