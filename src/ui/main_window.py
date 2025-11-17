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
from utils.styles import AppColors, AppFonts, AppStyles, StyledFrame, StyledButton, StyledEntry, StyledLabel

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
        # Sidebar frame with gradient background effect
        self.sidebar = StyledFrame(
            self,
            width=280,
            corner_radius=0,
            fg_color=("#f8f9fa", "#2c3e50")  # Light gray / Dark blue-gray
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)  # Make the area before status expandable

        # App logo area
        logo_frame = StyledFrame(
            self.sidebar,
            height=80,
            fg_color=(AppColors.PRIMARY, AppColors.PRIMARY_DARK),
            corner_radius=0
        )
        logo_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        logo_frame.grid_rowconfigure(0, weight=1)
        logo_frame.grid_columnconfigure(0, weight=1)

        # App title with better styling
        self.title_label = StyledLabel(
            logo_frame,
            text="🚀 Project Manager",
            variant="title",
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, pady=20)

        # Subtitle
        self.subtitle_label = StyledLabel(
            logo_frame,
            text="Organize • Track • Learn",
            variant="caption",
            text_color=AppColors.GRAY_200
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 20))

        # Navigation section
        nav_label = StyledLabel(
            self.sidebar,
            text="NAVIGATION",
            variant="caption",
            text_color=(AppColors.GRAY_500, AppColors.GRAY_400)
        )
        nav_label.grid(row=1, column=0, padx=25, pady=(30, 10), sticky="w")

        # Navigation buttons with better styling
        self.nav_buttons = {}
        nav_items = [
            ("Projects", "📁", AppColors.PRIMARY),
            ("Learnings", "📚", AppColors.SUCCESS),
            ("Calendar", "📅", AppColors.SECONDARY),
            ("Statistics", "📊", AppColors.WARNING),
            ("Settings", "⚙️", AppColors.GRAY_600)
        ]

        for i, (text, icon, color) in enumerate(nav_items, start=2):
            # Custom styled nav button
            btn = StyledButton(
                self.sidebar,
                style="ghost",
                text=f"  {icon}  {text}",
                command=lambda t=text: self._nav_button_clicked(t),
                width=230,
                height=45,
                font=AppFonts.get_font(13, "normal"),
                anchor="w",
                justify="left"
            )
            btn.grid(row=i, column=0, padx=25, pady=5)

            # Store button and its color for hover effects
            self.nav_buttons[text] = {"button": btn, "color": color}

        # Separator with better styling
        separator = StyledFrame(
            self.sidebar,
            height=2,
            fg_color=(AppColors.GRAY_300, AppColors.GRAY_600),
            corner_radius=1
        )
        separator.grid(row=7, column=0, padx=25, pady=20, sticky="ew")

        # Quick Actions section
        actions_label = StyledLabel(
            self.sidebar,
            text="QUICK ACTIONS",
            variant="caption",
            text_color=(AppColors.GRAY_500, AppColors.GRAY_400)
        )
        actions_label.grid(row=8, column=0, padx=25, pady=(0, 15), sticky="w")

        # Enhanced quick action buttons
        self.add_project_btn = StyledButton(
            self.sidebar,
            style="primary",
            text="➕ New Project",
            command=self._add_project,
            width=230,
            height=42,
            font=AppFonts.get_font(12, "bold")
        )
        self.add_project_btn.grid(row=9, column=0, padx=25, pady=(0, 10))

        self.add_learning_btn = StyledButton(
            self.sidebar,
            style="outline",
            text="📝 Capture Learning",
            command=self._add_learning,
            width=230,
            height=42,
            font=AppFonts.get_font(12, "bold")
        )
        self.add_learning_btn.grid(row=10, column=0, padx=25, pady=(0, 20))

        # Status indicator with better styling
        status_frame = StyledFrame(
            self.sidebar,
            fg_color=(AppColors.GRAY_100, AppColors.GRAY_800),
            corner_radius=AppStyles.CARD_CORNER_RADIUS
        )
        status_frame.grid(row=11, column=0, padx=25, pady=(0, 20), sticky="ew")

        self.status_label = StyledLabel(
            status_frame,
            text="🟢 Online • Synced",
            variant="caption",
            text_color=(AppColors.SUCCESS_DARK, AppColors.SUCCESS_LIGHT)
        )
        self.status_label.grid(row=0, column=0, padx=15, pady=10)

    def _create_main_content(self):
        """Create the main content area with enhanced styling."""
        # Main content frame with background
        self.main_content = StyledFrame(
            self,
            fg_color=("#ffffff", "#1e1e1e"),
            corner_radius=0
        )
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Enhanced header frame with gradient effect
        self.header_frame = StyledFrame(
            self.main_content,
            height=80,
            fg_color=(AppColors.GRAY_50, AppColors.GRAY_900),
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Left section: Page title with subtitle
        title_frame = StyledFrame(
            self.header_frame,
            fg_color="transparent"
        )
        title_frame.grid(row=0, column=0, padx=30, pady=20, sticky="w")

        self.page_title = StyledLabel(
            title_frame,
            text="📁 Projects",
            variant="title"
        )
        self.page_title.grid(row=0, column=0, sticky="w")

        self.page_subtitle = StyledLabel(
            title_frame,
            text="Manage your active projects and track progress",
            variant="caption"
        )
        self.page_subtitle.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Center section: Enhanced search bar
        search_container = StyledFrame(
            self.header_frame,
            width=400,
            fg_color="transparent"
        )
        search_container.grid(row=0, column=1, pady=20)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)

        # Search entry with icon
        search_frame = StyledFrame(
            search_container,
            fg_color=(AppColors.WHITE, AppColors.GRAY_800),
            corner_radius=AppStyles.INPUT_CORNER_RADIUS,
            border_width=1,
            border_color=(AppColors.GRAY_300, AppColors.GRAY_600)
        )
        search_frame.pack(fill="x")

        # Search icon
        search_icon = StyledLabel(
            search_frame,
            text="🔍",
            variant="caption"
        )
        search_icon.pack(side="left", padx=(15, 5))

        # Search entry
        self.search_entry = StyledEntry(
            search_frame,
            placeholder_text="Search projects, learnings, tags...",
            textvariable=self.search_var,
            border_width=0,
            fg_color="transparent",
            font=AppFonts.get_font(13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=12)

        # Right section: Action buttons
        actions_frame = StyledFrame(
            self.header_frame,
            fg_color="transparent"
        )
        actions_frame.grid(row=0, column=2, padx=30, pady=20, sticky="e")

        # Refresh button with enhanced styling
        self.refresh_btn = StyledButton(
            actions_frame,
            style="ghost",
            text="🔄 Refresh",
            command=self._refresh_all,
            width=100,
            height=40,
            font=AppFonts.get_font(11, "bold")
        )
        self.refresh_btn.pack(side="right", padx=(10, 0))

        # Filter button (new)
        self.filter_btn = StyledButton(
            actions_frame,
            style="outline",
            text="⚡ Filter",
            command=self._show_filters,
            width=100,
            height=40,
            font=AppFonts.get_font(11, "bold")
        )
        self.filter_btn.pack(side="right")

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
        # Update button states with enhanced styling
        for btn_name, btn_data in self.nav_buttons.items():
            btn = btn_data["button"]
            color = btn_data["color"]
            if btn_name == view_name:
                # Highlight selected button with color
                btn.configure(
                    fg_color=(color, color),
                    text_color="white",
                    hover_color=(color, color)
                )
            else:
                # Reset other buttons to ghost style
                btn.configure(
                    fg_color="transparent",
                    text_color=(AppColors.GRAY_700, AppColors.GRAY_300),
                    hover_color=(AppColors.GRAY_100, AppColors.GRAY_800)
                )

        # Update page title with icon
        icons = {
            "Projects": "📁",
            "Learnings": "📚",
            "Calendar": "📅",
            "Statistics": "📊",
            "Settings": "⚙️"
        }
        icon = icons.get(view_name, "")
        self.page_title.configure(text=f"{icon} {view_name}")

        # Show corresponding view with smooth transition
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
        """Create an enhanced project card widget."""
        # Modern card frame with hover effects
        card = StyledFrame(
            self.projects_container,
            fg_color=(AppColors.WHITE, AppColors.GRAY_800),
            border_width=1,
            border_color=(AppColors.GRAY_200, AppColors.GRAY_700),
            corner_radius=AppStyles.CARD_CORNER_RADIUS
        )
        card.grid(row=row, column=0, padx=12, pady=12, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Priority indicator with modern design
        priority_color = get_priority_color(project['priority'])
        priority_frame = StyledFrame(
            card,
            width=4,
            fg_color=priority_color,
            corner_radius=2
        )
        priority_frame.grid(row=0, column=0, rowspan=3, padx=(0, 15), sticky="ns", pady=15)

        # Main content area
        content_frame = StyledFrame(
            card,
            fg_color="transparent"
        )
        content_frame.grid(row=0, column=1, rowspan=3, padx=(0, 15), pady=15, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)

        # Top row: Project name and status
        top_row = StyledFrame(
            content_frame,
            fg_color="transparent"
        )
        top_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # Priority icon
        priority_icons = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        priority_icon = StyledLabel(
            top_row,
            text=priority_icons.get(project['priority'], "⚪"),
            variant="caption"
        )
        priority_icon.grid(row=0, column=0, padx=(0, 8))

        # Project name
        name_label = StyledLabel(
            top_row,
            text=project['name'],
            variant="subheading"
        )
        name_label.grid(row=0, column=1, sticky="w")

        # Status badge with modern styling
        status_colors = {
            'planning': AppColors.STATUS_PLANNING,
            'active': AppColors.STATUS_ACTIVE,
            'completed': AppColors.STATUS_COMPLETED,
            'paused': AppColors.STATUS_PAUSED
        }
        status_color = status_colors.get(project['status'], AppColors.GRAY_500)

        status_badge = StyledFrame(
            top_row,
            fg_color=status_color,
            corner_radius=12
        )
        status_badge.grid(row=0, column=2, padx=(15, 0))

        status_text = StyledLabel(
            status_badge,
            text=project['status'].title(),
            variant="caption",
            text_color="white",
            font=AppFonts.get_font(10, "bold")
        )
        status_text.pack(padx=12, pady=4)

        # Description with better typography
        if project['description']:
            desc_text = project['description']
            if len(desc_text) > 120:
                desc_text = desc_text[:120] + "..."

            desc_label = StyledLabel(
                content_frame,
                text=desc_text,
                variant="body",
                wraplength=450,
                justify="left"
            )
            desc_label.grid(row=1, column=0, sticky="w", pady=(0, 12))

        # Progress section with enhanced design
        progress_frame = StyledFrame(
            content_frame,
            fg_color="transparent"
        )
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        progress_frame.grid_columnconfigure(0, weight=1)

        # Progress label with color
        progress_color = AppColors.get_progress_color(project['progress'])
        progress_label = StyledLabel(
            progress_frame,
            text=f"📊 Progress: {project['progress']}%",
            variant="caption",
            text_color=progress_color
        )
        progress_label.grid(row=0, column=0, sticky="w")

        # Progress bar with modern styling
        progress_bar_frame = StyledFrame(
            progress_frame,
            fg_color=(AppColors.GRAY_200, AppColors.GRAY_700),
            corner_radius=10,
            height=8
        )
        progress_bar_frame.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        # Progress fill
        progress_fill = StyledFrame(
            progress_bar_frame,
            fg_color=progress_color,
            corner_radius=8
        )
        progress_width = int((project['progress'] / 100) * 400)  # Approximate width
        progress_fill.place(x=0, y=0, relwidth=project['progress']/100, relheight=1)

        # Right side: Deadline and metadata
        metadata_frame = StyledFrame(
            card,
            fg_color="transparent"
        )
        metadata_frame.grid(row=0, column=2, rowspan=3, padx=(0, 15), pady=15, sticky="n")

        # Deadline with enhanced styling
        if project['deadline']:
            days_remaining = calculate_days_remaining(project['deadline'])
            deadline_color = AppColors.get_deadline_urgency_color(days_remaining)

            # Deadline icon and text
            deadline_frame = StyledFrame(
                metadata_frame,
                fg_color=(AppColors.GRAY_50, AppColors.GRAY_900),
                corner_radius=8,
                width=140
            )
            deadline_frame.grid(row=0, column=0, pady=(0, 10))

            deadline_icon = StyledLabel(
                deadline_frame,
                text="📅",
                variant="caption"
            )
            deadline_icon.pack(pady=(8, 2))

            deadline_text = f"{format_date(project['deadline'])}"
            if days_remaining < 0:
                deadline_text = f"Overdue"
            elif days_remaining == 0:
                deadline_text = f"Due Today"
            elif days_remaining <= 3:
                deadline_text = f"{days_remaining} days"
            else:
                deadline_text = f"{days_remaining} days"

            deadline_label = StyledLabel(
                deadline_frame,
                text=deadline_text,
                variant="caption",
                text_color=deadline_color,
                font=AppFonts.get_font(9, "bold")
            )
            deadline_label.pack(pady=(0, 8))

        # Tags with pill design
        if project['tags']:
            tags_frame = StyledFrame(
                metadata_frame,
                fg_color="transparent"
            )
            tags_frame.grid(row=1, column=0)

            for i, tag in enumerate(project['tags'][:2]):  # Show max 2 tags
                tag_frame = StyledFrame(
                    tags_frame,
                    fg_color=(AppColors.GRAY_100, AppColors.GRAY_700),
                    corner_radius=10
                )
                tag_frame.grid(row=i, column=0, pady=(0, 4))

                tag_label = StyledLabel(
                    tag_frame,
                    text=f"#{tag.lower()}",
                    variant="caption",
                    text_color=(AppColors.GRAY_700, AppColors.GRAY_300)
                )
                tag_label.pack(padx=8, py=2)

            if len(project['tags']) > 2:
                more_label = StyledLabel(
                    tags_frame,
                    text=f"+{len(project['tags']) - 2} more",
                    variant="caption",
                    text_color=(AppColors.GRAY_500, AppColors.GRAY_400)
                )
                more_label.grid(row=2, column=0, pady=(2, 0))

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

            # Ensure any existing dialogs are properly closed
            self.update_idletasks()

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
            print(f"Error opening add learning dialog: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to open add learning dialog: {e}")

    def _open_settings(self):
        """Handle open settings button click."""
        try:
            from .dialogs.settings import SettingsDialog

            # Ensure any existing dialogs are properly closed
            self.update_idletasks()

            dialog = SettingsDialog(
                parent=self,
                app_config=self.config,
                notification_service=self.notification_service,
                callback=self._on_settings_changed
            )

        except ImportError:
            messagebox.showerror("Error", "Settings dialog not available.")
        except Exception as e:
            print(f"Error opening settings dialog: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to open settings dialog: {e}")

    def _show_filters(self):
        """Show filter dialog."""
        # For now, just show a simple filter
        messagebox.showinfo("Filters", "Advanced filters coming soon! You'll be able to filter by:\n• Status (Active, Completed, Paused)\n• Priority (High, Medium, Low)\n• Tags\n• Date ranges\n• Progress percentage")

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