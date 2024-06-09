from lognormaldistribution import compute_lognormal_dist
from impliedvolatility import compute_implied_volatility_stock
from historicalvolatility import compute_historical_volatility
import mpmath as mp
# from scipy.stats import norm # verfied! code is right.

mp.dps = 5 
mp.pretty = True

'''
time_remaining must be in days
o/p: return theoritical strike price for each option
'''
def compute_theoritical_option_price(stock_ticker, current_stock_price, strike_price, time_remaining_days, expiration_date_choice):
  # the current intrest on 3 month US treasury bill i.e. 5.46\% 
  CURRENT_RISK_FREE_INTEREST_RATE = 0.546
  
  # volatility computation will call another function in another file
  volatility = compute_implied_volatility_stock(stock_ticker, expiration_date_choice)
  # print("[theoriticalprice.py] Implied Volatility is {}".format(volatility))

  
  
  time_remaining_years = time_remaining_days/365
  time_remaining_years = round(time_remaining_years, 5)
  # print("[theoriticalprice] Time remaining in years is {}".format(time_remaining_years))

  # delta or hedge ratio or N(d1)
  temp_numerator_1 = mp.ln(current_stock_price/strike_price)
  # print("[theoriticalprice] compute for temp_numerator_1 is {}".format(temp_numerator_1))
  # print("[theoriticalprice] volatility is {}".format(volatility))
  temp_numerator_2 = (CURRENT_RISK_FREE_INTEREST_RATE+((volatility ** 2)/2))
  # print("[theoriticalprice] compute for temp_numerator_2 is {}".format(temp_numerator_2))
  temp_denominator = volatility * mp.sqrt(time_remaining_years)
  temporary_variable_d1 = (temp_numerator_1 + (temp_numerator_2 * time_remaining_years)) / temp_denominator

  temporary_variable_d1 = round(temporary_variable_d1, 5)
  # print("[theoriticalprice.py] *** Value of d1 or DELTA is {} ***".format(temporary_variable_d1))

  # computation of d2
  temporary_variable_d2 = temporary_variable_d1 - (volatility*mp.sqrt(time_remaining_years))

  temporary_variable_d2 = round(temporary_variable_d2, 5)
  # print("Value of d2 is {}".format(temporary_variable_d2))

  # compute theoritical option price
  # print("[theoriticalprice.py PACKAGE] **N(d1) or DELTA** is {}".format(norm.cdf(temporary_variable_d1, 0, 1)))
  print("[theoriticalprice.py] **N(d1) or DELTA** is {}".format(compute_lognormal_dist(temporary_variable_d1)))
  theoritical_price_left_expression = current_stock_price * compute_lognormal_dist(temporary_variable_d1)

  
  # print("N(d2) is {}".format(compute_lognormal_dist(temporary_variable_d2)))
  theoritical_price_right_expression = strike_price * mp.exp(-(CURRENT_RISK_FREE_INTEREST_RATE * time_remaining_years))*compute_lognormal_dist(temporary_variable_d2)

  theoritical_option_price = theoritical_price_left_expression - theoritical_price_right_expression


  theoritical_option_price = round(theoritical_option_price, 4)
  # theoritical_option_price = theoritical_option_price * 100

  return theoritical_option_price