"""SkyFare Analytics - Flight Fare Data Analytics & Visualization mini-project."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from data import (
    AIRLINES, CITIES, CLASSES, CHANNELS, DAYS, DEPARTURE_SLOTS, NON_FEATURES, TARGET,
    estimate_duration, generate_dataset, route_distance,
)

st.set_page_config(page_title="SkyFare Analytics", page_icon="✈️", layout="wide")

MISSING_COLS = ["duration_hours", "seat_availability_pct", "airline_rating"]


# ----------------------------------------------------------------------------
# Data + model helpers (cached so they only run once)
# ----------------------------------------------------------------------------
@st.cache_data
def load_raw() -> pd.DataFrame:
    return generate_dataset()


@st.cache_data
def clean_data(raw: pd.DataFrame):
    df = raw.copy()
    report = []
    for col in MISSING_COLS:
        n_missing = int(df[col].isna().sum())
        median = float(df[col].median())
        df[col] = df[col].fillna(median)
        report.append({"Column": col, "Missing values": n_missing,
                       "Cleaning method": f"Filled with median ({median:.2f})"})
    n_dupes = int(df.duplicated().sum())
    df = df.drop_duplicates()
    return df, pd.DataFrame(report), n_dupes


@st.cache_resource
def train_models(df: pd.DataFrame):
    X = df.drop(columns=NON_FEATURES)
    y = df[TARGET]
    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()

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
    fitted, rows, preds = {}, [], {}
    for name, est in models.items():
        pipe = Pipeline([("pre", make_pre()), ("model", est)]).fit(X_tr, y_tr)
        p = pipe.predict(X_te)
        fitted[name], preds[name] = pipe, p
        rows.append({
            "Model": name,
            "MAE": mean_absolute_error(y_te, p),
            "RMSE": float(np.sqrt(mean_squared_error(y_te, p))),
            "R²": r2_score(y_te, p),
        })
    metrics = pd.DataFrame(rows)

    rf = fitted["Random Forest"]
    names = rf.named_steps["pre"].get_feature_names_out()
    importance = (pd.DataFrame({"Feature": names,
                                "Importance": rf.named_steps["model"].feature_importances_})
                  .sort_values("Importance", ascending=False).head(15))
    importance["Feature"] = importance["Feature"].str.replace(r"^(num|cat)__", "", regex=True)

    return {"pipes": fitted, "metrics": metrics, "y_test": y_te.reset_index(drop=True),
            "preds": preds, "importance": importance, "feature_cols": X.columns.tolist(),
            "n_train": len(X_tr), "n_test": len(X_te)}


raw_df = load_raw()
clean_df, missing_report, n_dupes = clean_data(raw_df)
art = train_models(clean_df)

# ----------------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------------
st.sidebar.title("✈️ SkyFare Analytics")
st.sidebar.caption("Flight fare analytics & prediction")
page = st.sidebar.radio(
    "Workflow",
    ["1. Actual Dataset", "2. Data Cleaning", "3. Exploratory Analysis",
     "4. Model Comparison", "5. Predict Fare"],
)
st.sidebar.markdown("---")
st.sidebar.write(f"**Records:** {len(raw_df):,}  \n**Columns:** {raw_df.shape[1]}")

st.title("SkyFare Analytics — Flight Fare Data Analytics & Visualization")

# ----------------------------------------------------------------------------
# 1. Actual dataset
# ----------------------------------------------------------------------------
if page.startswith("1"):
    st.header("1. Actual Dataset")
    st.write("A reproducible **synthetic flight-booking dataset** of 10,000 records for "
             "Indian domestic routes. This is the raw data, before any cleaning.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records", f"{len(raw_df):,}")
    c2.metric("Columns", raw_df.shape[1])
    c3.metric("Missing cells", int(raw_df.isna().sum().sum()))
    c4.metric("Target", TARGET)

    st.subheader("Raw records")
    st.dataframe(raw_df.head(200))
    st.caption("Showing the first 200 rows.")

    st.subheader("Column dictionary")
    desc = {
        "flight_id": "Unique booking identifier",
        "airline": "Carrier operating the flight",
        "source_city / destination_city": "Origin and destination metro cities",
        "distance_km": "Approximate air distance of the route",
        "departure_time": "Departure slot of the day",
        "day_of_week": "Day of travel",
        "stops": "Number of stops (0 = non-stop)",
        "travel_class": "Economy / Premium Economy / Business",
        "days_before_departure": "How many days in advance the ticket was booked",
        "duration_hours": "Total journey time in hours",
        "seat_availability_pct": "Seats still unsold at booking time (%)",
        "baggage_kg": "Checked baggage allowance",
        "meal_included": "Whether a meal is included",
        "airline_rating": "Customer rating of the airline (1-5)",
        "booking_channel": "Website / Mobile App / Travel Agent",
        "holiday_season": "Whether travel falls in a holiday period",
        "fare_inr": "Final ticket fare in INR (prediction target)",
        "booking_status": "Confirmed / Rescheduled / Cancelled",
    }
    st.table(pd.DataFrame({"Column": desc.keys(), "Description": desc.values()}))

    st.download_button("Download raw dataset (CSV)", raw_df.to_csv(index=False),
                       file_name="flight_fares_raw.csv", mime="text/csv")

# ----------------------------------------------------------------------------
# 2. Data cleaning
# ----------------------------------------------------------------------------
elif page.startswith("2"):
    st.header("2. Data Cleaning")
    st.write("The raw data intentionally contains missing values so the preprocessing "
             "step can be demonstrated.")

    st.subheader("Missing values before cleaning")
    before = raw_df.isna().sum()
    before = before[before > 0].reset_index()
    before.columns = ["Column", "Missing values"]
    c1, c2 = st.columns([1, 1])
    c1.dataframe(before)
    fig = px.bar(before, x="Column", y="Missing values", text="Missing values",
                 title="Missing values per column")
    c2.plotly_chart(fig)

    st.subheader("Cleaning operations")
    st.dataframe(missing_report)
    total = int(raw_df.isna().sum().sum())
    st.success(f"{total} missing cells were handled by median imputation, "
               "without deleting any rows.")

    st.subheader("Duplicate check")
    if n_dupes == 0:
        st.info("No duplicate rows were found, so no valid records were removed.")
    else:
        st.warning(f"{n_dupes} duplicate rows were removed.")

    st.subheader("After cleaning")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(clean_df):,}")
    c2.metric("Missing cells", int(clean_df.isna().sum().sum()))
    c3.metric("Duplicates", int(clean_df.duplicated().sum()))
    st.dataframe(clean_df.head(200))

    st.subheader("Preprocessing used before model training")
    st.markdown(
        "- Numeric features are median-imputed and standardized.\n"
        "- Categorical features are filled with the most frequent value.\n"
        "- Categorical values are converted using one-hot encoding.\n"
        "- `flight_id`, `fare_inr` and `booking_status` are excluded from the inputs.\n"
        "- The same preprocessing pipeline is used for both models."
    )

# ----------------------------------------------------------------------------
# 3. EDA
# ----------------------------------------------------------------------------
elif page.startswith("3"):
    st.header("3. Exploratory Data Analysis")
    df = clean_df

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average fare", f"₹{df[TARGET].mean():,.0f}")
    c2.metric("Median fare", f"₹{df[TARGET].median():,.0f}")
    c3.metric("Cheapest", f"₹{df[TARGET].min():,.0f}")
    c4.metric("Most expensive", f"₹{df[TARGET].max():,.0f}")

    st.subheader("Fare distribution")
    st.plotly_chart(px.histogram(df, x=TARGET, nbins=60, color_discrete_sequence=["#1f77b4"],
                                 title="Distribution of ticket fares (INR)"))
    st.caption("Fares are right-skewed: most tickets are cheap, with a long tail of "
               "last-minute and business-class bookings.")

    c1, c2 = st.columns(2)
    status = df["booking_status"].value_counts().reset_index()
    status.columns = ["Status", "Count"]
    c1.plotly_chart(px.pie(status, names="Status", values="Count", hole=0.45,
                           title="Booking status distribution"))
    cls = df.groupby("travel_class")[TARGET].mean().reindex(CLASSES).reset_index()
    c2.plotly_chart(px.bar(cls, x="travel_class", y=TARGET, text_auto=".0f",
                           title="Average fare by travel class"))

    st.subheader("Booking window vs fare")
    sample = df.sample(3000, random_state=1)
    st.plotly_chart(px.scatter(sample, x="days_before_departure", y=TARGET,
                               color="travel_class", opacity=0.6,
                               title="Fares rise sharply for last-minute bookings"))

    st.subheader("Average fare by airline")
    air = df.groupby("airline")[TARGET].mean().sort_values(ascending=False).reset_index()
    st.plotly_chart(px.bar(air, x="airline", y=TARGET, text_auto=".0f",
                           color=TARGET, color_continuous_scale="Blues"))

    c1, c2 = st.columns(2)
    dist = df.groupby("distance_km")[TARGET].mean().reset_index().sort_values("distance_km")
    c1.plotly_chart(px.line(dist, x="distance_km", y=TARGET, markers=True,
                            title="Average fare vs route distance"))
    dep = df.groupby("departure_time")[TARGET].mean().reindex(DEPARTURE_SLOTS).reset_index()
    c2.plotly_chart(px.bar(dep, x="departure_time", y=TARGET, text_auto=".0f",
                           title="Average fare by departure time"))

    st.subheader("Numeric correlation matrix")
    corr = df.select_dtypes(include="number").corr()
    st.plotly_chart(px.imshow(corr, text_auto=".2f", aspect="auto",
                              color_continuous_scale="RdBu_r", zmin=-1, zmax=1))

# ----------------------------------------------------------------------------
# 4. Model comparison
# ----------------------------------------------------------------------------
elif page.startswith("4"):
    st.header("4. Model Comparison")
    st.write("Both models predict **fare_inr** using the same 80/20 train-test split "
             f"({art['n_train']:,} train / {art['n_test']:,} test rows) and the same "
             "preprocessing pipeline.")

    m = art["metrics"].copy()
    st.dataframe(m.style.format({"MAE": "{:,.2f}", "RMSE": "{:,.2f}", "R²": "{:.3f}"}))

    best = m.sort_values("R²", ascending=False).iloc[0]
    other = m.sort_values("R²", ascending=False).iloc[1]
    st.success(f"**{best['Model']} is the better model for this dataset.**")
    st.markdown(
        f"- Lower MAE: **{best['MAE']:,.2f}** vs {other['MAE']:,.2f}\n"
        f"- Lower RMSE: **{best['RMSE']:,.2f}** vs {other['RMSE']:,.2f}\n"
        f"- Higher R²: **{best['R²']:.3f}** vs {other['R²']:.3f}\n\n"
        "MAE and RMSE measure prediction error in rupees, so lower is better. "
        "R² is the share of fare variation explained by the model, so higher is better."
    )
    st.info("Why? Fares here depend on non-linear effects such as the last-minute price "
            "spike and interactions between class, airline and demand. A straight-line "
            "model cannot capture these, while a tree-based model can.")

    c1, c2, c3 = st.columns(3)
    for col, metric in zip([c1, c2, c3], ["MAE", "RMSE", "R²"]):
        col.plotly_chart(px.bar(m, x="Model", y=metric, color="Model", text_auto=".3s",
                                title=metric))

    st.subheader("Actual vs predicted")
    choice = st.selectbox("Model", list(art["preds"].keys()),
                          index=list(art["preds"].keys()).index(best["Model"]))
    n = min(1500, len(art["y_test"]))
    idx = np.random.default_rng(0).choice(len(art["y_test"]), n, replace=False)
    actual = art["y_test"].iloc[idx]
    predicted = art["preds"][choice][idx]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual, y=predicted, mode="markers", opacity=0.5, name="Test rows"))
    lim = [0, float(max(actual.max(), predicted.max()))]
    fig.add_trace(go.Scatter(x=lim, y=lim, mode="lines", name="Perfect prediction",
                             line=dict(dash="dash", color="red")))
    fig.update_layout(xaxis_title="Actual fare (INR)", yaxis_title="Predicted fare (INR)")
    st.plotly_chart(fig)

    st.subheader("What drives fares? (Random Forest feature importance)")
    imp = art["importance"].sort_values("Importance")
    st.plotly_chart(px.bar(imp, x="Importance", y="Feature", orientation="h"))

# ----------------------------------------------------------------------------
# 5. Predict
# ----------------------------------------------------------------------------
else:
    st.header("5. Predict Fare")
    st.write("Enter a flight booking profile to get a fare prediction from both models.")

    with st.form("predict_form"):
        c1, c2, c3 = st.columns(3)
        airline = c1.selectbox("Airline", AIRLINES)
        src = c2.selectbox("Source city", CITIES, index=0)
        dst = c3.selectbox("Destination city", CITIES, index=1)

        c1, c2, c3 = st.columns(3)
        travel_class = c1.selectbox("Travel class", CLASSES)
        departure = c2.selectbox("Departure time", DEPARTURE_SLOTS, index=1)
        day = c3.selectbox("Day of week", DAYS)

        c1, c2, c3 = st.columns(3)
        stops = c1.selectbox("Stops", [0, 1, 2])
        days_before = c2.slider("Days before departure", 1, 60, 14)
        seats = c3.slider("Seat availability (%)", 3, 100, 55)

        c1, c2, c3 = st.columns(3)
        baggage = c1.selectbox("Baggage (kg)", [15, 20, 25, 30])
        rating = c2.slider("Airline rating", 1.0, 5.0, 4.0, 0.1)
        channel = c3.selectbox("Booking channel", CHANNELS)

        c1, c2 = st.columns(2)
        meal = c1.radio("Meal included", ["Yes", "No"], horizontal=True, index=1)
        holiday = c2.radio("Holiday season", ["Yes", "No"], horizontal=True, index=1)

        submitted = st.form_submit_button("Predict fare")

    if submitted:
        if src == dst:
            st.error("Source and destination must be different cities.")
        else:
            distance = route_distance(src, dst)
            duration = estimate_duration(distance, stops)
            row = pd.DataFrame([{
                "airline": airline, "source_city": src, "destination_city": dst,
                "distance_km": distance, "departure_time": departure, "day_of_week": day,
                "stops": stops, "travel_class": travel_class,
                "days_before_departure": days_before, "duration_hours": duration,
                "seat_availability_pct": float(seats), "baggage_kg": baggage,
                "meal_included": meal, "airline_rating": rating,
                "booking_channel": channel, "holiday_season": holiday,
            }])[art["feature_cols"]]

            st.caption(f"Route distance: {distance:,} km · Estimated duration: {duration} h")
            c1, c2 = st.columns(2)
            for col, name in zip([c1, c2], art["pipes"].keys()):
                pred = float(art["pipes"][name].predict(row)[0])
                col.metric(name, f"₹{max(pred, 0):,.0f}")
            best_name = art["metrics"].sort_values("R²", ascending=False).iloc[0]["Model"]
            st.info(f"{best_name} has the better accuracy on the test data, "
                    "so treat its prediction as the primary estimate.")
