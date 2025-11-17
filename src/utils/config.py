"""
Configuration management for the Project Manager application.
Handles application settings and preferences.
"""

import os
import json
from typing import Dict, Any, List

class Config:
    """Manages application configuration."""

    def __init__(self):
        """Initialize configuration with default values."""
        self.config_file = "config.json"
        self.default_config = {
            "app": {
                "name": "Project Manager",
                "version": "1.0.0",
                "window_width": 1200,
                "window_height": 800,
                "remember_window_size": True,
                "minimize_to_tray": False,
                "start_with_system": False
            },
            "notifications": {
                "enabled": True,
                "learning_reminder_times": ["09:00", "14:00"],
                "deadline_warnings": ["1", "3", "7"],  # days before deadline
                "quiet_hours_start": "22:00",
                "quiet_hours_end": "08:00",
                "sound_enabled": True
            },
            "ui": {
                "theme": "light",  # light, dark, system
                "font_size": 12,
                "items_per_page": 20,
                "auto_refresh_interval": 30  # seconds
            },
            "database": {
                "path": "project_manager.db",
                "backup_enabled": True,
                "backup_interval_days": 7,
                "max_backups": 10
            },
            "features": {
                "auto_save": True,
                "auto_save_interval": 300,  # seconds
                "export_format": "json",  # json, csv
                "date_format": "%Y-%m-%d",
                "time_format": "%H:%M"
            }
        }
        self._config = {}

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create with defaults."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to handle new settings
                self._config = self._merge_configs(self.default_config, loaded_config)
            else:
                self._config = self.default_config.copy()
                self.save_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            self._config = self.default_config.copy()

        return self._config

    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False

    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Merge loaded config with defaults, preserving structure."""
        merged = default.copy()
        for key, value in loaded.items():
            if key in merged:
                if isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = self._merge_configs(merged[key], value)
                else:
                    merged[key] = value
        return merged

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by key path.

        Args:
            key_path: Dot-separated path (e.g., 'app.window_width')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if not self._config:
            self.load_config()

        keys = key_path.split('.')
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any) -> bool:
        """
        Set configuration value by key path.

        Args:
            key_path: Dot-separated path (e.g., 'app.window_width')
            value: Value to set

        Returns:
            True if successful, False otherwise
        """
        if not self._config:
            self.load_config()

        keys = key_path.split('.')
        config = self._config

        try:
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]

            # Set the value
            config[keys[-1]] = value
            return True
        except (KeyError, TypeError):
            return False

    def get_window_geometry(self) -> Dict[str, int]:
        """Get window size and position."""
        return {
            'width': self.get('app.window_width', 1200),
            'height': self.get('app.window_height', 800)
        }

    def set_window_geometry(self, width: int, height: int) -> bool:
        """Set window size and position."""
        return self.set('app.window_width', width) and self.set('app.window_height', height)

    def get_notification_settings(self) -> Dict[str, Any]:
        """Get notification-related settings."""
        return {
            'enabled': self.get('notifications.enabled', True),
            'learning_reminder_times': self.get('notifications.learning_reminder_times', ["09:00", "14:00"]),
            'deadline_warnings': self.get('notifications.deadline_warnings', ["1", "3", "7"]),
            'quiet_hours_start': self.get('notifications.quiet_hours_start', "22:00"),
            'quiet_hours_end': self.get('notifications.quiet_hours_end', "08:00"),
            'sound_enabled': self.get('notifications.sound_enabled', True)
        }

    def set_notification_settings(self, settings: Dict[str, Any]) -> bool:
        """Update notification settings."""
        success = True
        for key, value in settings.items():
            full_key = f'notifications.{key}'
            success = self.set(full_key, value) and success
        return success

    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI-related settings."""
        return {
            'theme': self.get('ui.theme', 'light'),
            'font_size': self.get('ui.font_size', 12),
            'items_per_page': self.get('ui.items_per_page', 20),
            'auto_refresh_interval': self.get('ui.auto_refresh_interval', 30)
        }

    def set_ui_settings(self, settings: Dict[str, Any]) -> bool:
        """Update UI settings."""
        success = True
        for key, value in settings.items():
            full_key = f'ui.{key}'
            success = self.set(full_key, value) and success
        return success

    def get_database_settings(self) -> Dict[str, Any]:
        """Get database-related settings."""
        return {
            'path': self.get('database.path', 'project_manager.db'),
            'backup_enabled': self.get('database.backup_enabled', True),
            'backup_interval_days': self.get('database.backup_interval_days', 7),
            'max_backups': self.get('database.max_backups', 10)
        }

    def reset_to_defaults(self) -> bool:
        """Reset all configuration to default values."""
        self._config = self.default_config.copy()
        return self.save_config()

# Global configuration instance
config = Config()