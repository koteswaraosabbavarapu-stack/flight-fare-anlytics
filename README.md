# SkyFare Analytics — Flight Fare Data Analytics & Visualization

A small data analytics mini-project built with **Python, Streamlit, Pandas, Plotly, and Scikit-learn**.
It analyses a synthetic flight-booking dataset and predicts the **ticket fare (INR)**.

## 1. Dataset

The project uses a reproducible **synthetic flight-booking dataset with 10,000 records** covering
domestic routes between six Indian metro cities. The data is generated with a fixed seed, so the same
dataset is recreated every time the app runs.

The dataset has **19 columns**:

| Column | Description |
| --- | --- |
| flight_id | Unique booking identifier |
| airline | IndiGo, Air India, Akasa Air, SpiceJet, Air India Express, Alliance Air |
| source_city, destination_city | Delhi, Mumbai, Bengaluru, Hyderabad, Kolkata, Chennai |
| distance_km | Route distance |
| departure_time | Early Morning / Morning / Afternoon / Evening / Night |
| day_of_week | Day of travel |
| stops | 0, 1 or 2 |
| travel_class | Economy / Premium Economy / Business |
| days_before_departure | Booking window (1–60 days) |
| duration_hours | Journey time |
| seat_availability_pct | Unsold seats at booking time |
| baggage_kg | Checked baggage allowance |
| meal_included | Yes / No |
| airline_rating | Customer rating (1–5) |
| booking_channel | Website / Mobile App / Travel Agent |
| holiday_season | Yes / No |
| **fare_inr** | **Final ticket fare (prediction target)** |
| booking_status | Confirmed / Rescheduled / Cancelled |

Fares are generated with realistic, **non-linear** pricing effects: a steep last-minute price spike,
demand-based pricing from seat availability, class and airline multipliers, weekend/holiday uplift and
baggage/meal/channel add-ons.

## 2. Data Cleaning

The raw dataset intentionally contains missing values so the preprocessing step can be demonstrated.

| Column | Missing values | Cleaning method |
| --- | --- | --- |
| duration_hours | 300 | Filled with the median |
| seat_availability_pct | 200 | Filled with the median |
| airline_rating | 250 | Filled with the median |

So **750 missing cells** are handled without deleting any rows. The dataset is also checked for
duplicate rows; none were found.

### Model preprocessing

- Numeric features are median-imputed and standardized.
- Categorical features are filled with the most frequent value, then one-hot encoded.
- `flight_id`, `fare_inr` and `booking_status` are excluded from the model inputs.
- The same preprocessing pipeline is used for both models.

## 3. Exploratory Data Analysis

- Fare distribution
- Booking status distribution
- Average fare by travel class and by airline
- Booking window vs fare (last-minute spike)
- Average fare vs route distance and by departure time
- Numeric correlation matrix

## 4. Machine Learning Models

Two regression models predict `fare_inr`, using the same **80/20 train-test split**:

1. **Linear Regression**
2. **Random Forest Regressor** (150 trees)

| Model | MAE | RMSE | R² |
| --- | --- | --- | --- |
| Linear Regression | 1,624.76 | 2,366.82 | 0.844 |
| Random Forest | 922.30 | 1,424.86 | 0.943 |

**Random Forest is the better model for this dataset.** It has lower MAE and RMSE and a higher R².
Fares depend on non-linear effects (for example, the price spike for last-minute bookings and
interactions between class, airline and demand), which a straight-line model cannot capture but a
tree-based model can. Feature importance shows travel class, route distance and booking window as the
main fare drivers.

## 5. Web Application Flow

1. **Actual Dataset** — raw records, column dictionary, CSV download.
2. **Data Cleaning** — missing values, cleaning operations, cleaned data.
3. **Exploratory Analysis** — distributions and relationships.
4. **Model Comparison** — MAE, RMSE, R², actual vs predicted, feature importance.
5. **Predict Fare** — enter a booking profile and get predictions from both models.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```
├── app.py            # Streamlit app (5 pages)
├── data.py           # Synthetic dataset generator
├── requirements.txt
└── README.md
```
