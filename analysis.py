import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("Retail_Sales.csv", encoding="latin1")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. CONVERT DATES
# ==========================================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("\nDates converted successfully!")


# ==========================================
# 3. CHECK MISSING VALUES
# ==========================================

print("\nMISSING VALUES:")
print(df.isnull().sum())


# ==========================================
# 4. CHECK DUPLICATES
# ==========================================

print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())


# ==========================================
# 5. BASIC STATISTICS
# ==========================================

print("\nBASIC STATISTICS:")
print(df.describe())


# ==========================================
# 6. CHECK CATEGORIES
# ==========================================

print("\nCATEGORIES:")
print(df["Category"].unique())

print("\nREGIONS:")
print(df["Region"].unique())

print("\nCUSTOMER SEGMENTS:")
print(df["Segment"].unique())


# ==========================================
# 7. CREATE YEAR AND MONTH COLUMNS
# ==========================================

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.month_name()


# ==========================================
# 8. FINAL DATASET INFORMATION
# ==========================================

print("\nFINAL DATASET INFORMATION:")
print(df.info())

print("\nDATA CLEANING COMPLETE!")
# ==========================================
# 9. KEY BUSINESS KPIs
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
average_order_value = total_sales / total_orders

print("\n==========================================")
print("           KEY BUSINESS KPIs")
print("==========================================")

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")

print("==========================================") 
# ==========================================
# 10. SALES VS PROFIT CHART
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

metrics = ["Sales", "Profit"]
values = [total_sales, total_profit]

plt.figure(figsize=(8, 5))

plt.bar(metrics, values)

plt.title("Sales vs Profit")
plt.xlabel("Metric")
plt.ylabel("Amount ($)")

# Add values on top of bars
for i, value in enumerate(values):
    plt.text(i, value, f"${value:,.0f}", ha="center", va="bottom")

plt.tight_layout()

# Save the chart
plt.savefig("sales_vs_profit.png", dpi=300, bbox_inches="tight")

# Display the chart
plt.show()
# ==========================================
# 11. SALES BY REGION
# ==========================================

region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

print("\nSALES BY REGION:")
print(region_sales)


# Create chart
plt.figure(figsize=(9, 5))

region_sales.plot(kind="bar")

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=0)

# Add values above bars
for i, value in enumerate(region_sales):
    plt.text(i, value, f"${value:,.0f}", ha="center", va="bottom")

plt.tight_layout()

# Save chart
plt.savefig("sales_by_region.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show() 
# ==========================================
# 12. SALES BY CATEGORY
# ==========================================

category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

print("\nSALES BY CATEGORY:")
print(category_sales)


# Create chart
plt.figure(figsize=(8, 5))

category_sales.plot(kind="bar")

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=0)

# Add values above bars
for i, value in enumerate(category_sales):
    plt.text(i, value, f"${value:,.0f}", ha="center", va="bottom")

plt.tight_layout()

# Save chart
plt.savefig("sales_by_category.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 13. PROFIT BY CATEGORY
# ==========================================

category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

print("\nPROFIT BY CATEGORY:")
print(category_profit)


# Create chart
plt.figure(figsize=(8, 5))

category_profit.plot(kind="bar")

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Profit ($)")
plt.xticks(rotation=0)

# Add values above bars
for i, value in enumerate(category_profit):
    plt.text(i, value, f"${value:,.0f}", ha="center", va="bottom")

plt.tight_layout()

# Save chart
plt.savefig("profit_by_category.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 14. SALES BY CUSTOMER SEGMENT
# ==========================================

segment_sales = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)

print("\nSALES BY CUSTOMER SEGMENT:")
print(segment_sales)


# Create chart
plt.figure(figsize=(8, 5))

segment_sales.plot(kind="bar")

plt.title("Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=0)

# Add values above bars
for i, value in enumerate(segment_sales):
    plt.text(i, value, f"${value:,.0f}", ha="center", va="bottom")

plt.tight_layout()

# Save chart
plt.savefig("sales_by_segment.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 15. MONTHLY SALES TREND
# ==========================================

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

print("\nMONTHLY SALES:")
print(monthly_sales)


# Create chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")

# Rotate month labels
plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

# Save chart
plt.savefig("monthly_sales_trend.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 16. TOP 10 PRODUCTS BY SALES
# ==========================================

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTS BY SALES:")
print(top_products)


# Create chart
plt.figure(figsize=(10, 6))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Product")

# Add values
for i, value in enumerate(top_products.sort_values()):
    plt.text(value, i, f" ${value:,.0f}", va="center")

plt.tight_layout()

# Save chart
plt.savefig("top_10_products.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 17. TOP 10 PRODUCTS BY PROFIT
# ==========================================

top_profit_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTS BY PROFIT:")
print(top_profit_products)


# Create chart
plt.figure(figsize=(10, 6))

top_profit_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Profit")
plt.xlabel("Total Profit ($)")
plt.ylabel("Product")

# Add values
for i, value in enumerate(top_profit_products.sort_values()):
    plt.text(value, i, f" ${value:,.0f}", va="center")

plt.tight_layout()

# Save chart
plt.savefig("top_10_products_by_profit.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()
# ==========================================
# 18. DISCOUNT VS PROFIT
# ==========================================

discount_profit = (
    df.groupby("Discount")["Profit"]
    .mean()
    .sort_index()
)

print("\nAVERAGE PROFIT BY DISCOUNT:")
print(discount_profit)


# Create chart
plt.figure(figsize=(10, 6))

plt.plot(
    discount_profit.index * 100,
    discount_profit.values,
    marker="o"
)

plt.title("Discount vs Average Profit")
plt.xlabel("Discount (%)")
plt.ylabel("Average Profit ($)")

plt.grid(True)

plt.tight_layout()

# Save chart
plt.savefig("discount_vs_profit.png", dpi=300, bbox_inches="tight")

# Display chart
plt.show()