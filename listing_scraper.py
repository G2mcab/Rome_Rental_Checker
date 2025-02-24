from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from scraping_modules.scrape_immobiliare import scrape_immobiliare

def scrape_all_listings():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_listings = []

    try:
        # Scrape Immobiliare.it
        immobiliare_listings = scrape_immobiliare(driver)
        all_listings.extend(immobiliare_listings)
        
        # Save to JSON
        with open("rome_rentals.json", "w", encoding="utf-8") as f:
            json.dump(all_listings, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(all_listings)} total listings to rome_rentals.json")
    
    finally:
        driver.quit()

    return all_listings

if __name__ == "__main__":
    scrape_all_listings()