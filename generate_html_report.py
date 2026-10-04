"""Generate the complete 11-page HTML document with embedded figures and compile to PDF."""

import os
import base64
import subprocess

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

assets = {
    f"fig{i}": get_b64(f"report_assets/{f}")
    for i, f in [
        (1, "fig1_missing.png"),
        (2, "fig2_status_share.png"),
        (3, "fig3_fare_dist.png"),
        (4, "fig4_fare_by_class.png"),
        (5, "fig5_fare_by_airline.png"),
        (6, "fig6_fare_by_dep.png"),
        (7, "fig7_corr_matrix.png"),
        (8, "fig8_booking_window.png"),
        (9, "fig9_fare_spread_box.png"),
        (10, "fig10_fare_vs_dist.png"),
        (11, "fig11_model_comparison.png"),
        (12, "fig12_actual_vs_predicted.png"),
        (13, "fig13_feature_importance.png"),
    ]
}

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flight Fare Analysis and Prediction - S. Koteswarao (A24126510107)</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    color: #111;
    margin: 0;
    padding: 0;
    background-color: #888;
  }}
  .page {{
    width: 210mm;
    height: 297mm;
    margin: 10px auto;
    background: white;
    padding: 14mm 15mm 12mm 15mm;
    position: relative;
    page-break-after: always;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
  }}
  .outer-border {{
    border: 1.5px solid #111;
    padding: 10mm 10mm;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .header-box {{
    text-align: center;
    border-bottom: 1.5px solid #222;
    padding-bottom: 6px;
    margin-bottom: 10px;
  }}
  .header-box h4 {{
    margin: 0;
    font-size: 9.5pt;
    font-weight: bold;
    color: #000;
    letter-spacing: 0.3px;
  }}
  .header-box h5 {{
    margin: 2px 0 0 0;
    font-size: 8.5pt;
    font-weight: bold;
    color: #222;
  }}
  .footer-box {{
    display: flex;
    justify-content: space-between;
    border-top: 1.5px solid #222;
    padding-top: 4px;
    font-size: 8.5pt;
    color: #111;
    margin-top: auto;
  }}
  .content-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
  }}
  h1.doc-title {{
    font-size: 15pt;
    font-weight: bold;
    color: #000;
    margin: 4px 0 2px 0;
  }}
  .sub-doc-title {{
    font-size: 9pt;
    font-weight: bold;
    color: #333;
    margin-bottom: 6px;
  }}
  h2.sec-heading {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #000;
    margin: 8px 0 4px 0;
    border-bottom: 1px solid #ddd;
    padding-bottom: 2px;
  }}
  h3.subsec-heading {{
    font-size: 9.5pt;
    font-weight: bold;
    color: #111;
    margin: 6px 0 3px 0;
  }}
  p, li {{
    font-size: 8.2pt;
    line-height: 1.38;
    margin: 2.5px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 2px 0;
    padding-left: 18px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0;
    font-size: 7.8pt;
  }}
  table, th, td {{
    border: 1px solid #777;
  }}
  th {{
    background-color: #f2f2f2;
    font-weight: bold;
    padding: 4px 6px;
    text-align: left;
  }}
  td {{
    padding: 3.5px 6px;
  }}
  .code-block {{
    background: #f8f9fa;
    border: 1px solid #ddd;
    border-left: 3px solid #29b6f6;
    padding: 5px 8px;
    font-family: "Courier New", Courier, monospace;
    font-size: 7.2pt;
    line-height: 1.25;
    margin: 4px 0;
    white-space: pre;
    overflow: hidden;
  }}
  .grid-2 {{
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin: 4px 0;
  }}
  .grid-2 > div {{
    flex: 1;
    text-align: center;
  }}
  .fig-caption {{
    font-size: 7.5pt;
    font-style: italic;
    color: #444;
    margin-top: 2px;
    text-align: center;
  }}
  .chart-img {{
    max-width: 100%;
    height: 120px;
    object-fit: contain;
    border: 1px solid #eee;
  }}
  .chart-img-tall {{
    max-width: 100%;
    height: 140px;
    object-fit: contain;
    border: 1px solid #eee;
  }}
  .meta-p {{
    font-size: 8pt;
    line-height: 1.32;
    margin: 2px 0;
  }}
  @media print {{
    body {{ background: transparent; }}
    .page {{
      margin: 0;
      box-shadow: none;
      width: 100%;
      height: 100vh;
      padding: 12mm 14mm 10mm 14mm;
    }}
  }}
</style>
</head>
<body>

<!-- ========================================== PAGE 1 ========================================== -->
<div class="page">
  <div class="outer-border" style="text-align: center; border: 2px solid #000;">
    <div>
      <p style="font-size: 11pt; font-weight: bold; letter-spacing: 0.8px; margin-top: 15px;">DATA ANALYTICS AND DATA VISUALIZATION</p>
      <p style="font-size: 9.5pt; color: #555; margin-top: 2px;">MINI PROJECT ON</p>
      
      <div style="margin: 55px 0 40px 0;">
        <h1 style="font-size: 26pt; font-weight: 900; letter-spacing: 1px; line-height: 1.2; color: #1a365d; margin: 0;">
          FLIGHT FARE<br>ANALYSIS AND<br>PREDICTION
        </h1>
      </div>

      <div style="margin-top: 40px;">
        <p style="font-size: 10pt; font-weight: bold; color: #2b6cb0; margin: 0;">BACHELOR OF TECHNOLOGY IN</p>
        <p style="font-size: 11.5pt; font-weight: bold; color: #1a202c; margin: 3px 0 0 0;">COMPUTER SCIENCE & ENGINEERING</p>
      </div>
    </div>

    <!-- ANITS LOGO ICON -->
    <div style="margin: 30px auto;">
      <svg width="110" height="110" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="90" fill="none" stroke="#1a365d" stroke-width="4"/>
        <path d="M100 25 C135 70, 135 130, 100 175 C65 130, 65 70, 100 25 Z" fill="none" stroke="#1a365d" stroke-width="2"/>
        <path d="M25 100 C70 135, 130 135, 175 100 C130 65, 70 65, 25 100 Z" fill="none" stroke="#1a365d" stroke-width="2"/>
        <text x="100" y="115" font-family="Arial" font-size="28" font-weight="bold" fill="#1a365d" text-anchor="middle">ANITS</text>
        <text x="100" y="140" font-family="Arial" font-size="9" fill="#555" text-anchor="middle" letter-spacing="1">PRAGNANAM BRAHMA</text>
      </svg>
    </div>

    <div>
      <p style="font-size: 10pt; font-weight: bold; margin: 3px 0;">DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</p>
      <p style="font-size: 11pt; font-weight: bold; color: #1a365d; margin: 3px 0;">ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</p>
      <p style="font-size: 8.5pt; font-weight: bold; margin: 2px 0;">(UGC AUTONOMOUS)</p>
      <p style="font-size: 8pt; color: #555; margin: 2px 0;">(Permanently Affiliated to AU, Approved by AICTE and Accredited by NBA & NAAC with A+)</p>
      <p style="font-size: 8.5pt; color: #444; margin: 2px 0;">Sangivalasa, Bheemili Mandal, Visakhapatnam - 531162. (A.P)</p>
      <p style="font-size: 10pt; font-weight: bold; margin-top: 15px;">2026-2027</p>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 2 ========================================== -->
<div class="page">
  <div class="outer-border" style="border: 2px solid #000;">
    <div class="header-box" style="border-bottom: 2px solid #000;">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div style="text-align: center; margin: 30px 0 20px 0;">
      <h2 style="font-size: 16pt; font-weight: bold; letter-spacing: 0.5px; border-bottom: 2px solid #1a365d; display: inline-block; padding-bottom: 4px; margin: 0;">
        BONAFIDE CERTIFICATE
      </h2>
    </div>

    <div style="padding: 10px 15px; margin: 15px 0;">
      <p style="font-size: 10.5pt; line-height: 1.8; text-align: justify;">
        This is to certify that the mini project report entitled <strong>“FLIGHT FARE ANALYSIS AND PREDICTION”</strong> submitted as part of the curriculum for the <strong>Data Analytics and Data Visualization</strong> course by the <strong>II/IV Computer Science and Engineering</strong> student at <strong>Anil Neerukonda Institute of Technology & Sciences (ANITS), Visakhapatnam</strong>, is a record of bona fide work carried out under my supervision.
      </p>
    </div>

    <div style="text-align: center; margin: 25px 0 45px 0;">
      <p style="font-size: 9.5pt; font-weight: bold; color: #555; margin-bottom: 4px;">SUBMITTED BY</p>
      <p style="font-size: 13.5pt; font-weight: bold; color: #1a365d; margin: 0;">
        S. KOTESWARAO &nbsp;-&nbsp; (A24126510107)
      </p>
    </div>

    <div style="margin-top: 50px; padding: 0 10px;">
      <table style="width: 100%; border: none;">
        <tr style="border: none; background: none;">
          <td style="width: 50%; border: none; text-align: left; vertical-align: bottom; padding: 0;">
            <p style="font-size: 9.5pt; font-weight: bold; margin: 0;">Faculty-In charge</p>
            <p style="font-size: 9.5pt; font-weight: bold; margin: 40px 0 2px 0;">Mrs. Y. Padma sri</p>
            <p style="font-size: 8.5pt; color: #555; margin: 0;">Assistant Professor</p>
          </td>
          <td style="width: 50%; border: none; text-align: right; vertical-align: bottom; padding: 0;">
            <p style="font-size: 9.5pt; font-weight: bold; margin: 0;">Head of Department - CSE</p>
            <p style="font-size: 9.5pt; font-weight: bold; margin: 40px 0 2px 0;">Dr. G. Srinivas</p>
            <p style="font-size: 8.5pt; color: #555; margin: 0;">Head of Department - CSE, ANITS</p>
          </td>
        </tr>
      </table>
    </div>

    <div class="footer-box" style="border-top: 1.5px solid #000; margin-top: auto;">
      <span>A24126510107</span>
      <span>Bonafide Certificate</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 3 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <h1 class="doc-title">FLIGHT FARE (DAV) ANALYSIS AND PREDICTION</h1>
      <div class="sub-doc-title">Data Analytics and Visualization (DAV) Mini Project Documentation</div>

      <div style="background: #f8f9fa; border: 1px solid #e2e8f0; padding: 6px 10px; margin-bottom: 6px;">
        <p class="meta-p"><strong>Project Type:</strong> Flight Fare Data Analytics, Machine Learning Prediction and Streamlit Web Application</p>
        <p class="meta-p"><strong>Programming Language:</strong> Python</p>
        <p class="meta-p"><strong>Libraries / Technologies:</strong> Pandas, NumPy, Scikit-learn, Plotly, Streamlit</p>
        <p class="meta-p"><strong>Student:</strong> S. Koteswarao (A24126510107), II/IV B.Tech CSE, ANITS</p>
        <p class="meta-p"><strong>Dataset:</strong> 10,000 domestic flight booking records across 6 metro Indian cities with 19 columns; all 10,000 records remain after cleaning</p>
        <p class="meta-p"><strong>GitHub Repository:</strong> https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics</p>
        <p class="meta-p"><strong>Project Goal:</strong> Analyse which factors drive ticket prices on Indian domestic routes, study non-linear pricing effects (last-minute booking surge, seat-demand pricing, travel class multipliers), compare Linear Regression with Random Forest and build an interactive web application that predicts the fare of a flight booking.</p>
      </div>

      <h2 class="sec-heading">1. Introduction</h2>
      <p>Data Analytics and Visualization is the process of collecting, cleaning, exploring and presenting data so that useful patterns can be understood easily. Airline ticket prices are dynamic: the same seat can cost very different amounts depending on demand, how early it is booked, the distance flown, the airline and the season. For travellers, understanding these drivers helps in booking at the right time; for airlines, fare prediction supports revenue management and seat allocation.</p>
      <p>This project applies the DAV workflow to a dataset of 10,000 domestic flight bookings between six metro cities and extends it with machine learning to predict the fare. It covers data loading, cleaning, exploratory data analysis, visualization, training and comparison of two regression models, and a multi-page Streamlit web application that presents the analysis and gives live fare predictions.</p>

      <h2 class="sec-heading">2. Objectives</h2>
      <ul>
        <li>Clean and prepare a dataset that contains missing values and verify that there are no duplicate records.</li>
        <li>Find how airline, travel class, booking window, seat availability and departure slot influence ticket prices.</li>
        <li>Quantify the steep non-linear price surge for last-minute bookings and for flights with few seats left.</li>
        <li>Create clear, interactive visualizations that communicate the main patterns in the data.</li>
        <li>Implement and compare two machine learning models that predict the fare (fare_inr) using R<sup>2</sup>, RMSE and MAE.</li>
        <li>Deliver the results through a web interface with a live fare prediction form.</li>
      </ul>

      <h2 class="sec-heading">3. Tools and Technologies Used</h2>
      <p><strong>Python 3.14:</strong> Main programming language for data preparation, analysis, modelling and the web server.</p>
      <p><strong>Pandas:</strong> DataFrames, grouping, aggregation, filtering, median imputation and duplicate removal.</p>
      <p><strong>NumPy:</strong> Numerical operations, vectorised calculations and exponential / logarithmic functions.</p>
      <p><strong>Scikit-learn:</strong> ColumnTransformer, SimpleImputer, StandardScaler, OneHotEncoder, Pipeline, Linear Regression, Random Forest and the evaluation metrics (R<sup>2</sup>, RMSE, MAE).</p>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 1 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 4 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <p><strong>Plotly Express and Graph Objects:</strong> Interactive charts with hover, zoom and colour maps shown inside the web application.</p>
      <p><strong>Matplotlib and Seaborn:</strong> Static charts used in this report.</p>
      <p><strong>Streamlit:</strong> Web framework used to build the five-page interactive dashboard.</p>
      <p><strong>Git and GitHub:</strong> Version control and hosting of the source code.</p>

      <h2 class="sec-heading">4. Project Workflow</h2>
      <p>Raw synthetic data (10,000 records) &rarr; Pandas DataFrame &rarr; Data cleaning (median imputation) &rarr; Exploratory analysis &rarr; Plotly visualization &rarr; Preprocessing pipeline (imputer + scaler + one-hot encoder) &rarr; 80/20 train/test split &rarr; Model training and comparison &rarr; Streamlit web application &rarr; Live fare prediction &rarr; Deployment on Streamlit Community Cloud and GitHub</p>
      <p>The dataset generator is kept in data.py, while the cleaning, modelling and dashboard logic is kept in app.py, so the same prepared data feeds the charts and the models.</p>

      <h2 class="sec-heading">5. Important Code Used</h2>
      <div class="code-block">import numpy as np
import pandas as pd
SEED = 2026
N_RECORDS = 10_000
# Base fare calculation with realistic non-linear multipliers
base = 1800 + 3.2 * distance
advance_mult = 1 + 1.6 * np.exp(-days_before / 8) # last-minute spike
demand_mult = 1 + 0.5 * ((100 - seats) / 100) ** 2 # fewer seats -> pricier
stops_mult = 1 - 0.07 * stops
fare = (
    base
    * np.array([AIRLINE_PRICE_MULT[a] for a in airline])
    * np.array([CLASS_MULT[c] for c in travel_class])
    * advance_mult * demand_mult * stops_mult
    * np.array([TIME_MULT[t] for t in departure])
    * np.array([DAY_MULT[d] for d in day])
    * np.where(holiday == "Yes", 1.18, 1.0)
)
fare += (baggage - 15) * 45 + np.where(meal == "Yes", 350, 0)
fare += np.array([CHANNEL_FEE[c] for c in channel])
fare *= rng.lognormal(0, 0.06, n)</div>
      <p>The dataset is generated with a fixed seed, so the same 10,000 records are recreated every time. The fare starts from a base price that grows with distance and is then multiplied by airline, travel class, booking-window, seat-demand, stops, departure-slot, weekday and holiday factors. The booking-window factor 1 + 1.6e<sup>-days/8</sup> makes prices rise sharply in the last days before departure, and the seat factor makes nearly full flights more expensive. Baggage, meal and booking-channel add-ons and a small random noise are added at the end.</p>

      <h3 class="subsec-heading">Data cleaning and imputation (app.py)</h3>
      <div class="code-block">@st.cache_data
def clean_data(raw: pd.DataFrame):
    df = raw.copy()
    report = []
    for col in ["duration_hours", "seat_availability_pct", "airline_rating"]:
        n_missing = int(df[col].isna().sum())
        median = float(df[col].median())
        df[col] = df[col].fillna(median)
        report.append({{"Column": col, "Missing values": n_missing,
                       "Cleaning method": f"Filled with median ({{median:.2f}})"}})</div>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 2 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 5 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <div class="code-block">    n_dupes = int(df.duplicated().sum())
    df = df.drop_duplicates()
    return df, pd.DataFrame(report), n_dupes</div>
      <p>Each of the three columns with gaps is filled with its own median, which is robust to the long tail of extreme values, and the table is then checked for duplicate rows. No rows are deleted, so all 10,000 records are retained.</p>

      <h3 class="subsec-heading">Preprocessing pipeline and model training (app.py)</h3>
      <div class="code-block">def make_pre():
    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
    ])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
models = {{
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1),
}}</div>
      <p>Numeric features are median-imputed and standardised, categorical features are filled with the most frequent value and one-hot encoded, and both models use exactly the same preprocessing and the same 80% / 20% split (8,000 training and 2,000 test records).</p>

      <h2 class="sec-heading">6. Dataset Description</h2>
      <p>The dataset contains <strong>10,000 flight records in 19 columns</strong> for domestic bookings between six metro cities: Delhi, Mumbai, Bengaluru, Hyderabad, Kolkata and Chennai. It is a reproducible synthetic dataset, and missing values were injected on purpose so that the cleaning step can be demonstrated.</p>

      <table>
        <thead>
          <tr>
            <th style="width: 25%;">Column</th>
            <th style="width: 18%;">Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>flight_id</td><td>String</td><td>Unique booking identifier (e.g. FL100001)</td></tr>
          <tr><td>airline</td><td>Categorical</td><td>IndiGo, Air India, Akasa Air, SpiceJet, Air India Express, Alliance Air</td></tr>
          <tr><td>source_city</td><td>Categorical</td><td>Origin metro city</td></tr>
          <tr><td>destination_city</td><td>Categorical</td><td>Destination metro city</td></tr>
          <tr><td>distance_km</td><td>Numeric</td><td>Route distance, 290 km to 1,760 km</td></tr>
          <tr><td>departure_time</td><td>Categorical</td><td>Early Morning, Morning, Afternoon, Evening, Night</td></tr>
          <tr><td>day_of_week</td><td>Categorical</td><td>Day of travel, Monday to Sunday</td></tr>
          <tr><td>stops</td><td>Numeric</td><td>Number of layovers (0, 1 or 2)</td></tr>
          <tr><td>travel_class</td><td>Categorical</td><td>Economy, Premium Economy, Business</td></tr>
          <tr><td>days_before_departure</td><td>Numeric</td><td>Booking lead time, 1 to 60 days</td></tr>
          <tr><td>duration_hours</td><td>Numeric</td><td>Flight travel time in hours</td></tr>
          <tr><td>seat_availability_pct</td><td>Numeric</td><td>Unsold seats at booking time (3% to 100%)</td></tr>
          <tr><td>baggage_kg</td><td>Numeric</td><td>Included baggage allowance (15, 20, 25, 30 kg)</td></tr>
          <tr><td>meal_included</td><td>Categorical</td><td>In-flight meal included (Yes / No)</td></tr>
          <tr><td>airline_rating</td><td>Numeric</td><td>Customer rating (1.0 to 5.0)</td></tr>
          <tr><td>booking_channel</td><td>Categorical</td><td>Website, Mobile App, Travel Agent</td></tr>
        </tbody>
      </table>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 3 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 6 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <table>
        <thead>
          <tr>
            <th style="width: 25%;">Column</th>
            <th style="width: 18%;">Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>holiday_season</td><td>Categorical</td><td>Peak holiday period (Yes / No)</td></tr>
          <tr><td>fare_inr</td><td>Numeric (target)</td><td>Final ticket fare in Indian Rupees (prediction target)</td></tr>
          <tr><td>booking_status</td><td>Categorical</td><td>Confirmed, Rescheduled, Cancelled</td></tr>
        </tbody>
      </table>

      <h2 class="sec-heading">7. Data Cleaning and Preparation</h2>
      <p>Data preparation turns the raw table into a reliable modelling table. The following steps were applied and measured:</p>

      <table>
        <thead>
          <tr>
            <th style="width: 50%;">Step</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Duplicate rows removed</td><td>0 rows (verified with drop_duplicates)</td></tr>
          <tr><td>duration_hours missing values</td><td>300 (3.0%) filled with the median, 2.69 h</td></tr>
          <tr><td>seat_availability_pct missing values</td><td>200 (2.0%) filled with the median, 54.9%</td></tr>
          <tr><td>airline_rating missing values</td><td>250 (2.5%) filled with the median, 3.9</td></tr>
          <tr><td><strong>Total missing cells imputed</strong></td><td><strong>750 cells</strong></td></tr>
          <tr><td>Numeric model features standardised (mean 0, SD 1)</td><td>7 features</td></tr>
          <tr><td>Categorical model features one-hot encoded</td><td>9 features</td></tr>
          <tr><td>Columns excluded from model inputs</td><td>flight_id, fare_inr (target), booking_status</td></tr>
          <tr><td><strong>Final clean dataset</strong></td><td><strong>10,000 rows (100% retained)</strong></td></tr>
        </tbody>
      </table>

      <p>The target is the numeric fare_inr. Linear Regression uses the standardised features inside a scikit-learn Pipeline. The data is split randomly: the training set has 8,000 records (80%) and the test set has 2,000 records (20%).</p>

      <h2 class="sec-heading">8. Exploratory Data Analysis (EDA)</h2>
      <p>Exploratory Data Analysis examines the structure, distributions and relationships in the data before modelling. In this project EDA uses Pandas aggregations together with visualization.</p>

      <div class="code-block">df.shape
df.isna().sum()
df['booking_status'].value_counts(normalize=True)
df.groupby('travel_class')['fare_inr'].mean()
df.groupby('airline')['fare_inr'].mean().sort_values()
df.groupby(pd.cut(df['days_before_departure'], [0, 3, 7, 14, 30, 60]))['fare_inr'].mean()
df[numeric_cols + ['fare_inr']].corr()</div>

      <p>These operations summarise 10,000 bookings into a few meaningful numbers, such as the average fare of each travel class, airline or booking window.</p>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 4 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 7 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <h2 class="sec-heading" style="margin-top: 0;">9. Data Visualization Techniques</h2>
      <p>The project uses a horizontal bar chart for missing values, a donut chart for booking status, a histogram with density curve for the fare distribution, bar charts for travel class, airline and departure-slot comparison, a scatter plot coloured by travel class for booking window versus fare, a line chart for fare versus route distance, a box plot for the spread of fares by booking window, a correlation heatmap, an actual-versus-predicted scatter plot and feature-importance bars for model evaluation. The web application shows the same analysis with interactive Plotly charts.</p>

      <h2 class="sec-heading">10. Project Output – Data Quality and Fare Patterns</h2>

      <div class="grid-2">
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig1']}">
          <div class="fig-caption">Figure 1: Missing values in the raw data</div>
        </div>
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig2']}">
          <div class="fig-caption">Figure 2: Share of booking status</div>
        </div>
      </div>

      <p>Only three columns had gaps: duration_hours (300), airline_rating (250) and seat_availability_pct (200), a total of 750 cells, all filled with the median. 90.6% of bookings are Confirmed, 6.6% Rescheduled and 2.8% Cancelled.</p>

      <div class="grid-2">
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig3']}">
          <div class="fig-caption">Figure 3: Distribution of ticket fares</div>
        </div>
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig4']}">
          <div class="fig-caption">Figure 4: Average fare by travel class</div>
        </div>
      </div>

      <p>Fares are strongly right-skewed: the average fare is <strong>₹10,251</strong> but the median is <strong>₹8,603</strong>, and fares range from ₹1,789 to ₹84,583. The most expensive ticket is a Business-class booking on a 1,760 km route made only 3 days before departure. 64.2% of Economy fares lie between ₹3,500 and ₹9,000, while Business-class and last-minute bookings create the long tail.</p>
      <p>Travel class is the biggest price lever: Business averages <strong>₹24,824</strong>, Premium Economy <strong>₹13,552</strong> and Economy <strong>₹8,119</strong>, so Business costs about <strong>3.1 times</strong> as much as Economy and Premium Economy about 1.7 times.</p>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 5 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 8 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig5']}">
          <div class="fig-caption">Figure 5: Average fare by airline</div>
        </div>
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig6']}">
          <div class="fig-caption">Figure 6: Average fare by departure slot</div>
        </div>
      </div>

      <p>Air India is the most expensive airline (average ₹12,062), followed by IndiGo (₹10,156). SpiceJet (₹9,321), Air India Express (₹9,325) and Akasa Air (₹9,433) have the lowest averages. Evening departures are the dearest (₹11,014) and night departures the cheapest (₹9,208). Holiday-season bookings cost about 16% more (₹11,576 versus ₹9,967).</p>

      <h2 class="sec-heading">11. Project Output – Relationships and Predictors</h2>

      <div class="grid-2">
        <div>
          <img class="chart-img-tall" src="data:image/png;base64,{assets['fig7']}">
          <div class="fig-caption">Figure 7: Correlation matrix of numeric features and fare</div>
        </div>
        <div>
          <img class="chart-img-tall" src="data:image/png;base64,{assets['fig8']}">
          <div class="fig-caption">Figure 8: Booking window versus fare</div>
        </div>
      </div>

      <p>Among the numeric features, route distance has the strongest linear correlation with the fare (0.42), followed by days before departure (-0.26) and seat availability (-0.13): longer routes cost more, and the earlier the booking or the more seats are free, the cheaper the ticket. Baggage allowance and airline rating are almost unrelated (0.02). Travel class is categorical, so it does not appear in the matrix although it is the strongest driver of all.</p>

      <div class="grid-2">
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig9']}">
          <div class="fig-caption">Figure 9: Fare spread by booking window</div>
        </div>
        <div>
          <img class="chart-img" src="data:image/png;base64,{assets['fig10']}">
          <div class="fig-caption">Figure 10: Average fare versus route distance</div>
        </div>
      </div>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 6 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 9 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <p>The relationship with the booking window is clearly non-linear. Tickets bought 1–3 days ahead average ₹17,584, 4–7 days ₹15,166, 8–14 days ₹11,689, 15–30 days ₹9,513 and 31–60 days only ₹8,507, so the last-minute ticket costs about 2.1 times a ticket booked a month or more ahead. Bookings made within 7 days cost 84% more on average than bookings made 31 days or more ahead, and 17.7% of all bookings are made within 10 days of departure.</p>
      <p>Seat scarcity adds a smaller premium: flights with under 15% seats available average ₹12,681 compared with ₹10,176 for the rest. Fares also grow with distance, from about ₹5,399 on the shortest 290 km route to ₹13,524 on the longest 1,760 km route.</p>

      <h2 class="sec-heading">12. Machine Learning Models and Comparison</h2>
      <p>Two regression models were trained on the same training data and evaluated on the same unseen test records. The target is the numeric fare_inr, and the inputs are the 16 booking features (7 numeric and 9 categorical).</p>
      
      <p><strong>Models used:</strong></p>
      <ul>
        <li><strong>Linear Regression</strong> – a simple, interpretable baseline that assumes constant additive effects.</li>
        <li><strong>Random Forest Regressor</strong> – an ensemble of 150 decision trees that captures non-linear effects and interactions.</li>
      </ul>

      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>R2</th>
            <th>RMSE (INR)</th>
            <th>MAE (INR)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Linear Regression</td><td>0.8435</td><td>2,366.82</td><td>1,624.76</td></tr>
          <tr><td><strong>Random Forest (best)</strong></td><td><strong>0.9433</strong></td><td><strong>1,424.86</strong></td><td><strong>922.30</strong></td></tr>
        </tbody>
      </table>

      <div style="text-align: center; margin: 6px 0;">
        <img class="chart-img-tall" style="height: 155px;" src="data:image/png;base64,{assets['fig11']}">
        <div class="fig-caption">Figure 11: Model comparison</div>
      </div>

      <p><strong>Random Forest achieved the best result with R<sup>2</sup> = 0.9433, RMSE = ₹1,424.86 and MAE = ₹922.30:</strong> on average its prediction is about ₹922 away from the real fare. This lowers the MAE by 43.2% (from ₹1,625 to ₹922) and the RMSE by 39.8% compared with Linear Regression (R<sup>2</sup> 0.8435). Fares depend on non-linear effects such as the exponential last-minute surge and the quadratic seat-demand effect, which a straight-line model cannot capture but decision trees can.</p>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 7 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 10 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div>
          <img class="chart-img-tall" src="data:image/png;base64,{assets['fig12']}">
          <div class="fig-caption">Figure 12: Actual versus predicted fare</div>
        </div>
        <div>
          <img class="chart-img-tall" src="data:image/png;base64,{assets['fig13']}">
          <div class="fig-caption">Figure 13: Random Forest feature importance</div>
        </div>
      </div>

      <p>The most important predictors are travel class (51.0%), route distance (21.8%), days before departure (16.3%), seat availability (3.1%) and airline (2.9%); all other features together contribute 4.8%. This agrees with the EDA, where class, distance and booking window showed the largest price differences.</p>

      <h2 class="sec-heading">13. Web Application</h2>
      <p>The project is delivered as a Streamlit web application (app.py) with interactive Plotly charts. It has five pages:</p>
      <ul>
        <li><strong>Actual Dataset</strong> – the raw 10,000 records, the 19-column data dictionary, summary metrics and a CSV download button.</li>
        <li><strong>Data Cleaning</strong> – missing values per column before and after median imputation, duplicate check and a description of the pipeline.</li>
        <li><strong>Exploratory Analysis</strong> – fare distribution, airline comparison, booking lead-time curves and the correlation heatmap.</li>
        <li><strong>Model Comparison</strong> – metric cards (MAE, RMSE, R<sup>2</sup>), actual-versus-predicted plot and feature importance.</li>
        <li><strong>Predict Fare</strong> – a booking form (airline, route, departure slot, travel class, lead days, seat availability, baggage) that returns the predicted fare from both models.</li>
      </ul>

      <p><strong>How to run:</strong></p>
      <div class="code-block">pip install -r requirements.txt
streamlit run app.py</div>
      <p>The application is also deployed on Streamlit Community Cloud, and the source code is available in the GitHub repository listed above.</p>

      <h2 class="sec-heading">14. Key Findings</h2>
      <ul>
        <li>The dataset has 10,000 bookings; after median imputation of 750 missing cells no record was lost.</li>
        <li>Travel class is the main price driver: Business costs about 3.1 times Economy and class alone accounts for about half of the model importance (51.0%).</li>
        <li>Last-minute bookings are the most expensive: a ticket bought 1–3 days ahead costs about 2.1 times one bought 31–60 days ahead.</li>
        <li>Air India is the most expensive airline (₹12,062 on average); SpiceJet, Air India Express and Akasa Air are the cheapest.</li>
        <li>Fewer seats and holiday periods push prices up (+25% below 15% seat availability, +16% in holiday season).</li>
      </ul>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 8 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

<!-- ========================================== PAGE 11 ========================================== -->
<div class="page">
  <div class="outer-border">
    <div class="header-box">
      <h4>ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES</h4>
      <h5>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</h5>
      <h5>DATA ANALYTICS AND DATA VISUALIZATION LAB</h5>
    </div>

    <div class="content-area">
      <ul>
        <li>Random Forest gives the best performance (R<sup>2</sup> 0.9433, MAE ₹922.30) and clearly beats Linear Regression because fares are non-linear.</li>
      </ul>

      <h2 class="sec-heading">15. Limitations</h2>
      <ul>
        <li>The dataset is synthetic: fares are produced by a formula with a fixed seed, so the patterns reflect the pricing rules built into it, not real airline data. The high R<sup>2</sup> partly shows that the model can rediscover these rules.</li>
        <li>The 750 missing values were imputed with the median, which can hide real variation.</li>
        <li>Only two models were compared and no hyper-parameter tuning was done; the train/test split is random, not time-based.</li>
        <li>Only six metro cities are covered, and holidays are a simple Yes/No flag with no real calendar or live fare feed.</li>
      </ul>

      <h2 class="sec-heading">16. Conclusion</h2>
      <p>The Flight Fare project demonstrates the complete DAV workflow: data handling, cleaning, exploratory analysis, visual communication, machine learning and deployment as a web application. Two models were compared on the same test data, and the best one, Random Forest (R<sup>2</sup> = 0.9433, MAE = ₹922), is used for live fare prediction. The analysis shows clearly how travel class, distance and booking lead time drive ticket prices.</p>
      <p>The project can be extended with real-time flight pricing APIs (such as Amadeus or Skyscanner), route-specific festive surge detection with lowest-fare alerts, and gradient boosting models such as XGBoost or LightGBM for further accuracy gains.</p>

      <h2 class="sec-heading">17. References</h2>
      <ul>
        <li><strong>Pandas:</strong> https://pandas.pydata.org/docs/</li>
        <li><strong>Scikit-learn ensemble methods:</strong> https://scikit-learn.org/stable/modules/ensemble.html</li>
        <li><strong>Plotly for Python:</strong> https://plotly.com/python/</li>
        <li><strong>Streamlit:</strong> https://docs.streamlit.io/</li>
        <li><strong>Project repository:</strong> https://github.com/koteswaraosabbavarapu-stack/flight-fare-anlytics (app.py, data.py, requirements.txt)</li>
      </ul>
    </div>

    <div class="footer-box">
      <span>A24126510107</span>
      <span>Page 9 of 9</span>
      <span>S.Koteswarao</span>
    </div>
  </div>
</div>

</body>
</html>
"""

with open("Flight_Fare_Analysis_and_Prediction_Report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated Flight_Fare_Analysis_and_Prediction_Report.html successfully.")
