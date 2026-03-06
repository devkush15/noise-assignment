from ingestion.scraper import scrape_flipkart_reviews

# Product 1 - Noise Master Buds Max
url1 = "https://www.flipkart.com/noise-master-buds-max-sound-bose-segment-leading-anc-dynamic-eq-60-hr-playtime-bluetooth/product-reviews/itm583241394db27?pid=ACCHGZH5WCCGB3Y4&lid=LSTACCHGZH5WCCGB3Y4LI6ZZJ&marketplace=FLIPKART"

# Product 2 - Noise Buds VS102 (or whatever Master Buds 1 URL you have)
url2 = "https://www.flipkart.com/noise-master-buds-sound-bose-49db-anc-6-mic-enc-44-hr-battery-spatial-audio-bluetooth/product-reviews/itm965e6651f8980?pid=ACCHE4GYFJ8J2ADE&lid=LSTACCHE4GYFJ8J2ADEQWIFCY&marketplace=FLIPKART"

print("Scraping Product 1...")
reviews1 = scrape_flipkart_reviews(url1, "Noise Master Buds Max", pages=6)

print("\nScraping Product 2...")
reviews2 = scrape_flipkart_reviews(url2, "Noise Master Buds 1", pages=15)

print(f"\nProduct 1 reviews: {len(reviews1)}")
print(f"Product 2 reviews: {len(reviews2)}")




