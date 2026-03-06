# Autonomous Voice of Customer (VoC) Intelligence Agent

An autonomous AI agent that scrapes, processes, and analyzes public e-commerce reviews to generate structured product and competitor intelligence — updated weekly.

## Project Structure
```
voc-agent/
├── agent/
│   └── agent.py          # Conversational VoC analyst chatbot
├── analysis/
│   └── sentiment.py      # Sentiment + theme tagging via Groq
├── data/
│   └── reviews.db        # SQLite database
├── database/
│   ├── db.py             # Database connection and queries
│   └── schema.sql        # Database schema
├── ingestion/
│   ├── scraper.py        # Flipkart scraper using Playwright
│   └── cleaner.py        # Data cleaning utilities
├── logs/                 # Weekly delta logs
├── reporting/
│   └── report_generator.py  # Global + weekly delta reports
├── reports/              # Generated markdown reports
├── scheduler/
│   ├── weekly_run.py     # Weekly pipeline runner
│   └── scheduler.py      # Automated scheduler
├── README.md
├── SOUL.md               # Agent identity and configuration
└── requirements.txt
```

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd voc-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Set environment variables
```bash
export GROQ_API_KEY="your-groq-api-key"
```
Get a free Groq API key at https://console.groq.com

### 4. Initialize the database
```bash
python init_db.py
```

## Usage

### Run the full weekly pipeline manually
```bash
python -m scheduler.weekly_run
```
This will:
- Scrape new reviews from Flipkart
- Save only new reviews to the database (incremental)
- Tag reviews with sentiment and themes
- Generate a Weekly Delta Report
- Generate a Global Action Item Report
- Save a delta log to `logs/`

### Run NLP analysis only
```bash
python -m analysis.sentiment
```

### Generate reports only
```bash
python -m reporting.report_generator
```

### Start the conversational VoC analyst
```bash
python -m agent.agent
```
Then ask questions like:
- "What does Buds 1 do better than Buds Max on ANC?"
- "What are the top complaints about battery life?"
- "What should the marketing team highlight?"

### Start the automated weekly scheduler
```bash
python -m scheduler.scheduler
```
Runs every Monday at 9:00 AM automatically.

## Deliverables
- `reports/global_action_items_*.md` — Global Action Item Report segmented by department
- `reports/weekly_delta_*.md` — Weekly Delta Report highlighting new trends
- `logs/delta_*.txt` — Delta log showing new reviews captured each week
- `data/reviews.db` — SQLite database with all reviews

## Tech Stack
- **Python** — core language
- **Playwright** — browser automation for scraping
- **SQLite** — local database
- **Groq (Llama 3.3)** — LLM for NLP analysis and report generation
- **Schedule** — weekly automation

## Environment Variables
| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for LLM access |
