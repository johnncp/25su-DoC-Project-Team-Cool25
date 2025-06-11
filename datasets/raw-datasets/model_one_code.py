## ORGANIZED INTO FUNCTIONS
import pandas as pd
import numpy as np


# training
def train_model(df):
    # drop rows w missing
    required_cols = [
        'birth_rate_per_thousand', 'weekly_hours',
        'cash_per_capita', 'maternity_per_capita', 'services_per_capita'
    ]
    df = df.dropna(subset=required_cols).copy()

    # add the squared/cubed
    df['weekly_hours_squared'] = df['weekly_hours'] ** 2
    df['weekly_hours_cubed'] = df['weekly_hours'] ** 3
    df['cash_per_capita_squared'] = df['cash_per_capita'] ** 2
    df['services_per_capita_squared'] = df['services_per_capita'] ** 2

    # features + target
    features = [
        'weekly_hours', 'cash_per_capita', 'maternity_per_capita', 'services_per_capita',
        'weekly_hours_squared', 'weekly_hours_cubed',
        'cash_per_capita_squared', 'services_per_capita_squared'
    ]
    X_raw = df[features].values
    Y = df['birth_rate_per_thousand'].values

    # standardize
    X_mean = X_raw.mean(axis=0)
    X_std = X_raw.std(axis=0)
    X_std[X_std == 0] = 1  # avoid division by zero
    X_standardized = (X_raw - X_mean) / X_std
    X_design = np.c_[np.ones(X_standardized.shape[0]), X_standardized]

    # train using normal equation
    beta = np.linalg.inv(X_design.T @ X_design) @ (X_design.T @ Y)

    # evaluate
    predictions = X_design @ beta
    mae = np.mean(np.abs(Y - predictions))
    r2 = 1 - np.sum((Y - predictions)**2) / np.sum((Y - np.mean(Y))**2)

    print("Model Evaluation:")
    print(f"MAE: {mae:}")
    print(f"R²:  {r2:}")

    # Print coefficients
    print("\nModel Coefficients:")
    feature_names = ['intercept'] + features
    for name, b in zip(feature_names, beta):
        print(f"{name:} {b:}")

    return beta, X_mean, X_std, features


# PREDICT
def predict_birth_rate(user_input: dict, beta, X_mean, X_std, features):
    # Build feature vector with squares and cubes
    user_df = pd.DataFrame([user_input])
    user_df['weekly_hours_squared'] = user_df['weekly_hours'] ** 2
    user_df['weekly_hours_cubed'] = user_df['weekly_hours'] ** 3
    user_df['cash_per_capita_squared'] = user_df['cash_per_capita'] ** 2
    user_df['services_per_capita_squared'] = user_df['services_per_capita'] ** 2

    # standardize
    X_input = user_df[features].values
    X_std_input = (X_input - X_mean) / X_std

    X_input_design = np.c_[np.ones((1,)), X_std_input]

    #
    return (X_input_design @ beta)[0]


