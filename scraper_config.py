# Configuration for Immobiliare.it scraping parameters
IMMOBILIARE_CONFIG = {
    "base_url": "https://www.immobiliare.it/affitto-case/roma/",
    "number_of_pages": 10,  # Numero di pagine da scrapare (Number of pages to scrape)
    "sorting_type": "prezzo&ordine=asc",  # Tipo di ordinamento (Sorting type), None = default sorting
    # Opzioni di ordinamento disponibili (Available sorting options):
    # "prezzo&ordine=asc"  # Prezzo crescente (Price ascending)
    # "prezzo&ordine=desc" # Prezzo decrescente (Price descending)
    # "superficie&ordine=asc"  # Superficie crescente (Surface ascending)
    # "superficie&ordine=desc" # Superficie decrescente (Surface descending)
    # "data&ordine=asc"    # Data crescente (Date ascending)
    # "data&ordine=desc"   # Data decrescente (Date descending)
    # "locali&ordine=asc"  # Locali crescente (Rooms ascending)
    # "locali&ordine=desc" # Locali decrescente (Rooms descending)
    # "da-privati"         # Solo da privati (Only from private individuals)
}