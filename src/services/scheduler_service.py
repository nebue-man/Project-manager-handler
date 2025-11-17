"""
Scheduler service for the Project Manager application.
Handles background task scheduling using APScheduler.
"""

import threading
import time
from datetime import datetime, time as dt_time, timedelta
from typing import List, Dict, Any, Optional

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.triggers.date import DateTrigger
except ImportError:
    print("Warning: APScheduler not available. Background scheduling disabled.")
    BackgroundScheduler = None

from .notification_service import NotificationService

class SchedulerService:
    """Manages background task scheduling."""

    def __init__(self, notification_service: NotificationService,
                 project_model, learning_model, config):
        """
        Initialize scheduler service.

        Args:
            notification_service: Notification service instance
            project_model: Project model instance
            learning_model: Learning model instance
            config: Configuration instance
        """
        self.scheduler = None
        self.notification_service = notification_service
        self.project_model = project_model
        self.learning_model = learning_model
        self.config = config
        self.running = False
        self.scheduler_thread = None

        if BackgroundScheduler is None:
            print("Scheduler disabled - APScheduler not available")
            return

    def start(self):
        """Start the scheduler service."""
        if BackgroundScheduler is None:
            return

        if self.running:
            return

        try:
            # Create background scheduler
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()
            self.running = True

            # Schedule jobs
            self._schedule_deadline_checks()
            self._schedule_learning_reminders()
            self._schedule_backup_tasks()
            self._schedule_maintenance_tasks()

            print("Scheduler service started successfully")

        except Exception as e:
            print(f"Error starting scheduler service: {e}")

    def stop(self):
        """Stop the scheduler service."""
        if not self.running or not self.scheduler:
            return

        try:
            self.scheduler.shutdown(wait=True)
            self.running = False
            print("Scheduler service stopped")

        except Exception as e:
            print(f"Error stopping scheduler service: {e}")

    def _schedule_deadline_checks(self):
        """Schedule daily deadline checking."""
        if not self.scheduler:
            return

        # Check deadlines every day at 9:00 AM
        self.scheduler.add_job(
            func=self._check_deadlines,
            trigger=CronTrigger(hour=9, minute=0),
            id='deadline_check',
            name='Daily deadline check',
            replace_existing=True
        )

        # Also check deadlines every hour for urgent notifications
        self.scheduler.add_job(
            func=self._check_urgent_deadlines,
            trigger=CronTrigger(minute=0),  # Every hour at minute 0
            id='urgent_deadline_check',
            name='Hourly urgent deadline check',
            replace_existing=True
        )

    def _schedule_learning_reminders(self):
        """Schedule learning reminder notifications."""
        if not self.scheduler:
            return

        notification_settings = self.config.get_notification_settings()
        reminder_times = notification_settings.get('learning_reminder_times', ['09:00', '14:00'])

        for i, reminder_time in enumerate(reminder_times):
            try:
                hour, minute = map(int, reminder_time.split(':'))
                self.scheduler.add_job(
                    func=self._send_learning_reminder,
                    trigger=CronTrigger(hour=hour, minute=minute),
                    id=f'learning_reminder_{i}',
                    name=f'Learning reminder at {reminder_time}',
                    replace_existing=True
                )
            except (ValueError, IndexError):
                print(f"Invalid reminder time format: {reminder_time}")

    def _schedule_backup_tasks(self):
        """Schedule automatic database backups."""
        if not self.scheduler:
            return

        database_settings = self.config.get_database_settings()

        if database_settings.get('backup_enabled', True):
            backup_interval = database_settings.get('backup_interval_days', 7)

            # Schedule backup every N days at 2:00 AM
            self.scheduler.add_job(
                func=self._perform_database_backup,
                trigger=CronTrigger(hour=2, minute=0, day=f'*/{backup_interval}'),
                id='database_backup',
                name='Database backup',
                replace_existing=True
            )

    def _schedule_maintenance_tasks(self):
        """Schedule regular maintenance tasks."""
        if not self.scheduler:
            return

        # Cleanup old temporary files daily at 3:00 AM
        self.scheduler.add_job(
            func=self._cleanup_temp_files,
            trigger=CronTrigger(hour=3, minute=0),
            id='cleanup_temp_files',
            name='Cleanup temporary files',
            replace_existing=True
        )

        # Update statistics every hour
        self.scheduler.add_job(
            func=self._update_statistics,
            trigger=IntervalTrigger(hours=1),
            id='update_statistics',
            name='Update statistics',
            replace_existing=True
        )

    def _check_deadlines(self):
        """Check for upcoming deadlines and send notifications."""
        try:
            notification_settings = self.config.get_notification_settings()

            if not notification_settings.get('enabled', True):
                return

            # Check quiet hours
            quiet_start = notification_settings.get('quiet_hours_start', '22:00')
            quiet_end = notification_settings.get('quiet_hours_end', '08:00')

            if self._is_quiet_hours(quiet_start, quiet_end):
                return

            # Get warning periods
            warning_days = notification_settings.get('deadline_warnings', ['1', '3', '7'])

            # Check upcoming deadlines
            for days_str in warning_days:
                try:
                    days = int(days_str)
                    upcoming_projects = self.project_model.get_upcoming_deadlines(days)

                    for project in upcoming_projects:
                        deadline_date = datetime.strptime(project['deadline'], '%Y-%m-%d').date()
                        days_remaining = (deadline_date - datetime.now().date()).days

                        self.notification_service.show_deadline_notification(
                            project['name'],
                            days_remaining,
                            project['priority']
                        )

                except ValueError:
                    continue

        except Exception as e:
            print(f"Error checking deadlines: {e}")

    def _check_urgent_deadlines(self):
        """Check for very urgent deadlines (today or overdue)."""
        try:
            notification_settings = self.config.get_notification_settings()

            if not notification_settings.get('enabled', True):
                return

            # Get projects due today or overdue
            upcoming_projects = self.project_model.get_upcoming_deadlines(1)
            overdue_projects = self.project_model.get_overdue_projects()

            # Process overdue projects
            for project in overdue_projects:
                deadline_date = datetime.strptime(project['deadline'], '%Y-%m-%d').date()
                days_remaining = (deadline_date - datetime.now().date()).days

                self.notification_service.show_deadline_notification(
                    project['name'],
                    days_remaining,
                    project['priority']
                )

            # Process projects due today (but not already notified)
            for project in upcoming_projects:
                deadline_date = datetime.strptime(project['deadline'], '%Y-%m-%d').date()
                days_remaining = (deadline_date - datetime.now().date()).days

                if days_remaining == 0:  # Due today
                    self.notification_service.show_deadline_notification(
                        project['name'],
                        days_remaining,
                        project['priority']
                    )

        except Exception as e:
            print(f"Error checking urgent deadlines: {e}")

    def _send_learning_reminder(self):
        """Send random learning reminder notification."""
        try:
            notification_settings = self.config.get_notification_settings()

            if not notification_settings.get('enabled', True):
                return

            # Check quiet hours
            quiet_start = notification_settings.get('quiet_hours_start', '22:00')
            quiet_end = notification_settings.get('quiet_hours_end', '08:00')

            if self._is_quiet_hours(quiet_start, quiet_end):
                return

            # Get random learning
            random_learnings = self.learning_model.get_random(limit=1)

            if random_learnings:
                learning = random_learnings[0]
                self.notification_service.show_learning_notification(
                    learning['title'],
                    learning['content'],
                    learning.get('project_name')
                )

        except Exception as e:
            print(f"Error sending learning reminder: {e}")

    def _perform_database_backup(self):
        """Perform automatic database backup."""
        try:
            # This is a placeholder - actual backup implementation would be here
            # For now, just show a notification
            backup_successful = True  # Would be actual backup result
            self.notification_service.show_backup_notification(backup_successful)

        except Exception as e:
            print(f"Error performing database backup: {e}")
            self.notification_service.show_backup_notification(False)

    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            # Placeholder for cleanup implementation
            pass

        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")

    def _update_statistics(self):
        """Update application statistics."""
        try:
            # Placeholder for statistics update
            pass

        except Exception as e:
            print(f"Error updating statistics: {e}")

    def _is_quiet_hours(self, start_time: str, end_time: str) -> bool:
        """Check if current time is within quiet hours."""
        try:
            now = datetime.now().time()
            start = dt_time.fromisoformat(start_time)
            end = dt_time.fromisoformat(end_time)

            if start <= end:
                # Same day range (e.g., 08:00 to 22:00)
                return start <= now <= end
            else:
                # Overnight range (e.g., 22:00 to 08:00)
                return now >= start or now <= end

        except ValueError:
            return False

    def add_custom_job(self, func, trigger, job_id: str, **kwargs):
        """
        Add a custom job to the scheduler.

        Args:
            func: Function to execute
            trigger: APScheduler trigger
            job_id: Unique job identifier
            **kwargs: Additional job arguments
        """
        if not self.scheduler:
            return False

        try:
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                replace_existing=True,
                **kwargs
            )
            return True

        except Exception as e:
            print(f"Error adding custom job: {e}")
            return False

    def remove_job(self, job_id: str) -> bool:
        """
        Remove a job from the scheduler.

        Args:
            job_id: Job identifier to remove

        Returns:
            True if job was removed, False otherwise
        """
        if not self.scheduler:
            return False

        try:
            self.scheduler.remove_job(job_id)
            return True

        except Exception as e:
            print(f"Error removing job: {e}")
            return False

    def get_scheduled_jobs(self) -> List[Dict[str, Any]]:
        """
        Get list of scheduled jobs.

        Returns:
            List of job information dictionaries
        """
        if not self.scheduler:
            return []

        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
            return jobs

        except Exception as e:
            print(f"Error getting scheduled jobs: {e}")
            return []

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self.running and self.scheduler is not None