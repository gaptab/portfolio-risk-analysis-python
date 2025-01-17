# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate dummy portfolio data
portfolio_data = pd.DataFrame({
    "Asset": [f"Asset_{i+1}" for i in range(10)],
    "Sector": np.random.choice(["Technology", "Finance", "Healthcare", "Energy"], size=10),
    "Allocation (%)": np.round(np.random.uniform(5, 20, size=10), 2),
    "Average Return (%)": np.round(np.random.uniform(5, 15, size=10), 2),
    "Volatility (%)": np.round(np.random.uniform(10, 30, size=10), 2),  # Risk metric
    "Correlation with Portfolio": np.round(np.random.uniform(0.5, 1.0, size=10), 2)
})

# Normalize allocations to ensure the sum is 100%
portfolio_data["Allocation (%)"] = (
    portfolio_data["Allocation (%)"] / portfolio_data["Allocation (%)"].sum() * 100
).round(2)

# Display the dataset
print(portfolio_data)

# Calculate Portfolio Expected Return and Risk
portfolio_data["Weighted Return"] = (
    portfolio_data["Allocation (%)"] * portfolio_data["Average Return (%)"] / 100
)
portfolio_data["Weighted Risk"] = (
    portfolio_data["Allocation (%)"] * portfolio_data["Volatility (%)"] / 100
)

# Portfolio-level metrics
portfolio_expected_return = portfolio_data["Weighted Return"].sum()
portfolio_risk = portfolio_data["Weighted Risk"].sum()

print(f"Portfolio Expected Return: {portfolio_expected_return:.2f}%")
print(f"Portfolio Risk: {portfolio_risk:.2f}%")

# Group by sector for risk spread
risk_by_sector = portfolio_data.groupby("Sector").agg({
    "Volatility (%)": "mean",
    "Allocation (%)": "sum"
}).rename(columns={"Volatility (%)": "Avg Volatility", "Allocation (%)": "Total Allocation"})

print(risk_by_sector)

import matplotlib.pyplot as plt
import seaborn as sns

# Portfolio Allocation by Sector
plt.figure(figsize=(8, 5))
sns.barplot(data=portfolio_data, x="Sector", y="Allocation (%)", errorbar=None, palette="Set2")
plt.title("Portfolio Allocation by Sector")
plt.ylabel("Allocation (%)")
plt.xlabel("Sector")
plt.show()

# Volatility Distribution
plt.figure(figsize=(8, 5))
sns.boxplot(data=portfolio_data, x="Sector", y="Volatility (%)", palette="Set3")
plt.title("Volatility Distribution by Sector")
plt.ylabel("Volatility (%)")
plt.xlabel("Sector")
plt.show()

# Assets with volatility above 25%
high_risk_assets = portfolio_data[portfolio_data["Volatility (%)"] > 25]
print("High-Risk Assets:")
print(high_risk_assets)

# Correlation-weighted risk
portfolio_data["Correlation-Weighted Risk"] = (
    portfolio_data["Volatility (%)"] * portfolio_data["Correlation with Portfolio"]
)

# Display correlation-weighted risk
print(portfolio_data[["Asset", "Correlation-Weighted Risk"]])

# Save portfolio data and risk-by-sector report
portfolio_data.to_csv("portfolio_data.csv", index=False)
risk_by_sector.to_csv("risk_by_sector.csv", index=True)

print("Portfolio data and risk reports saved as CSV files.")
