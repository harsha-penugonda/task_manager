# Quick Reference Guide - Lite Todo App

## Keyboard & Mouse Actions

### Main Window

| Action            | Method                            |
| ----------------- | --------------------------------- |
| Add new task      | Click "➕ Add Task" button        |
| Generate report   | Click "📊 Generate Report" button |
| Sort tasks        | Click any column header           |
| Open context menu | Right-click on a task             |

### Context Menu (Right-Click)

| Option      | Description                         |
| ----------- | ----------------------------------- |
| Mark Done   | Mark the selected task as completed |
| Edit Task   | Open edit dialog for the task       |
| Delete Task | Remove task (with confirmation)     |

### Task Popup

| Field    | Details                               |
| -------- | ------------------------------------- |
| Title    | **Required** - Task name/description  |
| Deadline | **Optional** - Format: YYYY-MM-DD     |
| Priority | **Optional** - Default: Medium        |
| Tags     | **Optional** - Comma-separated values |

## Color Coding

- **Light Red Background**: Overdue pending tasks
- **Green Button**: Add Task action
- **Blue Button**: Generate Report action
- **✅**: Task completed
- **☐**: Task pending

## Priority Levels

1. **High**: Urgent, critical tasks
2. **Medium**: Normal priority (default)
3. **Low**: Nice-to-have, non-urgent

## Date Range Filtering (Reports)

| Start Date | End Date   | Result                   |
| ---------- | ---------- | ------------------------ |
| Empty      | Empty      | All tasks                |
| 2026-02-01 | Empty      | Tasks from Feb 1 onwards |
| Empty      | 2026-02-28 | Tasks until Feb 28       |
| 2026-02-01 | 2026-02-28 | Tasks in February        |

## Report Sections

### DONE Section

- Shows tasks completed within the date range
- Includes completion date
- Shows tags if present

### PENDING Section

- Shows all pending tasks (regardless of date range)
- Includes deadline if set
- Shows priority if not Medium
- Shows tags if present

## Common Workflows

### Daily Standup Report

1. Click "📊 Generate Report"
2. Enter yesterday's date as Start Date
3. Enter today's date as End Date
4. Click "Generate"
5. Click "Copy to Clipboard"
6. Paste in team chat/meeting

### Weekly Review

1. Click "📊 Generate Report"
2. Enter last Monday as Start Date
3. Enter today as End Date
4. Click "Generate"
5. Click "Export to File" for records

### Quick Task Entry

1. Click "➕ Add Task"
2. Enter title
3. Click "Save" (other fields optional)

### Bulk Task Management

1. Sort by Priority (click Priority header)
2. Right-click high-priority tasks
3. Mark done or edit as needed

## Tips

### Tag Suggestions

- **work**, **personal** - Context
- **urgent**, **important** - Priority modifiers
- **bug**, **feature** - Type of work
- **meeting**, **email** - Action type
- **client-name** - Client/project reference

### Deadline Best Practices

- Set realistic deadlines
- Use sorting to prioritize work
- Review overdue tasks daily (highlighted in red)
- Update or mark done overdue tasks promptly

### Report Best Practices

- Generate daily for standup meetings
- Use weekly reports for retrospectives
- Export monthly reports for records
- Include relevant tags for context

## Data Management

### Backup

```bash
# Create backup
cp tasks.json tasks_backup_$(date +%Y%m%d).json

# Restore from backup
cp tasks_backup_20260219.json tasks.json
```

### Reset

```bash
# Clear all tasks
echo "[]" > tasks.json
```

### Manual Edit

Tasks can be edited directly in `tasks.json`:

```json
{
    "title": "New Task",
    "deadline": "2026-03-01",
    "priority": "High",
    "status": "Pending",
    "tags": ["example"],
    "completion_date": null
}
```

## Troubleshooting Quick Fixes

| Issue                    | Quick Fix                    |
| ------------------------ | ---------------------------- |
| Can't save task          | Check title is not empty     |
| Invalid date error       | Use YYYY-MM-DD format        |
| Tasks not sorting        | Click column header again    |
| Report shows wrong tasks | Check date range format      |
| App won't start          | Verify Python 3.7+ installed |

## Performance Notes

- **Recommended max tasks**: ~500 (for optimal performance)
- **Storage**: ~1KB per task
- **Startup time**: < 1 second for ~100 tasks
- **Sort time**: Instant for < 1000 tasks

---

For detailed documentation, see README.md
