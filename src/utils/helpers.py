"""
Helper utilities for the Project Manager application.
Contains common functions and utilities.
"""

import os
import json
import csv
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
import re

def format_date(date_obj: Any, date_format: str = "%Y-%m-%d") -> str:
    """
    Format a date object to string.

    Args:
        date_obj: Date object or string
        date_format: Format string

    Returns:
        Formatted date string
    """
    if not date_obj:
        return ""

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj

    return date_obj.strftime(date_format)

def parse_date(date_str: str, date_format: str = "%Y-%m-%d") -> Optional[date]:
    """
    Parse a date string to date object.

    Args:
        date_str: Date string
        date_format: Format string

    Returns:
        Date object or None if parsing fails
    """
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        return None

def calculate_days_remaining(deadline: str) -> int:
    """
    Calculate days remaining until deadline.

    Args:
        deadline: Deadline date string (YYYY-MM-DD)

    Returns:
        Number of days remaining (negative if overdue)
    """
    if not deadline:
        return 0

    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        today = date.today()
        return (deadline_date - today).days
    except ValueError:
        return 0

def get_priority_color(priority: str) -> str:
    """
    Get color associated with priority level.

    Args:
        priority: Priority level (low, medium, high)

    Returns:
        Color hex code
    """
    colors = {
        'low': '#4CAF50',      # Green
        'medium': '#FF9800',   # Orange
        'high': '#F44336'      # Red
    }
    return colors.get(priority.lower(), '#9E9E9E')  # Default gray

def get_status_color(status: str) -> str:
    """
    Get color associated with project status.

    Args:
        status: Status (planning, active, completed, paused)

    Returns:
        Color hex code
    """
    colors = {
        'planning': '#2196F3',  # Blue
        'active': '#8BC34A',    # Light Green
        'completed': '#607D8B', # Blue Gray
        'paused': '#FF5722'     # Deep Orange
    }
    return colors.get(status.lower(), '#9E9E9E')  # Default gray

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text or ""

    return text[:max_length - len(suffix)] + suffix

def clean_tags(tags: List[str]) -> List[str]:
    """
    Clean and normalize tags list.

    Args:
        tags: List of tags

    Returns:
        Cleaned list of unique tags
    """
    if not tags:
        return []

    # Remove empty strings and whitespace, convert to lowercase, remove duplicates
    cleaned = []
    seen = set()

    for tag in tags:
        if tag and tag.strip():
            clean_tag = tag.strip().lower()
            if clean_tag not in seen:
                cleaned.append(clean_tag)
                seen.add(clean_tag)

    return cleaned

def parse_tags(tags_string: str) -> List[str]:
    """
    Parse tags from comma-separated string.

    Args:
        tags_string: Comma-separated tags

    Returns:
        List of clean tags
    """
    if not tags_string:
        return []

    tags = [tag.strip() for tag in tags_string.split(',')]
    return clean_tags(tags)

def tags_to_string(tags: List[str]) -> str:
    """
    Convert tags list to comma-separated string.

    Args:
        tags: List of tags

    Returns:
        Comma-separated string
    """
    return ', '.join(tags) if tags else ""

def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_project_name(name: str) -> bool:
    """
    Validate project name.

    Args:
        name: Project name

    Returns:
        True if valid, False otherwise
    """
    if not name or not name.strip():
        return False

    # Project name should be 1-100 characters and not contain control characters
    clean_name = name.strip()
    if len(clean_name) < 1 or len(clean_name) > 100:
        return False

    # Check for invalid characters
    if any(ord(c) < 32 for c in clean_name):
        return False

    return True

def validate_deadline(deadline: str) -> bool:
    """
    Validate deadline date format and that it's in the future.

    Args:
        deadline: Deadline date string (YYYY-MM-DD)

    Returns:
        True if valid and future, False otherwise
    """
    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        return deadline_date >= date.today()
    except ValueError:
        return False

def get_time_ago(date_obj: Any) -> str:
    """
    Get human-readable time ago string.

    Args:
        date_obj: Date object or string

    Returns:
        Time ago string (e.g., "2 days ago")
    """
    if not date_obj:
        return "Never"

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
            except ValueError:
                return "Unknown"

    now = datetime.now()
    diff = now - date_obj

    if diff.days == 0:
        hours = diff.seconds // 3600
        if hours == 0:
            minutes = diff.seconds // 60
            if minutes == 0:
                return "Just now"
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days < 7:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif diff.days < 365:
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"

def generate_backup_filename(base_name: str, timestamp: datetime = None) -> str:
    """
    Generate backup filename with timestamp.

    Args:
        base_name: Base filename
        timestamp: Timestamp to use (defaults to now)

    Returns:
        Backup filename
    """
    if timestamp is None:
        timestamp = datetime.now()

    timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S')
    name_part = os.path.splitext(base_name)[0]
    extension = os.path.splitext(base_name)[1]

    return f"{name_part}_backup_{timestamp_str}{extension}"

def export_to_json(data: List[Dict[Any, Any]], file_path: str) -> bool:
    """
    Export data to JSON file.

    Args:
        data: List of dictionaries to export
        file_path: Output file path

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except (IOError, TypeError) as e:
        print(f"Error exporting to JSON: {e}")
        return False

def export_to_csv(data: List[Dict[str, Any]], file_path: str, fieldnames: List[str] = None) -> bool:
    """
    Export data to CSV file.

    Args:
        data: List of dictionaries to export
        file_path: Output file path
        fieldnames: List of field names (columns)

    Returns:
        True if successful, False otherwise
    """
    if not data:
        return False

    try:
        # Use keys from first record if fieldnames not provided
        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                # Convert complex objects to strings
                clean_row = {}
                for key, value in row.items():
                    if key in fieldnames:
                        clean_row[key] = str(value) if not isinstance(value, (str, int, float, bool)) else value
                writer.writerow(clean_row)

        return True
    except (IOError, csv.Error) as e:
        print(f"Error exporting to CSV: {e}")
        return False

def safe_filename(filename: str) -> str:
    """
    Make filename safe for filesystem.

    Args:
        filename: Original filename

    Returns:
        Safe filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    safe_name = filename

    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')

    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(' .')

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name[:255]  # Limit length

def is_quiet_hours(start_time: str, end_time: str) -> bool:
    """
    Check if current time is within quiet hours.

    Args:
        start_time: Quiet hours start time (HH:MM)
        end_time: Quiet hours end time (HH:MM)

    Returns:
        True if currently in quiet hours
    """
    try:
        now = datetime.now().time()
        start = datetime.strptime(start_time, '%H:%M').time()
        end = datetime.strptime(end_time, '%H:%M').time()

        if start <= end:
            # Same day range (e.g., 22:00 to 08:00 is overnight)
            return now >= start or now <= end
        else:
            # Normal range (e.g., 08:00 to 22:00)
            return start <= now <= end
    except ValueError:
        return False

def get_available_colors() -> List[str]:
    """
    Get list of predefined colors for UI elements.

    Returns:
        List of color hex codes
    """
    return [
        '#F44336',  # Red
        '#E91E63',  # Pink
        '#9C27B0',  # Purple
        '#673AB7',  # Deep Purple
        '#3F51B5',  # Indigo
        '#2196F3',  # Blue
        '#03A9F4',  # Light Blue
        '#00BCD4',  # Cyan
        '#009688',  # Teal
        '#4CAF50',  # Green
        '#8BC34A',  # Light Green
        '#CDDC39',  # Lime
        '#FFEB3B',  # Yellow
        '#FFC107',  # Amber
        '#FF9800',  # Orange
        '#FF5722',  # Deep Orange
        '#795548',  # Brown
        '#9E9E9E',  # Grey
        '#607D8B',  # Blue Grey
    ]