'''
This module recursively computes the ranked output of the options chains for a given stock. 
'''

# Import necessary modules
from yahoo_fin import stock_info
import mpmath as mp
import pandas as pd
from impliedvolatility import compute_implied_volatility_stock
from filteroptionchain import compute_filter_option_chain
from theoriticalprice import compute_theoritical_option_price


mp.dps = 5 
mp.pretty = True


def compute_option_ranker(stock_ticker, holding_period, expected_stock_movement, expiration_date_choice):
    '''
    Computes the ranked output of the options chains for a given stock.

    Parameters:
    - stock_ticker: Ticker symbol of the stock.
    - holding_period: Holding period in months.
    - expected_stock_movement: Expected uniform standard deviation value.
    - expiration_date_choice: Chosen expiration date for the options.

    Returns:
    - df: Ranked DataFrame of option contracts.
    '''

    # Compute implied volatility for the stock
    print("**** **** **** *****  \n")
    print("**** Start Implied Volatility Computation ****\n")
    print("**** **** **** *****  \n")
    volatility = compute_implied_volatility_stock(stock_ticker, expiration_date_choice)
    print("[optionranker.py] Stock implied volatility is ", volatility)
    # print("[optionranker.py] filter option chain is ", options_chain_filtered_df)

    # Retrieve the live price of the stock
    current_stock_price = round(stock_info.get_live_price(stock_ticker), 2)
    # print("[optionranker.py] current stock price is ", current_stock_price)

    # Convert annual volatility to volatility of time period
    # this does not make sense using implied volatility
    # use I.V. cause it is projected vol and coming from options dataframe 
    v_t = volatility * mp.sqrt(holding_period/12)
    # so using 365 days historical volatility 
    # v_t = volatility_info_dict[365][0] * mp.sqrt(holding_period/12)    
    v_t = round(v_t, 5)
    print("[optionranker.py] computed value of v_t for holding period {} is {}".format(holding_period, v_t))

    # Calculate potential bullish and bearish stock prices
    potential_stock_price_bullish = current_stock_price * (mp.exp(expected_stock_movement * v_t))
    potential_stock_price_bearish = current_stock_price * (mp.exp(-(expected_stock_movement * v_t)))
    print("[optionranker.py] **Potential bullish stock price is {} and potential bearish stock price is {}**".format(potential_stock_price_bullish, potential_stock_price_bearish))

    # Get list of option contracts for the stock
    options_chain_filtered_df = compute_filter_option_chain(stock_ticker, expiration_date_choice)

    # Calculate number of days remaining
    if holding_period == 0.5:
        time_remaining_days = 14
    elif holding_period == 0.7:
        time_remaining_days = 21
    elif holding_period == 1:
        time_remaining_days = 30
    elif holding_period == 1.5:
        time_remaining_days = 45
    elif holding_period == 2:
        time_remaining_days = 60
    elif holding_period == 3:
        time_remaining_days = 90
    else:
        print("Something went wrong in holding period selection\n")
        exit()

    # Initialize dictionary to store ranked option contracts
    contract_ranked_dict = {}

    # Iterate over each option contract in the option chain
    for index, row in options_chain_filtered_df.iterrows():
        contract_label = row["Contract Name"]    
        strike_price = row["Strike"]
        last_price = row["Last Price"]

        # Compute potential profit
        theoritical_option_price = compute_theoritical_option_price(stock_ticker, potential_stock_price_bullish, strike_price, time_remaining_days, expiration_date_choice)
        print("[optionranker.py] Computed theory price for profit movement is {}".format(theoritical_option_price))
        print("[optionranker.py] Computed last price for contract {} is {}".format(contract_label, last_price))

        potential_profit = ((theoritical_option_price - last_price) / last_price) * 100
        print("[optionranker.py] Potential profit is {}".format(potential_profit))

        # Compute potential risk
        theoritical_option_price = compute_theoritical_option_price(stock_ticker, potential_stock_price_bearish, strike_price, time_remaining_days, expiration_date_choice)
        print("[optionranker.py] Computed theory price for risk movement is {}".format(theoritical_option_price))

        potential_risk = ((last_price - theoritical_option_price) / last_price) * 100
        print("[optionranker.py] Potential risk is {}".format(potential_risk))

        # Compute reward-risk ratio
        reward_risk_ratio = potential_profit / potential_risk
        print("reward- risk ration for {} is {} \n".format(contract_label, reward_risk_ratio))

        # Add to the dictionary for ranking all computed option chain profit
        contract_ranked_dict[contract_label] = reward_risk_ratio
        # print("[optionranker.py] Inside for loop contract ranked dict is {}".format(contract_ranked_dict))
    
    # Sort the dictionary by reward-risk ratio in descending order
    # sorted_contract_ranked_dict = dict(sorted(contract_ranked_dict.items(), key=lambda item: item[1], reverse=True))

    # print("[optionranker.py] The final dictonary for reward risk is {}".format(contract_ranked_dict))

    # Convert to DataFrame
    # df = pd.DataFrame(contract_ranked_dict, index=[0])
    df = pd.DataFrame(list(contract_ranked_dict.items()), columns=['Key', 'Value'])
    df.sort_values(by='Value', ascending=False, inplace=True)
    print("[optionranker.py] the resulting dataframe is:\n {}".format(df))
  
    return df
