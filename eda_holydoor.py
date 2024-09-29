import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the preprocessed data
df = pd.read_csv('holydoor_sales_data_cleaned.csv')

# Convert date columns to datetime
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Set up the plotting style
plt.style.use('default')  # Changed from 'seaborn' to 'default'
plt.figure(figsize=(12, 8))

# 1. Total sales over time
df.set_index('start_date')['total_sales'].resample('W').sum().plot()
plt.title('Weekly Total Sales Over Time')
plt.ylabel('Total Sales')
plt.savefig('weekly_total_sales.png')
plt.close()

# 2. Top 10 products by total sales
top_products = df.groupby('product_id')['total_sales'].sum().sort_values(ascending=False).head(10)
top_products.plot(kind='bar')
plt.title('Top 10 Products by Total Sales')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_products.png')
plt.close()

# 3. Sales distribution by color
plt.figure(figsize=(10, 6))
sns.boxplot(x='color', y='total_sales', data=df)
plt.title('Sales Distribution by Color')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('sales_by_color.png')
plt.close()

# 4. Correlation heatmap of numeric columns
numeric_columns = ['100cm', '100cm_glass', '90cm', '90cm_glass', 'child_wing_closed', 'child_wing_open', 'frame', 'trim', 'total_sales']
correlation_matrix = df[numeric_columns].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Numeric Features')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

# 5. Sales by model
model_sales = df.groupby('model')['total_sales'].sum().sort_values(ascending=False)
model_sales.plot(kind='bar')
plt.title('Total Sales by Model')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('sales_by_model.png')
plt.close()

# 6. Monthly sales trend
monthly_sales = df.set_index('start_date')['total_sales'].resample('M').sum()
monthly_sales.plot()
plt.title('Monthly Sales Trend')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('monthly_sales_trend.png')
plt.close()

print("EDA visualizations have been saved as PNG files.")

# Print some additional insights
print("\nAdditional Insights:")
print(f"Total number of sales records: {len(df)}")
print(f"Date range: {df['start_date'].min()} to {df['end_date'].max()}")
print(f"Number of unique products: {df['product_id'].nunique()}")
print(f"Number of unique colors: {df['color'].nunique()}")
print(f"Number of unique models: {df['model'].nunique()}")
print("\nTop 5 selling products:")
print(top_products.head())
print("\nAverage sales by color:")
print(df.groupby('color')['total_sales'].mean().sort_values(ascending=False))