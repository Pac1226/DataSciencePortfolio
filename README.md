# DataSciencePortfolio

A collection of selected data science projects to demonstrate programming skills, knowledge of tools, and the ability to solve business problems.

---

## Contents

- **PythonOOP:** A modular FinTech loan-qualifier application that serves as an example of object oriented programming in Python3.
- **SQL:** Examples of executing and formulating SQL queries on simulated financial problems.
- **Prophet:** Timeseries analysis and sales forecasting case study for an eCommerce company that uses Prophet.
- **Unsupervised Learning:** Clustering cryptocurrencies using K-means algorithm and Principal Component Analysis (PCA).
- **Supervised Learning:** Clean, resuable code that leverages machine learning algorithms for algorithmic trading and credit risk analysis.
- **GeoMapping:** Analysis of US housing data that demonstrates proficiency with geospatial analysis and the MapBox API.

---

## Results

The algorithmic trading model was backtested with 25 stocks and outperformed a buy/hold strategy by 141%. It produced an average return of 41% across the 25 stocks over a one year period. A buy/hold strategy would've returned -12%. The algorithm performs better with high beta stocks and underperforms with energy stocks.

The algorithm bought a stock when its price dropped below the long-term trendline and sold it when the price rose above it. The buy/sell signals can be changed to optimize returns. For example, the buy signal can be set to "2 Standard Deviations (Below)" the mean and the sell signal to "1 Standard Deviation (Above)" the mean.

Returns were optimized by applying the Logistic Regression, Random Forest Classification, and Support Vector Machine algorithms. They all failed to outpeform the human-designed trading bot, but often outperformed the buy/hold strategy.

The following results are from 05/01/21 to 05/16/22.

![Stock Performance](images/stock_performance.png)

![Sector Performance](images/sector_performance.png)
