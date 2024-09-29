import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load the preprocessed data
df = pd.read_csv('holydoor_sales_data_cleaned.csv')

# Prepare the data for Prophet
prophet_df = df[['start_date', 'total_sales']].rename(columns={'start_date': 'ds', 'total_sales': 'y'})

# Create and fit the model
model = Prophet()
model.fit(prophet_df)

# Create future dates for prediction
future_dates = model.make_future_dataframe(periods=30)  # Predict for the next 30 days

# Make predictions
forecast = model.predict(future_dates)

# Plot the forecast
fig1 = model.plot(forecast)
plt.title('Sales Forecast')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.savefig('sales_forecast.png')
plt.close()

# Plot the components of the forecast
fig2 = model.plot_components(forecast)
plt.savefig('forecast_components.png')
plt.close()

print("Sales prediction model has been created and visualizations have been saved.")

# Print some basic metrics
print("\nForecast for the next 7 days:")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))