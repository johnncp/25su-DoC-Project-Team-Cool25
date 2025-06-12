import pandas as pd
import numpy as np
import plotly.express as px
import pycountry

df = pd.read_csv("/Users/miagiargiari/Documents/GitHub/25su-DoC-Project-Team-Cool25/datasets/raw-datasets/family_employment_data.csv")

features = ["weekly_hours", "cash_per_capita", "maternity_per_capita", "services_per_capita"]
df = df.dropna(subset=features)
df_latest = df.sort_values("year").groupby("country_code", as_index=False).tail(1).reset_index(drop=True)
df_latest["year"] = 2023



df_norm = df_latest.copy()
df_norm[features] = (df_latest[features] - df_latest[features].min()) / (
    df_latest[features].max() - df_latest[features].min()
)


def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

df_norm["iso_code"] = df_norm["Country"].apply(get_iso3)
df_norm = df_norm.dropna(subset=["iso_code"])

def normalize_user_input(user_input, max_scale=10):
    return np.array([user_input[feature] / max_scale for feature in features])


def compute_cosine_similarity(user_vec, country_vec):
    dot = np.dot(user_vec, country_vec)
    norm_user = np.linalg.norm(user_vec)
    norm_country = np.linalg.norm(country_vec)
    if norm_user == 0 or norm_country == 0:
        return 0
    return dot / (norm_user * norm_country)


def compute_similarities(user_input_raw):
    user_vec = normalize_user_input(user_input_raw)
    similarities = []

    for _, row in df_norm.iterrows():
        country_vec = row[features].values
        similarity = compute_cosine_similarity(user_vec, country_vec)
        similarities.append(similarity)

    df_norm["similarity"] = similarities
    return df_norm.sort_values("similarity", ascending=False)

user_input = {
    "weekly_hours": 3,
    "cash_per_capita": 6,
    "maternity_per_capita": 8,
    "services_per_capita": 9
}

result_df = compute_similarities(user_input)

fig = px.choropleth(
    result_df,
    locations="iso_code",
    color="similarity",
    hover_name="Country",
    color_continuous_scale="Blues",
    range_color=(0, 1),
    locationmode="ISO-3",
    scope="europe",
    title="Similarity Score by Country (Higher = Better Match)"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()

result_df.to_csv("country_similarity_scores.csv", index=False)
