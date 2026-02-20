# Lite Todo / Standup App

A lightweight, cross-platform task management application designed to help users track tasks with deadlines and priorities, mark them as done, and generate standup-ready reports.

## Features

### ✨ Task Management

- **Add Tasks**: Create tasks with title (required), deadline, priority (High/Medium/Low), and tags
- **Edit Tasks**: Update any task attribute through a simple popup interface
- **Delete Tasks**: Remove tasks with confirmation dialog
- **Mark Done**: Change task status to Done with automatic completion date tracking
- **Task Status**: Visual indicators (✅ for done, ☐ for pending)
- **Overdue Highlighting**: Overdue pending tasks are highlighted in light red

### 📊 Task Display

- **Sortable Columns**: Click on any column header to sort
    - Status: Pending/Done
    - Priority: High → Medium → Low
    - Title: Alphabetical
    - Deadline: Chronological (ascending)
    - Tags: Alphabetical
- **Right-Click Menu**: Quick access to Mark Done, Edit, and Delete actions
- **Optimized Layout**: Column widths optimized for readability

### 📈 Standup Report Generation

- **Date Range Selection**: Filter tasks by completion date range
- **Two Sections**:
    - **Done**: Tasks completed in the selected period (with completion dates)
    - **Pending**: Current pending tasks (with deadlines and priorities)
- **Report Actions**:
    - Copy to clipboard for easy sharing
    - Export to text file for archiving
- **Flexible Filtering**: Leave dates blank to show all tasks

### 💾 Data Storage

- **Local JSON Storage**: Tasks stored in `tasks.json` file
- **Human-Readable Format**: Easy to edit manually if needed
- **Persistent Data**: Tasks persist across app restarts
- **Extensible**: JSON format ready for future cloud sync features

## Installation

### Requirements

- Python 3.7+
- tkinter (usually included with Python)

### Quick Start

```bash
# Clone or download the project
cd task_manager

# Run the application
python main.py
```

## Usage

### Adding a Task

1. Click the "➕ Add Task" button
2. Fill in the task details:
    - **Title**: Required field
    - **Deadline**: Optional, format YYYY-MM-DD (e.g., 2026-12-31)
    - **Priority**: Select High, Medium, or Low
    - **Tags**: Optional, comma-separated (e.g., "work, urgent")
3. Click "Save" or "Cancel"

### Managing Tasks

- **Sort**: Click any column header to sort tasks
- **Mark Done**: Right-click a task → "Mark Done"
- **Edit**: Right-click a task → "Edit Task"
- **Delete**: Right-click a task → "Delete Task" (with confirmation)

### Generating Reports

1. Click the "📊 Generate Report" button
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
├── main.py              # GUI application
├── task_manager.py      # Task logic and data management
├── tasks.json          # Task data storage (created automatically)
└── README.md           # This file
```

## Features Implemented

### Core Requirements ✅

- [x] Add, Edit, Delete, Mark Done tasks
- [x] Task prioritization (High/Medium/Low)
- [x] Deadline tracking with overdue highlighting
- [x] Tag support for categorization
- [x] Sortable task table
- [x] Right-click context menu
- [x] Standup report generation with date filtering
- [x] Copy report to clipboard
- [x] Export report to file
- [x] Local JSON storage
- [x] Completion date tracking

### UI/UX ✅

- [x] Minimalist, intuitive interface
- [x] Visual status indicators
- [x] Color-coded buttons
- [x] Overdue task highlighting
- [x] Input validation for dates
- [x] Confirmation dialogs for destructive actions

## Future Enhancements (Optional)

The following features can be added in future versions:

- [ ] Keyboard shortcuts (e.g., Ctrl+N for new task)
- [ ] Dark mode / Light mode toggle
- [ ] Tag-based filtering
- [ ] System notifications for approaching deadlines
- [ ] Cloud sync across devices
- [ ] Export reports in PDF format
- [ ] Recurring tasks
- [ ] Task notes/descriptions
- [ ] Search functionality

## Tips & Best Practices

1. **Date Format**: Always use YYYY-MM-DD format for deadlines
2. **Priorities**: Use High for urgent tasks, Medium for normal tasks, Low for nice-to-haves
3. **Tags**: Keep tags short and consistent (e.g., "work", "personal", "urgent")
4. **Reports**: Generate reports regularly for standup meetings
5. **Sorting**: Sort by deadline to see what's coming up next
6. **Backup**: Periodically backup your `tasks.json` file

## Troubleshooting

**Q: The app doesn't start**

- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python -m tkinter`

**Q: Tasks don't persist after closing**

- Check that `tasks.json` has write permissions
- Verify the file is in the same directory as the scripts

**Q: Invalid date error**

- Use the format YYYY-MM-DD (e.g., 2026-03-15)
- Leave the deadline field blank if no deadline

**Q: Tasks disappear after edit**

- This shouldn't happen - check `tasks.json` for data integrity
- Report as a bug if it persists

## License

This project is open-source and available for personal and commercial use.

## Contributing

Suggestions and improvements are welcome! Feel free to fork and submit pull requests.

---

**Version**: 1.0  
**Last Updated**: February 19, 2026
