from groq import Groq
from database.db import get_connection
from datetime import datetime
import os

client = Groq()

def get_all_reviews_text(product=None):
    conn = get_connection()
    cursor = conn.cursor()
    if product:
        cursor.execute("SELECT product, rating, title, text, sentiment, themes FROM reviews WHERE product = ?", (product,))
    else:
        cursor.execute("SELECT product, rating, title, text, sentiment, themes FROM reviews")
    rows = cursor.fetchall()
    conn.close()
    return rows

def format_reviews_for_prompt(rows):
    formatted = ""
    for r in rows:
        product, rating, title, text, sentiment, themes = r
        formatted += f"Product: {product} | Rating: {rating} | Sentiment: {sentiment} | Themes: {themes}\nReview: {text}\n\n"
    return formatted

def generate_global_report():
    print("Generating Global Action Item Report...")
    rows = get_all_reviews_text()
    reviews_text = format_reviews_for_prompt(rows)

    prompt = f"""You are a Voice of Customer analyst. Based on the following product reviews, generate a structured Action Item Report segmented by department.

REVIEWS:
{reviews_text}

Use this exact format:

## 1. PRODUCT TEAM
- **[Issue]**: [specific action needed] (Evidence: "[quote from review]")

## 2. MARKETING TEAM
- **[Opportunity]**: [specific recommendation] (Evidence: "[quote from review]")

## 3. SUPPORT TEAM
- **[Issue]**: [troubleshooting guide or action needed] (Evidence: "[quote from review]")

List at least 4 bullet points per section. Be specific and actionable."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    report = response.choices[0].message.content
    save_report(report, "global_action_items")
    return report

def generate_weekly_delta_report(new_reviews):
    if not new_reviews:
        print("No new reviews to analyze.")
        return

    print("Generating Weekly Delta Report...")
    reviews_text = ""
    for r in new_reviews:
        reviews_text += f"Product: {r['product']} | Rating: {r['rating']} | Title: {r['title']}\nReview: {r['text']}\n\n"

    prompt = f"""You are a Voice of Customer analyst. Based on ONLY these NEW reviews from this week, generate a Weekly Delta Report highlighting any sudden spikes in complaints or praise.

NEW REVIEWS THIS WEEK:
{reviews_text}

Use this exact format:

## 1. SUDDEN SPIKES
- **[Theme]**: [description of spike and why it matters]

## 2. PRODUCT TEAM
- **[Issue]**: [urgent action needed] (Evidence: "[quote from review]")

## 3. MARKETING TEAM
- **[Opportunity]**: [action to take] (Evidence: "[quote from review]")

## 4. SUPPORT TEAM
- **[Issue]**: [action to take] (Evidence: "[quote from review]")

Be specific and cite the reviews. List at least 3 bullet points per section."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    report = response.choices[0].message.content
    save_report(report, "weekly_delta")
    return report

def save_report(content, report_type):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{report_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(filename, "w") as f:
        f.write(f"# VoC {report_type.replace('_', ' ').title()} Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(content)
    print(f"Report saved to {filename}")

if __name__ == "__main__":
    generate_global_report()