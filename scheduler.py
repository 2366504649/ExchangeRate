from apscheduler.schedulers.blocking import BlockingScheduler
from fetcher import fetch_rates
from app import app, db
import datetime

def scheduled_job():
    print(f"Starting scheduled fetch at {datetime.datetime.now()}")
    with app.app_context():
        db.create_all() # Ensure tables exist
        fetch_rates()
    print("Fetch completed.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule to run every day at 09:00 AM
    scheduler.add_job(scheduled_job, 'cron', hour=9, minute=0)
    print("Scheduler started. Will run daily at 09:00.")
    
    # Also run once immediately on start if needed, or just wait.
    # scheduled_job() 
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
