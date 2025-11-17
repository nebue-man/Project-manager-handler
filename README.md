# Personal Project Manager

A cross-platform desktop application built with Python and CustomTkinter that helps you manage your projects, capture learnings during development, and stay on track with notifications.

## Features

### 📁 Project Management
- Create and manage projects with deadlines, priorities, and progress tracking
- Add descriptions and tags for better organization
- Visual progress bars and status indicators
- Deadline tracking with overdue warnings

### 📚 Learning Capture
- Document insights, discoveries, and lessons learned
- Associate learnings with specific projects
- Tag-based organization for easy retrieval
- Rich text content with templates for quick capture

### 🔔 Smart Notifications
- **Deadline Alerts**: Get notified before project deadlines (customizable warning periods)
- **Learning Reminders**: Random learning notifications twice daily to reinforce knowledge
- **Quiet Hours**: Respect your focus time with configurable quiet hours
- **Desktop Integration**: Native system notifications

### 🎨 Modern Interface
- Clean, intuitive sidebar navigation
- Dark/Light/System theme support
- Responsive project and learning cards
- Search functionality across projects and learnings

### ⚙️ Configuration & Data
- Customizable notification schedules
- Data export/import capabilities
- Automatic database backups
- Persistent configuration settings

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

1. **Clone or download the project:**
   ```bash
   # If cloning from git
   git clone <repository-url>
   cd Project-manager-handler

   # Or download and extract the ZIP file, then navigate to the directory
   cd Project-manager-handler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Dependencies (requirements.txt)
```
customtkinter>=5.2.0    # Modern UI components
plyer>=2.1.0            # Cross-platform notifications
APScheduler>=3.10.0     # Background task scheduling
```

## Usage

### Getting Started

1. **Launch the application** by running `python main.py`
2. **Create your first project** using the "+ New Project" button in the sidebar
3. **Capture learnings** as you work using the "+ Capture Learning" button
4. **Configure notifications** in Settings to match your schedule

### Project Management

**Creating a Project:**
- Click "+ New Project" in the sidebar
- Fill in required fields:
  - **Name** (required): Project title
  - **Deadline** (required): Target completion date
  - **Priority**: Low, Medium, or High
  - **Description**: Optional details about the project
  - **Tags**: Comma-separated keywords for organization
- Set initial progress with the slider
- Click "Create Project"

**Managing Projects:**
- View all active projects in the Projects tab
- See progress bars, deadline countdowns, and status indicators
- Projects are color-coded by priority and status
- Use the search bar to find specific projects

### Learning Capture

**Documenting Learnings:**
- Click "+ Capture Learning" to open the learning dialog
- **Title** (required, max 100 chars): A concise summary of what you learned
- **Content** (required, max 2000 chars): Detailed explanation
- **Associated Project**: Link to a specific project or keep it general
- **Tags**: Categorize your learnings for easy retrieval

**Quick Templates:**
- Problem/Solution: Document challenges and their solutions
- Key Insight: Capture important discoveries
- Technical Learning: Note technical implementation details
- Process Improvement: Record workflow improvements
- Best Practice: Document standards and best practices

### Notifications

**Default Schedule:**
- **Learning Reminders**: 9:00 AM and 2:00 PM daily
- **Deadline Warnings**: 1, 3, and 7 days before deadlines
- **Quiet Hours**: 10:00 PM to 8:00 AM (notifications disabled)

**Customization:**
- Adjust all notification times in Settings
- Enable/disable sound notifications
- Configure custom deadline warning periods
- Set your preferred quiet hours

### Settings Configuration

Access Settings via the sidebar to configure:

**Notifications Tab:**
- Toggle all notifications on/off
- Set learning reminder times (24-hour format, comma-separated)
- Configure deadline warning periods
- Set quiet hours for uninterrupted work
- Enable/disable notification sounds

**Appearance Tab:**
- Choose theme: Light, Dark, or System
- Adjust font size (10-18px)
- Set items per page for list views

**Database Tab:**
- Enable automatic backups
- Set backup interval (days)
- Configure maximum backup retention
- Manual backup, export, and import options

## Data Storage

### Database
- Uses SQLite for local data storage
- Database file: `project_manager.db` (created on first run)
- Automatic schema initialization
- Data is stored locally and privately

### Backups
- Automatic backups can be enabled in Settings
- Backup files include timestamp: `project_manager_backup_YYYYMMDD_HHMMSS.db`
- Manual backup options available in Settings
- Export functionality for data portability

## Keyboard Shortcuts

### Application
- `Ctrl+Q` or `Alt+F4`: Quit application
- `F5`: Refresh current view

### Dialog Windows
- `Enter`: Confirm/Save action
- `Escape`: Cancel/Close dialog
- `Ctrl+S`: Save (in learning dialog)
- `Ctrl+Enter`: Save (alternative)

## Troubleshooting

### Common Issues

**Application won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r requirements.txt

# Run in verbose mode
python -v main.py
```

**Notifications not working:**
- Check system notification permissions
- Test notifications in Settings dialog
- Verify plyer installation: `pip show plyer`

**Database errors:**
- Ensure write permissions in application directory
- Delete corrupted database file (`project_manager.db`) to recreate
- Check available disk space

**UI display issues:**
- Update customtkinter: `pip install --upgrade customtkinter`
- Try different theme setting in Preferences
- Restart application after theme changes

### Platform-Specific Notes

**Windows:**
- May need to allow notifications through Windows Security
- Run as Administrator if notification permissions issues persist

**macOS:**
- Grant notification permissions in System Preferences
- May need to allow app access in Security & Privacy

**Linux:**
- Install notification daemon: `sudo apt install libnotify-bin` (Ubuntu/Debian)
- Ensure desktop environment supports notifications

## Development

### Project Structure
```
Project-manager-handler/
├── src/
│   ├── app.py                    # Main application entry point
│   ├── ui/
│   │   ├── main_window.py        # Main application window
│   │   ├── components/           # UI components
│   │   └── dialogs/              # Dialog windows
│   ├── models/
│   │   ├── database.py           # SQLite database operations
│   │   ├── project.py            # Project data model
│   │   └── learning.py           # Learning data model
│   ├── services/
│   │   ├── notification_service.py  # Desktop notifications
│   │   └── scheduler_service.py     # Background scheduling
│   └── utils/
│       ├── config.py             # Application configuration
│       └── helpers.py            # Utility functions
├── requirements.txt              # Python dependencies
├── main.py                       # Application launcher
└── README.md                     # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Extending the Application

**Adding New Features:**
- Follow existing code patterns and naming conventions
- Add proper error handling and validation
- Update documentation for new features
- Test cross-platform compatibility

**UI Components:**
- Use CustomTkinter for consistency
- Follow the established design patterns
- Implement proper keyboard navigation
- Ensure accessibility compliance

## License

This project is open-source and available under the MIT License.

## Support

For issues, feature requests, or questions:
1. Check the troubleshooting section above
2. Search existing issues if available
3. Create detailed bug reports with:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Error messages/tracebacks
4. Include screenshots for UI issues when applicable

---

**Happy project managing!** 🚀

Built with ❤️ using Python and CustomTkinter