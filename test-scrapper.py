import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_balance_sheet(url):
    """
    Scrapes the balance sheet data from the given Yahoo Finance URL.

    Parameters:
    url (str): The URL of the Yahoo Finance balance sheet page.

    Returns:
    pd.DataFrame: A DataFrame containing the balance sheet data.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the balance sheet data
    table = soup.find('div', {'class': 'D(tbrg)'})
    
    if table is None:
        raise ValueError("Could not find balance sheet data on the page")

    rows = table.find_all('div', {'class': 'D(tbr)'})

    # Extract column headers
    headers = [header.get_text() for header in rows[0].find_all('div', {'class': 'D(ib)'})]

    data = []
    for row in rows[1:]:
        cells = row.find_all('div', {'class': 'D(tbc)'})
        row_data = [cell.get_text() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)

    return df

# Example usage:
url = 'https://finance.yahoo.com/quote/MSFT/balance-sheet/?p=MSFT'
balance_sheet_df = scrape_balance_sheet(url)
print(balance_sheet_df.head())
