import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si # need this to plot against SPY
import numpy as np

def plot_change_in_historical_volatility(stock_ticker, hist_vola_dict, volatility_info_dict_SPY):
    fig, ax = plt.subplots()  # Unpack fig and ax variables correctly

    # Set the figure size
    fig.set_size_inches(25, 15)

    keys = list(hist_vola_dict.keys())
    values_stock = [val[1] for val in hist_vola_dict.values()]
    values_spy = [val[1] for val in volatility_info_dict_SPY.values()]

    bar_width = 0.35
    indices = np.arange(len(keys))

    bars1 = ax.bar(indices, values_stock, bar_width, label=stock_ticker)
    bars2 = ax.bar(indices + bar_width, values_spy, bar_width, label='SPY')


    # ax.bar(keys, values)

    ax.set_xlabel('Days')
    ax.set_ylabel('Annualized Historical Volatility')
    ax.set_title('Bar Plot trend in annualized historical volatility of 10, 20, 50, 100, and 180 days')

    ax.set_xticks(indices + bar_width / 2)
    ax.set_xticklabels(keys, rotation=30)

    ax.legend()
    
    # ax.set_xticks(keys)  # Set x-axis ticks

    # ax.set_xticklabels(keys, rotation=30)  # Set x-axis tick labels with rotation

    figure_file_title = "./screeneroutput/" + stock_ticker + "  annualized historical volatility trend"
    plt.savefig(figure_file_title, bbox_inches='tight')
    # plt.show()  # Show plot
    # plt.close(fig)  # Close the figure to release resources
    return
