# 📊 End-to-End Data Analytics & Business Intelligence Portfolio

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQLite-Data%20Querying-003B57.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboarding-F2C811.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Author**: Rutuja Shinde  
> **Program**: DecodeLabs Industrial Data Analytics Training (Batch 2026)  
> **Repository**: [https://github.com/Rutuja1423/Internship.git](https://github.com/Rutuja1423/Internship.git)  
> **Live Portfolio Web App**: Open [`index.html`](file:///r:/Projects/Internship/index.html) in your browser for the interactive web dashboard experience.

---

## 📌 Executive Summary

This repository contains an industrial-grade end-to-end data analytics suite developed across 4 core projects on a 1,200-order e-commerce transactions dataset representing **$1.26M+ in Gross Revenue**. 

The analytics workflow spans data cleaning & validation, statistical exploratory data analysis (EDA), financial revenue leak diagnosis, SQL analytical querying, and an interactive Power BI executive dashboard.

### 💡 Key Portfolio Insights & Achievements
- **Data Integrity**: Processed 1,200 orders across 14 attributes, rectifying price inconsistencies (`TotalPrice = Quantity * UnitPrice`), handling missing promotion codes (`CouponCode` -> `NoCoupon`), and enforcing pattern formats for Order and Tracking IDs.
- **Financial Loss Forensic**: Diagnosed a **$519.7k Gross Revenue Leak** (41.09% revenue share lost to Cancellations and Returns).
- **Outlier Forensics**: Compared IQR vs. Z-Score methods on right-skewed sales data, successfully identifying 8 high-value VIP transactions (`> $3,200`) where traditional Z-score thresholds failed.
- **SQL Analytics Engine**: Built an in-memory SQLite analytical engine in Python to run aggregations, windowing, and segment-level queries.
- **Power BI Executive Dashboard**: Engineered an interactive Power BI report (`powerdashboard4.pbix`) with interactive slicers, KPI breakdown cards, and decomposition trees.

---

## 📂 Repository Structure

```directory
Internship/
├── index.html                 # 🌐 Interactive Web Portfolio Web App
├── style.css                  # 🎨 Portfolio Design System & Glassmorphism Styles
├── app.js                     # ⚡ Interactive Portfolio Logic & SQL Playground
├── README.md                  # 📖 Comprehensive Repository Documentation
├── .gitignore                 # 🚫 Git Exclusions (.mypy_cache, .ipynb_checkpoints)
│
├── Project_1/                 # 🧹 Data Cleaning & Preparation Pipeline
│   ├── data_analysis.py       # Python automated cleaning script
│   ├── data_analysis.ipynb    # Data cleaning Jupyter notebook
│   ├── Cleaned_Dataset.csv    # Post-cleaning normalized dataset
│   ├── Dataset for Data Analytics - Sheet1.csv # Raw dataset
│   ├── DATA ANALYTICS p1.pdf  # Project 1 PDF documentation
│   └── offer letter.pdf       # Offer letter documentation
│
├── Project_2/                 # 🔬 Exploratory Data Analysis & Forensics
│   ├── eda_analysis.py        # Python EDA & visualization engine
│   ├── eda_analysis.ipynb     # Interactive EDA notebook
│   ├── Cleaned_Dataset.csv    # Cleaned dataset copy
│   ├── Data analytics P2.pdf  # Project 2 report PDF
│   └── charts/                # 🖼️ 8 Publication-Ready Dark Theme Charts
│       ├── 01_univariate_distributions.png
│       ├── 02_five_number_summary_boxplots.png
│       ├── 03_outlier_iqr_vs_zscore.png
│       ├── 04_correlation_heatmap.png
│       ├── 05_order_status_financial_impact.png
│       ├── 06_product_performance_returns.png
│       ├── 07_referral_coupon_matrix.png
│       └── 08_monthly_sales_trend.png
│
├── project_3/                 # 🗄️ SQL Analytical Query Engine
│   ├── sql_data_analysis.ipynb# SQLite3 + Pandas analytical queries notebook
│   ├── Cleaned_Dataset.csv    # Cleaned dataset copy
│   └── Data Analytics Project 3.pdf # Project 3 documentation
│
└── project_4/                 # 📊 Power BI Executive Dashboard
    ├── powerdashboard4.pbix   # Power BI Desktop interactive dashboard
    └── Cleaned_Dataset.csv    # Cleaned dataset copy
```

---

## 🚀 Project Overview & Technical Deep-Dive

### 🔹 Project 1: Data Cleaning & Preparation Pipeline
* **Folder**: [`Project_1/`](file:///r:/Projects/Internship/Project_1/)
* **Core Script**: [`Project_1/data_analysis.py`](file:///r:/Projects/Internship/Project_1/data_analysis.py)
* **Objective**: Automate data audit, missing value imputation, duplicate removal, format standardization, and logical price checks.

#### Key Engineering Steps:
1. **Missing Data Imputation**: Handled missing `CouponCode` entries by imputing `'NoCoupon'` (acknowledging that non-use of coupons is meaningful business data).
2. **Duplicate Audit**: Enforced unique `OrderID` constraint (`ORDxxxxxx`) and removed duplicate rows.
3. **Format Standardization**: Standardized `Date` format (`YYYY-MM-DD`), verified `TrackingNumber` string patterns (`TRKxxxxxxxx`), and trimmed whitespace across categorical features.
4. **Logical Consistency Verification**: Calculated `Calculated_Total = Quantity * UnitPrice` and rectified all row-level discrepancies where `TotalPrice` deviated from unit calculations.

---

### 🔹 Project 2: Forensic EDA & Financial Leak Analysis
* **Folder**: [`Project_2/`](file:///r:/Projects/Internship/Project_2/)
* **Core Script**: [`Project_2/eda_analysis.py`](file:///r:/Projects/Internship/Project_2/eda_analysis.py)
* **Objective**: Perform statistical distribution profiling, correlation mapping, outlier forensics, and financial revenue leak analysis.

#### Statistical Highlights:
| Metric / Feature | Quantity | UnitPrice ($) | ItemsInCart | TotalPrice ($) |
| :--- | :---: | :---: | :---: | :---: |
| **Mean** | 3.00 | $401.12 | 5.50 | $1,200.75 |
| **Std Dev** | 1.41 | $230.15 | 2.87 | $892.40 |
| **Q1 (25th %)** | 2.00 | $200.50 | 3.00 | $485.20 |
| **Median (50th %)** | 3.00 | $402.10 | 5.50 | $995.80 |
| **Q3 (75th %)** | 4.00 | $601.30 | 8.00 | $1,750.40 |
| **Max** | 5.00 | $799.50 | 10.00 | $3,456.40 |
| **Skewness** | 0.002 | -0.012 | 0.001 | 0.654 (Right Skew) |

#### Outlier Forensic Finding (IQR vs. Z-Score):
- **IQR Method** ($Q3 + 1.5 \times IQR$): Flagged **8 VIP High-Value Outliers** (orders above `$3,250`).
- **Z-Score Method** ($|Z| > 3.0$): Flagged **0 Outliers** because extreme variance in `UnitPrice` widened standard deviation, masking right-skewed VIP purchases.

#### Financial Revenue Leak Diagnostic:
```
Gross Revenue Breakdown ($1.26M Total):
├── Delivered Revenue : $375.4k (29.7%)  🟢
├── Shipped Revenue   : $367.2k (29.1%)  🔵
├── Pending Revenue   : $0.0k   (0.0%)   🟡
├── Cancelled Revenue : $261.3k (20.7%)  🔴 LEAK
└── Returned Revenue  : $258.4k (20.4%)  🟠 LEAK
                          Total Leak: $519.7k (41.09%)
```

---

### 🔹 Project 3: SQL Analytical Engine
* **Folder**: [`project_3/`](file:///r:/Projects/Internship/project_3/)
* **Core Notebook**: [`project_3/sql_data_analysis.ipynb`](file:///r:/Projects/Internship/project_3/sql_data_analysis.ipynb)
* **Objective**: Leverage SQLite3 in Python to perform structured analytical queries on order patterns, customer behavior, and marketing channels.

#### Key SQL Queries & Capabilities:
- **Filtering & Aggregations**: Identifying high-value orders (`TotalPrice > $2,000`), computing average cart sizes, and segmenting order volume by referral channel.
- **HAVING Clause Analysis**: Filtering categories where return rates exceed 15%.
- **Percentage Contribution**: Calculating revenue share by payment method (Credit Card, Online, Debit Card, Cash, Gift Card).

---

### 🔹 Project 4: Power BI Executive Dashboard
* **Folder**: [`project_4/`](file:///r:/Projects/Internship/project_4/)
* **File**: [`project_4/powerdashboard4.pbix`](file:///r:/Projects/Internship/project_4/powerdashboard4.pbix)
* **Objective**: Deliver an executive BI report with interactive filtering, KPI cards, and trend analysis.

#### Dashboard Capabilities:
- **KPI Cards**: Real-time display of Total Revenue, Total Orders, Average Order Value (AOV), and Return/Cancellation Rates.
- **Interactive Slicers**: Date range picker (Jan 2023 – Jun 2025), Product selector, Order Status filter, and Referral Source matrix.
- **Visual Analytics**: Monthly sales trend line charts, product performance comparisons, and payment channel breakdown.

---

## 🛠️ How to Run Locally

### Prerequisites
- Python 3.9+
- Jupyter Notebook / JupyterLab
- Power BI Desktop (for opening `.pbix` files)

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Rutuja1423/Internship.git
   cd Internship
   ```

2. **Install Required Python Packages**:
   ```bash
   pip install pandas numpy matplotlib seaborn scipy sqlite3
   ```

3. **Execute Data Pipeline Scripts**:
   ```bash
   # Run Project 1 Data Cleaning
   python Project_1/data_analysis.py

   # Run Project 2 Forensic EDA & Generate Charts
   python Project_2/eda_analysis.py
   ```

4. **Launch Portfolio Web Application**:
   Simply double-click [`index.html`](file:///r:/Projects/Internship/index.html) or run a local web server:
   ```bash
   python -m http.server 8000
   ```
   Navigate to `http://localhost:8000` in your web browser.

---

## 📜 License & Acknowledgments

This project portfolio is created by **Rutuja Shinde** as part of the **DecodeLabs Industrial Data Analytics Training**. All data rights and project materials belong to their respective owners.
