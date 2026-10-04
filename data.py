"""Synthetic flight-fare dataset generator (10,000 records, fixed seed)."""

import numpy as np
import pandas as pd

SEED = 2026
N_RECORDS = 10_000

CITIES = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Kolkata", "Chennai"]

# Approximate air distance between city pairs (km)
_DIST = {
    ("Delhi", "Mumbai"): 1150, ("Delhi", "Bengaluru"): 1750, ("Delhi", "Hyderabad"): 1250,
    ("Delhi", "Kolkata"): 1300, ("Delhi", "Chennai"): 1760, ("Mumbai", "Bengaluru"): 840,
    ("Mumbai", "Hyderabad"): 620, ("Mumbai", "Kolkata"): 1660, ("Mumbai", "Chennai"): 1030,
    ("Bengaluru", "Hyderabad"): 500, ("Bengaluru", "Kolkata"): 1560, ("Bengaluru", "Chennai"): 290,
    ("Hyderabad", "Kolkata"): 1190, ("Hyderabad", "Chennai"): 520, ("Kolkata", "Chennai"): 1370,
}


def route_distance(src: str, dst: str) -> int:
    """Distance in km between two cities (order does not matter)."""
    return _DIST.get((src, dst)) or _DIST[(dst, src)]


AIRLINES = ["IndiGo", "Air India", "Akasa Air", "SpiceJet", "Air India Express", "Alliance Air"]
AIRLINE_PRICE_MULT = {
    "IndiGo": 1.00, "Air India": 1.18, "Akasa Air": 0.95,
    "SpiceJet": 0.92, "Air India Express": 0.90, "Alliance Air": 0.97,
}
AIRLINE_RATING_BASE = {
    "IndiGo": 4.1, "Air India": 3.9, "Akasa Air": 4.2,
    "SpiceJet": 3.5, "Air India Express": 3.7, "Alliance Air": 3.3,
}

DEPARTURE_SLOTS = ["Early Morning", "Morning", "Afternoon", "Evening", "Night"]
TIME_MULT = {"Early Morning": 0.95, "Morning": 1.05, "Afternoon": 1.00, "Evening": 1.12, "Night": 0.93}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_MULT = {"Monday": 1.03, "Tuesday": 0.95, "Wednesday": 0.95, "Thursday": 1.00,
            "Friday": 1.08, "Saturday": 1.00, "Sunday": 1.10}

CLASSES = ["Economy", "Premium Economy", "Business"]
CLASS_MULT = {"Economy": 1.0, "Premium Economy": 1.7, "Business": 3.2}

CHANNELS = ["Website", "Mobile App", "Travel Agent"]
CHANNEL_FEE = {"Website": 0, "Mobile App": -100, "Travel Agent": 250}

TARGET = "fare_inr"
# Columns that are never used as model inputs
NON_FEATURES = ["flight_id", TARGET, "booking_status"]


def estimate_duration(distance_km: float, stops: int) -> float:
    """Rough flight duration in hours (used by the prediction page)."""
    return round(distance_km / 780 + 0.6 + 1.8 * stops, 2)


def generate_dataset(n: int = N_RECORDS, seed: int = SEED, with_missing: bool = True) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    airline = rng.choice(AIRLINES, n, p=[0.35, 0.22, 0.12, 0.11, 0.14, 0.06])

    # Source != destination
    src = rng.choice(CITIES, n)
    dst = rng.choice(CITIES, n)
    clash = src == dst
    while clash.any():
        dst[clash] = rng.choice(CITIES, clash.sum())
        clash = src == dst
    distance = np.array([route_distance(s, d) for s, d in zip(src, dst)])

    departure = rng.choice(DEPARTURE_SLOTS, n, p=[0.14, 0.26, 0.20, 0.24, 0.16])
    day = rng.choice(DAYS, n)
    stops = rng.choice([0, 1, 2], n, p=[0.58, 0.34, 0.08])
    travel_class = rng.choice(CLASSES, n, p=[0.76, 0.17, 0.07])
    days_before = np.clip(rng.gamma(2.2, 11, n).astype(int) + 1, 1, 60)
    duration = np.round(distance / 780 + 0.6 + 1.8 * stops + rng.normal(0, 0.25, n), 2)
    duration = np.clip(duration, 0.8, None)
    seats = np.clip(rng.normal(55, 22, n), 3, 100).round(1)
    baggage = rng.choice([15, 20, 25, 30], n, p=[0.40, 0.30, 0.20, 0.10])
    meal = rng.choice(["Yes", "No"], n, p=[0.45, 0.55])
    rating = np.clip(
        np.array([AIRLINE_RATING_BASE[a] for a in airline]) + rng.normal(0, 0.3, n), 1.0, 5.0
    ).round(1)
    channel = rng.choice(CHANNELS, n, p=[0.45, 0.42, 0.13])
    holiday = rng.choice(["Yes", "No"], n, p=[0.18, 0.82])

    # ---- Fare logic (deliberately non-linear) ----
    base = 1800 + 3.2 * distance
    advance_mult = 1 + 1.6 * np.exp(-days_before / 8)          # last-minute spike
    demand_mult = 1 + 0.5 * ((100 - seats) / 100) ** 2          # fewer seats -> pricier
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
    fare = fare.round(0)

    # Booking outcome: pricier tickets are cancelled a little more often
    p_cancel = np.clip(0.03 + (fare - fare.mean()) / fare.std() * 0.012, 0.01, 0.12)
    p_resched = np.full(n, 0.07)
    r = rng.random(n)
    status = np.where(r < p_cancel, "Cancelled",
                      np.where(r < p_cancel + p_resched, "Rescheduled", "Confirmed"))

    df = pd.DataFrame({
        "flight_id": [f"FL{100000 + i}" for i in range(n)],
        "airline": airline,
        "source_city": src,
        "destination_city": dst,
        "distance_km": distance,
        "departure_time": departure,
        "day_of_week": day,
        "stops": stops,
        "travel_class": travel_class,
        "days_before_departure": days_before,
        "duration_hours": duration,
        "seat_availability_pct": seats,
        "baggage_kg": baggage,
        "meal_included": meal,
        "airline_rating": rating,
        "booking_channel": channel,
        "holiday_season": holiday,
        TARGET: fare,
        "booking_status": status,
    })

    if with_missing:
        # Intentionally inject missing values to demonstrate cleaning
        for col, k in [("duration_hours", 300), ("seat_availability_pct", 200), ("airline_rating", 250)]:
            idx = rng.choice(n, k, replace=False)
            df.loc[idx, col] = np.nan

    return df


if __name__ == "__main__":
    out = generate_dataset()
    out.to_csv("flight_fares_raw.csv", index=False)
    print(out.shape)
    print(out.isna().sum()[out.isna().sum() > 0])
