"""Generate all 13 report figures for the Flight Fare project documentation."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import data

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 9

os.makedirs("report_assets", exist_ok=True)

# 1. Load Data
raw_df = data.generate_dataset()
clean_df = raw_df.copy()
for col in ["duration_hours", "seat_availability_pct", "airline_rating"]:
    clean_df[col] = clean_df[col].fillna(clean_df[col].median())
clean_df = clean_df.drop_duplicates()

# -------------------------------------------------------------
# Figure 1: Missing values in the raw data
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3.2), dpi=200)
missing = raw_df[["duration_hours", "airline_rating", "seat_availability_pct"]].isna().sum().sort_values(ascending=True)
bars = ax.barh(missing.index, missing.values, color='#ff7f0e', height=0.6)
ax.set_title("Missing values per column (before cleaning)", fontsize=10, pad=10)
ax.set_xlabel("Count")
ax.grid(axis='x', linestyle='--', alpha=0.7)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 5, bar.get_y() + bar.get_height()/2, f"{int(w)}", va='center', fontsize=8)
plt.tight_layout()
plt.savefig("report_assets/fig1_missing.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 2: Share of booking status
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=200)
status_counts = clean_df["booking_status"].value_counts()
colors = ['#8bc34a', '#ff9800', '#78909c']
wedges, texts, autotexts = ax.pie(
    status_counts, 
    labels=status_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    wedgeprops=dict(width=0.4, edgecolor='w')
)
for at in autotexts:
    at.set_fontsize(8)
    at.set_weight('bold')
for t in texts:
    t.set_fontsize(8)
ax.set_title("Booking status share", fontsize=10, pad=10)
plt.tight_layout()
plt.savefig("report_assets/fig2_status_share.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 3: Distribution of ticket fares
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3.2), dpi=200)
sns.histplot(clean_df["fare_inr"], bins=60, kde=True, color="#42a5f5", edgecolor="#1e88e5", ax=ax)
ax.set_title("Distribution of ticket fares", fontsize=10, pad=10)
ax.set_xlabel("Fare (INR)")
ax.set_ylabel("Count")
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("report_assets/fig3_fare_dist.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 4: Average fare by travel class
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=200)
class_avg = clean_df.groupby("travel_class")["fare_inr"].mean().reindex(["Economy", "Premium Economy", "Business"])
colors = ['#26a69a', '#ff7043', '#2979ff']
bars = ax.bar(class_avg.index, class_avg.values, color=colors, width=0.6, edgecolor='#333', linewidth=0.5)
ax.set_title("Average fare by travel class", fontsize=10, pad=10)
ax.set_ylabel("Avg fare (INR)")
ax.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 500, f"₹{int(h):,}", ha='center', fontsize=8, weight='bold')
plt.tight_layout()
plt.savefig("report_assets/fig4_fare_by_class.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 5: Average fare by airline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=200)
air_avg = clean_df.groupby("airline")["fare_inr"].mean().sort_values(ascending=False)
bars = ax.bar(air_avg.index, air_avg.values, color='#ff9800', width=0.65, edgecolor='#d84315', linewidth=0.5)
ax.set_title("Average fare by airline", fontsize=10, pad=10)
ax.set_ylabel("Avg fare (INR)")
plt.xticks(rotation=25, ha='right', fontsize=8)
ax.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 200, f"{int(h):,}", ha='center', fontsize=7.5)
plt.tight_layout()
plt.savefig("report_assets/fig5_fare_by_airline.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 6: Average fare by departure slot
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=200)
slots = ["Early Morning", "Morning", "Afternoon", "Evening", "Night"]
slot_avg = clean_df.groupby("departure_time")["fare_inr"].mean().reindex(slots)
bars = ax.bar(slot_avg.index, slot_avg.values, color='#26a69a', width=0.6, edgecolor='#00695c', linewidth=0.5)
ax.set_title("Average fare by departure slot", fontsize=10, pad=10)
ax.set_ylabel("Avg fare (INR)")
plt.xticks(rotation=20, ha='right', fontsize=8)
ax.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 200, f"{int(h):,}", ha='center', fontsize=7.5)
plt.tight_layout()
plt.savefig("report_assets/fig6_fare_by_dep.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 7: Correlation matrix of numeric features and fare
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 4.2), dpi=200)
num_cols = ["distance_km", "stops", "days_before_departure", "duration_hours", 
            "seat_availability_pct", "baggage_kg", "airline_rating", "fare_inr"]
corr = clean_df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, 
            cbar=True, square=True, annot_kws={"size": 7}, ax=ax)
ax.set_title("Correlation matrix (numeric features)", fontsize=10, pad=10)
plt.xticks(rotation=45, ha='right', fontsize=7.5)
plt.yticks(rotation=0, fontsize=7.5)
plt.tight_layout()
plt.savefig("report_assets/fig7_corr_matrix.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 8: Booking window vs fare (last-minute spike)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=200)
sample = clean_df.sample(2000, random_state=42)
palette = {"Economy": "#26a69a", "Premium Economy": "#ff7043", "Business": "#2979ff"}
for cls_name, color in palette.items():
    sub = sample[sample["travel_class"] == cls_name]
    ax.scatter(sub["days_before_departure"], sub["fare_inr"], label=cls_name, color=color, alpha=0.55, s=12)
ax.set_title("Booking window vs fare (last-minute spike)", fontsize=10, pad=10)
ax.set_xlabel("days_before_departure")
ax.set_ylabel("fare_inr")
ax.legend(title="travel_class", fontsize=7.5, title_fontsize=8)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("report_assets/fig8_booking_window.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 9: Fare spread by booking window
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3.4), dpi=200)
bins = [0, 3, 7, 14, 30, 60]
labels = ["1-3", "4-7", "8-14", "15-30", "31-60"]
clean_df["window_bin"] = pd.cut(clean_df["days_before_departure"], bins=bins, labels=labels)
sns.boxplot(x="window_bin", y="fare_inr", data=clean_df, palette="YlOrRd", ax=ax, width=0.5, fliersize=2)
ax.set_title("Fare spread by booking window", fontsize=10, pad=10)
ax.set_xlabel("Days before departure")
ax.set_ylabel("fare_inr")
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("report_assets/fig9_fare_spread_box.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 10: Average fare vs route distance
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3.4), dpi=200)
dist_avg = clean_df.groupby("distance_km")["fare_inr"].mean().reset_index().sort_values("distance_km")
ax.plot(dist_avg["distance_km"], dist_avg["fare_inr"], marker='o', color='#1565c0', linewidth=2, markersize=5)
ax.set_title("Average fare vs route distance", fontsize=10, pad=10)
ax.set_xlabel("Distance (km)")
ax.set_ylabel("fare_inr")
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("report_assets/fig10_fare_vs_dist.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Model Training & Comparison (Figure 11, 12, 13)
# -------------------------------------------------------------
X = clean_df.drop(columns=data.NON_FEATURES + ["window_bin"], errors="ignore")
y = clean_df[data.TARGET]
num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()

pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

lr_pipe = Pipeline([("pre", pre), ("model", LinearRegression())]).fit(X_tr, y_tr)
rf_pipe = Pipeline([("pre", pre), ("model", RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1))]).fit(X_tr, y_tr)

lr_pred = lr_pipe.predict(X_te)
rf_pred = rf_pipe.predict(X_te)

metrics = {
    "Model": ["Linear Regression", "Random Forest"],
    "R2": [r2_score(y_te, lr_pred), r2_score(y_te, rf_pred)],
    "RMSE": [float(np.sqrt(mean_squared_error(y_te, lr_pred))), float(np.sqrt(mean_squared_error(y_te, rf_pred)))],
    "MAE": [mean_absolute_error(y_te, lr_pred), mean_absolute_error(y_te, rf_pred)],
}

# -------------------------------------------------------------
# Figure 11: Model comparison
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.2), dpi=200)
models_label = ["Linear Regression", "Random Forest"]

# R2 subplot
ax1.bar(models_label, metrics["R2"], color=['#2979ff', '#ff9800'], width=0.5)
ax1.set_title("R2 (higher is better)", fontsize=9)
ax1.set_ylim(0.7, 1.0)
ax1.set_xticklabels(models_label, rotation=15, fontsize=8)
for i, v in enumerate(metrics["R2"]):
    ax1.text(i, v + 0.01, f"{v:.4f}", ha='center', fontsize=8, weight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Error subplot (RMSE & MAE)
x = np.arange(len(models_label))
width = 0.35
ax2.bar(x - width/2, metrics["RMSE"], width, label='RMSE', color='#ff9800')
ax2.bar(x + width/2, metrics["MAE"], width, label='MAE', color='#2979ff')
ax2.set_title("Error (lower is better)", fontsize=9)
ax2.set_xticks(x)
ax2.set_xticklabels(models_label, rotation=15, fontsize=8)
ax2.legend(fontsize=7.5)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("report_assets/fig11_model_comparison.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 12: Actual vs predicted fare (Random Forest)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 3.8), dpi=200)
ax.scatter(y_te, rf_pred, alpha=0.45, color='#009688', s=12, edgecolors='none')
min_val = min(y_te.min(), rf_pred.min())
max_val = max(y_te.max(), rf_pred.max())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.7, linewidth=1.5, label='Ideal fit')
ax.set_title("Actual vs predicted fare (Random Forest)", fontsize=10, pad=10)
ax.set_xlabel("Actual fare")
ax.set_ylabel("Predicted fare")
ax.legend(fontsize=8)
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("report_assets/fig12_actual_vs_predicted.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Figure 13: Random Forest feature importance (grouped)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=200)
feat_names = rf_pipe.named_steps["pre"].get_feature_names_out()
importances = rf_pipe.named_steps["model"].feature_importances_

# Group one-hot categories back to raw feature categories
group_map = {}
for name, imp in zip(feat_names, importances):
    clean_name = name.replace("num__", "").replace("cat__", "")
    base_feat = clean_name.split("_")[0]
    # Check exact base matches
    for orig in X.columns:
        if clean_name.startswith(orig):
            base_feat = orig
            break
    group_map[base_feat] = group_map.get(base_feat, 0.0) + imp

imp_df = pd.DataFrame(list(group_map.items()), columns=["Feature", "Importance"]).sort_values("Importance", ascending=True)
bars = ax.barh(imp_df["Feature"], imp_df["Importance"], color='#00897b', height=0.65)
ax.set_title("Random Forest feature importance (grouped)", fontsize=10, pad=10)
ax.set_xlabel("Importance")
ax.grid(axis='x', linestyle='--', alpha=0.7)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.01, bar.get_y() + bar.get_height()/2, f"{w:.3f}", va='center', fontsize=7.5)
plt.tight_layout()
plt.savefig("report_assets/fig13_feature_importance.png", dpi=200)
plt.close()

print("All 13 figures generated successfully in report_assets/")
