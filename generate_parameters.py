import numpy as np
import random

def generate_random_parameters():
    """
    Generate random values for the optimization parameters.
    These parameters simulate external factors affecting pricing decisions.
    
    :return: A dictionary with randomized parameters.
    """
    parameters = {
        # Simulated demand (randomly chosen within a reasonable range)
        "demand": np.random.uniform(100, 1000),  # Adjust range as needed
        
        # Simulated supply (randomly chosen within a reasonable range)
        "supply": np.random.uniform(50, 500),  # Adjust range as needed
        
        # Weather impact factor (adjusts the price based on weather conditions)
        # A factor > 1 indicates favorable weather; < 1 indicates unfavorable weather
        "weather_impact": np.random.uniform(0.8, 1.2),
        
        # Festival boost (multiplier for higher demand during festivals)
        # 1 means no festival, >1 means there's a festival
        "festival_boost": random.choice([1, 1.1, 1.2]),
        
        # Competitor price sensitivity (how much competitor pricing affects demand)
        "competitor_price_sensitivity": np.random.uniform(0.5, 1.5),  # Sensitivity to competitor prices
        
        # Seasonal multiplier (higher values for in-season products)
        "seasonal_multiplier": np.random.uniform(0.9, 1.3),
    }
    return parameters


# Example usage
if __name__ == "__main__":
    params = generate_random_parameters()
    print("Generated Parameters:")
    for key, value in params.items():
        print(f"{key}: {value:.2f}")
