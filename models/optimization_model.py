import numpy as np
from generate_parameters import generate_random_parameters
from price_forecasting import forecast_price
from datetime import datetime
from scipy.optimize import minimize

def optimize_price(commodity, quantity, competitor_price=None):
    """
    Optimize the price for a given commodity based on various dynamic factors.
    
    :param commodity: Name of the commodity.
    :param quantity: Quantity available for the commodity.
    :param competitor_price: Optional competitor price.
    :return: Optimized price, estimated profit, and parameters used.
    """
    def objective(price):
        """
        Objective function to maximize profit or revenue.
        :param price: Price to evaluate.
        :return: Negative of profit/revenue for minimization.
        """
        # Adjust demand based on price, inventory, and competitor price (if provided)
        demand = params["demand"]
        if competitor_price:
            demand *= (1 - params["competitor_price_sensitivity"] * abs(price - competitor_price) / max(price, competitor_price))

        # Demand decreases with higher prices, increases with lower prices
        demand *= (1 - 0.01 * (price - base_price))

        # Ensure demand does not exceed available quantity
        effective_demand = max(0, min(demand, quantity))

        # Calculate profit
        profit = (price - 0.7 * base_price) * effective_demand

        return -profit  # Negate for minimization

    # Get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Forecast the base price using the forecasting model
    try:
        base_price = forecast_price(commodity, today_date)
    except Exception as e:
        print(f"Error in forecasting model: {e}")
        return None, None, None

    # Generate dynamic parameters for optimization
    params = generate_random_parameters()

    # Adjust price dynamically based on parameters
    price = base_price
    price *= params["weather_impact"]  # Weather impact multiplier
    price *= params["festival_boost"]  # Festival demand boost
    price *= params["seasonal_multiplier"]  # Seasonal effect multiplier

    # Competitor price adjustment (if provided)
    if competitor_price:
        competitor_factor = params["competitor_price_sensitivity"]
        price = (price + competitor_price * competitor_factor) / (1 + competitor_factor)

    # Simulate demand based on quantity and price
    demand = params["demand"] - params["supply"] * (price / base_price)
    demand = max(0, min(demand, quantity))  # Ensure demand is non-negative and within available quantity

    price_bounds = [(0.5 * base_price, 2 * base_price)]
    result = minimize(
        objective,
        x0=[base_price],  # Start with the base price
        bounds=price_bounds,
        method="L-BFGS-B"
    )

    # Extract optimized price and calculate final profit/revenue
    optimized_price = result.x[0]
    final_profit = -objective(optimized_price)

    # Estimate profit
    cost_price = 0.7 * base_price  # Assume cost price is 70% of base price
    profit = (price - cost_price) * demand  # Profit calculation based on sold quantity

    return round(price, 2), round(profit, 2), params
