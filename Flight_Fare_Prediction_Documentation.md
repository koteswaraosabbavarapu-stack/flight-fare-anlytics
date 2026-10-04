# DATA ANALYTICS AND DATA VISUALIZATION

## MINI PROJECT REPORT ON
# **FLIGHT FARE ANALYSIS AND PREDICTION**

**BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE & ENGINEERING**

---

### **DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**
### **ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES**
**(UGC AUTONOMOUS)**  
*(Permanently Affiliated to AU, Approved by AICTE and Accredited by NBA & NAAC with A+)*  
*Sangivalasa, Bheemili Mandal, Visakhapatnam - 531162. (A.P)*  
**2026-2027**

---
<div style="page-break-after: always;"></div>

# ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES
### DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
### DATA ANALYTICS AND DATA VISUALIZATION LAB

---

## **BONAFIDE CERTIFICATE**

This is to certify that the mini project report entitled **“FLIGHT FARE ANALYSIS AND PREDICTION”** submitted as part of the curriculum for the **Data Analytics and Data Visualization** course by the **II/IV Computer Science and Engineering** student at **Anil Neerukonda Institute of Technology & Sciences (ANITS), Visakhapatnam**, is a record of bona fide work carried out under my supervision.

<br><br>

### **SUBMITTED BY**

### **S. KOTESWARAO - (A24126510107)**

<br><br><br>

| **Faculty-In charge** | **Head of Department - CSE** |
| :--- | :--- |
| **Mrs. Y. Padma sri** | **Dr. G. Srinivas** |
| Assistant Professor | Head of Department - CSE, ANITS |

---
<div style="page-break-after: always;"></div>

# **FLIGHT FARE (DAV) ANALYSIS AND PREDICTION**
### **Data Analytics and Visualization (DAV) Mini Project Documentation**

- **Project Type:** Flight Fare Data Analytics, Machine Learning Prediction & Streamlit Web Application
- **Programming Language:** Python
- **Libraries / Technologies:** Pandas, NumPy, Scikit-learn, Plotly, Streamlit
- **Student Name:** S. Koteswarao
- **Roll Number:** A24126510107
- **Class / Branch:** II/IV B.Tech CSE, ANITS
- **Dataset:** 10,000 domestic flight booking records across 6 metro Indian cities (19 columns)
- **GitHub Repository:** [https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics](https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics)
- **Project Goal:** Analyze key pricing factors across Indian domestic airlines, study non-linear pricing effects (last-minute booking surge, demand elasticity, travel class multipliers), train and compare regression models (Linear Regression vs. Random Forest), and deploy an interactive web dashboard for real-time fare predictions.

---

## **1. Introduction**

Data Analytics and Visualization (DAV) is the process of collecting, inspecting, cleaning, transforming, and modeling data to discover useful information, inform conclusions, and support decision-making. 

The aviation industry operates in a dynamic pricing environment where ticket fares fluctuate continuously based on demand, lead time, route distance, airline operational models, and seasonal trends. For travelers and travel agencies, understanding fare drivers helps in making cost-effective booking decisions. For airlines, predictive analytics assists in revenue management and seat allocation.

This project applies the end-to-end DAV workflow to a comprehensive 10,000-record dataset of Indian domestic flights covering 6 major metro cities. It encompasses data loading, imputation of missing values, duplicate verification, feature engineering, extensive exploratory data analysis with interactive Plotly visualizations, training of two machine learning regression algorithms (Linear Regression and Random Forest Regressor), and deployment of a multi-page interactive web application using Streamlit.

---

## **2. Objectives**

- **Data Wrangling & Cleaning:** Clean a multi-feature dataset containing realistic missing values and verify absence of duplicate entries.
- **Identify Pricing Patterns:** Analyze how airline carriers, seat availability, travel class, booking window, and departure slots influence ticket prices.
- **Demand & Booking Lead-Time Analysis:** Quantify the steep non-linear price surge associated with last-minute bookings (< 10 days before departure) and low seat availability.
- **Interactive Visualizations:** Build intuitive and interactive visual dashboards using Plotly to communicate trends, distributions, and correlation matrices.
- **Machine Learning Modeling:** Build, train, and evaluate regression models to predict ticket fares (`fare_inr`) with high accuracy ($R^2$, $RMSE$, and $MAE$).
- **Web Application Deployment:** Package the entire analytics pipeline and trained models into a modern Streamlit application deployed on the cloud.

---

## **3. Tools and Technologies Used**

- **Python 3.14:** Core programming language for data wrangling, model development, and web serving.
- **Pandas:** Tabular data manipulation, statistical aggregation, filtering, and missing data imputation.
- **NumPy:** Vectorized calculations, numerical operations, and logarithmic transformations.
- **Scikit-learn:** Data preprocessing (`ColumnTransformer`, `StandardScaler`, `SimpleImputer`, `OneHotEncoder`), regression modeling (`LinearRegression`, `RandomForestRegressor`), and evaluation metrics ($R^2$, $RMSE$, $MAE$).
- **Plotly Express & Graph Objects:** Dynamic, interactive data visualizations with hover tooltips, color maps, and zoom capabilities.
- **Streamlit:** Fast, responsive web framework for building and sharing interactive data dashboards.
- **Git & GitHub:** Version control and source code repository hosting.

---

## **4. Project Workflow**

```
Raw Synthetic Data (10,000 records)
           │
           ▼
Data Cleaning & Median Imputation (750 missing values across 3 features)
           │
           ▼
Exploratory Data Analysis (EDA) & Plotly Interactive Visualizations
           │
           ▼
Feature Preprocessing Pipeline (Median Imputer + StandardScaler + OneHotEncoder)
           │
           ▼
80/20 Train-Test Split (8,000 Training Records / 2,000 Testing Records)
           │
           ▼
Model Training & Evaluation (Linear Regression vs. Random Forest Regressor)
           │
           ▼
Interactive Streamlit Web Dashboard (5 Workflow Modules + Live Fare Predictor)
           │
           ▼
Deployment to Streamlit Community Cloud & GitHub Repository
```

---

## **5. Important Code Implementation**

### **5.1 Dataset Generation & Non-Linear Fare Mechanics (`data.py`)**

```python
import numpy as np
import pandas as pd

SEED = 2026
N_RECORDS = 10_000

# Base fare calculation with realistic non-linear multipliers
base = 1800 + 3.2 * distance
advance_mult = 1 + 1.6 * np.exp(-days_before / 8)          # Exponential last-minute spike
demand_mult = 1 + 0.5 * ((100 - seats) / 100) ** 2          # Quadratic demand effect
stops_mult = 1 - 0.07 * stops

fare = (
    base
    * np.array([AIRLINE_PRICE_MULT[a] for a in airline])
    * np.array([CLASS_MULT[c] for c in travel_class])
    * advance_mult
    * demand_mult
    * stops_mult
    * np.array([TIME_MULT[t] for t in departure])
    * np.array([DAY_MULT[d] for d in day])
    * np.where(holiday == "Yes", 1.18, 1.0)
)
fare += (baggage - 15) * 45 + np.where(meal == "Yes", 350, 0)
fare += np.array([CHANNEL_FEE[c] for c in channel])
fare *= rng.lognormal(0, 0.06, n)
```

### **5.2 Data Cleaning & Imputation Pipeline (`app.py`)**

```python
@st.cache_data
def clean_data(raw: pd.DataFrame):
    df = raw.copy()
    report = []
    for col in ["duration_hours", "seat_availability_pct", "airline_rating"]:
        n_missing = int(df[col].isna().sum())
        median = float(df[col].median())
        df[col] = df[col].fillna(median)
        report.append({
            "Column": col,
            "Missing values": n_missing,
            "Cleaning method": f"Filled with median ({median:.2f})"
        })
    n_dupes = int(df.duplicated().sum())
    df = df.drop_duplicates()
    return df, pd.DataFrame(report), n_dupes
```

### **5.3 Machine Learning Pipeline & Model Training (`app.py`)**

```python
def make_pre():
    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
    ])

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1),
}
```

---

## **6. Dataset Description**

The dataset consists of **10,000 flight records** across **19 columns**, representing Indian domestic flight bookings between six metropolitan hubs: **Delhi, Mumbai, Bengaluru, Hyderabad, Kolkata, and Chennai**.

| # | Column Name | Data Type | Description |
|---|---|---|---|
| 1 | `flight_id` | String | Unique flight booking identifier (e.g., `FL100001`) |
| 2 | `airline` | Categorical | Airline carrier (IndiGo, Air India, Akasa Air, SpiceJet, etc.) |
| 3 | `source_city` | Categorical | Origin metro city |
| 4 | `destination_city` | Categorical | Destination metro city |
| 5 | `distance_km` | Numeric | Direct route distance in kilometers (290 km to 1,760 km) |
| 6 | `departure_time` | Categorical | Departure slot (Early Morning, Morning, Afternoon, Evening, Night) |
| 7 | `day_of_week` | Categorical | Day of travel (Monday through Sunday) |
| 8 | `stops` | Numeric | Number of intermediate layovers (0, 1, or 2) |
| 9 | `travel_class` | Categorical | Cabin class (Economy, Premium Economy, Business) |
| 10 | `days_before_departure` | Numeric | Booking lead time (1 to 60 days in advance) |
| 11 | `duration_hours` | Numeric | Flight travel time in hours |
| 12 | `seat_availability_pct` | Numeric | Available unsold seats at booking time (3% to 100%) |
| 13 | `baggage_kg` | Numeric | Included baggage allowance (15, 20, 25, 30 kg) |
| 14 | `meal_included` | Categorical | In-flight meal inclusion (Yes / No) |
| 15 | `airline_rating` | Numeric | Customer feedback rating (1.0 to 5.0 stars) |
| 16 | `booking_channel` | Categorical | Booking source (Website, Mobile App, Travel Agent) |
| 17 | `holiday_season` | Categorical | Peak festival / holiday period (Yes / No) |
| 18 | **`fare_inr`** | **Numeric (Target)** | **Final ticket fare in Indian Rupees (INR)** |
| 19 | `booking_status` | Categorical | Booking lifecycle status (Confirmed, Rescheduled, Cancelled) |

---

## **7. Data Cleaning and Preparation**

The raw dataset intentionally contains missing values across three continuous attributes to simulate real-world data collection anomalies.

| Cleaning Step | Target Column | Missing / Anomaly Count | Remediation Technique |
|---|---|---|---|
| **Imputation** | `duration_hours` | 300 missing values (3.0%) | Median Imputation |
| **Imputation** | `seat_availability_pct` | 200 missing values (2.0%) | Median Imputation |
| **Imputation** | `airline_rating` | 250 missing values (2.5%) | Median Imputation |
| **Deduplication** | Entire DataFrame | 0 duplicate records | Verified via `.drop_duplicates()` |
| **Feature Scaling** | Numeric features | 5 features | Standardized ($\mu=0, \sigma=1$) |
| **Encoding** | Categorical features | 11 features | One-Hot Encoding (`handle_unknown='ignore'`) |

- **Total missing cells imputed:** **750 cells**
- **Cleaned records retained:** **10,000 / 10,000 rows (100% data retention)**
- **Train / Test split:** **8,000 training records (80%)** and **2,000 testing records (20%)**

---

## **8. Exploratory Data Analysis (EDA)**

1. **Overall Fare Statistics:**
   - **Average Fare:** ₹9,142
   - **Median Fare:** ₹7,250
   - **Minimum Fare:** ₹2,410
   - **Maximum Fare:** ₹38,920 (Business class last-minute booking)
2. **Distribution Skewness:** Fares follow a right-skewed distribution; the majority of economy flights are clustered between ₹3,500 and ₹9,000, while business class and last-minute bookings create an extended long tail.
3. **Travel Class Influence:** Business class tickets command a 3.2× premium over Economy, averaging over ₹22,000.
4. **Booking Lead Time Dynamic:** Fares increase exponentially when booked within **10 days** of departure due to reduced seat availability and urgent business traveler inelasticity.
5. **Airlines Pricing Comparison:** Air India shows higher average fares due to full-service inclusions, whereas Akasa Air and SpiceJet offer the most competitive base rates.

---

## **9. Data Visualization Techniques**

The project employs rich Plotly visualizations across the dashboard:
- **Histogram with KDE:** Distribution of ticket fares showing positive skewness.
- **Donut Chart:** Proportion of confirmed vs. rescheduled vs. cancelled bookings.
- **Bar Charts:** Average ticket fare broken down by travel class, airline, and departure slot.
- **Scatter Plot with Categorical Hue:** Non-linear relationship between `days_before_departure` and `fare_inr` colored by `travel_class`.
- **Line Charts:** Fare escalation versus route distance across Indian metro pairings.
- **Correlation Heatmap:** Linear correlation coefficients between all numerical attributes and target fare.

---

## **10. Machine Learning Models and Performance Comparison**

Two predictive regression models were trained on the exact same 80/20 train-test partition using identical preprocessing pipelines.

### **Performance Evaluation Metrics:**

| Model | Mean Absolute Error ($MAE$) | Root Mean Squared Error ($RMSE$) | Coefficient of Determination ($R^2$) | Rank |
|---|---|---|---|---|
| **Linear Regression** | ₹1,624.76 | ₹2,366.82 | **0.844 (84.4%)** | 2 |
| **Random Forest Regressor (150 trees)** | **₹922.30** | **₹1,424.86** | **0.943 (94.3%)** | **1 (Best)** |

### **Model Analysis:**
- **Random Forest is significantly superior**, reducing the $MAE$ by **43.2%** (from ₹1,624 to ₹922) and raising $R^2$ to **0.943**.
- **Reasoning:** Airline fares are heavily dictated by non-linear phenomena—such as exponential lead-time penalty curves ($e^{-t/8}$) and quadratic seat demand multiplier effects. A linear model assumes constant additive increments, while the ensemble decision trees in Random Forest accurately segment and model complex non-linear feature interactions.

---

## **11. Feature Importance Analysis**

The Random Forest Regressor provides Gini importance scores indicating the primary drivers of ticket prices:

1. **`travel_class` (Business vs. Economy):** ~54.2% importance (dominant fare determinant)
2. **`distance_km` (Route distance):** ~18.6% importance
3. **`days_before_departure` (Booking lead time):** ~14.1% importance
4. **`airline` (Carrier pricing tiers):** ~5.3% importance
5. **`seat_availability_pct` (Remaining seat inventory):** ~3.8% importance
6. **Other features (meals, baggage, time slot, day):** ~4.0% aggregate importance

---

## **12. Web Application Structure**

The web application is structured into five modular navigation pages:

1. **1. Actual Dataset:** Interactive view of raw 10,000 records, complete 19-column data dictionary, summary metrics, and direct CSV download button.
2. **2. Data Cleaning:** Visualization of missing value counts per column before and after median imputation, duplicate checking, and pipeline description.
3. **3. Exploratory Analysis:** Dynamic Plotly charts for fare distributions, airline comparisons, booking lead-time curves, and correlation heatmaps.
4. **4. Model Comparison:** Side-by-side metric cards ($MAE$, $RMSE$, $R^2$), Actual vs. Predicted scatter plots, and feature importance rankings.
5. **5. Predict Fare:** Live flight booking form where users select airline, route, departure slot, travel class, lead days, seat availability, and baggage allowance to obtain instant real-time fare predictions from both models.

---

## **13. Key Findings**

- **Class is Paramount:** Cabin class accounts for more than half of the price variance; Business class tickets average over 300% of standard Economy fares.
- **Last-Minute Premium:** Tickets booked within 7 days of travel cost up to 160% more than tickets booked 30+ days in advance.
- **Seat Scarcity Effect:** Flights with under 15% seat availability exhibit dynamic surge pricing regardless of booking lead time.
- **Ensemble Power:** Non-linear decision trees capture multi-factor pricing interactions that traditional linear models miss.

---

## **14. Conclusion & Future Enhancements**

The **SkyFare Analytics** project demonstrates the full Data Analytics and Visualization lifecycle: data ingestion, cleaning, exploratory visualization, model building, and cloud web deployment. The Random Forest model delivers accurate fare estimates ($R^2 = 0.943$, $MAE = ₹922$), making it a reliable tool for fare estimation.

### **Future Scope:**
- Integration of real-time flight pricing APIs (e.g., Amadeus or Skyscanner API).
- Expansion into route-specific festive surge detection and automated lowest-fare alert notifications.
- Deployment of Gradient Boosting (XGBoost / LightGBM) for further incremental accuracy improvements.

---

## **15. References**

1. **Pandas Documentation:** [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
2. **Scikit-Learn Regression Guide:** [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html)
3. **Plotly Python Graphing Library:** [https://plotly.com/python/](https://plotly.com/python/)
4. **Streamlit Framework Documentation:** [https://docs.streamlit.io/](https://docs.streamlit.io/)
5. **GitHub Project Repository:** [https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics](https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics)
