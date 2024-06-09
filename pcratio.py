# start off with computing PCR ratio
# individual call open interest and put open interest 
# to find resistance and support we will do after this 

from yahoo_fin import options
import mpmath as mp

def compute_pcr_ratio(stock_ticker, expiration_date):
  call_open_interest = options.get_calls(stock_ticker, expiration_date)['Open Interest']
  put_open_interest = options.get_puts(stock_ticker, expiration_date)['Open Interest']

  call_open_interest_sum = mp.fsum(call_open_interest)
  put_open_interest_sum = mp.fsum(put_open_interest)

  pcr_ratio = put_open_interest_sum / call_open_interest_sum
  pcr_ratio = round(pcr_ratio, 5)

  print("**** **** **** **** \n")
  print("**** **** **** **** \n")
  print("* PCR for ticker {} on option chain expiring on {} is {} \n *".format(stock_ticker, expiration_date, pcr_ratio))
  print("**** **** **** **** \n")
  print("**** **** **** **** \n")

  if pcr_ratio<0.5:
    print("pcr_ratio is less than 0.5. Signal: STRONGLY BEARISH. Maybe after long down move or price may be at support level")
  elif pcr_ratio >= 0.5 and pcr_ratio < 0.8:
    print("Signal: BEARISH")
  elif pcr_ratio >= 0.8 and pcr_ratio < 1.2:
    print("Signal: NEUTRAL or SIDEWAYS MARKET")
  elif pcr_ratio >= 1.2 and pcr_ratio < 1.6:
    print("Signal: BULLISH")
  elif pcr_ratio > 1.6: 
    print("Signal: STRONG BULLISH. Market at resistance")
  else:
    print("Incorrect pcr value computed. check data!!")
    
  return pcr_ratio
