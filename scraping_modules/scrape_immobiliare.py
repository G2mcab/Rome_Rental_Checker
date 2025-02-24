from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
from scraper_config import IMMOBILIARE_CONFIG

def scrape_immobiliare(driver):
    listings = []
    base_url = IMMOBILIARE_CONFIG["base_url"]
    max_pages = IMMOBILIARE_CONFIG["number_of_pages"]
    sorting = IMMOBILIARE_CONFIG["sorting_type"]
    
    # Construct initial URL with sorting if specified
    url = base_url
    if sorting:
        url = f"{base_url}?criterio={sorting}" if not sorting.startswith("da-privati") else f"{base_url}{sorting}/"
    
    # Load first page
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "in-searchLayoutListItem"))
    )
    print(f"Loaded initial page: {driver.current_url}")

    # Get last page number from pagination
    try:
        pagination = driver.find_element(By.CLASS_NAME, "in-pagination__list")
        page_items = pagination.find_elements(By.CLASS_NAME, "in-paginationItem")
        # Filter for numeric pages only, excluding "..." or disabled buttons
        numeric_pages = [int(item.text) for item in page_items if item.text.isdigit()]
        last_page = max(numeric_pages) if numeric_pages else max_pages
        print(f"Detected last page: {last_page}")
    except Exception as e:
        last_page = max_pages  # Use config value if pagination fails
        print(f"Could not detect pagination, using config max_pages ({last_page}): {e}")
    if max_pages and max_pages < last_page:
        last_page = max_pages
        print(f"Limiting to {last_page} pages as per config")

    # Loop through pages
    for page in range(1, last_page + 1):
        if page > 1:
            page_url = f"{url}&pag={page}"
            driver.get(page_url)
            print(f"Navigating to: {page_url}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "in-searchLayoutListItem"))
            )
            print(f"Confirmed page {page} loaded: {driver.current_url}")
        else:
            print(f"Scraping first page: {driver.current_url}")

        listing_items = driver.find_elements(By.CLASS_NAME, "in-searchLayoutListItem")
        print(f"Found {len(listing_items)} listings on page {page}/{last_page}")
        for item in listing_items:
            try:
                title = item.find_element(By.CLASS_NAME, "in-listingCardTitle").text.strip() or "N/A"
                price = item.find_element(By.CLASS_NAME, "in-listingCardPrice").text.strip() or "N/A"
                link = item.find_element(By.CLASS_NAME, "in-listingCardTitle").get_attribute("href") or "N/A"
                
                description = "N/A"
                try:
                    description_elem = item.find_element(By.CLASS_NAME, "in-listingCardDescription")
                    description = description_elem.text.strip() or "N/A"
                except Exception:
                    pass
                
                image_elements = item.find_elements(By.CSS_SELECTOR, ".nd-slideshow__item img")
                image_urls = [img.get_attribute("src") for img in image_elements if img.get_attribute("src")]

                listings.append({
                    "title": title,
                    "website": "Immobiliare.it",
                    "price": price,
                    "description": description,
                    "image_urls": image_urls,
                    "location": "Rome",
                    "phone": "N/A",
                    "url": link
                })
            except Exception as e:
                print(f"Error scraping listing on page {page}: {e}")
    
    return listings

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        listings = scrape_immobiliare(driver)
        with open("test_immobiliare.json", "w", encoding="utf-8") as f:
            json.dump(listings, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(listings)} listings to test_immobiliare.json")
    finally:
        driver.quit()