from apscheduler.schedulers.background import BackgroundScheduler
import time 

def start_scheduler(agent):
    scheduler = BackgroundScheduler(timezone="UTC")

    for task in agent.tasks:
        frequency = task.config.get("frequency", "daily")

        if frequency == "daily":
            trigger_args = {"seconds": 60}

        elif frequency == "hourly":
            trigger_args = {"seconds": 60}

        elif frequency == "10min": 
            trigger_args = {"seconds": 10}

        else: 
            trigger_args = {"seconds": 60}
        
        scheduler.add_job(
            func=task.execute,
            args=[agent.personality],
            trigger="interval",
            **trigger_args
        )
    
    scheduler.start()

    try: 
        print("[SCHEUDLER] Starting scheduler.")
        while True: 
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("[SCHEDULER] Scheduler stopped.")





