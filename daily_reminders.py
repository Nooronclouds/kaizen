"""
Daily reminder system for Kaizen adaptive learning platform.

Schedules and sends daily learning reminders at customizable times
with personality-driven messages.
"""

import schedule
import time
import threading
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional
import data_manager
from notification_service import NotificationService
from streak_tracker import StreakTracker


class DailyReminderScheduler:
    """
    Manages daily learning reminders for all users.

    Features:
    - Customizable reminder times per user
    - Personality-driven reminder messages
    - Streak-aware notifications
    - Automatic scheduling and management
    - Background thread execution
    """

    def __init__(self):
        """Initialize the reminder scheduler."""
        self.notification_service = NotificationService()
        self.streak_tracker = StreakTracker()
        self.scheduler_thread = None
        self.running = False

    def schedule_user_reminder(self, username: str, reminder_time: str = "09:00"):
        """
        Schedule a daily reminder for a specific user.

        Args:
            username: User's identifier
            reminder_time: Time in HH:MM format (24-hour)
        """
        user_data = data_manager.load_user_data(username)
        if not user_data:
            raise ValueError(f"User {username} not found")

        # Parse time
        try:
            hour, minute = map(int, reminder_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except:
            raise ValueError(f"Invalid time format: {reminder_time}. Use HH:MM format.")

        # Schedule the job
        schedule.every().day.at(reminder_time).do(
            self._send_reminder, username=username
        ).tag(username)

        print(f"✓ Scheduled daily reminder for {username} at {reminder_time}")

    def _send_reminder(self, username: str):
        """
        Send a daily reminder notification to a user.

        Args:
            username: User's identifier
        """
        try:
            # Get streak info
            streak_stats = self.streak_tracker.get_streak_stats(username)

            # Generate streak-aware message
            if streak_stats['current_streak'] > 0:
                # Include streak in notification
                streak_message = self.streak_tracker.get_streak_message(username)
                message = f"{streak_message}\n\nReady for today's lesson?"
            else:
                # Send regular daily notification
                result = self.notification_service.send_daily_notification(username)
                message = result['message']

            # Send notification
            self.notification_service._send_desktop_notification(
                title=f"🌱 Kaizen - Daily Learning Reminder",
                message=message,
                app_name="Kaizen"
            )

            print(f"✓ Sent reminder to {username} at {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            print(f"✗ Error sending reminder to {username}: {e}")

    def schedule_all_users(self, default_time: str = "09:00"):
        """
        Schedule reminders for all existing users.

        Args:
            default_time: Default reminder time for all users
        """
        usernames = data_manager.get_all_usernames()

        if not usernames:
            print("No users found to schedule")
            return

        for username in usernames:
            try:
                self.schedule_user_reminder(username, default_time)
            except Exception as e:
                print(f"✗ Failed to schedule for {username}: {e}")

        print(f"\n✓ Scheduled reminders for {len(usernames)} user(s)")

    def remove_user_reminder(self, username: str):
        """
        Remove scheduled reminders for a user.

        Args:
            username: User's identifier
        """
        schedule.clear(username)
        print(f"✓ Removed reminders for {username}")

    def list_scheduled_jobs(self) -> List[Dict]:
        """
        Get list of all scheduled reminder jobs.

        Returns:
            List of dictionaries with job information
        """
        jobs = []
        for job in schedule.get_jobs():
            jobs.append({
                'next_run': job.next_run,
                'tags': list(job.tags),
                'job': str(job)
            })
        return jobs

    def start_scheduler(self):
        """
        Start the scheduler in a background thread.

        This will run continuously and execute scheduled jobs.
        """
        if self.running:
            print("Scheduler is already running")
            return

        self.running = True

        def run_scheduler():
            print("🚀 Daily reminder scheduler started")
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()

        print("✓ Scheduler running in background")

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        print("✓ Scheduler stopped")

    def get_next_reminder_time(self, username: str) -> Optional[datetime]:
        """
        Get the next scheduled reminder time for a user.

        Args:
            username: User's identifier

        Returns:
            Datetime of next reminder, or None if not scheduled
        """
        for job in schedule.get_jobs(username):
            return job.next_run
        return None


def schedule_daily_notifications(reminder_time: str = "09:00"):
    """
    Main function to schedule daily notifications for all users.

    Args:
        reminder_time: Time to send reminders (HH:MM format)

    Example:
        schedule_daily_notifications("09:00")  # 9 AM daily
        schedule_daily_notifications("20:00")  # 8 PM daily
    """
    scheduler = DailyReminderScheduler()

    # Schedule all users
    scheduler.schedule_all_users(default_time=reminder_time)

    # Show scheduled jobs
    jobs = scheduler.list_scheduled_jobs()
    print(f"\n📅 Scheduled Jobs:")
    for job in jobs:
        tags = ', '.join(job['tags'])
        print(f"  User(s): {tags}")
        print(f"  Next run: {job['next_run']}")
        print()

    return scheduler


if __name__ == "__main__":
    print("="*70)
    print("Daily Reminder System Demo")
    print("="*70 + "\n")

    # Initialize scheduler
    scheduler = DailyReminderScheduler()

    # Get all users
    usernames = data_manager.get_all_usernames()

    if not usernames:
        print("No users found. Create users first using the web app or demos.")
    else:
        print(f"Found {len(usernames)} user(s): {', '.join(usernames)}\n")

        # Demo: Schedule reminders for testing (1 minute from now)
        now = datetime.now()
        test_time = (now + timedelta(minutes=1)).strftime("%H:%M")

        print(f"Demo: Scheduling test reminders for {test_time}")
        print("(In production, use a time like '09:00' for 9 AM)\n")

        for username in usernames[:3]:  # Limit to 3 users for demo
            try:
                scheduler.schedule_user_reminder(username, test_time)
            except Exception as e:
                print(f"Error scheduling {username}: {e}")

        # Show scheduled jobs
        print(f"\n📅 Scheduled Reminders:")
        jobs = scheduler.list_scheduled_jobs()
        for job in jobs:
            print(f"  {job['job']}")
            print(f"  Next run: {job['next_run']}\n")

        print("="*70)
        print("Scheduler Demo Complete!")
        print("="*70)
        print("\nTo run continuously:")
        print("  scheduler = DailyReminderScheduler()")
        print("  scheduler.schedule_all_users('09:00')")
        print("  scheduler.start_scheduler()  # Runs in background")
        print("\nPress Ctrl+C to stop when running")
