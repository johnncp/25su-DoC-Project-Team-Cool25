# Required libraries
import pandas as pd
import numpy as np
import os

os.chdir("/Users/miagiargiari/Desktop/CS Project")
print("Current working directory:", os.getcwd())

df = pd.read_csv("family_employment_data.csv")

df_filtered = df.dropna(subset=[
    "weekly_hours",
    "cash_per_capita",
    "maternity_per_capita",
    "services_per_capita"
])

df_latest = (
    df_filtered.sort_values("year")
    .groupby("country_code", as_index=False)
    .tail(1)
    .reset_index(drop=True)
)

features = ["weekly_hours", "cash_per_capita", "maternity_per_capita", "services_per_capita"]
df_normalized = df_latest.copy()
df_normalized[features] = (df_latest[features] - df_latest[features].min()) / (
        df_latest[features].max() - df_latest[features].min()
)


def recommend_countries(desired_hours_weight, cash_weight, maternity_weight, services_weight):
    weights = np.array([
        desired_hours_weight,
        cash_weight,
        maternity_weight,
        services_weight
    ])

    # normalize the weights
    weights = weights / weights.sum()

    feature_matrix = df_normalized[features].values

    # Score each country
    scores = feature_matrix @ weights

    df_scored = df_normalized.copy()
    df_scored["score"] = scores

    # sort by score descending
    ranked = df_scored.sort_values(by="score", ascending=False)

    return ranked[["Country", "score"] + features], weights


desired_hours_weight = 1
cash_weight = 2
maternity_weight = 3
services_weight = 5

results, normalized_weights = recommend_countries(
    desired_hours_weight=desired_hours_weight,
    cash_weight=cash_weight,
    maternity_weight=maternity_weight,
    services_weight=services_weight
)

print(results.head(10))

user_weights_df = pd.DataFrame({
    "feature": features,
    "user_input_weight": [desired_hours_weight, cash_weight, maternity_weight, services_weight],
    "normalized_weight": normalized_weights
})

results.to_csv("recommended_countries.csv", index=False)
user_weights_df.to_csv("user_input_weights.csv", index=False)
