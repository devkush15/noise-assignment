from groq import Groq
import json

client = Groq()

THEMES = [
    "Sound Quality",
    "Battery Life",
    "Comfort/Fit",
    "App Experience",
    "Price/Value",
    "Delivery",
    "Build Quality",
    "ANC"
]

def analyze_review(text):
    prompt = f"""Analyze this product review and return ONLY a JSON object with no extra text, no markdown, no backticks:

Review: "{text}"

Return exactly this format:
{{
    "sentiment": "Positive" or "Negative" or "Neutral",
    "themes": ["theme1", "theme2"]
}}

Only use themes from this list: {THEMES}
Pick 1-3 most relevant themes only."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result = response.choices[0].message.content.strip()
    return json.loads(result)

def process_unanalyzed_reviews():
    from database.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM reviews WHERE sentiment IS NULL")
    unanalyzed = cursor.fetchall()
    print(f"Found {len(unanalyzed)} unanalyzed reviews...")

    for review_id, text in unanalyzed:
        try:
            result = analyze_review(text)
            themes_str = ", ".join(result["themes"])

            cursor.execute('''
                UPDATE reviews
                SET sentiment = ?, themes = ?
                WHERE id = ?
            ''', (result["sentiment"], themes_str, review_id))

            print(f"✓ Review {review_id}: {result['sentiment']} | {themes_str}")
        except Exception as e:
            print(f"✗ Review {review_id} failed: {e}")
            continue

    conn.commit()
    conn.close()
    print("\nAnalysis complete!")

if __name__ == "__main__":
    process_unanalyzed_reviews()