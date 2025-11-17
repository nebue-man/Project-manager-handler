"""
Notification service for the Project Manager application.
Handles desktop notifications using plyer library.
"""

import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from plyer import notification
except ImportError:
    print("Warning: plyer not available. Notifications disabled.")
    notification = None

class NotificationService:
    """Manages desktop notifications."""

    def __init__(self):
        """Initialize notification service."""
        self.app_name = "Project Manager"
        self.app_icon = None  # Could be set to path to icon file
        self.enabled = True
        self.last_notification_time = 0
        self.notification_cooldown = 5  # seconds between notifications

    def is_available(self) -> bool:
        """Check if notification service is available."""
        return notification is not None

    def show_notification(self, title: str, message: str,
                         timeout: int = 10, urgency: str = 'normal') -> bool:
        """
        Show a desktop notification.

        Args:
            title: Notification title
            message: Notification message
            timeout: Time to show notification (seconds)
            urgency: Notification urgency ('low', 'normal', 'critical')

        Returns:
            True if notification was shown, False otherwise
        """
        if not self.is_available() or not self.enabled:
            return False

        # Prevent notification spam
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            return False

        try:
            # Use plyer for cross-platform notifications
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                app_icon=self.app_icon,
                timeout=timeout,
                urgency=urgency
            )

            self.last_notification_time = current_time
            return True

        except Exception as e:
            print(f"Error showing notification: {e}")
            return False

    def show_deadline_notification(self, project_name: str, days_remaining: int,
                                  priority: str = 'medium') -> bool:
        """
        Show deadline notification for a project.

        Args:
            project_name: Name of the project
            days_remaining: Days remaining until deadline
            priority: Project priority

        Returns:
            True if notification was shown
        """
        if days_remaining < 0:
            title = "Project Deadline Overdue!"
            message = f"'{project_name}' is {abs(days_remaining)} days overdue!"
            urgency = 'critical'
        elif days_remaining == 0:
            title = "Project Deadline Today!"
            message = f"'{project_name}' deadline is today!"
            urgency = 'critical'
        elif days_remaining <= 3:
            title = f"Project Deadline in {days_remaining} Days"
            message = f"'{project_name}' deadline is approaching!"
            urgency = 'high'
        else:
            title = f"Project Deadline in {days_remaining} Days"
            message = f"'{project_name}' deadline reminder."
            urgency = 'normal'

        return self.show_notification(title, message, urgency=urgency)

    def show_learning_notification(self, learning_title: str, learning_content: str,
                                  project_name: Optional[str] = None) -> bool:
        """
        Show learning reminder notification.

        Args:
            learning_title: Title of the learning
            learning_content: Content of the learning (will be truncated)
            project_name: Optional project name

        Returns:
            True if notification was shown
        """
        # Truncate learning content for notification
        max_content_length = 100
        if len(learning_content) > max_content_length:
            learning_content = learning_content[:max_content_length - 3] + "..."

        title = "Learning Reminder"

        if project_name:
            message = f"From {project_name}:\n{learning_title}\n\n{learning_content}"
        else:
            message = f"{learning_title}\n\n{learning_content}"

        return self.show_notification(title, message, timeout=15)

    def show_project_created_notification(self, project_name: str) -> bool:
        """Show notification when project is created."""
        return self.show_notification(
            "Project Created",
            f"Project '{project_name}' has been created successfully."
        )

    def show_learning_created_notification(self, learning_title: str) -> bool:
        """Show notification when learning is captured."""
        return self.show_notification(
            "Learning Captured",
            f"Learning '{learning_title}' has been saved."
        )

    def show_project_completed_notification(self, project_name: str) -> bool:
        """Show notification when project is completed."""
        return self.show_notification(
            "Project Completed!",
            f"Congratulations! Project '{project_name}' has been completed.",
            urgency='high'
        )

    def show_backup_notification(self, backup_successful: bool) -> bool:
        """Show backup status notification."""
        if backup_successful:
            return self.show_notification(
                "Backup Successful",
                "Database backup completed successfully."
            )
        else:
            return self.show_notification(
                "Backup Failed",
                "Database backup failed. Please check logs.",
                urgency='high'
            )

    def show_error_notification(self, error_message: str) -> bool:
        """Show error notification."""
        return self.show_notification(
            "Error",
            error_message,
            urgency='critical'
        )

    def show_success_notification(self, success_message: str) -> bool:
        """Show success notification."""
        return self.show_notification(
            "Success",
            success_message
        )

    def set_enabled(self, enabled: bool):
        """Enable or disable notifications."""
        self.enabled = enabled

    def is_enabled(self) -> bool:
        """Check if notifications are enabled."""
        return self.enabled

    def test_notification(self) -> bool:
        """Send a test notification."""
        return self.show_notification(
            "Test Notification",
            "If you see this, notifications are working correctly!"
        )

    def get_notification_capabilities(self) -> Dict[str, Any]:
        """
        Get information about notification capabilities.

        Returns:
            Dictionary with notification capabilities
        """
        return {
            'available': self.is_available(),
            'enabled': self.is_enabled(),
            'supports_urgency': True,
            'supports_timeout': True,
            'supports_sound': True,  # Most platforms support sound
            'app_name': self.app_name
        }

    def configure_sound(self, enabled: bool):
        """Configure notification sound (if supported by platform)."""
        # This is a placeholder - sound configuration would need
        # platform-specific implementation
        pass

    def configure_urgency_levels(self, urgency_mapping: Dict[str, str]):
        """
        Configure urgency level mappings.

        Args:
            urgency_mapping: Mapping of notification types to urgency levels
        """
        # Store custom urgency mapping for future use
        self.urgency_mapping = urgency_mapping

class SilentNotificationService(NotificationService):
    """Silent notification service for testing or when notifications should be disabled."""

    def __init__(self):
        """Initialize silent notification service."""
        super().__init__()
        self.enabled = False
        self.notification_log = []  # Keep track of notifications that would have been sent

    def show_notification(self, title: str, message: str,
                         timeout: int = 10, urgency: str = 'normal') -> bool:
        """Log notification instead of showing it."""
        self.notification_log.append({
            'title': title,
            'message': message,
            'timeout': timeout,
            'urgency': urgency,
            'timestamp': datetime.now().isoformat()
        })
        return True

    def get_notification_log(self) -> list:
        """Get list of notifications that would have been shown."""
        return self.notification_log.copy()

    def clear_notification_log(self):
        """Clear the notification log."""
        self.notification_log.clear()