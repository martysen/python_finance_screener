# lib needed to install - yahoo_fin
# https://theautomatic.net/yahoo_fin-documentation/
# need this library as well - requests_html
from yahoo_fin import options
import pandas as pd 
import xlsxwriter

'''
get_calls
get_expiration_dates
get_options_chain
get_puts
'''

# from file_name import function_name1, function_name2

# feed the stock list from the stock screener here 
# call function to return stock list or read from file
stock = 'AAPL'

# grab the options chain 
pd.set_option('display.max_columns', None)
# chain = options.get_options_chain(stock)
# print(chain)
# if you only want call options; similar for puts 
# print(chain['calls'])
# or you can do options.get_calls or get_puts instead of line 11

# If you want to find options that expire on a certain date 
# chain = options.get_options_chain(stock, 'July 23, 2024')
# print(chain['calls'])

# IF you want to know what expiration dates are possible
# print(options.get_expiration_dates(stock))
# print(options.get)


# To build the screener you can filter or query the dataframe
#  called chain above
screener_df = options.get_calls(stock)

# df[["a", "b"]] = df[["a", "b"]].apply(pd.to_numeric, errors='coerce')
# df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
screener_df["Volume"] = pd.to_numeric(screener_df["Volume"], errors='coerce')
# remove the % char in the IV col
screener_df['Implied Volatility'] = screener_df['Implied Volatility'].str.replace(r'\D','',regex=True)
# convert IV col to numeric
screener_df["Implied Volatility"] = pd.to_numeric(screener_df["Implied Volatility"], errors='coerce')

# print(screener_df['Implied Volatility'])

# create a mask 
# mask = screener_df['Volume'].values >= 100 
result = screener_df.loc[(screener_df['Implied Volatility'].values >= 25) & (screener_df['Volume'].values >= 100)] 

# use mask to filter dataframe
# PRINT THIS TO EXCEL FOR SCREENED VALUES OF A STOCK
print(result)


# export df to tables 
# note that df.to_ can do many exports like csv etc
# table_name = stock+'_options_chain'
# screener_df.to_excel('./testExcel.xlsx', sheet_name=table_name, engine='xlsxwriter')

# >>> df2 = df1.copy()
# >>> with pd.ExcelWriter('output.xlsx') as writer:  
# ...     df1.to_excel(writer, sheet_name='Sheet_name_1')
# ...     df2.to_excel(writer, sheet_name='Sheet_name_2')