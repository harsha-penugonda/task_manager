# Lite Todo / Standup App - Optimized Edition

A powerful, lightweight task management application with advanced features including dark mode, search & filtering, keyboard shortcuts, and automatic backups.

## 🚀 New Features (Optimized Version)

### ⌨️ Keyboard Shortcuts

- **Ctrl+N**: Add new task
- **Ctrl+R**: Generate report
- **Ctrl+F**: Focus search box
- **F5**: Refresh tasks from file
- **Enter**: Mark selected task as done (when task selected)
- **Delete**: Delete selected task (when task selected)
- **Escape**: Close popups
- **Double-click**: Edit task

### 🔍 Search & Filtering

- **Real-time Search**: Search by task title, tags, or priority
- **Quick Filters**:
    - All tasks
    - Pending only
    - Done only
    - Overdue tasks
    - High priority tasks

### 🌙 Dark Mode

- Toggle between light and dark themes
- Preferences saved automatically
- Easy on the eyes for night work

### 📊 Enhanced Status Bar

- Real-time task statistics:
    - Total tasks
    - Pending count
    - Done count
    - Overdue count
    - Filtered count (when filtering active)

### 🔄 Data Reliability

- **Automatic Backups**: Every save creates a backup file
- **Corruption Recovery**: Auto-restore from backup if main file corrupted
- **Safe Operations**: All data operations protected with error handling

### 🎨 Improved UI

- Modern flat design
- Color-coded buttons with icons
- Scrollable task list
- Better spacing and readability
- Radio buttons for priority selection
- Enhanced report formatting

### 📋 Additional Features

- **Copy Task Title**: Right-click menu option
- **Refresh Button**: Reload tasks from file
- **Double-click to Edit**: Quick access to edit dialog
- **Numbered Reports**: Better formatted standup reports
- **Better Visual Feedback**: Hover effects on buttons

## 📦 Installation

```bash
# No installation required! Uses only Python standard library
cd task_manager
python main.py
```

## 🎯 Quick Start Guide

### Adding a Task

1. Click **➕ Add Task** or press **Ctrl+N**
2. Fill in task details (title is required)
3. Press **Enter** or click **💾 Save**

### Finding Tasks

1. Use the **🔍 Search** box to find tasks by keyword
2. Use **Filter** radio buttons for quick views
3. Click column headers to sort

### Managing Tasks

- **Right-click** any task for quick actions
- **Double-click** to edit
- Select and press **Enter** to mark done
- Select and press **Delete** to remove

### Generating Reports

1. Click **📊 Report** or press **Ctrl+R**
2. Optionally enter date range
3. Click **📊 Generate**
4. **📋 Copy** to clipboard or **💾 Export** to file

### Theme Switching

- Click **🌙** (moon) or **☀️** (sun) button
- Restart app to apply new theme
- Preference saved for next session

## ⌨️ Complete Keyboard Shortcuts

| Shortcut     | Action                      |
| ------------ | --------------------------- |
| Ctrl+N       | Add new task                |
| Ctrl+R       | Generate report             |
| Ctrl+F       | Focus search box            |
| F5           | Refresh tasks               |
| Enter        | Mark done (task selected)   |
| Delete       | Delete task (task selected) |
| Double-click | Edit task                   |
| Escape       | Close popup/dialog          |
| Return       | Save form (in dialogs)      |

## 🎨 Color Scheme

### Light Mode

- Background: Light gray (#f5f5f5)
- Buttons: White with colored accents
- Overdue: Light red (#ffcccb)

### Dark Mode

- Background: Dark gray (#2b2b2b)
- Text: White
- Buttons: Dark with colored accents
- Overdue: Dark red (#8b0000)

## 📁 File Structure

```
task_manager/
├── main.py                 # Optimized main application
├── main_old.py            # Original version (backup)
├── main_optimized.py      # Optimized source (duplicate)
├── task_manager.py        # Enhanced task logic with backups
├── tasks.json            # Task data
├── tasks_backup.json     # Automatic backup (auto-created)
├── config.json           # User preferences (auto-created)
├── README.md             # This file
└── QUICK_REFERENCE.md    # Quick reference guide
```

## 🔒 Data Safety

### Automatic Backups

- Every save creates `tasks_backup.json`
- Backup is previous version before changes
- Used for recovery if main file corrupted

### Error Recovery

1. If `tasks.json` is corrupted, app automatically:
    - Detects the corruption
    - Restores from `tasks_backup.json`
    - Notifies you of the recovery

2. If no backup exists:
    - Creates new empty task list
    - Preserves any recoverable data

### Manual Backup

```bash
# Create timestamped backup
cp tasks.json tasks_$(date +%Y%m%d_%H%M%S).json
```

## 🆕 What's New vs Original

| Feature            | Original | Optimized |
| ------------------ | -------- | --------- |
| Keyboard shortcuts | ❌       | ✅        |
| Search             | ❌       | ✅        |
| Filtering          | ❌       | ✅        |
| Dark mode          | ❌       | ✅        |
| Status bar         | ❌       | ✅        |
| Auto backup        | ❌       | ✅        |
| Refresh button     | ❌       | ✅        |
| Copy task title    | ❌       | ✅        |
| Double-click edit  | ❌       | ✅        |
| Scrollable list    | ❌       | ✅        |
| Radio priorities   | ❌       | ✅        |
| Enhanced reports   | ❌       | ✅        |
| Hover effects      | ❌       | ✅        |

## 🐛 Troubleshooting

### App doesn't start

```bash
# Check Python version
python --version  # Should be 3.7+

# Try running directly
python main.py
```

### Dark mode not applying

- Restart the app after toggling theme
- Check `config.json` exists with `"dark_mode": true`

### Tasks not saving

- Check file permissions in directory
- Look for `tasks_backup.json` for recovery
- Check terminal for error messages

### Search not working

- Clear search box and try again
- Check spelling of search term
- Try using filter buttons instead

## 💡 Tips & Tricks

### Workflow Optimization

1. **Quick Add**: Press Ctrl+N, type title, press Enter
2. **Bulk Operations**: Use filters to view specific groups
3. **Daily Standup**: Ctrl+R, enter yesterday-today, Copy
4. **Focus Mode**: Filter by "High Priority" or "Overdue"

### Search Tips

- Search by partial words: "doc" finds "documentation"
- Search by tags: "work" finds all work-tagged tasks
- Search by priority: "high" shows high priority tasks

### Keyboard-Only Workflow

1. Ctrl+N → Type task → Enter (Add task)
2. Arrow keys → Enter (Mark done)
3. Arrow keys → Delete (Remove task)
4. Ctrl+F → Type → Enter (Search)
5. Ctrl+R → Enter → Ctrl+C (Generate & copy report)

## 📈 Performance

- **Startup**: < 1 second
- **Task Load**: Instant for < 1000 tasks
- **Search**: Real-time for < 500 tasks
- **Memory**: ~30-50 MB
- **Storage**: ~1 KB per task

## 🔮 Future Enhancements

Potential features for next version:

- [ ] Drag & drop task reordering
- [ ] Recurring tasks
- [ ] Task notes/descriptions
- [ ] Calendar view
- [ ] Export to PDF
- [ ] Cloud sync
- [ ] Mobile app companion
- [ ] Pomodoro timer integration

## 📝 Version History

**v2.0 (Optimized Edition)** - February 19, 2026

- Added keyboard shortcuts
- Added search & filtering
- Added dark mode
- Added status bar
- Added automatic backups
- Enhanced UI/UX
- Improved error handling

**v1.0** - February 19, 2026

- Initial release
- Core task management
- Sorting
- Reports
- Basic UI

## 🙏 Acknowledgments

Built with Python and tkinter - no external dependencies required!

## 📄 License

Open-source - free for personal and commercial use.

---

**Pro Tip**: Press Ctrl+N right now to add your first task and start being productive! 🚀
