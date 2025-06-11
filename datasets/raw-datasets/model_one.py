import pandas as pd
import numpy as np

# get data
def load_data():
    df = pd.read_csv("Model_data.csv")
    df = df.dropna(subset=[
        'birth_rate_per_thousand', 'weekly_hours',
        'cash_per_capita', 'maternity_per_capita',
        'services_per_capita', 'year'
    ]).copy()

    df['weekly_hours_squared'] = df['weekly_hours'] ** 2
    df['cash_per_capita_squared'] = df['cash_per_capita'] ** 2
    df['services_per_capita_squared'] = df['services_per_capita'] ** 2

    return df

# get features
def get_features():
    features = [
        'weekly_hours', 'maternity_per_capita', 'services_per_capita', 'year',
        'weekly_hours_squared', 'cash_per_capita_squared', 'services_per_capita_squared'
    ]
    target = 'birth_rate_per_thousand'
    return features, target

# train-test split data (80/20)
def split_data(X, y):
    np.random.seed(42)
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    split = int(0.2 * len(X))
    test_idx = indices[:split]
    train_idx = indices[split:]
    return X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]

# standardizes features (subtract by mean and divide by standard dev)
def standardize(X_train, X_test):
    mean = X_train.mean()
    std = X_train.std().replace(0, 1)
    X_train_std = (X_train - mean) / std
    X_test_std = (X_test - mean) / std
    return X_train_std, X_test_std, mean, std

# trains model
def train_model(X_train_std, y_train):
    X_design_train = np.c_[np.ones(X_train_std.shape[0]), X_train_std]
    beta = np.linalg.inv(X_design_train.T @ X_design_train) @ (X_design_train.T @ y_train)
    return beta

# predicts and evaluates
def evaluate_model(X_test_std, y_test, beta):
    X_design_test = np.c_[np.ones(X_test_std.shape[0]), X_test_std]
    y_pred = X_design_test @ beta

    residuals = y_test - y_pred
    mae = np.mean(np.abs(residuals))
    mse = np.mean(residuals**2)
    rmse = np.sqrt(mse)
    r2 = 1 - np.sum(residuals**2) / np.sum((y_test - np.mean(y_test))**2)

    print("\n--- Evaluation on Test Set ---")
    print(f"MAE:  {mae:.4f}")
    print(f"MSE:  {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²:   {r2:.4f}")
    return r2

# testing prediction
def predict_example(country_input, features, mean, std, beta):
    country_input['weekly_hours_squared'] = country_input['weekly_hours'] ** 2
    country_input['cash_per_capita_squared'] = country_input['cash_per_capita'] ** 2
    country_input['services_per_capita_squared'] = country_input['services_per_capita'] ** 2

    example_df = pd.DataFrame([country_input])
    example_std = (example_df[features] - mean) / std
    y_example_pred = np.c_[np.ones(1), example_std] @ beta

    print("\n--- Example ---")
    print(f"Predicted birth rate for Country Y: {y_example_pred[0]:.2f}")
    return y_example_pred[0]

# pipeline to run all
def run_pipeline(country_input):
    df = load_data()
    features, target = get_features()
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_std, X_test_std, mean, std = standardize(X_train, X_test)
    beta = train_model(X_train_std, y_train)
    r2 = evaluate_model(X_test_std, y_test, beta)
    predicted = predict_example(country_input, features, mean, std, beta)
    return predicted, r2, beta, mean, std, features


if __name__ == "__main__":
    country_Y = {
        'weekly_hours': 35.5,
        'maternity_per_capita': 700,
        'services_per_capita': 16000,
        'cash_per_capita': 20000,
        'year': 2024
    }

    run_pipeline(country_Y)
