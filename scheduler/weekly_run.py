from ingestion.scraper import scrape_flipkart_reviews
from reporting.report_generator import generate_global_report, generate_weekly_delta_report
from datetime import datetime
import sqlite3
import os

PRODUCTS = [
    {
        "name": "Noise Master Buds Max",
        "url": "https://www.flipkart.com/noise-master-buds-max-sound-bose-segment-leading-anc-dynamic-eq-60-hr-playtime-bluetooth/product-reviews/itm583241394db27?pid=ACCHGZH5WCCGB3Y4&lid=LSTACCHGZH5WCCGB3Y4LI6ZZJ&marketplace=FLIPKART"
    },
    {
        "name": "Noise Master Buds 1",
        "url": "https://www.flipkart.com/noise-master-buds-sound-bose-49db-anc-6-mic-enc-44-hr-battery-spatial-audio-bluetooth/product-reviews/itm965e6651f8980?pid=ACCHE4GYFJ8J2ADE&lid=LSTACCHE4GYFJ8J2ADEQWIFCY&marketplace=FLIPKART"
    }
]

def get_review_count(product_name):
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE product = ?", (product_name,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def write_delta_log(new_reviews):
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/delta_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(log_path, "w") as f:
        f.write(f"Delta Log - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"{'='*50}\n")
        f.write(f"Total new reviews this run: {len(new_reviews)}\n\n")
        f.write("Sample new reviews:\n\n")
        for r in new_reviews[:10]:
            f.write(f"Product: {r['product']}\n")
            f.write(f"Rating: {r['rating']}\n")
            f.write(f"Title: {r['title']}\n")
            f.write(f"Text: {r['text'][:150]}\n")
            f.write(f"{'-'*30}\n")
    print(f"Delta log saved to {log_path}")

def run_weekly_pipeline():
    print(f"\n{'='*50}")
    print(f"Weekly VoC Pipeline Run: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

    all_new_reviews = []

    for product in PRODUCTS:
        print(f"\nScraping {product['name']}...")
        before_count = get_review_count(product['name'])
        reviews = scrape_flipkart_reviews(product['url'], product['name'], pages=5)
        after_count = get_review_count(product['name'])
        new_count = after_count - before_count
        print(f"New reviews added for {product['name']}: {new_count}")
        all_new_reviews.extend(reviews[-new_count:] if new_count > 0 else [])

    # write delta log
    write_delta_log(all_new_reviews)

    # generate weekly delta report
    if all_new_reviews:
        generate_weekly_delta_report(all_new_reviews)

    # generate global report
    generate_global_report()

    print(f"\n✅ Weekly pipeline complete!")

if __name__ == "__main__":
    run_weekly_pipeline()