"""
scheduler.py
Menjalankan ingest.py secara berkala (default tiap 60 menit, atur via .env).

Jalankan:
    python scripts/scheduler.py
"""

import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from ingest import run_ingest_all

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("scheduler")

INTERVAL_MINUTES = int(os.getenv("INGEST_INTERVAL_MINUTES", "60"))


def main():
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(run_ingest_all, "interval", minutes=INTERVAL_MINUTES, next_run_time=None)

    logger.info(f"Scheduler aktif, ingest akan berjalan tiap {INTERVAL_MINUTES} menit.")
    logger.info("Menjalankan ingest pertama kali sekarang...")
    run_ingest_all()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler dihentikan.")


if __name__ == "__main__":
    main()