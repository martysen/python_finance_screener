from yahoo_fin import stock_info as si
# import pandas as pd
import mpmath as mp
from datetime import datetime, timedelta
from computedays import compute_business_days


ANNUAL_TRADING_DAYS = 252



# 10-day 20-day 50-day 100-day or 180-day
def compute_historical_volatility(stock_ticker, day_offset):

    # set list data structure to store n-day volatility, annual_hist_vol
    volatility_info_list = []
    
    # Get today's date
    current_date = datetime.today().date()
    print("Today's date is", current_date)

    # Calculate the target date based on the day offset
    # if we want 10-day volati. this will return 11 days as instructed
    # todo: need to exclude holidays
    target_date = compute_business_days(current_date, day_offset)
    print("Target date is", target_date)

    # Fetch historical price info from target_date to current_date
    # this basically is a series. access like series[0] etc..
    historical_price_info_series = si.get_data(stock_ticker, start_date=target_date, end_date=current_date, index_as_date=True)['close']


    # start computation for n-day volatility
    idx = 0
    X_i_list = []
    # generate the X_i values and store in list
    while idx < (len(historical_price_info_series) - 1):
        P_i = historical_price_info_series[idx + 1]        
        P_i_1 = historical_price_info_series[idx]
        # DEBUG PRINT
        # print("Value of Pi/Pi-1 in index {} is {}".format((idx+1), (mp.ln(P_i / P_i_1))))
        X_i_list.append(mp.ln(P_i / P_i_1))
        idx += 1
    # compute avg of X_i's over desired days
    X_avg = mp.fsum(X_i_list) / len(X_i_list)
    X_avg = round(X_avg, 7)
    # DEBUG PRINT
    # print("Average of X is {}".format(X_avg))

    # compute (X_i - X_avg)squared and store them back in X_i_list[]
    loop_ctr = 0
    while loop_ctr < len(X_i_list):
        X_i_list[loop_ctr] = mp.power((X_i_list[loop_ctr] - X_avg), 2)
        # DEBUG PRINT
        # print("Computation of X_i - X_avg sqared is {}".format(X_i_list[loop_ctr]))
        loop_ctr += 1 
    
    # compute summation and sqrt to get the numerator 
    temp_numerator = mp.fsum(X_i_list)
    # DEBUG PRINT
    # print("temp numerator is {}".format(temp_numerator))
    n_day_historical_volatility = temp_numerator / (len(X_i_list) - 1)
    n_day_historical_volatility = mp.sqrt(n_day_historical_volatility)
    n_day_historical_volatility_percent = round(n_day_historical_volatility, 4) * 100

    print("{}-day volatility for {} is {} or {}".format(day_offset, stock_ticker, n_day_historical_volatility, n_day_historical_volatility_percent))
    volatility_info_list.append(n_day_historical_volatility)

    # convert to annual volatility. assuming 252 NYSE trading days in a year
    annual_historical_volatility = n_day_historical_volatility * mp.sqrt(ANNUAL_TRADING_DAYS) 
    annual_historical_volatility = round(annual_historical_volatility, 4)
    annual_historical_volatility_percent = annual_historical_volatility*100

    volatility_info_list.append(annual_historical_volatility_percent)

    print("This converted to annual volatility is {} or {}%".format(annual_historical_volatility, annual_historical_volatility*100))


    # X_i = mp.ln()
    # temp_numerator = mp.sqrt()

    return volatility_info_list


