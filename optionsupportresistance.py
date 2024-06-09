'''
go over the call and put option chain for a ticker with expiration date
input args: ticker, expiration_date
logic: 
compute the largest two values of call chains and store resp. strike prices
compute the larget two values of put chain and store resp. strike prices
the call chain creates resistance 
the put chain creates support
this can be used to against live price to see breakout and reversal strat
to give signal if price is close to supp or resistance 
'''
from yahoo_fin import options
from yahoo_fin import stock_info as si
import mpmath as mp
import matplotlib.pyplot as plt

# function to plot support-resistance strike price against stock price
def plot_support_resistance_stock(support_bands, resistance_bands, stock_price, stock_ticker, expiration_date):
    """
    Plots the support and resistance bands along with the stock price and saves the plot.

    Parameters:
    support_bands (list): List of values for support bands.
    resistance_bands (list): List of values for resistance bands.
    stock_price (float): Value for the stock price.
    filename (str): The name of the file to save the plot to.
    """
    # Initialize the plot
    fig = plt.figure()
    fig.set_size_inches(25, 15)

    # Plot the support bands
    for value in support_bands:
        plt.axhline(y=value, color='green', linestyle='-', linewidth=2, label='Support Bands' if value == support_bands[0] else "")

    # Plot the resistance bands
    for value in resistance_bands:
        plt.axhline(y=value, color='red', linestyle='-', linewidth=2, label='Resistance Bands' if value == resistance_bands[0] else "")

    # Plot the stock price
    plt.axhline(y=stock_price, color='black', linestyle='-', linewidth=2, label='Stock Price')

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Support and Resistance Bands with Stock Price')

    # Add legend
    plt.legend(loc='upper left')

    # Remove x-axis values
    plt.xticks([])

    # Save the plot to a file
    figure_file_title = "./screeneroutput/"+ stock_ticker + " " + expiration_date + " Support-resistance-analysis"
    plt.savefig(figure_file_title)

# function to plot change in option contract prices 
def plot_change_in_lastprice_chart(call_df, put_df, stock_ticker, expiration_date):
    fig, ax = plt.subplots()
    # w, h
    fig.set_size_inches(25,15)

    call_bars = ax.bar(call_df['Strike'], call_df['Change'], color='green', label='Call')

    put_bars = ax.bar(put_df['Strike'], put_df['Change'], color='red', label='Put')

    ax.set_xlabel('Strike')
    ax.set_ylabel('Change')
    ax.set_title('Option price Change for calls and puts. If for a strike price, Call > Puts More bearish and vice versa. Double Check')
    ax.legend()
    
    plt.xticks(call_df['Strike'], call_df['Strike'], rotation=30)
    plt.xticks(put_df['Strike'], put_df['Strike'], rotation=30)

    figure_file_title = "./screeneroutput/"+ stock_ticker + " " + expiration_date
    plt.savefig(figure_file_title, bbox_inches='tight')
    # plt.show()
    # plt.close(fig)
    

def compute_option_support_resistance_bands(stock_ticker, expiration_date):
  
  # get stock live price 
  stock_price = si.get_live_price(stock_ticker)
  
  # compute resistance
  call_open_interest = options.get_calls(stock_ticker, expiration_date)

  # compute first resistance and 2nd resistance mark
  # Find highest and second highest values in column open interest
  highest_call_open_interest = call_open_interest['Open Interest'].nlargest(1).index[0]
  second_highest_call_open_interest = call_open_interest['Open Interest'].nlargest(2).index[1]

  # extract the strike price corresponding to highest and second high index
  highest_call_oi_strike = call_open_interest.at[highest_call_open_interest, 'Strike']
  second_highest_call_oi_strike = call_open_interest.at[second_highest_call_open_interest, 'Strike']
  print("**** **** **** ****")
  print("[optionsupportresistance.py] highest and 2nd highest resistance strikes are {} {}".format(highest_call_oi_strike, second_highest_call_oi_strike))
  print("**** **** **** ****")

  # Rows between highest and second highest values of column C
  # to find change in Last Price between the resistance bands
  # between_rows = call_open_interest.loc[(call_open_interest.index >= second_highest_call_oi_strike) & (call_open_interest.index <= highest_call_oi_strike)]
#   print("{}".format(call_open_interest))

  # ********************************************************
  # ********************************************************
  # Section break into puts
  # ********************************************************
  # ********************************************************
  # Compute Support through Put options 
  put_open_interest = options.get_puts(stock_ticker, expiration_date)

  # compute first support and 2nd support mark
  # Find highest and second highest values in column open interest
  highest_put_open_interest = put_open_interest['Open Interest'].nlargest(1).index[0]
  second_highest_put_open_interest = put_open_interest['Open Interest'].nlargest(2).index[1]

  # extract the strike price corresponding to highest and second high index
  highest_put_oi_strike = put_open_interest.at[highest_put_open_interest, 'Strike']
  second_highest_put_oi_strike = put_open_interest.at[second_highest_put_open_interest, 'Strike']
  print("**** **** **** ****")
  print("[optionsupportresistance.py] highest and 2nd highest strikes for support bands are {} {}".format(highest_put_oi_strike, second_highest_put_oi_strike))
  print("**** **** **** ****")

  # Rows between highest and second highest values of column C
  # to find change in Last Price between the resistance bands
  # between_rows = put_open_interest.loc[(put_open_interest.index >= second_highest_put_oi_strike) & (put_open_interest.index <= highest_put_oi_strike)]
  # print("{}".format(put_open_interest))   


  # ********************************************************
  # PLOT FUNCTIONS 
  # ********************************************************
  plot_change_in_lastprice_chart(call_open_interest, put_open_interest, stock_ticker, expiration_date)
  support_bands = [highest_put_oi_strike, second_highest_put_oi_strike]
  resistance_bands = [highest_call_oi_strike, second_highest_call_oi_strike]
  plot_support_resistance_stock(support_bands, resistance_bands, stock_price, stock_ticker, expiration_date)

  return