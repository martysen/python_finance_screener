from datetime import datetime, timedelta

# function to find target_date from current given the number of business days we want to calculate volatility for 
# excludes weekends. Need to add exclusion for holidays.
def compute_business_days(end_date, day_offset):
    target_date = end_date
    while day_offset >= 0:
        target_date = target_date - timedelta(days=1)
        if target_date.weekday() < 5:  # Monday to Friday
            day_offset -= 1
    return target_date