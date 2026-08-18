from __future__ import annotations

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import AppConfig
from .providers import MarketDataProvider
from .report import generate_report


def run_scheduler(config: AppConfig, provider: MarketDataProvider) -> None:
    if not config.schedule.enabled:
        raise ValueError("Scheduler is disabled in configuration")
    scheduler = BlockingScheduler(timezone=config.report.timezone)

    def job() -> None:
        try:
            result = generate_report(config, provider)
            logging.info("Generated %s with %d quality flags", result.path, len(result.flags))
        except Exception:
            logging.exception("Market Wrap generation failed")

    trigger = CronTrigger(
        day_of_week=config.schedule.weekdays,
        hour=config.schedule.hour,
        minute=config.schedule.minute,
        timezone=config.report.timezone,
    )
    scheduler.add_job(job, trigger, id="daily-market-wrap", max_instances=1, coalesce=True, misfire_grace_time=3600)
    logging.info("Scheduler started: %s", trigger)
    scheduler.start()

