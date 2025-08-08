"""Scheduling functionality for AI News Agent"""

import schedule
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Callable, Optional


class NewsScheduler:
    """Handles scheduling of daily news processes"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.scheduler')
        
        # Get scheduling configuration
        scheduling_config = self.config.get('scheduling', {})
        self.daily_time = scheduling_config.get('daily_time', '08:00')
        self.timezone = scheduling_config.get('timezone', 'UTC')
        self.enabled = scheduling_config.get('enabled', True)
        
        self.is_running = False
        self.scheduler_thread = None
    
    def schedule_daily_task(self, task_function: Callable):
        """
        Schedule a daily task to run at the configured time
        
        Args:
            task_function: Function to call daily
        """
        try:
            self.logger.info(f"Scheduling daily task for {self.daily_time}")
            
            # Clear any existing schedules
            schedule.clear()
            
            # Schedule the task
            schedule.every().day.at(self.daily_time).do(self._safe_task_execution, task_function)
            
            self.logger.info(f"Daily task scheduled successfully for {self.daily_time}")
            
        except Exception as e:
            self.logger.error(f"Error scheduling daily task: {e}")
            raise
    
    def _safe_task_execution(self, task_function: Callable):
        """Safely execute task with error handling"""
        try:
            self.logger.info("Executing scheduled daily task")
            task_function()
            self.logger.info("Scheduled task completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in scheduled task execution: {e}")
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if self.is_running:
            self.logger.warning("Scheduler is already running")
            return
        
        if not self.enabled:
            self.logger.info("Scheduling is disabled in configuration")
            return
        
        try:
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            self.logger.info("Scheduler started successfully")
            
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {e}")
            self.is_running = False
            raise
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if not self.is_running:
            self.logger.warning("Scheduler is not running")
            return
        
        try:
            self.is_running = False
            schedule.clear()
            
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=5)
            
            self.logger.info("Scheduler stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {e}")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        self.logger.info("Scheduler loop started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Continue after error
        
        self.logger.info("Scheduler loop ended")
    
    def run_once_now(self, task_function: Callable):
        """Run the task immediately (for testing)"""
        try:
            self.logger.info("Running task immediately")
            self._safe_task_execution(task_function)
            
        except Exception as e:
            self.logger.error(f"Error running immediate task: {e}")
            raise
    
    def get_next_run_time(self) -> Optional[datetime]:
        """Get the next scheduled run time"""
        try:
            jobs = schedule.get_jobs()
            if not jobs:
                return None
            
            next_run = jobs[0].next_run
            return next_run
            
        except Exception as e:
            self.logger.error(f"Error getting next run time: {e}")
            return None
    
    def get_schedule_info(self) -> dict:
        """Get information about the current schedule"""
        return {
            'enabled': self.enabled,
            'daily_time': self.daily_time,
            'timezone': self.timezone,
            'is_running': self.is_running,
            'next_run': self.get_next_run_time(),
            'jobs_count': len(schedule.get_jobs())
        }
