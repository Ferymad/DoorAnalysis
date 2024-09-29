import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('holydoor_sales_data_cleaned.csv')
    df['start_date'] = pd.to_datetime(df['start_date'])
    return df

# Load the prediction model
@st.cache_resource
def load_model():
    df = load_data()
    prophet_df = df[['start_date', 'total_sales']].rename(columns={'start_date': 'ds', 'total_sales': 'y'})
    model = Prophet()
    model.fit(prophet_df)
    return model

# Main function to run the Streamlit app
def main():
    st.title('HolyDoor Sales Prediction and Inventory Tracker')

    # Load data and model
    df = load_data()
    model = load_model()

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Overview", "Sales Prediction", "Inventory"])

    if page == "Overview":
        st.header("Overview")
        st.write(f"Total number of sales records: {len(df)}")
        st.write(f"Date range: {df['start_date'].min()} to {df['end_date'].max()}")
        st.write(f"Number of unique products: {df['product_id'].nunique()}")

        # Display top selling products
        st.subheader("Top 5 Selling Products")
        top_products = df.groupby('product_id')['total_sales'].sum().sort_values(ascending=False).head()
        st.bar_chart(top_products)

    elif page == "Sales Prediction":
        st.header("Sales Prediction")
        
        # Create future dates for prediction
        future_days = st.slider("Select number of days to forecast", 1, 90, 30)
        future_dates = model.make_future_dataframe(periods=future_days)

        # Make predictions
        forecast = model.predict(future_dates)

        # Plot the forecast
        fig = model.plot(forecast)
        st.pyplot(fig)

        # Display forecast data
        st.subheader(f"Forecast for the next {future_days} days:")
        st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(future_days))

    elif page == "Inventory":
        st.header("Current Inventory")
        
        # Group by product and sum the total sales
        inventory = df.groupby('product_id')['total_sales'].sum().sort_values(ascending=False)
        
        # Display inventory as a table
        st.dataframe(inventory.reset_index().rename(columns={'product_id': 'Product', 'total_sales': 'Total Sales'}))

        # Display inventory as a bar chart
        st.bar_chart(inventory)

if __name__ == "__main__":
    main()