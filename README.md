# Task Manager Pro

A modern, feature-rich task management application built with Python and Tkinter. Designed to help users track tasks with deadlines and priorities, manage task status, and generate standup-ready reports.

## Features

### ✨ Task Management

- **Add Tasks**: Create tasks with title (required), deadline, priority (High/Medium/Low), and tags
- **Edit Tasks**: Update any task attribute through a modern popup dialog
- **Delete Tasks**: Remove tasks with confirmation dialog
- **Mark Done**: Change task status to Done with automatic completion date tracking
- **Task Status**: Visual indicators (✅ for done, ☐ for pending)
- **Overdue Highlighting**: Overdue pending tasks are highlighted in red

### 📊 Task Display

- **Sortable Columns**: Click on any column header to sort
    - Status: Pending/Done
    - Priority: High → Medium → Low
    - Title: Alphabetical
    - Deadline: Chronological
    - Tags: Alphabetical
- **Right-Click Menu**: Quick access to Mark Done, Edit, and Delete actions
- **Tooltips**: Hover over cells to see full text for truncated content

### 🔍 Search & Filter

- **Real-time Search**: Search tasks by title, tags, or any field
- **Quick Filters**: Filter by All, Pending, Done, Overdue, or High Priority
- **Keyboard Shortcuts**:
    - `Ctrl+N` - Add new task
    - `Ctrl+R` - Generate report
    - `Ctrl+F` - Focus search box
    - `F5` - Refresh tasks

### 🎨 Theming

- **Dark Mode / Light Mode**: Toggle between themes with one click
- **Persistent Theme**: Your theme preference is saved in `config.json`
- **Modern UI**: Clean design with color-coded buttons and visual hierarchy

### 📈 Standup Report Generation

- **Date Range Selection**: Filter tasks by completion date range
- **Two Sections**:
    - **Done**: Tasks completed in the selected period (with completion dates)
    - **Pending**: Current pending tasks (with deadlines and priorities)
- **Report Actions**:
    - Copy to clipboard for easy sharing
    - Export to text file for archiving
- **Calendar Widget**: Modern date picker for selecting date ranges

### 💾 Data Storage

- **Local JSON Storage**: Tasks stored in `tasks.json` file
- **Automatic Backup**: Backup file `tasks_backup.json` for data recovery
- **Persistent Data**: Tasks persist across app restarts
- **Human-Readable Format**: Easy to edit manually if needed

## Installation

### Requirements

- Python 3.7+
- tkinter (usually included with Python)
- tkcalendar (for date picker widget)

### Quick Start

```bash
# Clone or download the project
cd task_manager

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Verify tkinter Installation

```bash
python -m tkinter
```

If this opens a small window, tkinter is installed correctly.

## Building Standalone Executable

You can build a standalone `.exe` file that runs without Python installed.

### Build Requirements

- PyInstaller (installed automatically by the build script)

### Build Steps

```bash
# Run the build script
python build.py
```

This will:
1. Install PyInstaller if not present
2. Create a single executable file
3. Output the executable to `dist/TaskManager.exe`

### Build Output

```
dist/
└── TaskManager.exe    # Standalone executable (~15-20 MB)
```

### Adding a Custom Icon

Place an `icon.ico` file in the project root before building. The build script will automatically use it.

### Distribution

To distribute the application:
1. Share the `dist/TaskManager.exe` file
2. The `tasks.json` file will be created automatically on first run

## Usage

### Adding a Task

1. Click the "➕ Add Task" button (or press `Ctrl+N`)
2. Fill in the task details:
    - **Title**: Required field
    - **Deadline**: Optional, use the calendar picker or enter YYYY-MM-DD format
    - **Priority**: Select High, Medium, or Low
    - **Tags**: Optional, comma-separated (e.g., "work, urgent")
3. Click "Save"

### Managing Tasks

- **Search**: Type in the search box to filter tasks
- **Filter**: Click filter buttons (All, Pending, Done, Overdue, High Priority)
- **Sort**: Click any column header to sort tasks
- **Mark Done**: Right-click a task → "Mark Done"
- **Edit**: Right-click a task → "Edit Task"
- **Delete**: Right-click a task → "Delete Task" (with confirmation)

### Toggling Theme

- Click "🌙 Dark" or "☀️ Light" button in the header
- Theme preference is saved automatically

### Generating Reports

1. Click the "📊 Report" button (or press `Ctrl+R`)
2. Optionally enter date range:
    - **Start Date**: Filter completed tasks from this date
    - **End Date**: Filter completed tasks until this date
    - Leave blank to show all tasks
3. Click "Generate" to update the report
4. Actions:
    - **Copy to Clipboard**: Share in standup meetings
    - **Export to File**: Save as .txt file

## Task Data Structure

Each task is stored in JSON format:

```json
{
    "title": "Implement feature X",
    "deadline": "2026-03-15",
    "priority": "High",
    "status": "Pending",
    "tags": ["development", "urgent"],
    "completion_date": null
}
```

When a task is marked done, `completion_date` is automatically set to the current date.

## File Structure

```
task_manager/
├── main.py              # Application entry point
├── app.py               # Main application class and UI
├── task_manager.py      # Task logic and data management
├── dialogs.py           # Dialog popups (Add/Edit Task, Report)
├── widgets.py           # Custom widgets (tooltips, buttons)
├── theme.py             # Theme and color configuration
├── utils.py             # Utility functions (DPI awareness, etc.)
├── build.py             # Build script for creating executables
├── requirements.txt     # Python dependencies
├── config.json          # User preferences (theme, etc.)
├── tasks.json           # Task data storage (created automatically)
├── tasks_backup.json    # Backup of task data
└── README.md            # This file
```

## Features Implemented

### Core Functionality ✅

- [x] Add, Edit, Delete, Mark Done tasks
- [x] Task prioritization (High/Medium/Low)
- [x] Deadline tracking with overdue highlighting
- [x] Tag support for categorization
- [x] Sortable task table
- [x] Right-click context menu
- [x] Standup report generation with date filtering
- [x] Copy report to clipboard
- [x] Export report to file
- [x] Local JSON storage with backup
- [x] Completion date tracking

### UI/UX Features ✅

- [x] Modern, clean interface
- [x] Dark mode / Light mode toggle
- [x] Real-time search functionality
- [x] Quick filter buttons
- [x] Keyboard shortcuts
- [x] Calendar date picker
- [x] Cell tooltips for long text
- [x] Visual status indicators
- [x] Color-coded buttons
- [x] Overdue task highlighting
- [x] Input validation
- [x] Confirmation dialogs
- [x] High-DPI support

## Future Enhancements

- [ ] System notifications for approaching deadlines
- [ ] Cloud sync across devices
- [ ] Export reports in PDF format
- [ ] Recurring tasks
- [ ] Task notes/descriptions
- [ ] Subtasks support
- [ ] Task attachments
- [ ] Multiple task lists/projects

## Tips & Best Practices

1. **Date Format**: Use the calendar picker or YYYY-MM-DD format for deadlines
2. **Priorities**: Use High for urgent tasks, Medium for normal tasks, Low for nice-to-haves
3. **Tags**: Keep tags short and consistent (e.g., "work", "personal", "urgent")
4. **Reports**: Generate reports regularly for standup meetings
5. **Sorting**: Sort by deadline to see what's coming up next
6. **Backup**: The app automatically creates `tasks_backup.json`

## Troubleshooting

**Q: The app doesn't start**

- Ensure Python 3.7+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check that tkinter is available: `python -m tkinter`

**Q: Calendar picker not showing**

- Install tkcalendar: `pip install tkcalendar`

**Q: Tasks don't persist after closing**

- Check that `tasks.json` has write permissions
- Verify the file is in the same directory as the executable

**Q: Invalid date error**

- Use the calendar picker or format YYYY-MM-DD (e.g., 2026-03-15)
- Leave the deadline field blank if no deadline

**Q: Building fails**

- Ensure PyInstaller is installed: `pip install pyinstaller`
- Run from the project directory
- Check for antivirus interference

## License

This project is open-source and available for personal and commercial use.

## Contributing

Suggestions and improvements are welcome! Feel free to fork and submit pull requests.

---

**Version**: 2.0  
**Last Updated**: February 20, 2026
