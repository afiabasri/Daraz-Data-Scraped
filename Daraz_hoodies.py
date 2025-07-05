from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_daraz_products(base_url, max_pages=2):
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US"
        )
        page = context.new_page()

        for page_num in range(1, max_pages + 1):
            print(f"\n🔄 Scraping page {page_num}")
            url = f"{base_url}&page={page_num}"
            try:
                page.goto(url, timeout=60000)
                page.wait_for_selector("div[class*='buTCk']", timeout=15000)
                soup = BeautifulSoup(page.content(), "html.parser")

                results = soup.select("div[class*='buTCk']")

                for result in results:
                    # Link
                    link_tag = result.select_one("a")
                    link = "https:" + link_tag['href'] if link_tag and link_tag.get("href") else "N/A"

                    # Title 
                    title_tag = result.select_one("a") 
                    title = title_tag.text.strip() if title_tag else "N/A"

                    # Price 
                    price_tag = result.select_one("span[class*=ooOxS]") 
                    price = price_tag.text.strip() if price_tag else "N/A"

                    # Rating 
                    rating_tag = result.select_one("span[class*=qzqFw]")
                    rating = rating_tag.text.strip() if rating_tag else "N/A"

                    data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Link": link
                    })

            except Exception as e:
                print(f"⚠️ Error on page {page_num}: {e}")
                continue

        browser.close()
    return data

# Daraz search URL
base_url = "https://www.daraz.pk/invisible-url6/?price=-2000&from=hp_categories&q=hoodies++sweatshirts"

# Scrape and save
products = scrape_daraz_products(base_url, max_pages=2)
df = pd.DataFrame(products)
df.to_excel("Daraz_hodies.xlsx", index=False)
print("✅ Data saved to 'Daraz_hodies.xlsx'")