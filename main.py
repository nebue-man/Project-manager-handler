#!/usr/bin/env python3
"""
Project Manager - Main Application Launcher
Entry point for the personal project management application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import ProjectManagerApp

def main():
    """Main entry point for the application."""
    try:
        app = ProjectManagerApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()