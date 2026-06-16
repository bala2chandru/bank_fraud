# 🏦 Bank Fraud Detection — EDA & Interactive Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> An end-to-end Exploratory Data Analysis project on 1 Million bank transactions — uncovering fraud patterns, high-risk segments, and behavioral signals, with a fully interactive Streamlit dashboard.

---

## 📊 Dataset Overview

| Feature | Detail |
|---------|--------|
| Records | 1,000,000 transactions |
| Fraud Rate | ~5.5% (55,255 fraudulent) |
| Countries | 10 (USA, UK, India, Germany, etc.) |
| Fraud Types | 6 (Phishing, Account Takeover, Card Cloning, etc.) |
| Features | 26 columns |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/bank-fraud-eda.git
cd bank-fraud-eda
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

### 4. Explore the Jupyter Notebook
```bash
jupyter notebook Bank_Fraud_EDA.ipynb
```

---

## 📁 Project Structure

```
bank-fraud-eda/
│
├── bank_fraud.csv               # Dataset (1M rows)
├── Bank_Fraud_EDA.ipynb         # Full EDA Jupyter Notebook
├── app.py                       # Streamlit Interactive Dashboard
├── requirements.txt             # Python dependencies
├── outputs/                     # Saved chart images
│   ├── fraud_overview.png
│   ├── transaction_amount.png
│   ├── time_patterns.png
│   ├── payment_device.png
│   ├── merchant_analysis.png
│   ├── customer_profile.png
│   └── behavioral_signals.png
└── README.md
```

---

## 🔍 Key Analyses

- **Fraud Overview** — Fraud rate, types, country-wise distribution
- **Transaction Amount** — Fraud vs Legit amount patterns by merchant
- **Time Patterns** — Hourly fraud trends, weekday vs weekend, day vs night
- **Payment & Device** — Riskiest payment methods and device types
- **Merchant Category** — Fraud rate and volume by merchant
- **Customer Profile** — Age, credit score, failed attempts, international txns
- **Behavioral Signals** — PIN changes, transaction frequency, time since last txn
- **Correlations** — Feature relationships with fraud indicator

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data manipulation |
| Matplotlib + Seaborn | Static visualizations (notebook) |
| Plotly | Interactive charts (dashboard) |
| Streamlit | Dashboard deployment |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Connect

Built with ❤️ for portfolio purposes.  
[LinkedIn](https://linkedin.com) | [GitHub](https://github.com)
