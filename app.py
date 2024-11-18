import streamlit as st
import pandas as pd
from models.optimization import optimize_daily_prices


# Load initial data
data = pd.read_csv("data/Updated_Market_Data.csv")

# Global variables for storing results
daily_optimized_prices = []
expected_profit = 0.0

# Streamlit app
st.set_page_config(page_title="Daily Price Optimization Dashboard", layout="wide")

# Dashboard Title
st.title("Daily Price Optimization Dashboard")

# Form for product details
with st.form("optimization_form"):
    st.header("Enter Product Details")
    product_name = st.text_input("Product Name", placeholder="Enter product name", key="product_name")
    quantity = st.number_input("Quantity (kg)", min_value=0.0, step=0.1, key="quantity")
    competitor_price = st.number_input("Competitor Price (optional)", min_value=0.0, step=0.1, key="competitor_price")
    submit_button = st.form_submit_button(label="Optimize Price")

# Handle form submission
if submit_button:
    try:
        st.write("Processing optimization...")
        # Prepare inputs
        inputs = {
            "product_names": [product_name],
            "quantities": [quantity],
            "competitor_prices": [competitor_price]
        }
        
        # Call the optimization function
        daily_optimized_prices, expected_profit = optimize_daily_prices(data, inputs)
        st.success("Optimization successful!")

    except Exception as e:
        st.error(f"Error during optimization: {str(e)}")

# Display optimized results
if daily_optimized_prices:
    st.header("Optimized Prices for the Day")
    column_mapping = {
    "name": "Product Name",
    "price": "Optimized Price",
    "inventory": "Inventory (kg)"
    }
    df = pd.DataFrame(daily_optimized_prices).rename(columns=column_mapping)
    st.table(df)
    st.subheader(f"Expected Profit for the Day: ${expected_profit:.2f}")
else:
    st.info("No results to display. Please submit product details to optimize prices.")

# Append results to a local CSV
if daily_optimized_prices:
    historical_data = pd.DataFrame(daily_optimized_prices)
    historical_data["expected_profit"] = expected_profit
    historical_data.to_csv("historical_optimizations.csv", mode="a", header=False, index=False)

# Display historical data
if st.sidebar.button("View Historical Data"):
    # Read the historical data
    history = pd.read_csv("historical_optimizations.csv")
    # Rename the columns before displaying the DataFrame
    history.columns = ["Product Name", "Optimized Price", "Inventory (kg)", "Profit for the Day"]
    # Display the historical data
    st.subheader("Historical Data")
    st.dataframe(history)

csv = pd.DataFrame(daily_optimized_prices).to_csv(index=False)
if st.sidebar.download_button(label="Download Optimized Prices", data=csv, file_name="optimized_prices.csv", mime="text/csv"):
    if daily_optimized_prices:
        csv = pd.DataFrame(daily_optimized_prices).to_csv(index=False)
        st.download_button(
            label="Download Optimized Prices",
            data=csv,
            file_name="optimized_prices.csv",
            mime="text/csv",
        )

if st.sidebar.checkbox("Batch Optimization"):
    product_details = st.file_uploader("Upload Product Details CSV (name, quantity, competitor_price)", type=["csv"])
    if product_details:
        batch_data = pd.read_csv(product_details)
        batch_results, batch_profit = optimize_daily_prices(data, batch_data)
        st.table(batch_results)
        st.subheader(f"Expected Total Profit: ${batch_profit:.2f}")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")


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


#import openai
#if st.sidebar.button("Ask the Assistant"):
    # openai.api_key = "api-key"

    # def ai_assistant_query(prompt):
    #     # Create a conversation with the new API interface
    #     response = openai.Completion.create(
    #         model="gpt-4",  # Specify the model to use
    #         prompt=prompt,  # Provide the user's prompt
    #         max_tokens=150  # Limit the response length
    #     )
    #     return response.choices[0].text.strip()  # Get the content of the AI response

    # # Streamlit interface
    # query = st.text_area("Ask the Assistant")
    # if st.button("Get Advice"):
    #     response = ai_assistant_query(query)
    #     st.write(response)





