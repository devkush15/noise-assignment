from groq import Groq
from database.db import get_connection
import os

client = Groq()

SOUL = """You are an expert Voice of Customer (VoC) Analyst AI agent. Your name is VocBot.

Your job is to analyze customer reviews and provide actionable insights to Product, Marketing, and Support teams.

RULES:
- Only answer questions based on the review data provided to you
- Always cite specific reviews or patterns as evidence
- Never hallucinate or make up data not present in the reviews
- Be concise, specific, and actionable
- When comparing products, be fair and data-driven
- Always mention sentiment distribution and key themes when relevant"""

def get_reviews_context(query):
    """Fetch relevant reviews from DB based on query keywords"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # get all reviews with sentiment and themes
    cursor.execute("""
        SELECT product, rating, title, text, sentiment, themes 
        FROM reviews 
        ORDER BY product
    """)
    rows = cursor.fetchall()
    conn.close()
    
    context = ""
    for r in rows:
        product, rating, title, text, sentiment, themes = r
        context += f"[{product} | Rating: {rating} | {sentiment} | Themes: {themes}]\n{text}\n\n"
    
    return context

def get_summary_stats():
    """Get summary statistics from DB"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT product, sentiment, COUNT(*) FROM reviews GROUP BY product, sentiment")
    stats = cursor.fetchall()
    
    cursor.execute("SELECT product, themes FROM reviews WHERE themes != ''")
    theme_rows = cursor.fetchall()
    
    conn.close()
    
    stats_text = "REVIEW STATISTICS:\n"
    for row in stats:
        stats_text += f"- {row[0]} | {row[1]}: {row[2]} reviews\n"
    
    return stats_text

def chat(user_message, conversation_history):
    """Send a message and get a response"""
    context = get_reviews_context(user_message)
    stats = get_summary_stats()
    
    system_prompt = f"""{SOUL}

{stats}

REVIEW DATABASE:
{context}

Answer the user's question based strictly on this data."""

    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *conversation_history
        ],
        temperature=0.3
    )
    
    assistant_message = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    return assistant_message, conversation_history

def main():
    print("\n" + "="*50)
    print("Welcome to VocBot - Voice of Customer Analyst")
    print("="*50)
    print("Ask me anything about your product reviews!")
    print("Type 'exit' to quit\n")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
            
        print("\nVocBot: thinking...")
        response, conversation_history = chat(user_input, conversation_history)
        print(f"\nVocBot: {response}\n")
        print("-"*50)

if __name__ == "__main__":
    main()