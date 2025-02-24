from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json  # Added import

def scrape_immobiliare(driver, url="https://www.immobiliare.it/affitto-case/roma/", max_pages=None):
    listings = []
    driver.get(url)
    sleep(3)  # Wait for page load

    # Get last page number from pagination
    try:
        pagination = driver.find_element(By.CLASS_NAME, "in-pagination__list")
        last_page_elem = pagination.find_elements(By.CLASS_NAME, "in-paginationItem")[-2]  # Last number before "..."
        last_page = int(last_page_elem.text)
    except Exception:
        last_page = 1  # Default to 1 if pagination not found
    if max_pages and max_pages < last_page:
        last_page = max_pages

    # Loop through pages
    for page in range(1, last_page + 1):
        if page > 1:
            driver.get(f"{url}?pag={page}")
            sleep(3)

        print(f"Scraping Immobiliare.it page {page}/{last_page}...")
        listing_items = driver.find_elements(By.CLASS_NAME, "in-searchLayoutListItem")
        for item in listing_items:
            try:
                title = item.find_element(By.CLASS_NAME, "in-listingCardTitle").text.strip() or "N/A"
                price = item.find_element(By.CLASS_NAME, "in-listingCardPrice").text.strip() or "N/A"
                link = item.find_element(By.CLASS_NAME, "in-listingCardTitle").get_attribute("href") or "N/A"
                description = item.find_element(By.CLASS_NAME, "in-listingCardDescription").text.strip() or "N/A"
                image_elements = item.find_elements(By.CSS_SELECTOR, ".nd-slideshow__item img")
                image_urls = [img.get_attribute("src") for img in image_elements if img.get_attribute("src")]

                listings.append({
                    "title": title,
                    "website": "Immobiliare.it",
                    "price": price,
                    "description": description,
                    "image_urls": image_urls,
                    "location": "Rome",  # Refine later if needed
                    "phone": "N/A",      # Requires individual page visit
                    "url": link
                })
            except Exception as e:
                print(f"Error scraping listing on page {page}: {e}")
    
    return listings

# For testing standalone
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        listings = scrape_immobiliare(driver, max_pages=2)  # Limit to 2 pages for testing
        with open("test_immobiliare.json", "w", encoding="utf-8") as f:
            json.dump(listings, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(listings)} listings to test_immobiliare.json")
    finally:
        driver.quit()