from yahoo_fin import options
from yahoo_fin import stock_info
import pandas as pd


def compute_filter_option_chain(stock_ticker, expiration_date_choice):
  # Retrieve options chain data for calls of the given stock ticker
    options_chain_df = options.get_calls(stock_ticker, expiration_date_choice)
    
    # Retrieve the live price of the stock
    current_stock_price = stock_info.get_live_price(stock_ticker)
    print("(filteroption.py) Current stock price is {}".format(current_stock_price))

    # Data preprocessing
    options_chain_df["Last Price"] = pd.to_numeric(options_chain_df["Last Price"], errors='coerce')
    options_chain_df["Strike"] = pd.to_numeric(options_chain_df["Strike"], errors='coerce')
    options_chain_df["Volume"] = pd.to_numeric(options_chain_df["Volume"], errors='coerce')
    options_chain_df['Implied Volatility'] = options_chain_df['Implied Volatility'].str.replace("%","")
    options_chain_df["Implied Volatility"] = pd.to_numeric(options_chain_df["Implied Volatility"], errors='coerce')
    options_chain_df["Implied Volatility"] = options_chain_df["Implied Volatility"]  / 100

    # Filter dataframe to extract rows where Strike is within a certain range around the current stock price
    idx = options_chain_df['Strike'].searchsorted(current_stock_price)
    less_than_idx = max(0, idx - 1)
    greater_than_idx = min(len(options_chain_df) - 1, idx)
    less_than_rows = options_chain_df.iloc[max(0, less_than_idx - 4):less_than_idx + 1]
    greater_than_rows = options_chain_df.iloc[greater_than_idx:min(greater_than_idx + 5, len(options_chain_df))]
    options_chain_filtered_df = pd.concat([less_than_rows, greater_than_rows])

    return options_chain_filtered_df
 