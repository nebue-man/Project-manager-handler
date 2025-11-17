"""
Settings Dialog for the Project Manager application.
Allows users to configure application preferences.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from typing import Dict, Any, Optional, Callable
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import config

class SettingsDialog(ctk.CTkToplevel):
    """Dialog for application settings."""

    def __init__(self, parent, app_config, notification_service=None, callback: Callable = None):
        """
        Initialize settings dialog.

        Args:
            parent: Parent window
            app_config: Configuration instance
            notification_service: Notification service instance
            callback: Optional callback function called after settings save
        """
        super().__init__(parent)

        # Store references
        self.config = app_config
        self.notification_service = notification_service
        self.callback = callback

        # Dialog configuration
        self.title("Settings")
        self.geometry("700x600")
        self.minsize(600, 500)
        self.resizable(True, True)

        # Make dialog modal (with error handling)
        self.transient(parent)
        try:
            self.grab_set()
        except Exception as e:
            # If grab_set fails, continue without modal behavior
            print(f"Warning: Could not set modal behavior: {e}")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Initialize variables
        self._init_variables()

        # Create UI components
        self._create_widgets()

        # Load current settings
        self._load_settings()

        # Center dialog relative to parent
        self._center_dialog(parent)

    def _init_variables(self):
        """Initialize form variables."""
        # Notification settings
        self.notifications_enabled_var = tk.BooleanVar()
        self.learning_reminder_times_var = tk.StringVar()
        self.deadline_warnings_var = tk.StringVar()
        self.quiet_hours_start_var = tk.StringVar()
        self.quiet_hours_end_var = tk.StringVar()
        self.sound_enabled_var = tk.BooleanVar()

        # UI settings
        self.theme_var = tk.StringVar()
        self.font_size_var = tk.IntVar()
        self.items_per_page_var = tk.IntVar()

        # Database settings
        self.backup_enabled_var = tk.BooleanVar()
        self.backup_interval_var = tk.IntVar()
        self.max_backups_var = tk.IntVar()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Application Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabview for settings categories
        self.settings_tabview = ctk.CTkTabview(self)
        self.settings_tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        # Create tabs
        self._create_notifications_tab()
        self._create_ui_tab()
        self._create_database_tab()
        self._create_about_tab()

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)

        # Test notifications button
        self.test_notifications_btn = ctk.CTkButton(
            button_frame,
            text="🔔 Test Notifications",
            command=self._test_notifications,
            width=140,
            height=40
        )
        self.test_notifications_btn.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=120,
            height=40
        )
        self.cancel_btn.grid(row=0, column=1, padx=(0, 10))

        # Save button
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Save Settings",
            command=self._on_save,
            width=120,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_btn.grid(row=0, column=2)

    def _create_notifications_tab(self):
        """Create notifications settings tab."""
        self.notifications_tab = self.settings_tabview.add("Notifications")

        # Scrollable frame for settings
        scrollable = ctk.CTkScrollableFrame(self.notifications_tab)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Enable notifications
        self.notifications_enabled_check = ctk.CTkCheckBox(
            scrollable,
            text="Enable Notifications",
            variable=self.notifications_enabled_var,
            command=self._toggle_notification_settings
        )
        self.notifications_enabled_check.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")

        # Separator
        separator1 = ctk.CTkFrame(scrollable, height=2)
        separator1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Learning reminders section
        learning_reminders_label = ctk.CTkLabel(
            scrollable,
            text="Learning Reminders",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        learning_reminders_label.grid(row=2, column=0, padx=10, pady=(20, 10), sticky="w")

        learning_reminders_help = ctk.CTkLabel(
            scrollable,
            text="Show random learning reminders at specified times",
            font=ctk.CTkFont(size=12),
            text_color="#666"
        )
        learning_reminders_help.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        self.learning_reminder_times_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.learning_reminder_times_var,
            placeholder_text="09:00, 14:00",
            width=200
        )
        self.learning_reminder_times_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")

        learning_times_help = ctk.CTkLabel(
            scrollable,
            text="Format: HH:MM, HH:MM (24-hour format)",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        )
        learning_times_help.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="w")

        # Separator
        separator2 = ctk.CTkFrame(scrollable, height=2)
        separator2.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Deadline warnings section
        deadline_warnings_label = ctk.CTkLabel(
            scrollable,
            text="Deadline Warnings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        deadline_warnings_label.grid(row=7, column=0, padx=10, pady=(20, 10), sticky="w")

        deadline_warnings_help = ctk.CTkLabel(
            scrollable,
            text="Get notified before project deadlines",
            font=ctk.CTkFont(size=12),
            text_color="#666"
        )
        deadline_warnings_help.grid(row=8, column=0, padx=10, pady=(0, 10), sticky="w")

        self.deadline_warnings_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.deadline_warnings_var,
            placeholder_text="1, 3, 7",
            width=200
        )
        self.deadline_warnings_entry.grid(row=9, column=0, padx=10, pady=(0, 5), sticky="w")

        deadline_warnings_help = ctk.CTkLabel(
            scrollable,
            text="Days before deadline: 1, 3, 7 (comma-separated)",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        )
        deadline_warnings_help.grid(row=10, column=0, padx=10, pady=(0, 20), sticky="w")

        # Separator
        separator3 = ctk.CTkFrame(scrollable, height=2)
        separator3.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

        # Quiet hours section
        quiet_hours_label = ctk.CTkLabel(
            scrollable,
            text="Quiet Hours",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        quiet_hours_label.grid(row=12, column=0, padx=10, pady=(20, 10), sticky="w")

        quiet_hours_help = ctk.CTkLabel(
            scrollable,
            text="Disable notifications during specified hours",
            font=ctk.CTkFont(size=12),
            text_color="#666"
        )
        quiet_hours_help.grid(row=13, column=0, padx=10, pady=(0, 10), sticky="w")

        # Quiet hours frame
        quiet_hours_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        quiet_hours_frame.grid(row=14, column=0, padx=10, pady=(0, 20), sticky="w")

        ctk.CTkLabel(quiet_hours_frame, text="From:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.quiet_hours_start_entry = ctk.CTkEntry(
            quiet_hours_frame,
            textvariable=self.quiet_hours_start_var,
            placeholder_text="22:00",
            width=100
        )
        self.quiet_hours_start_entry.grid(row=0, column=1, padx=(0, 20))

        ctk.CTkLabel(quiet_hours_frame, text="To:").grid(row=0, column=2, padx=(0, 5), sticky="w")
        self.quiet_hours_end_entry = ctk.CTkEntry(
            quiet_hours_frame,
            textvariable=self.quiet_hours_end_var,
            placeholder_text="08:00",
            width=100
        )
        self.quiet_hours_end_entry.grid(row=0, column=3)

        # Sound checkbox
        self.sound_enabled_check = ctk.CTkCheckBox(
            scrollable,
            text="Enable notification sounds",
            variable=self.sound_enabled_var
        )
        self.sound_enabled_check.grid(row=15, column=0, padx=10, pady=(20, 10), sticky="w")

    def _create_ui_tab(self):
        """Create UI settings tab."""
        self.ui_tab = self.settings_tabview.add("Appearance")

        # Scrollable frame for settings
        scrollable = ctk.CTkScrollableFrame(self.ui_tab)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Theme section
        theme_label = ctk.CTkLabel(
            scrollable,
            text="Theme",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        theme_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        self.theme_option = ctk.CTkOptionMenu(
            scrollable,
            variable=self.theme_var,
            values=["light", "dark", "system"],
            width=200
        )
        self.theme_option.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="w")

        # Separator
        separator1 = ctk.CTkFrame(scrollable, height=2)
        separator1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Font settings section
        font_label = ctk.CTkLabel(
            scrollable,
            text="Font Size",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        font_label.grid(row=3, column=0, padx=10, pady=(20, 10), sticky="w")

        self.font_size_slider = ctk.CTkSlider(
            scrollable,
            from_=10,
            to=18,
            variable=self.font_size_var,
            width=200,
            number_of_steps=9
        )
        self.font_size_slider.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")

        self.font_size_label = ctk.CTkLabel(
            scrollable,
            text="12px",
            font=ctk.CTkFont(size=12)
        )
        self.font_size_label.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="w")

        # Bind slider change
        self.font_size_slider.configure(command=self._update_font_size_label)

        # Separator
        separator2 = ctk.CTkFrame(scrollable, height=2)
        separator2.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Display settings section
        display_label = ctk.CTkLabel(
            scrollable,
            text="Display Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        display_label.grid(row=7, column=0, padx=10, pady=(20, 10), sticky="w")

        ctk.CTkLabel(scrollable, text="Items per page:").grid(row=8, column=0, padx=10, pady=(0, 5), sticky="w")
        self.items_per_page_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.items_per_page_var,
            width=100
        )
        self.items_per_page_entry.grid(row=9, column=0, padx=10, pady=(0, 20), sticky="w")

    def _create_database_tab(self):
        """Create database settings tab."""
        self.database_tab = self.settings_tabview.add("Database")

        # Scrollable frame for settings
        scrollable = ctk.CTkScrollableFrame(self.database_tab)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Backup settings section
        backup_label = ctk.CTkLabel(
            scrollable,
            text="Automatic Backups",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        backup_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        self.backup_enabled_check = ctk.CTkCheckBox(
            scrollable,
            text="Enable automatic backups",
            variable=self.backup_enabled_var,
            command=self._toggle_backup_settings
        )
        self.backup_enabled_check.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="w")

        # Backup interval
        ctk.CTkLabel(scrollable, text="Backup interval (days):").grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        self.backup_interval_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.backup_interval_var,
            width=100
        )
        self.backup_interval_entry.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="w")

        # Max backups
        ctk.CTkLabel(scrollable, text="Maximum backups to keep:").grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")
        self.max_backups_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.max_backups_var,
            width=100
        )
        self.max_backups_entry.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="w")

        # Separator
        separator = ctk.CTkFrame(scrollable, height=2)
        separator.grid(row=6, column=0, padx=10, pady=20, sticky="ew")

        # Manual actions
        actions_label = ctk.CTkLabel(
            scrollable,
            text="Manual Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        actions_label.grid(row=7, column=0, padx=10, pady=(20, 10), sticky="w")

        # Action buttons frame
        actions_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        actions_frame.grid(row=8, column=0, padx=10, pady=(0, 20), sticky="w")

        self.backup_now_btn = ctk.CTkButton(
            actions_frame,
            text="💾 Backup Now",
            command=self._backup_now,
            width=120
        )
        self.backup_now_btn.grid(row=0, column=0, padx=(0, 10))

        self.export_data_btn = ctk.CTkButton(
            actions_frame,
            text="📤 Export Data",
            command=self._export_data,
            width=120
        )
        self.export_data_btn.grid(row=0, column=1, padx=(0, 10))

        self.import_data_btn = ctk.CTkButton(
            actions_frame,
            text="📥 Import Data",
            command=self._import_data,
            width=120
        )
        self.import_data_btn.grid(row=0, column=2)

    def _create_about_tab(self):
        """Create about tab."""
        self.about_tab = self.settings_tabview.add("About")

        # About content
        about_frame = ctk.CTkFrame(self.about_tab)
        about_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # App info
        app_title = ctk.CTkLabel(
            about_frame,
            text="Project Manager",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        app_title.pack(pady=(30, 10))

        version_label = ctk.CTkLabel(
            about_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=16)
        )
        version_label.pack(pady=(0, 20))

        # Description
        desc_text = """A personal project management application designed to help you
track your projects, capture learnings, and stay organized.

Features:
• Project creation and deadline tracking
• Learning capture and documentation
• Desktop notifications for deadlines and reminders
• Clean, intuitive interface
• Data export and backup functionality

Built with Python and CustomTkinter for cross-platform compatibility."""

        desc_label = ctk.CTkLabel(
            about_frame,
            text=desc_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        desc_label.pack(pady=(20, 30), padx=40)

        # GitHub link (placeholder)
        github_btn = ctk.CTkButton(
            about_frame,
            text="📂 View on GitHub",
            width=200
        )
        github_btn.pack(pady=(0, 20))

    def _update_font_size_label(self, value):
        """Update font size label when slider changes."""
        self.font_size_label.configure(text=f"{int(value)}px")

    def _toggle_notification_settings(self):
        """Enable/disable notification-related settings."""
        enabled = self.notifications_enabled_var.get()
        state = "normal" if enabled else "disabled"

        # Enable/disable all notification settings
        for widget in [self.learning_reminder_times_entry, self.deadline_warnings_entry,
                      self.quiet_hours_start_entry, self.quiet_hours_end_entry,
                      self.sound_enabled_check]:
            widget.configure(state=state)

    def _toggle_backup_settings(self):
        """Enable/disable backup-related settings."""
        enabled = self.backup_enabled_var.get()
        state = "normal" if enabled else "disabled"

        # Enable/disable backup settings
        for widget in [self.backup_interval_entry, self.max_backups_entry]:
            widget.configure(state=state)

    def _load_settings(self):
        """Load current settings into form."""
        try:
            # Load notification settings
            notification_settings = self.config.get_notification_settings()
            self.notifications_enabled_var.set(notification_settings.get('enabled', True))
            self.learning_reminder_times_var.set(', '.join(notification_settings.get('learning_reminder_times', ['09:00', '14:00'])))
            self.deadline_warnings_var.set(', '.join(notification_settings.get('deadline_warnings', ['1', '3', '7'])))
            self.quiet_hours_start_var.set(notification_settings.get('quiet_hours_start', '22:00'))
            self.quiet_hours_end_var.set(notification_settings.get('quiet_hours_end', '08:00'))
            self.sound_enabled_var.set(notification_settings.get('sound_enabled', True))

            # Load UI settings
            ui_settings = self.config.get_ui_settings()
            self.theme_var.set(ui_settings.get('theme', 'light'))
            self.font_size_var.set(ui_settings.get('font_size', 12))
            self.items_per_page_var.set(ui_settings.get('items_per_page', 20))

            # Load database settings
            db_settings = self.config.get_database_settings()
            self.backup_enabled_var.set(db_settings.get('backup_enabled', True))
            self.backup_interval_var.set(db_settings.get('backup_interval_days', 7))
            self.max_backups_var.set(db_settings.get('max_backups', 10))

            # Update UI based on current settings
            self._toggle_notification_settings()
            self._toggle_backup_settings()
            self._update_font_size_label(self.font_size_var.get())

        except Exception as e:
            print(f"Error loading settings: {e}")

    def _validate_settings(self) -> bool:
        """Validate settings inputs."""
        try:
            # Validate learning reminder times
            times_text = self.learning_reminder_times_var.get().strip()
            if times_text:
                for time_str in times_text.split(','):
                    time_str = time_str.strip()
                    if not time_str:
                        continue
                    try:
                        hours, minutes = map(int, time_str.split(':'))
                        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Validation Error", f"Invalid time format: {time_str}. Use HH:MM format.")
                        return False

            # Validate deadline warnings
            warnings_text = self.deadline_warnings_var.get().strip()
            if warnings_text:
                for warning_str in warnings_text.split(','):
                    warning_str = warning_str.strip()
                    if not warning_str:
                        continue
                    try:
                        days = int(warning_str)
                        if days < 1:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Validation Error", f"Invalid deadline warning: {warning_str}. Must be positive integers.")
                        return False

            # Validate quiet hours
            quiet_start = self.quiet_hours_start_var.get().strip()
            quiet_end = self.quiet_hours_end_var.get().strip()

            if quiet_start and quiet_end:
                try:
                    start_hours, start_minutes = map(int, quiet_start.split(':'))
                    end_hours, end_minutes = map(int, quiet_end.split(':'))
                    if not (0 <= start_hours <= 23 and 0 <= start_minutes <= 59 and
                           0 <= end_hours <= 23 and 0 <= end_minutes <= 59):
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Validation Error", "Invalid quiet hours format. Use HH:MM format.")
                    return False

            # Validate database settings
            if self.backup_enabled_var.get():
                backup_interval = self.backup_interval_var.get()
                max_backups = self.max_backups_var.get()

                if backup_interval < 1:
                    messagebox.showerror("Validation Error", "Backup interval must be at least 1 day.")
                    return False

                if max_backups < 1:
                    messagebox.showerror("Validation Error", "Maximum backups must be at least 1.")
                    return False

            return True

        except Exception as e:
            messagebox.showerror("Validation Error", f"Settings validation failed: {e}")
            return False

    def _on_save(self):
        """Handle save settings button click."""
        if not self._validate_settings():
            return

        try:
            # Parse and save notification settings
            learning_times = [t.strip() for t in self.learning_reminder_times_var.get().split(',') if t.strip()]
            deadline_warnings = [w.strip() for w in self.deadline_warnings_var.get().split(',') if w.strip()]

            notification_settings = {
                'enabled': self.notifications_enabled_var.get(),
                'learning_reminder_times': learning_times,
                'deadline_warnings': deadline_warnings,
                'quiet_hours_start': self.quiet_hours_start_var.get(),
                'quiet_hours_end': self.quiet_hours_end_var.get(),
                'sound_enabled': self.sound_enabled_var.get()
            }
            self.config.set_notification_settings(notification_settings)

            # Save UI settings
            ui_settings = {
                'theme': self.theme_var.get(),
                'font_size': self.font_size_var.get(),
                'items_per_page': self.items_per_page_var.get()
            }
            self.config.set_ui_settings(ui_settings)

            # Save database settings
            db_settings = {
                'backup_enabled': self.backup_enabled_var.get(),
                'backup_interval_days': self.backup_interval_var.get(),
                'max_backups': self.max_backups_var.get()
            }
            for key, value in db_settings.items():
                self.config.set(f'database.{key}', value)

            # Save to file
            if self.config.save_config():
                messagebox.showinfo("Success", "Settings saved successfully!")

                # Call callback if provided
                if self.callback:
                    self.callback()

                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _on_cancel(self):
        """Handle cancel button click."""
        self.destroy()

    def _test_notifications(self):
        """Test notification functionality."""
        if self.notification_service:
            if self.notification_service.test_notification():
                messagebox.showinfo("Test Successful", "Test notification sent successfully!")
            else:
                messagebox.showerror("Test Failed", "Failed to send test notification.")
        else:
            messagebox.showerror("Not Available", "Notification service is not available.")

    def _backup_now(self):
        """Perform immediate backup."""
        # Placeholder for backup functionality
        messagebox.showinfo("Backup", "Backup functionality will be implemented.")

    def _export_data(self):
        """Export application data."""
        # Placeholder for export functionality
        messagebox.showinfo("Export", "Data export functionality will be implemented.")

    def _import_data(self):
        """Import application data."""
        # Placeholder for import functionality
        messagebox.showinfo("Import", "Data import functionality will be implemented.")

    def _center_dialog(self, parent):
        """Center dialog relative to parent window."""
        try:
            self.update_idletasks()

            # Ensure parent window is properly mapped
            parent.update_idletasks()

            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()

            dialog_width = self.winfo_width()
            dialog_height = self.winfo_height()

            # Handle case where parent dimensions are 0
            if parent_width <= 1:
                parent_width = 1200  # Default width
            if parent_height <= 1:
                parent_height = 800  # Default height

            # Calculate center position
            x = parent_x + (parent_width // 2) - (dialog_width // 2)
            y = parent_y + (parent_height // 2) - (dialog_height // 2)

            # Ensure dialog is visible on screen
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()

            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + dialog_width > screen_width:
                x = screen_width - dialog_width
            if y + dialog_height > screen_height:
                y = screen_height - dialog_height

            self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        except Exception as e:
            print(f"Warning: Could not center dialog: {e}")
            # Fall back to center on screen
            self.geometry("+100+100")