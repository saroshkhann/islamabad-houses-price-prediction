import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

base_url = "https://www.zameen.com/Homes/Islamabad-3-{}.html"

START_PAGE =1
END_PAGE =6

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.zameen.com/',
    'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

all_homes= []

for page in range(START_PAGE, END_PAGE):
    print(f"Scraping page {page}...")
    print(f'Fetching [{page}/{END_PAGE}]')

    url = base_url.format(page)

    response = requests.get(url, headers=headers, timeout=15)

    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all('li', role='article')

    for card in cards:
        price_tag = card.find('span', {'aria-label': 'Price'})
        price = price_tag.get_text(strip=True) if price_tag else None

        if price:
            all_homes.append({
                'Price':price
            })
    
df = pd.DataFrame(all_homes)

print(df)
