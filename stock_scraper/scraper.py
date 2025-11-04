import requests
from bs4 import BeautifulSoup

BASE_URL = "https://finance.yahoo.com/quote/"

def scrape_ticker(ticker: str):
    ticker = ticker.strip().upper()
    url = f"{BASE_URL}{ticker}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WilsonStockScraper/1.0)"
    }

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 1) header with company name
    header = soup.find("section", attrs={"data-testid": "quote-hdr"})

    if header:
        title_el = header.find("h1")
    else:
        # fallback – whole page
        title_el = soup.find("h1")

    company_name = title_el.get_text(strip=True) if title_el else ticker

    # 2) price
    price = soup.find("span", attrs={"data-testid": "qsp-price"})
    if price:
        price = price.get_text(strip=True)
    else:
        price = None

    # 3) summary table
    summary_data = {}
    stats_div = soup.find("div", attrs={"data-testid": "quote-statistics"})
    if stats_div:
        for li in stats_div.select("li"):
            text_bits = [t.strip() for t in li.stripped_strings]
            if len(text_bits) >= 2:
                label = text_bits[0]
                value = text_bits[-1]
                summary_data[label] = value

    return {
        "ticker": ticker,
        "company_name": company_name,
        "price": price,
        "summary": summary_data,
        "source_url": url,
    }
