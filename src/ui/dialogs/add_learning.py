"""
Add Learning Dialog for the Project Manager application.
Allows users to capture and document what they've learned.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any, Optional, Callable, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.helpers import parse_tags, clean_tags

class AddLearningDialog(ctk.CTkToplevel):
    """Dialog for adding new learning entries."""

    def __init__(self, parent, learning_model, project_model=None,
                 notification_service=None, callback: Callable = None,
                 default_project_id: int = None):
        """
        Initialize add learning dialog.

        Args:
            parent: Parent window
            learning_model: Learning model instance
            project_model: Project model instance (optional)
            notification_service: Notification service instance
            callback: Optional callback function called after successful creation
            default_project_id: Default project ID to pre-select
        """
        super().__init__(parent)

        # Store references
        self.learning_model = learning_model
        self.project_model = project_model
        self.notification_service = notification_service
        self.callback = callback
        self.default_project_id = default_project_id

        # Get projects list for dropdown
        self.projects = []
        if self.project_model:
            self.projects = self.project_model.get_all(status='active')

        # Dialog configuration
        self.title("Capture Learning")
        self.geometry("600x700")
        self.minsize(500, 600)
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

        # Set focus to title field
        self.title_entry.focus_set()

        # Center dialog relative to parent
        self._center_dialog(parent)

    def _init_variables(self):
        """Initialize form variables."""
        self.title_var = tk.StringVar()
        self.content_var = tk.StringVar()
        self.project_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.char_count_var = tk.StringVar(value="0 / 2000")

        # Set default project if provided
        if self.default_project_id and self.projects:
            self.project_var.set(str(self.default_project_id))

    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Capture What You've Learned",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Document your insights, discoveries, and lessons learned",
            font=ctk.CTkFont(size=12),
            text_color="#666"
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Learning title field (required)
        title_label = ctk.CTkLabel(
            form_frame,
            text="Learning Title *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.title_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.title_var,
            placeholder_text="Give your learning a concise title...",
            height=35
        )
        self.title_entry.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")

        title_help = ctk.CTkLabel(
            form_frame,
            text="Maximum 100 characters",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        )
        title_help.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="w")

        # Project association
        if self.projects:
            project_label = ctk.CTkLabel(
                form_frame,
                text="Associated Project",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            project_label.grid(row=3, column=0, padx=20, pady=(15, 5), sticky="w")

            # Create project options list for dropdown
            project_options = ["(General)"]  # Option for learnings not tied to a specific project
            project_options.extend([f"{project['name']} (ID: {project['id']})" for project in self.projects])

            self.project_option = ctk.CTkOptionMenu(
                form_frame,
                variable=self.project_var,
                values=project_options,
                width=300,
                height=35
            )
            self.project_option.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")

        # Learning content field (required)
        content_label = ctk.CTkLabel(
            form_frame,
            text="What did you learn? *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        content_label.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")

        # Content text area with character count
        content_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        content_frame.grid(row=6, column=0, padx=20, pady=(0, 5), sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        self.content_text = ctk.CTkTextbox(
            content_frame,
            height=250,
            wrap="word"
        )
        self.content_text.grid(row=0, column=0, sticky="nsew")

        # Bind text change to character count
        self.content_text.bind('<KeyRelease>', self._update_char_count)
        self.content_text.bind('<Button-1>', self._update_char_count)

        # Character count
        char_count_label = ctk.CTkLabel(
            content_frame,
            textvariable=self.char_count_var,
            font=ctk.CTkFont(size=10),
            text_color="#666"
        )
        char_count_label.grid(row=1, column=0, pady=(5, 0), sticky="e")

        # Quick templates
        templates_label = ctk.CTkLabel(
            form_frame,
            text="Quick Templates",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        templates_label.grid(row=7, column=0, padx=20, pady=(15, 5), sticky="w")

        templates_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        templates_frame.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")

        templates = [
            ("Problem/Solution", "I faced the problem of... and discovered that... The solution was..."),
            ("Key Insight", "The key insight I gained was... This matters because..."),
            ("Technical Learning", "I learned that... by implementing... The takeaway is..."),
            ("Process Improvement", "I improved my process by... This resulted in..."),
            ("Best Practice", "The best practice I discovered is... It helps by...")
        ]

        for i, (template_name, template_content) in enumerate(templates):
            btn = ctk.CTkButton(
                templates_frame,
                text=template_name,
                command=lambda content=template_content: self._apply_template(content),
                width=120,
                height=30
            )
            btn.grid(row=i//3, column=i%3, padx=(0, 10) if i%3 < 2 else (0, 0), pady=(0, 5))

        # Tags field
        tags_label = ctk.CTkLabel(
            form_frame,
            text="Tags (comma-separated)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        tags_label.grid(row=9, column=0, padx=20, pady=(15, 5), sticky="w")

        tags_help = ctk.CTkLabel(
            form_frame,
            text="e.g., debugging, api, best-practice",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        )
        tags_help.grid(row=10, column=0, padx=20, pady=(0, 5), sticky="w")

        self.tags_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.tags_var,
            placeholder_text="Enter tags...",
            height=35
        )
        self.tags_entry.grid(row=11, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
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

        # Save Learning button
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Save Learning",
            command=self._on_save,
            width=120,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_btn.grid(row=0, column=2)

        # Bind keyboard shortcuts
        self.bind('<Control-s>', lambda e: self._on_save())
        self.bind('<Control-Return>', lambda e: self._on_save())
        self.bind('<Escape>', lambda e: self._on_cancel())

    def _update_char_count(self, event=None):
        """Update character count display."""
        content = self.content_text.get("1.0", tk.END)
        char_count = len(content.strip())
        self.char_count_var.set(f"{char_count} / 2000")

        # Change color if approaching limit
        if char_count > 1900:
            self.char_count_var.configure(text_color="#F44336")
        elif char_count > 1800:
            self.char_count_var.configure(text_color="#FF9800")
        else:
            self.char_count_var.configure(text_color="#666")

    def _apply_template(self, template_content: str):
        """Apply a template to the content field."""
        current_content = self.content_text.get("1.0", tk.END).strip()
        if current_content:
            # Append with separator if there's existing content
            self.content_text.insert(tk.END, f"\n\n{template_content}")
        else:
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", template_content)

        self._update_char_count()

    def _validate_form(self) -> bool:
        """Validate form inputs."""
        # Validate learning title
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Learning title is required.")
            self.title_entry.focus_set()
            return False

        if len(title) > 100:
            messagebox.showerror("Validation Error", "Learning title must be 100 characters or less.")
            self.title_entry.focus_set()
            return False

        # Validate learning content
        content = self.content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Validation Error", "Learning content is required.")
            self.content_text.focus_set()
            return False

        if len(content) > 2000:
            messagebox.showerror("Validation Error", "Learning content must be 2000 characters or less.")
            self.content_text.focus_set()
            return False

        return True

    def _extract_project_id(self) -> Optional[int]:
        """Extract project ID from the selected option."""
        project_selection = self.project_var.get()
        if not project_selection or project_selection == "(General)":
            return None

        # Extract ID from format "Project Name (ID: X)"
        try:
            import re
            match = re.search(r'ID: (\d+)', project_selection)
            if match:
                return int(match.group(1))
        except (ValueError, AttributeError):
            pass

        return None

    def _on_save(self):
        """Handle save learning button click."""
        if not self._validate_form():
            return

        try:
            # Get form data
            title = self.title_var.get().strip()
            content = self.content_text.get("1.0", tk.END).strip()
            project_id = self._extract_project_id()
            tags = parse_tags(self.tags_var.get())

            # Create learning
            learning_id = self.learning_model.create(
                title=title,
                content=content,
                project_id=project_id,
                tags=tags
            )

            # Show notification
            if self.notification_service:
                self.notification_service.show_learning_created_notification(title)

            # Call callback if provided
            if self.callback:
                self.callback(learning_id)

            messagebox.showinfo("Success", f"Learning '{title}' saved successfully!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save learning: {str(e)}")

    def _on_cancel(self):
        """Handle cancel button click."""
        # Check if there's unsaved content
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if title or content:
            if messagebox.askyesno("Unsaved Changes",
                                 "You have unsaved changes. Are you sure you want to close?"):
                self.destroy()
        else:
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

class EditLearningDialog(AddLearningDialog):
    """Dialog for editing existing learning entries."""

    def __init__(self, parent, learning_model, learning_id: int,
                 project_model=None, notification_service=None, callback: Callable = None):
        """
        Initialize edit learning dialog.

        Args:
            parent: Parent window
            learning_model: Learning model instance
            learning_id: ID of learning to edit
            project_model: Project model instance (optional)
            notification_service: Notification service instance
            callback: Optional callback function called after successful edit
        """
        self.learning_id = learning_id
        self.learning_data = None

        # Initialize parent class
        super().__init__(parent, learning_model, project_model, notification_service, callback)

        # Update dialog title and button
        self.title("Edit Learning")
        self.save_btn.configure(text="Save Changes")

        # Load learning data
        self._load_learning_data()

    def _load_learning_data(self):
        """Load existing learning data into form."""
        try:
            self.learning_data = self.learning_model.get_by_id(self.learning_id)

            if not self.learning_data:
                messagebox.showerror("Error", "Learning entry not found.")
                self.destroy()
                return

            # Populate form fields
            self.title_var.set(self.learning_data['title'])
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", self.learning_data['content'])

            # Set project selection
            if self.learning_data['project_id']:
                # Find the project name and construct the selection
                for project in self.projects:
                    if project['id'] == self.learning_data['project_id']:
                        selection = f"{project['name']} (ID: {project['id']})"
                        self.project_var.set(selection)
                        break
            else:
                self.project_var.set("(General)")

            # Set tags
            if self.learning_data['tags']:
                self.tags_var.set(', '.join(self.learning_data['tags']))

            # Update character count
            self._update_char_count()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load learning data: {str(e)}")
            self.destroy()

    def _on_save(self):
        """Handle save changes button click."""
        if not self._validate_form():
            return

        try:
            # Get form data
            title = self.title_var.get().strip()
            content = self.content_text.get("1.0", tk.END).strip()
            project_id = self._extract_project_id()
            tags = parse_tags(self.tags_var.get())

            # Update learning
            success = self.learning_model.update(
                self.learning_id,
                title=title,
                content=content,
                project_id=project_id,
                tags=tags
            )

            if success:
                # Show notification
                if self.notification_service:
                    self.notification_service.show_success_notification(
                        f"Learning '{title}' updated successfully!"
                    )

                # Call callback if provided
                if self.callback:
                    self.callback(self.learning_id)

                messagebox.showinfo("Success", f"Learning '{title}' updated successfully!")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to update learning.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update learning: {str(e)}")