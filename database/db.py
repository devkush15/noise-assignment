import sqlite3

DB_PATH = "data/reviews.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    with open("database/schema.sql", "r") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


def insert_review(review):
    conn = get_connection()
    cursor = conn.cursor()

    # check for duplicate based on product_id and text
    cursor.execute(
        "SELECT id FROM reviews WHERE product_id = ? AND text = ?",
        (review["product_id"], review["text"])
    )
    
    if cursor.fetchone() is not None:
        conn.close()
        return  # skip duplicate

    cursor.execute("""
        INSERT INTO reviews(product, product_id, rating, title, text, date, sentiment, themes)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        review["product"],
        review["product_id"],
        review["rating"],
        review["title"],
        review["text"],
        review["date"],
        review.get("sentiment"),
        review.get("themes")
    ))

    conn.commit()
    conn.close()


def fetch_all_reviews():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews")
    rows = cursor.fetchall()

    conn.close()
    return rows