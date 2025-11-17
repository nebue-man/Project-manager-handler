"""
Main application class for the Project Manager.
Coordinates all components and manages the application lifecycle.
"""

import sys
import os
import threading
import signal

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from models.database import DatabaseManager
from models.project import Project
from models.learning import Learning
from services.notification_service import NotificationService
from services.scheduler_service import SchedulerService
from utils.config import config
from utils.helpers import is_quiet_hours

try:
    import customtkinter as ctk
    GUI_AVAILABLE = True
except (ImportError, Exception) as e:
    print(f"Warning: GUI not available ({e}). Running in headless mode.")
    GUI_AVAILABLE = False
    # Create a minimal mock for headless operation
    class MockCTk:
        def set_appearance_mode(self, mode): pass
        def set_default_color_theme(self, theme): pass
        def CTk(self):
            class MockRoot:
                def mainloop(self):
                    print("Running in headless mode - database operations only.")
                    print("Use Ctrl+C to exit.")
                    try:
                        import time
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        pass
                def geometry(self, *args): pass
                def title(self, *args): pass
                def protocol(self, *args): pass
                def destroy(self): pass
                def _center_window(self): pass
                def __getattr__(self, name):
                    def mock_method(*args, **kwargs): pass
                    return mock_method
            return MockRoot()
        def CTkFrame(self, *args, **kwargs):
            class MockFrame:
                def pack(self, *args, **kwargs): pass
                def grid(self, *args, **kwargs): pass
                def place(self, *args, **kwargs): pass
                def configure(self, *args, **kwargs): pass
                def cget(self, *args): return None
                def bind(self, *args, **kwargs): pass
                def destroy(self): pass
                def __getattr__(self, name):
                    def mock_method(*args, **kwargs): pass
                    return mock_method
            return MockFrame()
        def CTkButton(self, *args, **kwargs):
            class MockButton:
                def pack(self, *args, **kwargs): pass
                def grid(self, *args, **kwargs): pass
                def configure(self, *args, **kwargs): pass
                def cget(self, *args): return None
                def bind(self, *args, **kwargs): pass
                def destroy(self): pass
                def __getattr__(self, name):
                    def mock_method(*args, **kwargs): pass
                    return mock_method
            return MockButton()
        def CTkLabel(self, *args, **kwargs):
            class MockLabel:
                def pack(self, *args, **kwargs): pass
                def grid(self, *args, **kwargs): pass
                def configure(self, *args, **kwargs): pass
                def cget(self, *args): return None
                def destroy(self): pass
                def __getattr__(self, name):
                    def mock_method(*args, **kwargs): pass
                    return mock_method
            return MockLabel()
        def CTkEntry(self, *args, **kwargs):
            class MockEntry:
                def pack(self, *args, **kwargs): pass
                def grid(self, *args, **kwargs): pass
                def configure(self, *args, **kwargs): pass
                def get(self): return ""
                def delete(self, *args): pass
                def insert(self, *args): pass
                def bind(self, *args, **kwargs): pass
                def destroy(self): pass
                def __getattr__(self, name):
                    def mock_method(*args, **kwargs): pass
                    return mock_method
            return MockEntry()

    ctk = MockCTk()

class ProjectManagerApp:
    """Main application class."""

    def __init__(self):
        """Initialize the application."""
        self.db = None
        self.project_model = None
        self.learning_model = None
        self.notification_service = None
        self.scheduler_service = None
        self.main_window = None

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Initialize configuration
        self.config = config
        self.config.load_config()

        # Initialize database and models
        self._init_database()
        self._init_services()

        # Set up CustomTkinter appearance
        self._setup_appearance()

    def _init_database(self):
        """Initialize database and models."""
        try:
            db_path = self.config.get('database.path', 'project_manager.db')
            self.db = DatabaseManager(db_path)
            self.project_model = Project(self.db)
            self.learning_model = Learning(self.db)
        except Exception as e:
            print(f"Error initializing database: {e}")
            sys.exit(1)

    def _init_services(self):
        """Initialize background services."""
        try:
            # Initialize notification service
            self.notification_service = NotificationService()

            # Initialize scheduler service
            self.scheduler_service = SchedulerService(
                notification_service=self.notification_service,
                project_model=self.project_model,
                learning_model=self.learning_model,
                config=self.config
            )

            # Start background services
            self.scheduler_service.start()

        except Exception as e:
            print(f"Error initializing services: {e}")
            # Continue without services rather than exit

    def _setup_appearance(self):
        """Set up CustomTkinter appearance based on configuration."""
        if not GUI_AVAILABLE:
            return

        # Set appearance mode based on theme setting
        theme = self.config.get('ui.theme', 'light')
        if theme == 'dark':
            ctk.set_appearance_mode('dark')
        elif theme == 'light':
            ctk.set_appearance_mode('light')
        else:  # system
            ctk.set_appearance_mode('system')

        # Set default color theme
        ctk.set_default_color_theme('blue')

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)

    def create_main_window(self):
        """Create and show the main window."""
        from ui.main_window import MainWindow

        try:
            # Create main window
            self.main_window = MainWindow(
                self.project_model,
                self.learning_model,
                self.notification_service,
                self.config
            )

            # Set window geometry from config
            geometry = self.config.get_window_geometry()
            self.main_window.geometry(f"{geometry['width']}x{geometry['height']}")

            # Center window on screen
            self.main_window._center_window()

            return self.main_window

        except Exception as e:
            print(f"Error creating main window: {e}")
            sys.exit(1)

    def run(self):
        """Run the application."""
        try:
            # Create main window
            root = self.create_main_window()

            # Start the GUI event loop
            root.mainloop()

        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        """Clean shutdown of application."""
        print("Shutting down application...")

        # Save window geometry if remember is enabled
        if (self.main_window and self.config.get('app.remember_window_size', True)):
            try:
                geometry = self.main_window.geometry()
                width, height = geometry.split('x')[0], geometry.split('x')[1].split('+')[0]
                self.config.set_window_geometry(int(width), int(height))
                self.config.save_config()
            except Exception:
                pass  # Ignore geometry saving errors

        # Stop scheduler service
        if self.scheduler_service:
            try:
                self.scheduler_service.stop()
            except Exception as e:
                print(f"Error stopping scheduler: {e}")

        # Close database connection
        if self.db:
            try:
                self.db.close()
            except Exception as e:
                print(f"Error closing database: {e}")

        print("Application shutdown complete.")

def main():
    """Entry point for the application."""
    app = ProjectManagerApp()
    app.run()

if __name__ == "__main__":
    main()