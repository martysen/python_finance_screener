"""
This script computes the implied volatility of a stock based on its options chain data.

It first retrieves the options chain data for calls of the given stock ticker using Yahoo Finance API.
Then, it computes the implied volatility of the stock by analyzing the options chain data.

The implied volatility of a stock is computed using the following steps:
1. Filter the options chain data to extract rows where the strike price is within a certain range around the current stock price.
2. Compute the volume weighting factor and distance weighting factor for each option based on its volume and distance from the current stock price.
3. Compute the implied volatility of the stock by summing the product of volume weighting factor, distance weighting factor, and implied volatility of each option, and dividing it by the sum of volume weighting factor and distance weighting factor of each option.

Functions:
    - compute_implied_volatility_stock(stock_ticker):
        This function computes the implied volatility of a stock.
        Args:
            stock_ticker (str): The ticker symbol of the stock.
        Returns:
            float: The computed implied volatility of the stock.

Dependencies:
    - yahoo_fin.options: Used to retrieve options chain data for a given stock ticker.
    - yahoo_fin.stock_info: Used to retrieve the live price of the stock.
    - pandas: Used for data manipulation and analysis.

Constants:
    - MAX_PERCENT_DISTANCE (float): A constant representing the maximum percentage distance of strike prices from the current stock price.

Note:
    - This function assumes that the options chain data for the given stock ticker is available and up-to-date.
    - It also assumes that the live price of the stock is available.
"""

from yahoo_fin import options
from yahoo_fin import stock_info
import pandas as pd
from filteroptionchain import compute_filter_option_chain
import mpmath as mp

mp.dps = 5 
mp.pretty = True


def compute_implied_volatility_stock(stock_ticker, expiration_date_choice):
    """
    Computes the implied volatility of a stock based on its options chain data.

    Args:
        stock_ticker (str): The ticker symbol of the stock.

    Returns:
        float: The computed implied volatility of the stock.
    """

    # Retrieve the live price of the stock
    current_stock_price = round(stock_info.get_live_price(stock_ticker), 2)
    
    # Initialize variables
    implied_volatility_stock = 0
    # todo : needs to be adjusted
    MAX_PERCENT_DISTANCE = 0.25

    options_chain_filtered_df = compute_filter_option_chain(stock_ticker, expiration_date_choice)
    print(" [impliedvolatility.py] filtered dataframe is .. \n", options_chain_filtered_df)

    # Compute sum of all values in the Volume column
    total_volume = options_chain_filtered_df['Volume'].sum()
    print("[impliedvolatility.py] total volume is {} ".format(total_volume))

    # Compute Volume Weighting Factor
    options_chain_filtered_df['Volume Weighting Factor'] = options_chain_filtered_df['Volume'] / total_volume
    options_chain_filtered_df['Volume Weighting Factor'] = options_chain_filtered_df['Volume Weighting Factor'].round(4)

    # Compute Distance from Stock Price
    options_chain_filtered_df['Distance from Stock Price'] = abs(options_chain_filtered_df['Strike'] - current_stock_price) / current_stock_price
    options_chain_filtered_df['Distance from Stock Price'] = options_chain_filtered_df['Distance from Stock Price'].round(3)

    # Compute Distance Weighting Factor
    options_chain_filtered_df['Distance Weighting Factor'] = 0
    options_chain_filtered_df.loc[options_chain_filtered_df['Distance from Stock Price'] > MAX_PERCENT_DISTANCE, 'Distance Weighting Factor'] = 0
    options_chain_filtered_df.loc[options_chain_filtered_df['Distance from Stock Price'] <= MAX_PERCENT_DISTANCE, 'Distance Weighting Factor'] = \
        ((options_chain_filtered_df['Distance from Stock Price'] - MAX_PERCENT_DISTANCE) ** 2) / (MAX_PERCENT_DISTANCE ** 2)

    # Compute implied_volatility_stock
    iv_numerator = (options_chain_filtered_df['Volume Weighting Factor'] * options_chain_filtered_df['Distance Weighting Factor'] *
                    options_chain_filtered_df['Implied Volatility']).sum()
    iv_denominator = (options_chain_filtered_df['Volume Weighting Factor'] * options_chain_filtered_df['Distance Weighting Factor']).sum()
    implied_volatility_stock = iv_numerator / iv_denominator
    # this need to adjusted with a smoothing effect which have not done

    return round(implied_volatility_stock, 4)
