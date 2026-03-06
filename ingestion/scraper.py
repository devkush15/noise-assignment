from database.db import insert_review
from playwright.sync_api import sync_playwright
import re

JUNK_PHRASES = [
    "ratings and", "review for:", "user reviews", "sorted by",
    "most helpful", "read more", "flipkart"
]

JUNK_TITLES = [
    "latest", "positive", "negative", "most helpful",
    "ago", "month", "day", "year", "week"
]

def is_junk(text):
    text_lower = text.lower()
    if "ago" in text_lower:
        return False
    return any(phrase in text_lower for phrase in JUNK_PHRASES)

def is_junk_title(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in JUNK_TITLES)

def is_rating(text):
    return bool(re.match(r'^[1-5](\.\d)?$', text))

def get_rating(text):
    return int(float(text))

def scrape_flipkart_reviews(url, product_name, pages=3):
    reviews = []
    seen = set()
    product_id = url.split("pid=")[1].split("&")[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_timeout(3000)

        try:
            page.locator("button:has-text('✕')").click(timeout=3000)
        except:
            pass

        for page_num in range(1, pages+1):
            print(f"\nScraping page {page_num}")
            page.goto(f"{url}&page={page_num}")
            page.wait_for_timeout(5000)

            blocks = page.locator("div[dir='auto']").all()
            print("Raw blocks:", len(blocks))

            current_review = {}

            for block in blocks:
                text = block.inner_text().strip()

                if not text or text in seen or is_junk(text):
                    continue

                # rating
                if is_rating(text):
                    # save any pending review without date
                    if "text" in current_review and current_review["text"] not in seen:
                        review = {
                            "product": current_review.get("product", product_name),
                            "product_id": current_review.get("product_id", product_id),
                            "rating": current_review.get("rating", 0),
                            "title": current_review.get("title", ""),
                            "text": current_review["text"],
                            "date": current_review.get("date", ""),
                            "sentiment": None,
                            "themes": None
                        }
                        reviews.append(review)
                        seen.add(current_review["text"])
                        insert_review(review)

                    current_review = {
                        "product": product_name,
                        "product_id": product_id,
                        "rating": get_rating(text)
                    }

                # date
                elif ("ago" in text.lower() or "month" in text.lower() or "week" in text.lower() or "day" in text.lower()) and "text" in current_review:
                    current_review["date"] = text.replace("·", "").replace("Verified Purchase", "").strip()

                    if current_review["text"] not in seen:
                        review = {
                            "product": current_review.get("product", product_name),
                            "product_id": current_review.get("product_id", product_id),
                            "rating": current_review.get("rating", 0),
                            "title": current_review.get("title", ""),
                            "text": current_review["text"],
                            "date": current_review["date"],
                            "sentiment": None,
                            "themes": None
                        }
                        reviews.append(review)
                        seen.add(current_review["text"])
                        insert_review(review)
                        current_review = {}

                # title
                elif "rating" in current_review and "title" not in current_review and 5 < len(text) < 100:
                    if not is_junk_title(text):
                        current_review["title"] = text

                # review body
                elif "rating" in current_review and "title" in current_review and "text" not in current_review and len(text) > 15:
                    current_review["text"] = text.replace("... more", "").strip()

        browser.close()

    print(f"\nTotal reviews scraped and saved: {len(reviews)}")
    return reviews