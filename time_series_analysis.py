import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Load the preprocessed data
df = pd.read_csv('holydoor_sales_data_cleaned.csv')

# Convert date columns to datetime
df['start_date'] = pd.to_datetime(df['start_date'])

# Set the date as index
df.set_index('start_date', inplace=True)

# Resample to daily frequency and sum the sales
daily_sales = df['total_sales'].resample('D').sum()

# Plot the daily sales
plt.figure(figsize=(12, 6))
daily_sales.plot()
plt.title('Daily Total Sales')
plt.ylabel('Total Sales')
plt.savefig('daily_total_sales.png')
plt.close()

# Perform seasonal decomposition
decomposition = seasonal_decompose(daily_sales, model='additive', period=7)  # Assuming weekly seasonality

# Plot the decomposition
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
decomposition.observed.plot(ax=ax1)
ax1.set_title('Observed')
decomposition.trend.plot(ax=ax2)
ax2.set_title('Trend')
decomposition.seasonal.plot(ax=ax3)
ax3.set_title('Seasonal')
decomposition.resid.plot(ax=ax4)
ax4.set_title('Residual')
plt.tight_layout()
plt.savefig('seasonal_decomposition.png')
plt.close()

# Plot ACF and PACF
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(daily_sales, ax=ax1)
plot_pacf(daily_sales, ax=ax2)
plt.savefig('acf_pacf_plots.png')
plt.close()

print("Time series analysis visualizations have been saved as PNG files.")

# Print some time series statistics
print("\nTime Series Statistics:")
print(f"Total days: {len(daily_sales)}")
print(f"Mean daily sales: {daily_sales.mean():.2f}")
print(f"Standard deviation of daily sales: {daily_sales.std():.2f}")
print(f"Minimum daily sales: {daily_sales.min():.2f}")
print(f"Maximum daily sales: {daily_sales.max():.2f}")