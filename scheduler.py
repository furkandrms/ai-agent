from apscheduler.schedulers.background import BackgroundScheduler
import time

def start_scheduler(agent, config):
    scheduler = BackgroundScheduler(timezone="UTC")

    for task in agent.tasks:
        frequency = task.config.get("frequency", "daily")

        if frequency == "daily":
            trigger_args = {"hours": 24}
        elif frequency == "hourly":
            trigger_args = {"hours": 1}
        elif frequency == "10min":
            trigger_args = {"minutes": 10}
        else:
            trigger_args = {"hours": 12} 

        scheduler.add_job(
            func=task.execute,
            args=[agent.personality, config],
            trigger="interval",
            **trigger_args
        )

    scheduler.start()

    try:
        print("[SCHEDULER] Starting scheduler.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("[SCHEDULER] Scheduler stopped.")
