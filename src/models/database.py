"""
Database operations for the Project Manager application.
Handles SQLite database setup and operations.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class DatabaseManager:
    """Manages SQLite database operations for projects and learnings."""

    def __init__(self, db_path: str = "project_manager.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable dictionary-like access
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")

    def create_tables(self):
        """Create all necessary database tables."""
        try:
            cursor = self.connection.cursor()

            # Create projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT CHECK(status IN ('planning', 'active', 'completed', 'paused')) DEFAULT 'active',
                    start_date DATE,
                    deadline DATE,
                    priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
                    progress INTEGER DEFAULT 0 CHECK(progress >= 0 AND progress <= 100),
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create learnings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    project_id INTEGER,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
                )
            ''')

            # Create notification_settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notification_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_name TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insert default notification settings
            default_settings = [
                ('learning_reminder_times', '["09:00", "14:00"]'),
                ('deadline_warnings', '["1", "3", "7"]'),  # days before deadline
                ('quiet_hours_start', '22:00'),
                ('quiet_hours_end', '08:00'),
                ('notifications_enabled', 'true'),
                ('theme', 'light')
            ]

            for setting_name, setting_value in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO notification_settings (setting_name, setting_value)
                    VALUES (?, ?)
                ''', (setting_name, setting_value))

            self.connection.commit()

        except sqlite3.Error as e:
            raise Exception(f"Table creation error: {e}")

    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Query execution error: {e}")

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            raise Exception(f"Update execution error: {e}")

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT query and return the last row ID."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            raise Exception(f"Insert execution error: {e}")

    def json_loads(self, json_str: str) -> List[str]:
        """Safely load JSON string to list."""
        if not json_str:
            return []
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return []

    def json_dumps(self, data: List[str]) -> str:
        """Safely dump list to JSON string."""
        if not data:
            return "[]"
        return json.dumps(data)

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()