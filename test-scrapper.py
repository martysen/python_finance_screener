from requests_html import HTMLSession
from bs4 import BeautifulSoup

def build_options_url(ticker):
    return f'https://finance.yahoo.com/quote/{ticker}/options?p={ticker}'

def get_expiration_dates(ticker):
    """Scrapes the expiration dates from each option chain for input ticker
    
       @param: ticker"""
    
    site = build_options_url(ticker)
    
    session = HTMLSession()
    resp = session.get(site)
    
    soup = BeautifulSoup(resp.content, 'html.parser')
    session.close()

    # Find all the option tags within the select tag
    select_tag = soup.find('select', {'name': 'expirationDates'})
    
    if select_tag is None:
        return []  # Return an empty list if no select tag is found

    option_tags = select_tag.find_all('option')
    
    # Extract the date values from the option tags
    dates = [option.get('value') for option in option_tags if option.get('value')]
    
    return dates

# Example usage:
ticker = "MSFT"
expiration_dates = get_expiration_dates(ticker)
print(expiration_dates)
