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

# Try to import enhanced components, fall back to basic ones if not available
try:
    from utils.styles import AppColors, AppFonts, AppStyles, StyledFrame, StyledButton, StyledEntry, StyledLabel
    from utils.animations import animator, AnimationType
    from ui.components.interactive import AnimatedButton, AnimatedCard, SmoothProgressBar
    ENHANCED_UI = True
except ImportError:
    print("Warning: Enhanced UI components not available, using basic components")
    # Fallback to basic components
    import customtkinter as ctk
    AppColors = None
    AppFonts = None
    AppStyles = None
    StyledFrame = ctk.CTkFrame
    StyledButton = ctk.CTkButton
    StyledEntry = ctk.CTkEntry
    StyledLabel = ctk.CTkLabel
    animator = None
    AnimationType = None
    AnimatedButton = StyledButton
    AnimatedCard = StyledFrame
    SmoothProgressBar = None
    ENHANCED_UI = False

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
        self.enhanced_ui = ENHANCED_UI if 'ENHANCED_UI' in globals() else False

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
            # Animated nav button with hover effects
            btn = AnimatedButton(
                self.sidebar,
                style="ghost",
                text=f"  {icon}  {text}",
                command=lambda t=text: self._nav_button_clicked(t),
                width=230,
                height=45,
                font=AppFonts.get_font(13, "normal"),
                anchor="w",
                justify="left",
                hover_effect=True,
                pulse_on_click=True
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

        # Enhanced quick action buttons with animations
        self.add_project_btn = AnimatedButton(
            self.sidebar,
            style="primary",
            text="➕ New Project",
            command=self._add_project,
            width=230,
            height=42,
            font=AppFonts.get_font(12, "bold"),
            hover_effect=True,
            pulse_on_click=True
        )
        self.add_project_btn.grid(row=9, column=0, padx=25, pady=(0, 10))

        self.add_learning_btn = AnimatedButton(
            self.sidebar,
            style="outline",
            text="📝 Capture Learning",
            command=self._add_learning,
            width=230,
            height=42,
            font=AppFonts.get_font(12, "bold"),
            hover_effect=True,
            pulse_on_click=True
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

        # Refresh button with enhanced styling and animations
        self.refresh_btn = AnimatedButton(
            actions_frame,
            style="ghost",
            text="🔄 Refresh",
            command=self._refresh_all,
            width=100,
            height=40,
            font=AppFonts.get_font(11, "bold"),
            hover_effect=True,
            pulse_on_click=True
        )
        self.refresh_btn.pack(side="right", padx=(10, 0))

        # Filter button with animations
        self.filter_btn = AnimatedButton(
            actions_frame,
            style="outline",
            text="⚡ Filter",
            command=self._show_filters,
            width=100,
            height=40,
            font=AppFonts.get_font(11, "bold"),
            hover_effect=True,
            pulse_on_click=True
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
        """Show projects view with smooth transition."""
        # Fade out current view
        current_visible = None
        for name, view in self.views.items():
            if view.winfo_viewable():
                current_visible = view
                break

        # Fade in projects view
        projects_view = self.views["Projects"]
        projects_view.grid(row=0, column=0, sticky="nsew")

        # Hide other views
        for name, view in self.views.items():
            if name != "Projects":
                view.grid_forget()

        # Animate view transition
        try:
            if current_visible:
                # Fade out current view
                current_visible.configure(fg_color=(AppColors.GRAY_100, AppColors.GRAY_900))
                self.after(100, lambda: current_visible.grid_forget())

            # Fade in projects view
            projects_view.configure(fg_color=(AppColors.WHITE, AppColors.GRAY_800))
        except:
            pass  # Fallback silently

    def _show_learnings_view(self):
        """Show learnings view with smooth transition."""
        self._smooth_transition_view("Learnings")

    def _show_calendar_view(self):
        """Show calendar view with smooth transition."""
        self._smooth_transition_view("Calendar")

    def _show_statistics_view(self):
        """Show statistics view with smooth transition."""
        self._smooth_transition_view("Statistics")

    def _show_settings_view(self):
        """Show settings view with smooth transition."""
        self._smooth_transition_view("Settings")

    def _smooth_transition_view(self, target_view_name: str):
        """Smoothly transition to a target view."""
        # Fade out current view
        current_visible = None
        for name, view in self.views.items():
            if view.winfo_viewable():
                current_visible = view
                break

        # Show target view
        target_view = self.views[target_view_name]
        target_view.grid(row=0, column=0, sticky="nsew")

        # Hide other views
        for name, view in self.views.items():
            if name != target_view_name:
                view.grid_forget()

        # Animate view transition
        try:
            if current_visible and current_visible != target_view:
                # Fade out current view
                current_visible.configure(fg_color=(AppColors.GRAY_100, AppColors.GRAY_900))
                self.after(100, lambda: current_visible.grid_forget())

            # Fade in target view
            target_view.configure(fg_color=(AppColors.WHITE, AppColors.GRAY_800))
        except:
            pass  # Fallback silently

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
        """Create an enhanced animated project card widget."""
        # Modern animated card frame with hover effects
        card = AnimatedCard(
            self.projects_container,
            fg_color=(AppColors.WHITE, AppColors.GRAY_800),
            border_width=1,
            border_color=(AppColors.GRAY_200, AppColors.GRAY_700),
            corner_radius=AppStyles.CARD_CORNER_RADIUS + 4,
            hover_lift=True,
            hover_highlight=True
        )
        card.grid(row=row, column=0, padx=12, pady=12, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Add click animation
        def on_card_click(event):
            try:
                animator.pulse(card, duration=0.2, scale=1.02)
            except:
                pass
        card.bind("<Button-1>", on_card_click)

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

        # Smooth animated progress bar
        progress_bar = SmoothProgressBar(
            progress_frame,
            width=400,
            height=8
        )
        progress_bar.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        progress_bar.set_progress(project['progress'], animated=True)

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
        """Create an enhanced learning card widget with modern styling."""
        # Modern animated card with gradient effect
        card = AnimatedCard(
            self.learnings_container,
            fg_color=(AppColors.WHITE, AppColors.GRAY_800),
            border_width=1,
            border_color=(AppColors.GRAY_200, AppColors.GRAY_700),
            corner_radius=AppStyles.CARD_CORNER_RADIUS + 2,
            hover_lift=True,
            hover_highlight=True
        )
        card.grid(row=row, column=0, padx=12, pady=12, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        # Add click animation
        def on_card_click(event):
            try:
                animator.pulse(card, duration=0.2, scale=1.02)
            except:
                pass
        card.bind("<Button-1>", on_card_click)

        # Main content area
        content_frame = StyledFrame(
            card,
            fg_color="transparent"
        )
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)

        # Top row: Title and project badge
        header_row = StyledFrame(
            content_frame,
            fg_color="transparent"
        )
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header_row.grid_columnconfigure(1, weight=1)

        # Learning icon
        learning_icon = StyledLabel(
            header_row,
            text="💡",
            variant="caption"
        )
        learning_icon.grid(row=0, column=0, padx=(0, 8), sticky="w")

        # Learning title with enhanced typography
        title_label = StyledLabel(
            header_row,
            text=learning['title'],
            variant="subheading",
            wraplength=400
        )
        title_label.grid(row=0, column=1, sticky="w")

        # Project association badge (if any)
        if learning['project_name']:
            project_badge = StyledFrame(
                header_row,
                fg_color=AppColors.PRIMARY,
                corner_radius=12
            )
            project_badge.grid(row=0, column=2, padx=(12, 0))

            project_text = StyledLabel(
                project_badge,
                text=f"📁 {learning['project_name']}",
                variant="caption",
                text_color="white",
                font=AppFonts.get_font(10, "bold")
            )
            project_text.pack(padx=10, py=4)

        # Learning content with better styling
        content_preview = learning['content']
        if len(content_preview) > 180:
            content_preview = content_preview[:180] + "..."

        content_label = StyledLabel(
            content_frame,
            text=content_preview,
            variant="body",
            wraplength=500,
            justify="left",
            text_color=(AppColors.GRAY_700, AppColors.GRAY_300)
        )
        content_label.grid(row=1, column=0, sticky="w", pady=(0, 16))

        # Metadata row: tags and date
        metadata_row = StyledFrame(
            content_frame,
            fg_color="transparent"
        )
        metadata_row.grid(row=2, column=0, sticky="ew")
        metadata_row.grid_columnconfigure(1, weight=1)

        # Tags with modern pill design
        if learning['tags']:
            tags_container = StyledFrame(
                metadata_row,
                fg_color="transparent"
            )
            tags_container.grid(row=0, column=0, sticky="w")

            for i, tag in enumerate(learning['tags'][:3]):  # Show max 3 tags
                tag_frame = StyledFrame(
                    tags_container,
                    fg_color=(AppColors.GRAY_100, AppColors.GRAY_700),
                    corner_radius=10
                )
                tag_frame.grid(row=0, column=i, padx=(0, 8))

                tag_label = StyledLabel(
                    tag_frame,
                    text=f"#{tag.lower()}",
                    variant="caption",
                    text_color=(AppColors.GRAY_700, AppColors.GRAY_300)
                )
                tag_label.pack(padx=8, py=2)

            if len(learning['tags']) > 3:
                more_label = StyledLabel(
                    tags_container,
                    text=f"+{len(learning['tags']) - 3} more",
                    variant="caption",
                    text_color=(AppColors.GRAY_500, AppColors.GRAY_400)
                )
                more_label.grid(row=0, column=3, padx=(8, 0))

        # Date with better styling
        created_date = format_date(learning['created_at'], '%B %d, %Y')
        date_frame = StyledFrame(
            metadata_row,
            fg_color=(AppColors.GRAY_50, AppColors.GRAY_900),
            corner_radius=8
        )
        date_frame.grid(row=0, column=1, sticky="e")

        date_label = StyledLabel(
            date_frame,
            text=f"📅 {created_date}",
            variant="caption",
            text_color=(AppColors.GRAY_600, AppColors.GRAY_400)
        )
        date_label.pack(padx=10, py=4)

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
        """Refresh all data displays with smooth feedback."""
        try:
            # Animate refresh button
            animator.pulse(self.refresh_btn, duration=0.3, scale=1.1)

            # Add loading state (optional enhancement)
            self.page_subtitle.configure(text="Refreshing data...")

            # Refresh data
            self._refresh_projects()
            self._refresh_learnings()

            # Show success feedback
            self.page_subtitle.configure(text="All data refreshed successfully!")
            self.after(2000, lambda: self.page_subtitle.configure(
                text="Manage your active projects and track progress"
            ))

        except Exception as e:
            self.page_subtitle.configure(text="Error refreshing data")
            print(f"Error during refresh: {e}")

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