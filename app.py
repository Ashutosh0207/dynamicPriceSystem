import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.optimization_model import optimize_price
from price_forecasting import forecast_price

# Streamlit app
st.set_page_config(page_title="Daily Price Optimization Dashboard", layout="wide")

# Dashboard Title
st.title("Daily Price Optimization Dashboard")

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
    st.subheader("Optimize Your Prices")
    st.write("Enter details of the vegetables you want to sell:")

    # Inputs
    vegetable = st.selectbox("Select Vegetable:", commodities)
    quantity = st.number_input("Quantity (kg):", min_value=1, value=10)
    competitor_price = st.number_input("Competitor Price (optional):", min_value=0.0, value=0.0)

    # Add data to table
    if st.button("Optimize Price"):
        st.write("Processing optimization...")
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

            st.success("Optimization successful!")
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
    st.subheader("Trends and Forecasting")

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

# Download Optimized Prices as CSV
if st.session_state["data_table"]:
    csv = pd.DataFrame(st.session_state["data_table"]).to_csv(index=False)
    st.sidebar.download_button(
        label="Download Optimized Prices",
        data=csv,
        file_name="optimized_prices.csv",
        mime="text/csv"
    )

# Append results to a local CSV file
if st.session_state["data_table"]:
    try:
        historical_data = pd.DataFrame(st.session_state["data_table"])
        historical_data.to_csv("historical_optimizations.csv", mode="a", header=False, index=False)
    except Exception as e:
        st.error(f"Error saving historical data: {e}")

# View Historical Data
if st.sidebar.button("View Historical Data"):
    try:
        # Read and display historical data
        history = pd.read_csv("historical_optimizations.csv", header=None)
        history.columns = ["Vegetable", "Quantity (kg)", "Competitor Price", "Optimized Price", "Profit (₹)"]
        
        st.subheader("Historical Data")
        st.dataframe(history)
    except Exception as e:
        st.error(f"Error loading historical data: {e}")

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

feedback = st.text_area("Share your feedback or suggestions")
# Submit button to save feedback
if st.button("Submit Feedback"):
    if feedback.strip():  # Check if feedback is not empty
        try:
            # Append feedback to the file
            with open("feedback.txt", "a") as f:
                 f.write(feedback + "\n")
            st.success("Thank you for your feedback!")
        except Exception as e:
            # Handle any errors during file writing
            st.error(f"An error occurred while saving feedback: {e}")
    else:
        st.warning("Please enter your feedback before submitting.")

# # Batch Optimization
# if st.sidebar.checkbox("Batch Optimization"):
#     st.subheader("Batch Optimization")
#     product_details = st.file_uploader("Upload Product Details CSV (name, quantity, competitor_price)", type=["csv"])

#     if product_details:
#         try:
#             # Load batch data
#             batch_data = pd.read_csv(product_details)

#             # Add new columns to batch_data for optimized price and profit
#             batch_data["Optimized Price"] = None
#             batch_data["Profit (₹)"] = None

#             # Initialize total profit if it doesn't exist in session state
#             if "total_profit" not in st.session_state:
#                 st.session_state["total_profit"] = 0

#             # Process each row in the uploaded file
#             for index, row in batch_data.iterrows():
#                 vegetable = row.get("name", "")
#                 quantity = row.get("quantity", 0)
#                 competitor_price = row.get("competitor_price", 0)

#                 if vegetable and quantity > 0:
#                     # Optimize prices using existing function
#                     optimized_price, profit, parameters = optimize_price(vegetable, quantity, competitor_price)

#                     # Update the DataFrame with results
#                     batch_data.loc[index, "Optimized Price"] = optimized_price
#                     batch_data.loc[index, "Profit (₹)"] = profit if profit else 0

#                     # Add results to session state table
#                     st.session_state["data_table"].append({
#                         "Vegetable": vegetable,
#                         "Quantity (kg)": quantity,
#                         "Competitor Price": competitor_price,
#                         "Optimized Price": optimized_price,
#                         "Profit (₹)": profit
#                     })

#                     # Ensure profit is not None and update total profit
#                     if profit is None:
#                         profit = 0
#                     st.session_state["total_profit"] += profit

#                     # Store parameters for display
#                     st.session_state["last_parameters"] = parameters

#             # Display the updated DataFrame with results
#             st.subheader("Batch Optimization Results")
#             st.table(batch_data)

#             # Display total profit
#             st.subheader(f"Expected Total Profit: ₹{st.session_state['total_profit']:.2f}")

#             st.success("Optimization successful!")

#         except Exception as e:
#             st.error(f"Error during batch optimization: {e}")
