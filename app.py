import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.optimization_model import optimize_price
from price_forecasting import forecast_price

# Load data
data = pd.read_csv('./data/prices.csv')
data['Date'] = pd.to_datetime(data['Date'])  # Ensure the date is in datetime format

# Get unique commodities
commodities = data['Commodity'].unique()

# Initialize session state for Section 1 table
if "data_table" not in st.session_state:
    st.session_state["data_table"] = []
if "total_profit" not in st.session_state:
    st.session_state["total_profit"] = 0
if "last_parameters" not in st.session_state:
    st.session_state["last_parameters"] = None

# Sidebar
st.sidebar.title("Vegetable Optimization and Trends")
section = st.sidebar.radio("Select a Section", ["Optimize Prices", "Trends and Forecasting"])

# Section 1: Optimize Prices
if section == "Optimize Prices":
    st.title("Optimize Your Prices")
    st.write("Enter details of the vegetables you want to sell:")

    # Inputs
    vegetable = st.selectbox("Select Vegetable:", commodities)
    quantity = st.number_input("Quantity (kg):", min_value=1, value=10)
    competitor_price = st.number_input("Competitor Price (optional):", min_value=0.0, value=0.0)

    # Add data to table
    if st.button("Optimize Price"):
        try:
            optimized_price, profit, parameters = optimize_price(vegetable, quantity, competitor_price)
            st.session_state["data_table"].append({
                "Vegetable": vegetable,
                "Quantity (kg)": quantity,
                "Competitor Price": competitor_price,
                "Optimized Price": optimized_price,
                "Profit (₹)": profit
            })
            st.session_state["total_profit"] += profit
            st.session_state["last_parameters"] = parameters  # Store parameters for display
        except Exception as e:
            st.error(f"Error: {e}")

    # Display Table
    if st.session_state["data_table"]:
        st.subheader("Optimized Pricing Table")
        st.write(pd.DataFrame(st.session_state["data_table"]))

        # Total Profit
        st.success(f"Total Estimated Profit: ₹{st.session_state['total_profit']:.2f}")

    # Display Last Parameters
    if st.session_state["last_parameters"]:
        st.subheader("Parameters Used in the Last Optimization")
        st.json(st.session_state["last_parameters"])

# Section 2: Trends and Forecasting
elif section == "Trends and Forecasting":
    st.title("Trends and Forecasting")

    # Dropdown to select vegetable
    selected_vegetable = st.selectbox("Select a vegetable:", commodities)

    # Display trends
    st.subheader(f"Historical Trends for {selected_vegetable}")
    # Filter data for the selected vegetable
    commodity_data = data[data['Commodity'] == selected_vegetable].sort_values('Date')

    # Line Plot
    plt.figure(figsize=(10, 5))
    plt.plot(commodity_data['Date'], commodity_data['Average'], label="Price", marker="o")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Price Trends for {selected_vegetable}")
    plt.legend()
    st.pyplot(plt)

    # Display Descriptive Stats
    st.subheader("Descriptive Statistics")
    st.write(commodity_data['Average'].describe())

    # Forecast Future Price
    st.subheader("Price Forecasting")
    target_date = st.date_input("Select a future date:")
    if st.button("Forecast Price"):
        try:
            predicted_price = forecast_price(selected_vegetable, target_date)
            st.success(f"Predicted price for {selected_vegetable} on {target_date}: ₹{predicted_price:.2f}")
        except Exception as e:
            st.error(f"Error: {e}")