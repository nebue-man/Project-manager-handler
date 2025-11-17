"""
Main window for the Project Manager application.
Contains the sidebar navigation and main content area.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import format_date, calculate_days_remaining, get_priority_color, get_status_color
from utils.config import config

class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self, project_model, learning_model, notification_service, config):
        """
        Initialize main window.

        Args:
            project_model: Project model instance
            learning_model: Learning model instance
            notification_service: Notification service instance
            config: Configuration instance
        """
        super().__init__()

        # Store references
        self.project_model = project_model
        self.learning_model = learning_model
        self.notification_service = notification_service
        self.config = config

        # Window configuration
        self.title("Project Manager")
        self.geometry("1200x800")
        self.minsize(800, 600)

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize UI components
        self._create_sidebar()
        self._create_main_content()

        # Load initial data
        self._refresh_projects()
        self._refresh_learnings()

        # Set initial view
        self._show_projects_view()

    def _create_sidebar(self):
        """Create the sidebar navigation."""
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)  # Make the area before settings expandable

        # App title
        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="Project Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Projects", "📁"),
            ("Learnings", "📚"),
            ("Calendar", "📅"),
            ("Statistics", "📊"),
            ("Settings", "⚙️")
        ]

        for i, (text, icon) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {text}",
                command=lambda t=text: self._nav_button_clicked(t),
                width=200,
                height=40,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            btn.grid(row=i, column=0, padx=20, pady=5)
            self.nav_buttons[text] = btn

        # Separator
        separator = ctk.CTkFrame(self.sidebar, height=2)
        separator.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # Quick actions
        self.quick_actions_label = ctk.CTkLabel(
            self.sidebar,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.quick_actions_label.grid(row=7, column=0, padx=20, pady=(10, 5))

        self.add_project_btn = ctk.CTkButton(
            self.sidebar,
            text="+ New Project",
            command=self._add_project,
            width=200,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.add_project_btn.grid(row=8, column=0, padx=20, pady=5)

        self.add_learning_btn = ctk.CTkButton(
            self.sidebar,
            text="+ Capture Learning",
            command=self._add_learning,
            width=200,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.add_learning_btn.grid(row=9, column=0, padx=20, pady=5)

        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="● Online",
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50"
        )
        self.status_label.grid(row=10, column=0, padx=20, pady=(20, 10))

    def _create_main_content(self):
        """Create the main content area."""
        # Main content frame
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Header frame
        self.header_frame = ctk.CTkFrame(self.main_content, height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        # Page title
        self.page_title = ctk.CTkLabel(
            self.header_frame,
            text="Projects",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.page_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        self.search_entry = ctk.CTkEntry(
            self.header_frame,
            placeholder_text="Search projects and learnings...",
            textvariable=self.search_var,
            width=300,
            height=35
        )
        self.search_entry.grid(row=0, column=1, padx=20, pady=15)

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            self.header_frame,
            text="🔄 Refresh",
            command=self._refresh_all,
            width=100,
            height=35
        )
        self.refresh_btn.grid(row=0, column=2, padx=20, pady=15, sticky="e")

        # Content frame (will hold different views)
        self.content_frame = ctk.CTkFrame(self.main_content)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize views
        self.views = {}
        self._create_projects_view()
        self._create_learnings_view()
        self._create_calendar_view()
        self._create_statistics_view()
        self._create_settings_view()

    def _create_projects_view(self):
        """Create the projects view."""
        # Projects scrollable frame
        self.projects_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            label_text="Active Projects",
            label_font=ctk.CTkFont(size=18, weight="bold")
        )
        self.projects_frame.grid_columnconfigure(0, weight=1)
        self.projects_frame.grid_rowconfigure(0, weight=1)

        # Projects container
        self.projects_container = ctk.CTkFrame(self.projects_frame)
        self.projects_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.projects_container.grid_columnconfigure(0, weight=1)

        # View reference
        self.views["Projects"] = self.projects_frame

    def _create_learnings_view(self):
        """Create the learnings view."""
        # Learnings scrollable frame
        self.learnings_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            label_text="Recent Learnings",
            label_font=ctk.CTkFont(size=18, weight="bold")
        )
        self.learnings_frame.grid_columnconfigure(0, weight=1)
        self.learnings_frame.grid_rowconfigure(0, weight=1)

        # Learnings container
        self.learnings_container = ctk.CTkFrame(self.learnings_frame)
        self.learnings_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.learnings_container.grid_columnconfigure(0, weight=1)

        # View reference
        self.views["Learnings"] = self.learnings_frame

    def _create_calendar_view(self):
        """Create the calendar view."""
        # Calendar frame
        self.calendar_frame = ctk.CTkFrame(self.content_frame)
        self.calendar_frame.grid_columnconfigure(0, weight=1)
        self.calendar_frame.grid_rowconfigure(0, weight=1)

        # Calendar content (placeholder)
        calendar_label = ctk.CTkLabel(
            self.calendar_frame,
            text="Calendar View\n\nShow project deadlines and learning timeline\n\n(Feature coming soon)",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        calendar_label.grid(row=0, column=0, pady=50)

        # View reference
        self.views["Calendar"] = self.calendar_frame

    def _create_statistics_view(self):
        """Create the statistics view."""
        # Statistics frame
        self.statistics_frame = ctk.CTkFrame(self.content_frame)
        self.statistics_frame.grid_columnconfigure(0, weight=1)
        self.statistics_frame.grid_rowconfigure(0, weight=1)

        # Statistics content (placeholder)
        stats_label = ctk.CTkLabel(
            self.statistics_frame,
            text="Statistics View\n\nShow project and learning statistics\n\n(Feature coming soon)",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        stats_label.grid(row=0, column=0, pady=50)

        # View reference
        self.views["Statistics"] = self.statistics_frame

    def _create_settings_view(self):
        """Create the settings view."""
        # Settings frame
        self.settings_frame = ctk.CTkFrame(self.content_frame)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(0, weight=1)

        # Settings button
        settings_btn = ctk.CTkButton(
            self.settings_frame,
            text="⚙️ Open Settings",
            command=self._open_settings,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        settings_btn.grid(row=0, column=0, pady=50)

        # View reference
        self.views["Settings"] = self.settings_frame

    def _nav_button_clicked(self, view_name: str):
        """Handle navigation button click."""
        # Update button states
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == view_name:
                btn.configure(fg_color=("#1f538d", "#1f538d"))  # Highlight selected
            else:
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        # Update page title
        self.page_title.configure(text=view_name)

        # Show corresponding view
        if view_name == "Projects":
            self._show_projects_view()
        elif view_name == "Learnings":
            self._show_learnings_view()
        elif view_name == "Calendar":
            self._show_calendar_view()
        elif view_name == "Statistics":
            self._show_statistics_view()
        elif view_name == "Settings":
            self._show_settings_view()

    def _show_projects_view(self):
        """Show projects view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()

        # Show projects view
        self.views["Projects"].grid(row=0, column=0, sticky="nsew")

    def _show_learnings_view(self):
        """Show learnings view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()

        # Show learnings view
        self.views["Learnings"].grid(row=0, column=0, sticky="nsew")

    def _show_calendar_view(self):
        """Show calendar view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()

        # Show calendar view
        self.views["Calendar"].grid(row=0, column=0, sticky="nsew")

    def _show_statistics_view(self):
        """Show statistics view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()

        # Show statistics view
        self.views["Statistics"].grid(row=0, column=0, sticky="nsew")

    def _show_settings_view(self):
        """Show settings view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()

        # Show settings view
        self.views["Settings"].grid(row=0, column=0, sticky="nsew")

    def _refresh_projects(self):
        """Refresh projects display."""
        try:
            # Clear existing project widgets
            for widget in self.projects_container.winfo_children():
                widget.destroy()

            # Get active projects
            projects = self.project_model.get_all(status='active')

            if not projects:
                # Show empty state
                empty_label = ctk.CTkLabel(
                    self.projects_container,
                    text="No active projects found.\n\nClick '+ New Project' to get started!",
                    font=ctk.CTkFont(size=14),
                    justify="center"
                )
                empty_label.grid(row=0, column=0, pady=50)
                return

            # Create project cards
            for i, project in enumerate(projects):
                self._create_project_card(project, i)

        except Exception as e:
            print(f"Error refreshing projects: {e}")
            messagebox.showerror("Error", f"Failed to refresh projects: {e}")

    def _refresh_learnings(self):
        """Refresh learnings display."""
        try:
            # Clear existing learning widgets
            for widget in self.learnings_container.winfo_children():
                widget.destroy()

            # Get recent learnings (limit to 20)
            learnings = self.learning_model.get_all(limit=20)

            if not learnings:
                # Show empty state
                empty_label = ctk.CTkLabel(
                    self.learnings_container,
                    text="No learnings captured yet.\n\nClick '+ Capture Learning' to document what you've learned!",
                    font=ctk.CTkFont(size=14),
                    justify="center"
                )
                empty_label.grid(row=0, column=0, pady=50)
                return

            # Create learning cards
            for i, learning in enumerate(learnings):
                self._create_learning_card(learning, i)

        except Exception as e:
            print(f"Error refreshing learnings: {e}")
            messagebox.showerror("Error", f"Failed to refresh learnings: {e}")

    def _create_project_card(self, project: Dict[str, Any], row: int):
        """Create a project card widget."""
        # Card frame
        card = ctk.CTkFrame(self.projects_container)
        card.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Priority indicator
        priority_color = get_priority_color(project['priority'])
        priority_indicator = ctk.CTkFrame(card, width=5, corner_radius=2)
        priority_indicator.configure(fg_color=priority_color)
        priority_indicator.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="ns")

        # Project name
        name_label = ctk.CTkLabel(
            card,
            text=project['name'],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

        # Status badge
        status_color = get_status_color(project['status'])
        status_badge = ctk.CTkLabel(
            card,
            text=project['status'].title(),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
            fg_color=status_color,
            corner_radius=4
        )
        status_badge.grid(row=0, column=2, padx=10, pady=(10, 0))

        # Description (if exists)
        if project['description']:
            desc_label = ctk.CTkLabel(
                card,
                text=project['description'][:100] + "..." if len(project['description']) > 100 else project['description'],
                font=ctk.CTkFont(size=12),
                wraplength=400,
                justify="left"
            )
            desc_label.grid(row=1, column=1, columnspan=2, padx=(0, 10), pady=(5, 0), sticky="w")

        # Progress bar
        progress_label = ctk.CTkLabel(
            card,
            text=f"Progress: {project['progress']}%",
            font=ctk.CTkFont(size=11)
        )
        progress_label.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

        progress_bar = ctk.CTkProgressBar(card, width=200)
        progress_bar.set(project['progress'] / 100)
        progress_bar.grid(row=2, column=1, padx=(0, 10), pady=(15, 10), sticky="w")

        # Deadline info
        if project['deadline']:
            days_remaining = calculate_days_remaining(project['deadline'])
            deadline_text = f"Deadline: {format_date(project['deadline'])}"
            if days_remaining < 0:
                deadline_text += f" (Overdue by {abs(days_remaining)} days)"
                deadline_color = "#F44336"
            elif days_remaining == 0:
                deadline_text += " (Due today!)"
                deadline_color = "#FF9800"
            elif days_remaining <= 3:
                deadline_text += f" ({days_remaining} days left)"
                deadline_color = "#FF9800"
            else:
                deadline_text += f" ({days_remaining} days left)"
                deadline_color = "#4CAF50"

            deadline_label = ctk.CTkLabel(
                card,
                text=deadline_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=deadline_color
            )
            deadline_label.grid(row=2, column=2, padx=10, pady=(10, 0), sticky="e")

        # Tags (if any)
        if project['tags']:
            tags_text = " | ".join(project['tags'])
            tags_label = ctk.CTkLabel(
                card,
                text=f"🏷️ {tags_text}",
                font=ctk.CTkFont(size=10),
                text_color="#666"
            )
            tags_label.grid(row=3, column=1, columnspan=2, padx=(0, 10), pady=(5, 10), sticky="w")

    def _create_learning_card(self, learning: Dict[str, Any], row: int):
        """Create a learning card widget."""
        # Card frame
        card = ctk.CTkFrame(self.learnings_container)
        card.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Learning title
        title_label = ctk.CTkLabel(
            card,
            text=learning['title'],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=(15, 10), pady=(15, 0), sticky="w")

        # Project association (if any)
        if learning['project_name']:
            project_label = ctk.CTkLabel(
                card,
                text=f"📁 {learning['project_name']}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2196F3"
            )
            project_label.grid(row=0, column=1, padx=10, pady=(15, 0), sticky="e")

        # Learning content (truncated)
        content_text = learning['content'][:200] + "..." if len(learning['content']) > 200 else learning['content']
        content_label = ctk.CTkLabel(
            card,
            text=content_text,
            font=ctk.CTkFont(size=12),
            wraplength=500,
            justify="left"
        )
        content_label.grid(row=1, column=0, columnspan=2, padx=(15, 15), pady=(10, 0), sticky="w")

        # Tags (if any)
        if learning['tags']:
            tags_text = " | ".join(learning['tags'])
            tags_label = ctk.CTkLabel(
                card,
                text=f"🏷️ {tags_text}",
                font=ctk.CTkFont(size=10),
                text_color="#666"
            )
            tags_label.grid(row=2, column=0, columnspan=2, padx=(15, 15), pady=(10, 0), sticky="w")

        # Created date
        created_date = format_date(learning['created_at'], '%B %d, %Y')
        date_label = ctk.CTkLabel(
            card,
            text=f"📅 {created_date}",
            font=ctk.CTkFont(size=10),
            text_color="#999"
        )
        date_label.grid(row=3, column=0, columnspan=2, padx=(15, 15), pady=(10, 15), sticky="w")

    def _add_project(self):
        """Handle add project button click."""
        try:
            from .dialogs.add_project import AddProjectDialog

            # Ensure any existing dialogs are properly closed
            self.update_idletasks()

            dialog = AddProjectDialog(
                parent=self,
                project_model=self.project_model,
                notification_service=self.notification_service,
                callback=lambda project_id: self._refresh_projects()
            )

        except ImportError:
            messagebox.showerror("Error", "Add project dialog not available.")
        except Exception as e:
            print(f"Error opening add project dialog: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to open add project dialog: {e}")

    def _add_learning(self):
        """Handle add learning button click."""
        try:
            from .dialogs.add_learning import AddLearningDialog

            dialog = AddLearningDialog(
                parent=self,
                learning_model=self.learning_model,
                project_model=self.project_model,
                notification_service=self.notification_service,
                callback=lambda learning_id: self._refresh_learnings()
            )

        except ImportError:
            messagebox.showerror("Error", "Add learning dialog not available.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open add learning dialog: {e}")

    def _open_settings(self):
        """Handle open settings button click."""
        try:
            from .dialogs.settings import SettingsDialog

            dialog = SettingsDialog(
                parent=self,
                app_config=self.config,
                notification_service=self.notification_service,
                callback=self._on_settings_changed
            )

        except ImportError:
            messagebox.showerror("Error", "Settings dialog not available.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings dialog: {e}")

    def _on_settings_changed(self):
        """Handle settings change callback."""
        # Refresh UI elements that depend on settings
        # For now, just show a message
        messagebox.showinfo("Settings", "Settings changed. Some changes may require restart.")

    def _refresh_all(self):
        """Refresh all data displays."""
        self._refresh_projects()
        self._refresh_learnings()
        messagebox.showinfo("Refresh", "Data refreshed successfully!")

    def _on_search_change(self, *args):
        """Handle search input change."""
        search_term = self.search_var.get().strip()
        if search_term:
            # Implement search functionality
            pass
        else:
            # Clear search, show all items
            self._refresh_projects()
            self._refresh_learnings()

    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')