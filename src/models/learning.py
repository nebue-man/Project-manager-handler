"""
Learning model for the Project Manager application.
Handles all learning-related database operations.
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Any
from .database import DatabaseManager

class Learning:
    """Represents a learning entry in the project manager."""

    def __init__(self, db: DatabaseManager):
        """Initialize Learning model with database connection."""
        self.db = db

    def create(self, title: str, content: str, project_id: int = None,
               tags: List[str] = None) -> int:
        """
        Create a new learning entry.

        Args:
            title: Learning title (required)
            content: Learning content (required)
            project_id: Associated project ID (optional)
            tags: List of tags

        Returns:
            ID of the created learning entry
        """
        # Validate required fields
        if not title or not title.strip():
            raise ValueError("Learning title is required")

        if not content or not content.strip():
            raise ValueError("Learning content is required")

        # Validate title length
        if len(title) > 100:
            raise ValueError("Learning title must be 100 characters or less")

        # Validate content length
        if len(content) > 2000:
            raise ValueError("Learning content must be 2000 characters or less")

        # Validate project_id if provided
        if project_id is not None:
            project_query = "SELECT id FROM projects WHERE id = ?"
            project_results = self.db.execute_query(project_query, (project_id,))
            if not project_results:
                raise ValueError("Invalid project ID")

        # Convert tags to JSON
        tags_json = self.db.json_dumps(tags or [])

        query = '''
            INSERT INTO learnings (title, content, project_id, tags)
            VALUES (?, ?, ?, ?)
        '''

        params = (
            title.strip(),
            content.strip(),
            project_id,
            tags_json
        )

        return self.db.execute_insert(query, params)

    def get_by_id(self, learning_id: int) -> Optional[Dict]:
        """Get a learning entry by ID."""
        query = '''
            SELECT l.*, p.name as project_name
            FROM learnings l
            LEFT JOIN projects p ON l.project_id = p.id
            WHERE l.id = ?
        '''
        results = self.db.execute_query(query, (learning_id,))

        if not results:
            return None

        learning = dict(results[0])
        learning['tags'] = self.db.json_loads(learning['tags'])
        return learning

    def get_all(self, project_id: int = None, tags: List[str] = None,
                limit: int = None, offset: int = 0) -> List[Dict]:
        """
        Get all learning entries, optionally filtered.

        Args:
            project_id: Filter by project ID
            tags: Filter by tags (any match)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of learning dictionaries
        """
        query = '''
            SELECT l.*, p.name as project_name
            FROM learnings l
            LEFT JOIN projects p ON l.project_id = p.id
            WHERE 1=1
        '''
        params = []

        # Filter by project
        if project_id is not None:
            query += " AND l.project_id = ?"
            params.append(project_id)

        # Filter by tags
        if tags:
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("l.tags LIKE ?")
                params.append(f"%{tag}%")
            query += " AND (" + " OR ".join(tag_conditions) + ")"

        query += " ORDER BY l.created_at DESC"

        # Add pagination
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        results = self.db.execute_query(query, tuple(params))
        learnings = []

        for result in results:
            learning = dict(result)
            learning['tags'] = self.db.json_loads(learning['tags'])
            learnings.append(learning)

        return learnings

    def update(self, learning_id: int, **kwargs) -> bool:
        """
        Update a learning entry.

        Args:
            learning_id: ID of learning to update
            **kwargs: Fields to update

        Returns:
            True if successful, False otherwise
        """
        # Check if learning exists
        if not self.get_by_id(learning_id):
            return False

        # Validate and prepare updates
        update_fields = []
        params = []

        # Update basic fields
        if 'title' in kwargs:
            title = kwargs['title']
            if not title or not str(title).strip():
                raise ValueError("Learning title cannot be empty")
            if len(str(title)) > 100:
                raise ValueError("Learning title must be 100 characters or less")

            update_fields.append("title = ?")
            params.append(str(title).strip())

        if 'content' in kwargs:
            content = kwargs['content']
            if not content or not str(content).strip():
                raise ValueError("Learning content cannot be empty")
            if len(str(content)) > 2000:
                raise ValueError("Learning content must be 2000 characters or less")

            update_fields.append("content = ?")
            params.append(str(content).strip())

        if 'project_id' in kwargs:
            project_id = kwargs['project_id']
            if project_id is not None:
                # Validate project exists
                project_query = "SELECT id FROM projects WHERE id = ?"
                project_results = self.db.execute_query(project_query, (project_id,))
                if not project_results:
                    raise ValueError("Invalid project ID")

            update_fields.append("project_id = ?")
            params.append(project_id)

        # Handle tags
        if 'tags' in kwargs:
            tags_json = self.db.json_dumps(kwargs['tags'])
            update_fields.append("tags = ?")
            params.append(tags_json)

        if not update_fields:
            return True  # No updates needed

        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")

        # Add learning_id to params
        params.append(learning_id)

        query = f"UPDATE learnings SET {', '.join(update_fields)} WHERE id = ?"
        affected_rows = self.db.execute_update(query, tuple(params))

        return affected_rows > 0

    def delete(self, learning_id: int) -> bool:
        """
        Delete a learning entry.

        Args:
            learning_id: ID of learning to delete

        Returns:
            True if successful, False otherwise
        """
        # Check if learning exists
        if not self.get_by_id(learning_id):
            return False

        query = "DELETE FROM learnings WHERE id = ?"
        affected_rows = self.db.execute_update(query, (learning_id,))

        return affected_rows > 0

    def search(self, search_term: str, project_id: int = None) -> List[Dict]:
        """
        Search learning entries by title, content, or tags.

        Args:
            search_term: Term to search for
            project_id: Optional project ID to filter by

        Returns:
            List of matching learning entries
        """
        query = '''
            SELECT l.*, p.name as project_name
            FROM learnings l
            LEFT JOIN projects p ON l.project_id = p.id
            WHERE (l.title LIKE ? OR l.content LIKE ? OR l.tags LIKE ?)
        '''
        params = []

        search_pattern = f"%{search_term}%"
        params = [search_pattern, search_pattern, search_pattern]

        if project_id is not None:
            query += " AND l.project_id = ?"
            params.append(project_id)

        query += " ORDER BY l.created_at DESC"

        results = self.db.execute_query(query, tuple(params))
        learnings = []

        for result in results:
            learning = dict(result)
            learning['tags'] = self.db.json_loads(learning['tags'])
            learnings.append(learning)

        return learnings

    def get_random(self, limit: int = 1, project_id: int = None) -> List[Dict]:
        """
        Get random learning entries.

        Args:
            limit: Number of random entries to return
            project_id: Optional project ID to filter by

        Returns:
            List of random learning entries
        """
        query = '''
            SELECT l.*, p.name as project_name
            FROM learnings l
            LEFT JOIN projects p ON l.project_id = p.id
            WHERE 1=1
        '''
        params = []

        if project_id is not None:
            query += " AND l.project_id = ?"
            params.append(project_id)

        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)

        results = self.db.execute_query(query, tuple(params))
        learnings = []

        for result in results:
            learning = dict(result)
            learning['tags'] = self.db.json_loads(learning['tags'])
            learnings.append(learning)

        return learnings

    def get_by_date_range(self, start_date: str, end_date: str,
                          project_id: int = None) -> List[Dict]:
        """
        Get learning entries within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            project_id: Optional project ID to filter by

        Returns:
            List of learning entries in date range
        """
        query = '''
            SELECT l.*, p.name as project_name
            FROM learnings l
            LEFT JOIN projects p ON l.project_id = p.id
            WHERE DATE(l.created_at) BETWEEN ? AND ?
        '''
        params = [start_date, end_date]

        if project_id is not None:
            query += " AND l.project_id = ?"
            params.append(project_id)

        query += " ORDER BY l.created_at DESC"

        results = self.db.execute_query(query, tuple(params))
        learnings = []

        for result in results:
            learning = dict(result)
            learning['tags'] = self.db.json_loads(learning['tags'])
            learnings.append(learning)

        return learnings

    def get_all_tags(self) -> List[str]:
        """
        Get all unique tags from learning entries.

        Returns:
            List of unique tags
        """
        query = "SELECT tags FROM learnings WHERE tags IS NOT NULL AND tags != '[]'"
        results = self.db.execute_query(query)

        all_tags = set()
        for result in results:
            tags = self.db.json_loads(result['tags'])
            all_tags.update(tags)

        return sorted(list(all_tags))

    def get_statistics(self, project_id: int = None) -> Dict[str, Any]:
        """
        Get learning statistics.

        Args:
            project_id: Optional project ID to filter by

        Returns:
            Dictionary with learning statistics
        """
        query = "SELECT COUNT(*) as total FROM learnings WHERE 1=1"
        params = []

        if project_id is not None:
            query += " AND project_id = ?"
            params.append(project_id)

        results = self.db.execute_query(query, tuple(params))
        total = results[0]['total'] if results else 0

        # Get learnings in last 30 days
        query_30 = '''
            SELECT COUNT(*) as recent
            FROM learnings
            WHERE created_at >= date('now', '-30 days')
        '''
        if project_id is not None:
            query_30 += " AND project_id = ?"

        results_30 = self.db.execute_query(query_30, tuple(params))
        recent_30 = results_30[0]['recent'] if results_30 else 0

        # Get total tags
        all_tags = self.get_all_tags()
        tag_count = len(all_tags)

        return {
            'total_learnings': total,
            'recent_learnings_30_days': recent_30,
            'total_tags': tag_count
        }