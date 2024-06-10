'''
Main script for analyzing and ranking option contracts for selected stocks.
The script performs the following steps:
1. Call the stockscreener module to identify potential bullish stocks for the month.
2. Pass the list of selected stock tickers to the optionranker module to rank suitable option contracts for each stock.
3. Optionally, perform historical volatility analysis on the selected options or stocks.
4. Compute the expected return for shortlisted options returned in step 2.
5. check this site to verify your work for option price calc - https://www.option-price.com/ 
'''

# Import necessary modules
from optionranker import compute_option_ranker
from pcratio import compute_pcr_ratio
from historicalvolatility import compute_historical_volatility
from optionsupportresistance import compute_option_support_resistance_bands
import pandas as pd
from plothistoricalvolatility import plot_change_in_historical_volatility
from yahoo_fin import options
from datetime import datetime

n_day_hist_volatility_list = [10,20,50,100,180]


# List of stocks to be evaluated
# later on this list needs to be populated from the screener
ranked_stocks = ["QQQ"]



# Dictionary to store ranked options for each stock
ranked_options_df_final = pd.DataFrame(columns=['Key', 'Value'])

# Iterate through each stock
for item in ranked_stocks:
    print("Starting evaluation for stock ticker - {} ".format(item))
    print("**** **** **** ****")
    print("** Available Expiration Dates **")
    print("**** **** **** ****")
    dates = options.get_expiration_dates(item)
    for date in dates: 
        print("{}".format(date))
    
    # Ensure expiration date choice is at least 3 weeks from the current date
    time_remaining_days = 0
    while time_remaining_days < 21:
        expiration_date_choice_str = input("Pick an expiration date to grab its call option chain. \nExpiration date should be at least 3 weeks from the current date {}:".format(datetime.now().date()))
        today_date = datetime.now().date()
        expiration_date_choice = datetime.strptime(expiration_date_choice_str, "%Y-%m-%d").date()
        time_remaining_days = (expiration_date_choice - today_date).days
    
    # Set holding period based on days to expire
    if 21 <= time_remaining_days <= 30:
        print("Time till expiry is 21 to 30 days.")
        print("Maximum holding period is set to 14 days or 0.5 month.")
        holding_period = 0.5
    elif 30 < time_remaining_days < 45:
        holding_period = 0.7
        print("Time till expiry is greater than 30 and less than 45 days.")
        print("Maximum holding period is set to 3 weeks or 0.7 month.")
    elif 45 <= time_remaining_days < 60:
        print("Time till expiry is greater than or equal to 45 and less than 60 days.")
        print("Maximum holding period is set to 4 weeks or 1 month.")
        holding_period = 1
    elif 60 <= time_remaining_days < 75:
        print("Time till expiry is greater than or equal to 60 and less than 75 days.")
        print("Maximum holding period is set to 1.5 months.")
        holding_period = 1.5
    elif 75 <= time_remaining_days <= 120:
        print("Time till expiry is greater than or equal to 75 and less than or equal to 120 days.")
        print("Maximum holding period is set to 2 months.")
        holding_period = 2
    else:
        print("Time till expiry is greater than 120 days.")
        print("Maximum holding period is set to 3 months.")
        holding_period = 3
    
    # Input expected stock movement
    expected_stock_movement = float(input("Enter desired uniform standard deviation value (e.g., 1 for 16 percent success, 0.7 for 25 percent success, or smaller values for smaller stock movements): "))

    # compute and print PCR value
    # creating a dummy variable for return in case needed later 
    # for now will get overwritten 
    pcr_ratio_value = compute_pcr_ratio(item, expiration_date_choice_str)

    # compute and plot historical volatility trend
    # Compute historical volatility for the stock
    print("**** **** **** *****  \n")
    print("**** Start Historical Volatility Computation ****\n")
    print("**** **** **** *****  \n")
    volatility_info_dict = dict()
    volatility_info_dict_SPY = dict()
    for n_day_index in n_day_hist_volatility_list:
        # not caring about capturing returned value
        # print statement in the function will print
        # if you need to process data then modify the return here
        volatility_info_list = compute_historical_volatility(item, n_day_index)
        volatility_info_list_SPY = compute_historical_volatility("SPY", n_day_index)
        volatility_info_dict[n_day_index] = volatility_info_list
        volatility_info_dict_SPY[n_day_index] = volatility_info_list_SPY
    
    plot_change_in_historical_volatility(item, volatility_info_dict, volatility_info_dict_SPY)



    # COMPUTE SUPP AND RESISTANCE BANDS 
    # This will also create the plots for manual analysis
    compute_option_support_resistance_bands(item, expiration_date_choice_str)
    
    # Invoke optionranker
    dataframe = compute_option_ranker(item, holding_period, expected_stock_movement, expiration_date_choice_str)
    # ranked_options_dict[item] = dataframe
    # ranked_options_df_final = ranked_options_df_final.append(dataframe)
    # ranked_options_df_final = pd.concat([ranked_options_df_final, dataframe], ignore_index=True)
    dataframe.to_csv('./screeneroutput/final_rank.csv', mode='a', index=False, header=None)

# Print the ranked options dictionary
# ranked_options_df_final.sort_values(by='Value', ascending=False, inplace=True)
# print("[app.py] Ranked options df is \n {}".format(ranked_options_df_final))
print("Teminated success!")

# warning to not buy on a monday or friday 
current_date = datetime.date.today()
day_of_week = current_date.weekday()

# Convert the day of the week to a string
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
current_day_of_week = days_of_week[day_of_week]
print("Today is:", current_day_of_week)

if current_day_of_week in ['Monday', 'Friday']:
  print("** WARNING ** do not buy on Monday or Friday. Wait for dip! ")


