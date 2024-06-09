from theoriticalprice import compute_theoritical_option_price
from historicalvolatility import compute_historical_volatility
from pcratio import compute_pcr_ratio
from optionsupportresistance import compute_option_support_resistance_bands
from requests_html import *


from yahoo_fin import options
# test_output = compute_theoritical_option_price("abc", 41, 40, 90, "2024-09-20")

# print(test_output)

# testing out the issue with getting expirations dates from yahoo fin
# shoould get a list back
exp_dates = options.get_expiration_dates("DOCU")
site = "https://finance.yahoo.com/quote/DOCU/options/?p=DOCU"
    
session = HTMLSession()
resp = session.get(site)

html = resp.html.raw_html.decode()
# print("here is content \n {}".format(html))
f = open("demofile2.txt", "a")
f.write(html)
f.close()

splits = html.split('<div role="options">')
print(splits)

dates = [split.split('</div>')[0].split('>')[-1].strip() for split in splits[1:]]

# dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
print(dates)

dates = [elt for elt in dates if elt != '']

session.close()
print(exp_dates)


# date = "2024-06-07"
# test_var = compute_option_support_resistance_bands("MCD", date)
# ratio = compute_pcr_ratio("MCD", date)
# print("\n Computed ratio is {}".format(ratio))