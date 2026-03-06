CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    product_id TEXT,
    rating INTEGER,
    title TEXT,
    text TEXT,
    date TEXT,
    sentiment TEXT,
    themes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);