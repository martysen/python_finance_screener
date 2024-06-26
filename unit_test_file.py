from theoriticalprice import compute_theoritical_option_price
from historicalvolatility import compute_historical_volatility
from pcratio import compute_pcr_ratio
from optionsupportresistance import compute_option_support_resistance_bands
from requests_html import *
from yahoo_fin import stock_info as si
import datetime
import re
import pandas as pd

from yahoo_fin import options
# test_output = compute_theoritical_option_price("abc", 41, 40, 90, "2024-09-20")

# print(test_output)

# not working 
# print(si.get_analysts_info("msft"))
# test = si.get_balance_sheet("MSFT")
# test = si.get_cash_flow("msft", yearly=True)
# test = si.get_company_info("msft")
# test = si.get_company_officers("msft")
# test = si.get_earnings("MSFT")
# test = si.get_earnings_for_date('2024-07-14') # string indices must be integers
# test = si.get_earnings_history("AMD")
# test = si.get_earnings_in_date_range('2024-06-10', '2024-06-14') # works but returns empty list. NEED!
# test = si.get_financials('AMD')
# test = si.get_income_statement('AMD')
# test = si.get_next_earnings_date('AMD') # NEED TO MAKE THIS WORK 
# test = si.get_premarket_price('AAPL')
# test = si.get_postmarket_price('AMD')
# test = si.get_quote_data('AMD')
# test = si.get_quote_table('AAPL', dict_result=True) # treating a dataframe as a list? see method
# test = si.tickers_sp500()

# not required
# test = si.get_market_status() # NOT REQUIRED ANYWAYS
# test = si.get_splits('aapl')

# working
# test = si.get_data("MSFT", index_as_date=True, interval="1wk")
# test = si.get_day_gainers() # has PE Ratio, Volume, 3 month avg vol., market cap (returned 30 instead 100)
# test = si.get_day_losers() # same as above. returned 100
# test = si.get_day_most_active() # same as above. i think sorted by volume; can run rsi on this?
# test = si.get_dividends("MSFT")
# below worthwhile output: Last Price and Change for S&P, DOW, Nasdaq, US treasury bond
# 10 year T note, 5 year T note, 2 year T note, Gold, Crude oil, natural gas
# test = si.get_futures()  
# test = si.get_holders('AMD') # can note how much % of shares held by All insiders 
# test= si.get_live_price('AMD')
# test = si.get_stats('AAPL') # contains VALUABLE FUNDAMENTAL ANALYSIS FIELDS
# test = si.get_stats_valuation('AAPL') # quaterly FUND ANALYSIS trends IMP!
# test = si.get_undervalued_large_caps() # IMPORTANT. you can grab by P/E ratio here?
# test = si.tickers_dow() # scrapes wikipedia
# test = si.tickers_nasdaq() # ftp://ftp.nasdaqtrader.com/SymbolDirectory/.
test = options.get_expiration_dates('MCD')
# print("{}".format(test))


# date = "2024-06-07"
# test_var = compute_option_support_resistance_bands("MCD", date)
# ratio = compute_pcr_ratio("MCD", date)
# print("\n Computed ratio is {}".format(ratio))