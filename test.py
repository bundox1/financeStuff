from yahooquery import Ticker
import pandas as pd


current_ratio_threshold = 3
interest_coverage_ratio_threshold = 4
roa_threshold = 0.05  # Minimum Return on Assets (ROA)
roe_threshold = 0.1  # Minimum Return on Equity (ROE)

all_tickers = pd.read_csv('all_tickers.csv')['Symbol'].tolist()  # Replace with the path to the CSV file containing all tickers

filtered_tickers = []

for ticker in all_tickers:
    try:
        financials = Ticker(ticker).balance_sheet(frequency='q').iloc[:, -1].dropna()

        current_assets = financials.loc['totalCurrentAssets']
        current_liabilities = financials.loc['totalCurrentLiabilities']
        current_ratio = current_assets / current_liabilities

        operating_income = Ticker(ticker).income_statement(frequency='q').iloc[:, -1].dropna().loc['operatingIncome']
        interest_expense = financials.loc['interestExpense']
        interest_coverage_ratio = operating_income / interest_expense

        net_income = Ticker(ticker).income_statement(frequency='q').iloc[:, -1].dropna().loc['netIncome']
        total_assets = financials.loc['totalAssets']
        roa = net_income / total_assets

        total_equity = financials.loc['totalStockholderEquity']
        roe = net_income / total_equity

        if (current_ratio > current_ratio_threshold) and (interest_coverage_ratio > interest_coverage_ratio_threshold) and \
                (roa > roa_threshold) and (roe > roe_threshold):
            filtered_tickers.append(ticker)

        if len(filtered_tickers) == 10:
            break

    except Exception as e:
        print(f"Error occurred while processing ticker {ticker}: {str(e)}")

selected_sector = "Consumer Staples"  # Replace with your preferred sector

# Filter the tickers by the selected sector
sector_tickers = []

for ticker in filtered_tickers:
    sector = Ticker(ticker).asset_profile['sector']
    if sector == selected_sector:
        sector_tickers.append(ticker)

weights = [1 / len(sector_tickers)] * len(sector_tickers)

# Perform portfolio volatility adjustment to target 10% annually
# You can use any portfolio optimization method of your choice (e.g., mean-variance optimization)

# Adjust the weights based on your portfolio optimization method

# Finalize the tickers based on the adjusted weights
final_tickers = [ticker for i, ticker in enumerate(sector_tickers) if weights[i] > 0]
