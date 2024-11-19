import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

# Load the dataset
data = pd.read_csv('./data/prices.csv')
data.columns = data.columns.str.strip()  # Clean column names
data['Date'] = pd.to_datetime(data['Date'])  # Convert date column to datetime

def train_and_save_model(commodity):
    """
    Train and save a model for the given commodity.
    :param commodity: Name of the commodity
    """
    # Filter the data for the specific commodity
    commodity_data = data[data['Commodity'] == commodity]

    if commodity_data.empty:
        raise ValueError(f"No data found for commodity: {commodity}")

    # Sort by date and engineer features
    commodity_data = commodity_data.sort_values('Date')
    commodity_data['Year'] = commodity_data['Date'].dt.year
    commodity_data['Month'] = commodity_data['Date'].dt.month
    commodity_data['Day'] = commodity_data['Date'].dt.day
    commodity_data['DayOfYear'] = commodity_data['Date'].dt.dayofyear
    commodity_data['Month_Sin'] = np.sin(2 * np.pi * commodity_data['Month'] / 12)
    commodity_data['Month_Cos'] = np.cos(2 * np.pi * commodity_data['Month'] / 12)

    # Prepare features and target
    X = commodity_data[['Year', 'Month', 'Day', 'DayOfYear', 'Month_Sin', 'Month_Cos']]
    y = commodity_data['Average']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Gradient Boosting Regressor
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    model_path = f'./models/forecasting_model_{commodity.lower().replace(" ", "_")}.pkl'
    os.makedirs('./models', exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model for {commodity} saved at {model_path}")


def forecast_price(commodity, target_date):
    """
    Predict the price for a specific commodity and date using a trained model.
    :param commodity: Name of the commodity
    :param target_date: Date for which to predict the price
    :return: Predicted price
    """
    # Load the model
    model_path = f'./models/forecasting_model_{commodity.lower().replace(" ", "_")}.pkl'
    if not os.path.exists(model_path):
        train_and_save_model(commodity)

    model = joblib.load(model_path)

    # Prepare input for the target date
    target_date = pd.to_datetime(target_date)
    target_features = {
        'Year': target_date.year,
        'Month': target_date.month,
        'Day': target_date.day,
        'DayOfYear': target_date.timetuple().tm_yday,
        'Month_Sin': np.sin(2 * np.pi * target_date.month / 12),
        'Month_Cos': np.cos(2 * np.pi * target_date.month / 12),
    }
    target_df = pd.DataFrame([target_features])

    # Predict the price
    predicted_price = model.predict(target_df)[0]
    return predicted_price
