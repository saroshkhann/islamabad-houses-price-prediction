import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time

base_url = "https://www.zameen.com/Homes/Islamabad-3-{}.html"

START_PAGE =1
END_PAGE =11

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

session = requests.Session()
session.headers.update(headers)

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

        loc_tag = card.find('div', {'aria-label': 'Location'})
        location = loc_tag.get_text(strip=True) if loc_tag else None

        beds_tag = card.find('span', {'aria-label': 'Beds'})
        beds = beds_tag.get_text(strip=True) if beds_tag else None

        baths_tag = card.find('span', {'aria-label': 'Baths'})
        baths = baths_tag.get_text(strip=True) if baths_tag else None

        area_tag = card.find('span', {'aria-label': 'Area'})
        area = area_tag.get_text(strip=True) if area_tag else None

        link_tag = card.find('a', href=True)
        listing_url =None

        if link_tag:
            href = link_tag['href']
            listing_url = (
                f'https://www.zameen.com{href}' if href.startswith('/') else href
            )
        
        description = None

        if listing_url:
            try:
                detail_res = session.get(listing_url, timeout=10)

                if detail_res.status_code == 200:
                    detail_soup = BeautifulSoup(detail_res.text, 'lxml')

                    desc_tag = detail_soup.find('div', {'aria-label': 'Property description'})
                    description = desc_tag.get_text(strip=True) if desc_tag else None

                    type_tag = detail_soup.find('span', {'aria-label': 'Type'})
                    type = type_tag.get_text(strip=True) if type_tag else None

            except Exception as e:
                print("Failed to fetch")

        if price or location:
            all_homes.append({
                'Type': type,
                'Price':price,
                'Location': location,
                'Beds': beds,
                'Baths': baths,
                "Area": area,
                "URL": listing_url,
                'Description': description
            })
    time.sleep(1)
    
df = pd.DataFrame(all_homes)

df.to_csv('data/raw/checking.csv', index=False)

print(df)
