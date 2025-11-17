"""
Add Project Dialog for the Project Manager application.
Allows users to create new projects with various properties.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
import customtkinter as ctk
from typing import Dict, Any, Optional, Callable
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.helpers import validate_project_name, validate_deadline, parse_tags, clean_tags

class AddProjectDialog(ctk.CTkToplevel):
    """Dialog for adding new projects."""

    def __init__(self, parent, project_model, notification_service=None, callback: Callable = None):
        """
        Initialize add project dialog.

        Args:
            parent: Parent window
            project_model: Project model instance
            notification_service: Notification service instance
            callback: Optional callback function called after successful creation
        """
        super().__init__(parent)

        # Store references
        self.project_model = project_model
        self.notification_service = notification_service
        self.callback = callback

        # Dialog configuration
        self.title("Add New Project")
        self.geometry("500x600")
        self.minsize(400, 500)
        self.resizable(True, True)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Initialize variables
        self._init_variables()

        # Create UI components
        self._create_widgets()

        # Set focus to name field
        self.name_entry.focus_set()

        # Center dialog relative to parent
        self._center_dialog(parent)

    def _init_variables(self):
        """Initialize form variables."""
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.deadline_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="medium")
        self.tags_var = tk.StringVar()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Create New Project",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Name field (required)
        name_label = ctk.CTkLabel(
            form_frame,
            text="Project Name *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.name_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.name_var,
            placeholder_text="Enter project name...",
            height=35
        )
        self.name_entry.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Description field
        desc_label = ctk.CTkLabel(
            form_frame,
            text="Description",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        desc_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")

        self.description_text = ctk.CTkTextbox(
            form_frame,
            height=100,
            wrap="word"
        )
        self.description_text.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Deadline field (required)
        deadline_label = ctk.CTkLabel(
            form_frame,
            text="Deadline *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        deadline_label.grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")

        # Deadline input frame
        deadline_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        deadline_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        deadline_frame.grid_columnconfigure(0, weight=1)
        deadline_frame.grid_columnconfigure(1, weight=0)

        self.deadline_entry = ctk.CTkEntry(
            deadline_frame,
            textvariable=self.deadline_var,
            placeholder_text="YYYY-MM-DD",
            width=150
        )
        self.deadline_entry.grid(row=0, column=0, sticky="w")

        # Quick deadline buttons
        quick_deadline_frame = ctk.CTkFrame(deadline_frame, fg_color="transparent")
        quick_deadline_frame.grid(row=0, column=1, padx=(10, 0), sticky="w")

        quick_deadlines = [
            ("1 Week", 7),
            ("2 Weeks", 14),
            ("1 Month", 30)
        ]

        for i, (text, days) in enumerate(quick_deadlines):
            btn = ctk.CTkButton(
                quick_deadline_frame,
                text=text,
                command=lambda d=days: self._set_deadline_days(d),
                width=70,
                height=28
            )
            btn.grid(row=0, column=i, padx=(0, 5) if i < len(quick_deadlines) - 1 else (0, 0))

        # Priority field
        priority_label = ctk.CTkLabel(
            form_frame,
            text="Priority",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        priority_label.grid(row=6, column=0, padx=20, pady=(20, 5), sticky="w")

        self.priority_option = ctk.CTkOptionMenu(
            form_frame,
            variable=self.priority_var,
            values=["low", "medium", "high"],
            width=200,
            height=35
        )
        self.priority_option.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="w")

        # Tags field
        tags_label = ctk.CTkLabel(
            form_frame,
            text="Tags (comma-separated)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        tags_label.grid(row=8, column=0, padx=20, pady=(20, 5), sticky="w")

        tags_help = ctk.CTkLabel(
            form_frame,
            text="e.g., web, python, urgent",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        )
        tags_help.grid(row=9, column=0, padx=20, pady=(0, 5), sticky="w")

        self.tags_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.tags_var,
            placeholder_text="Enter tags...",
            height=35
        )
        self.tags_entry.grid(row=10, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Progress preview
        progress_label = ctk.CTkLabel(
            form_frame,
            text="Initial Progress",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        progress_label.grid(row=11, column=0, padx=20, pady=(20, 5), sticky="w")

        self.progress_slider = ctk.CTkSlider(
            form_frame,
            from_=0,
            to=100,
            number_of_steps=20,
            width=300
        )
        self.progress_slider.set(0)
        self.progress_slider.grid(row=12, column=0, padx=20, pady=(0, 5), sticky="w")

        self.progress_label = ctk.CTkLabel(
            form_frame,
            text="0%",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=13, column=0, padx=20, pady=(0, 20), sticky="w")

        # Bind slider change
        self.progress_slider.configure(command=self._update_progress_label)

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=120,
            height=40
        )
        self.cancel_btn.grid(row=0, column=1, padx=(0, 10))

        # Create button
        self.create_btn = ctk.CTkButton(
            button_frame,
            text="Create Project",
            command=self._on_create,
            width=120,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.create_btn.grid(row=0, column=2)

        # Bind Enter key
        self.bind('<Return>', lambda e: self._on_create())
        self.bind('<Escape>', lambda e: self._on_cancel())

    def _set_deadline_days(self, days: int):
        """Set deadline to N days from today."""
        future_date = date.today() + timedelta(days=days)
        self.deadline_var.set(future_date.strftime('%Y-%m-%d'))

    def _update_progress_label(self, value):
        """Update progress label when slider changes."""
        self.progress_label.configure(text=f"{int(value)}%")

    def _validate_form(self) -> bool:
        """Validate form inputs."""
        # Validate project name
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Project name is required.")
            self.name_entry.focus_set()
            return False

        if not validate_project_name(name):
            messagebox.showerror(
                "Validation Error",
                "Project name must be between 1 and 100 characters and not contain invalid characters."
            )
            self.name_entry.focus_set()
            return False

        # Validate deadline
        deadline = self.deadline_var.get().strip()
        if not deadline:
            messagebox.showerror("Validation Error", "Project deadline is required.")
            self.deadline_entry.focus_set()
            return False

        if not validate_deadline(deadline):
            messagebox.showerror(
                "Validation Error",
                "Deadline must be a valid future date in YYYY-MM-DD format."
            )
            self.deadline_entry.focus_set()
            return False

        return True

    def _on_create(self):
        """Handle create button click."""
        if not self._validate_form():
            return

        try:
            # Get form data
            name = self.name_var.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            deadline = self.deadline_var.get().strip()
            priority = self.priority_var.get()
            progress = int(self.progress_slider.get())
            tags = parse_tags(self.tags_var.get())

            # Create project
            project_id = self.project_model.create(
                name=name,
                description=description,
                deadline=deadline,
                priority=priority,
                tags=tags
            )

            # Update progress if not zero
            if progress > 0:
                self.project_model.update(project_id, progress=progress)

            # Show notification
            if self.notification_service:
                self.notification_service.show_project_created_notification(name)

            # Call callback if provided
            if self.callback:
                self.callback(project_id)

            messagebox.showinfo("Success", f"Project '{name}' created successfully!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")

    def _on_cancel(self):
        """Handle cancel button click."""
        self.destroy()

    def _center_dialog(self, parent):
        """Center dialog relative to parent window."""
        self.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)

        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

class EditProjectDialog(AddProjectDialog):
    """Dialog for editing existing projects."""

    def __init__(self, parent, project_model, project_id: int,
                 notification_service=None, callback: Callable = None):
        """
        Initialize edit project dialog.

        Args:
            parent: Parent window
            project_model: Project model instance
            project_id: ID of project to edit
            notification_service: Notification service instance
            callback: Optional callback function called after successful edit
        """
        self.project_id = project_id
        self.project_data = None

        # Initialize parent class
        super().__init__(parent, project_model, notification_service, callback)

        # Load project data
        self._load_project_data()

        # Update dialog title and button
        self.title("Edit Project")
        self.create_btn.configure(text="Save Changes")

    def _load_project_data(self):
        """Load existing project data into form."""
        try:
            self.project_data = self.project_model.get_by_id(self.project_id)

            if not self.project_data:
                messagebox.showerror("Error", "Project not found.")
                self.destroy()
                return

            # Populate form fields
            self.name_var.set(self.project_data['name'])
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert("1.0", self.project_data['description'] or "")
            self.deadline_var.set(self.project_data['deadline'] or "")
            self.priority_var.set(self.project_data['priority'])
            self.tags_var.set(', '.join(self.project_data['tags']))
            self.progress_slider.set(self.project_data['progress'])
            self._update_progress_label(self.project_data['progress'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load project data: {str(e)}")
            self.destroy()

    def _on_create(self):
        """Handle save changes button click."""
        if not self._validate_form():
            return

        try:
            # Get form data
            name = self.name_var.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            deadline = self.deadline_var.get().strip()
            priority = self.priority_var.get()
            progress = int(self.progress_slider.get())
            tags = parse_tags(self.tags_var.get())

            # Update project
            success = self.project_model.update(
                self.project_id,
                name=name,
                description=description,
                deadline=deadline,
                priority=priority,
                progress=progress,
                tags=tags
            )

            if success:
                # Show notification
                if self.notification_service:
                    self.notification_service.show_success_notification(
                        f"Project '{name}' updated successfully!"
                    )

                # Call callback if provided
                if self.callback:
                    self.callback(self.project_id)

                messagebox.showinfo("Success", f"Project '{name}' updated successfully!")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to update project.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update project: {str(e)}")