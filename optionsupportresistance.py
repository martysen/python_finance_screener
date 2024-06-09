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

    figure_file_title = stock_ticker + " " + expiration_date
    plt.savefig(figure_file_title, bbox_inches='tight')
    # plt.show()
    # plt.close(fig)
    

def compute_option_support_resistance_bands(stock_ticker, expiration_date):
  # compute resistance
  call_open_interest = options.get_calls(stock_ticker, expiration_date)

  # compute first resistance and 2nd resistance mark
  # Find highest and second highest values in column open interest
  highest_call_open_interest = call_open_interest['Open Interest'].nlargest(1).index[0]
  second_highest_call_open_interest = call_open_interest['Open Interest'].nlargest(2).index[1]

  # extract the strike price corresponding to highest and second high index
  highest_call_oi_strike = call_open_interest.at[highest_call_open_interest, 'Strike']
  second_highest_call_oi_strike = call_open_interest.at[second_highest_call_open_interest, 'Strike']
  print("highest and 2nd highest resistance strikes are {} {}".format(highest_call_oi_strike, second_highest_call_oi_strike))

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
  print("highest and 2nd highest strikes for support bands are {} {}".format(highest_put_oi_strike, second_highest_put_oi_strike))

  # Rows between highest and second highest values of column C
  # to find change in Last Price between the resistance bands
  # between_rows = put_open_interest.loc[(put_open_interest.index >= second_highest_put_oi_strike) & (put_open_interest.index <= highest_put_oi_strike)]
  # print("{}".format(put_open_interest))   


  # ********************************************************
  # PLOT FUNCTIONS 
  # ********************************************************
  plot_change_in_lastprice_chart(call_open_interest, put_open_interest, stock_ticker, expiration_date)

  return