import schedule
import time
from scheduler.weekly_run import run_weekly_pipeline

def start():
    print("Scheduler started — pipeline runs every Monday at 9am")
    schedule.every().monday.at("09:00").do(run_weekly_pipeline)
    
    # uncomment to test every minute:
    # schedule.every(1).minutes.do(run_weekly_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_weekly_pipeline()  # run once immediately
    start()