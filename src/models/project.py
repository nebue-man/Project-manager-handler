"""
Project model for the Project Manager application.
Handles all project-related database operations.
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Any
from .database import DatabaseManager

class Project:
    """Represents a project in the project manager."""

    def __init__(self, db: DatabaseManager):
        """Initialize Project model with database connection."""
        self.db = db

    def create(self, name: str, description: str = "", deadline: str = None,
               priority: str = "medium", tags: List[str] = None) -> int:
        """
        Create a new project.

        Args:
            name: Project name (required)
            description: Project description
            deadline: Deadline date (YYYY-MM-DD format)
            priority: Priority level (low, medium, high)
            tags: List of tags

        Returns:
            ID of the created project
        """
        # Validate required fields
        if not name or not name.strip():
            raise ValueError("Project name is required")

        # Validate deadline format
        if deadline:
            try:
                datetime.strptime(deadline, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Deadline must be in YYYY-MM-DD format")

        # Validate priority
        if priority not in ['low', 'medium', 'high']:
            raise ValueError("Priority must be low, medium, or high")

        # Convert tags to JSON
        tags_json = self.db.json_dumps(tags or [])

        query = '''
            INSERT INTO projects (name, description, status, start_date, deadline, priority, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        params = (
            name.strip(),
            description.strip(),
            'active',
            date.today().strftime('%Y-%m-%d'),
            deadline,
            priority,
            tags_json
        )

        return self.db.execute_insert(query, params)

    def get_by_id(self, project_id: int) -> Optional[Dict]:
        """Get a project by ID."""
        query = "SELECT * FROM projects WHERE id = ?"
        results = self.db.execute_query(query, (project_id,))

        if not results:
            return None

        project = dict(results[0])
        project['tags'] = self.db.json_loads(project['tags'])
        return project

    def get_all(self, status: str = None, sort_by: str = "deadline") -> List[Dict]:
        """
        Get all projects, optionally filtered by status.

        Args:
            status: Filter by status (planning, active, completed, paused)
            sort_by: Sort by field (deadline, priority, created_at, updated_at)

        Returns:
            List of project dictionaries
        """
        # Validate sort_by
        valid_sort_fields = ['deadline', 'priority', 'created_at', 'updated_at', 'name']
        if sort_by not in valid_sort_fields:
            sort_by = 'deadline'

        query = "SELECT * FROM projects"
        params = []

        if status:
            query += " WHERE status = ?"
            params.append(status)

        # Add ordering - null deadlines go last for active projects
        if sort_by == 'deadline':
            query += " ORDER BY CASE WHEN deadline IS NULL THEN 1 ELSE 0 END, deadline ASC"
        elif sort_by == 'priority':
            query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END"
        else:
            query += f" ORDER BY {sort_by} DESC"

        results = self.db.execute_query(query, tuple(params))
        projects = []

        for result in results:
            project = dict(result)
            project['tags'] = self.db.json_loads(project['tags'])
            projects.append(project)

        return projects

    def update(self, project_id: int, **kwargs) -> bool:
        """
        Update a project.

        Args:
            project_id: ID of project to update
            **kwargs: Fields to update

        Returns:
            True if successful, False otherwise
        """
        # Check if project exists
        if not self.get_by_id(project_id):
            return False

        # Validate and prepare updates
        update_fields = []
        params = []

        # Update basic fields
        for field in ['name', 'description', 'deadline', 'priority', 'progress']:
            if field in kwargs:
                value = kwargs[field]

                if field == 'name' and (not value or not str(value).strip()):
                    raise ValueError("Project name cannot be empty")

                if field == 'deadline' and value:
                    try:
                        datetime.strptime(str(value), '%Y-%m-%d')
                    except ValueError:
                        raise ValueError("Deadline must be in YYYY-MM-DD format")

                if field == 'priority' and value not in ['low', 'medium', 'high']:
                    raise ValueError("Priority must be low, medium, or high")

                if field == 'progress' and (not isinstance(value, int) or not (0 <= value <= 100)):
                    raise ValueError("Progress must be an integer between 0 and 100")

                update_fields.append(f"{field} = ?")
                params.append(value)

        # Handle status changes with automatic progress updates
        if 'status' in kwargs:
            status = kwargs['status']
            if status not in ['planning', 'active', 'completed', 'paused']:
                raise ValueError("Invalid status")

            update_fields.append("status = ?")
            params.append(status)

            # Auto-set progress based on status
            if status == 'completed':
                update_fields.append("progress = 100")
                params.append(100)  # For the progress = 100 part

        # Handle tags
        if 'tags' in kwargs:
            tags_json = self.db.json_dumps(kwargs['tags'])
            update_fields.append("tags = ?")
            params.append(tags_json)

        if not update_fields:
            return True  # No updates needed

        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")

        # Add project_id to params
        params.append(project_id)

        query = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = ?"
        affected_rows = self.db.execute_update(query, tuple(params))

        return affected_rows > 0

    def delete(self, project_id: int) -> bool:
        """
        Delete a project.

        Args:
            project_id: ID of project to delete

        Returns:
            True if successful, False otherwise
        """
        # Check if project exists
        if not self.get_by_id(project_id):
            return False

        query = "DELETE FROM projects WHERE id = ?"
        affected_rows = self.db.execute_update(query, (project_id,))

        return affected_rows > 0

    def search(self, search_term: str) -> List[Dict]:
        """
        Search projects by name, description, or tags.

        Args:
            search_term: Term to search for

        Returns:
            List of matching projects
        """
        query = '''
            SELECT * FROM projects
            WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
            ORDER BY name
        '''

        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)

        results = self.db.execute_query(query, params)
        projects = []

        for result in results:
            project = dict(result)
            project['tags'] = self.db.json_loads(project['tags'])
            projects.append(project)

        return projects

    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict]:
        """
        Get projects with deadlines in the next N days.

        Args:
            days: Number of days to look ahead

        Returns:
            List of projects with upcoming deadlines
        """
        query = '''
            SELECT * FROM projects
            WHERE status = 'active'
            AND deadline IS NOT NULL
            AND deadline >= date('now')
            AND deadline <= date('now', '+{} days')
            ORDER BY deadline ASC
        '''.format(days)

        results = self.db.execute_query(query)
        projects = []

        for result in results:
            project = dict(result)
            project['tags'] = self.db.json_loads(project['tags'])
            projects.append(project)

        return projects

    def get_overdue_projects(self) -> List[Dict]:
        """
        Get projects with missed deadlines.

        Returns:
            List of overdue projects
        """
        query = '''
            SELECT * FROM projects
            WHERE status = 'active'
            AND deadline IS NOT NULL
            AND deadline < date('now')
            ORDER BY deadline ASC
        '''

        results = self.db.execute_query(query)
        projects = []

        for result in results:
            project = dict(result)
            project['tags'] = self.db.json_loads(project['tags'])
            projects.append(project)

        return projects