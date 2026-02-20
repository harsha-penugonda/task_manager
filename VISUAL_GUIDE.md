# Visual Guide - Lite Todo App UI

## Main Window Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ Lite Todo App                                            [_][□][X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌────────────────────┐                       │
│  │ ➕ Add Task  │  │ 📊 Generate Report │                       │
│  └──────────────┘  └────────────────────┘                       │
│                                                                   │
│ ╔════════╦══════════╦═══════════════════════╦═══════════╦═══════╗│
│ ║ Status ║ Priority ║ Title                 ║ Deadline  ║ Tags  ║│
│ ╠════════╬══════════╬═══════════════════════╬═══════════╬═══════╣│
│ ║ ☐      ║ High     ║ Fix login bug         ║ 2026-02-15║ bug   ║│ <- OVERDUE (Red)
│ ║ ✅     ║ High     ║ Review pull requests  ║ 2026-02-20║ work  ║│
│ ║ ☐      ║ High     ║ Complete docs         ║ 2026-02-25║ work  ║│
│ ║ ☐      ║ Medium   ║ Update dependencies   ║ 2026-03-01║ maint ║│
│ ║ ✅     ║ Low      ║ Prepare standup notes ║           ║ meet  ║│
│ ╚════════╩══════════╩═══════════════════════╩═══════════╩═══════╝│
│                                                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

Right-click menu:
┌───────────────┐
│ Mark Done     │
│ Edit Task     │
│ Delete Task   │
└───────────────┘
```

## Add/Edit Task Popup

```
┌─────────────────────────────────────┐
│ Add Task                     [_][X] │
├─────────────────────────────────────┤
│                                     │
│  Task Title:                        │
│  ┌───────────────────────────────┐ │
│  │ Implement new feature X       │ │
│  └───────────────────────────────┘ │
│                                     │
│  Deadline (YYYY-MM-DD):             │
│  ┌───────────────────────────────┐ │
│  │ 2026-03-01                    │ │
│  └───────────────────────────────┘ │
│                                     │
│  Priority:                          │
│  ┌───────────────────────────────┐ │
│  │ High              ▼           │ │
│  └───────────────────────────────┘ │
│                                     │
│  Tags (comma separated):            │
│  ┌───────────────────────────────┐ │
│  │ development, urgent           │ │
│  └───────────────────────────────┘ │
│                                     │
│     ┌──────┐      ┌──────┐         │
│     │ Save │      │Cancel│         │
│     └──────┘      └──────┘         │
│                                     │
└─────────────────────────────────────┘
```

## Generate Report Popup

```
┌──────────────────────────────────────────────────────────┐
│ Standup Report                                    [_][X] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Start Date: ┌────────────┐  End Date: ┌────────────┐   │
│  (YYYY-MM-DD)│ 2026-02-18 │  (YYYY-MM-DD)│2026-02-19│   │
│              └────────────┘             └────────────┘   │
│                                    ┌──────────┐          │
│                                    │ Generate │          │
│                                    └──────────┘          │
│                                                          │
│ ┌────────────────────────────────────────────────────┐  │
│ │ Standup Report                                     │  │
│ │ Period: 2026-02-18 to 2026-02-19                   │  │
│ │ ==================================================  │  │
│ │                                                     │  │
│ │ DONE:                                              │  │
│ │ - Review pull requests (completed: 2026-02-19)     │  │
│ │   [work, code-review]                              │  │
│ │ - Prepare standup notes (completed: 2026-02-18)    │  │
│ │   [meeting]                                        │  │
│ │                                                     │  │
│ │ PENDING:                                           │  │
│ │ - Fix login bug (deadline: 2026-02-15)             │  │
│ │   [Priority: High] [bug, urgent]                   │  │
│ │ - Complete project documentation                   │  │
│ │   (deadline: 2026-02-25) [Priority: High]          │  │
│ │   [work, documentation]                            │  │
│ │ - Update dependencies (deadline: 2026-03-01)       │  │
│ │   [maintenance]                                    │  │
│ │                                                     │  │
│ └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────┐    ┌─────────────────┐            │
│  │Copy to Clipboard │    │ Export to File  │            │
│  └──────────────────┘    └─────────────────┘            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Color Scheme

### Main Window

- **Background**: Default system (light gray/white)
- **Add Task Button**: Green (#4CAF50) with white text
- **Generate Report Button**: Blue (#2196F3) with white text
- **Overdue Tasks**: Light red background (#FFC0C0)

### Status Indicators

- **✅**: Task completed (green checkmark)
- **☐**: Task pending (empty checkbox)

### Priority Colors (Future Enhancement)

- **High**: Could be red/orange
- **Medium**: Could be yellow
- **Low**: Could be green

## User Interaction Flow

```
Start
  │
  ├─→ [Add Task] ──→ Fill Form ──→ Save ──→ Task appears in list
  │                      │
  │                      └─→ Cancel ──→ Back to main window
  │
  ├─→ [Right-click Task] ──┬─→ Mark Done ──→ Status changes to ✅
  │                         │
  │                         ├─→ Edit ──→ Update Form ──→ Save
  │                         │
  │                         └─→ Delete ──→ Confirm ──→ Task removed
  │
  ├─→ [Sort by Column] ──→ Click header ──→ List reorders
  │
  └─→ [Generate Report] ──→ Select dates ──→ Generate
                                │
                                ├─→ Copy to clipboard
                                │
                                └─→ Export to file
```

## Example Workflows

### Morning Standup

1. Open app
2. Click "📊 Generate Report"
3. Enter yesterday's date as both start and end
4. Click "Generate"
5. Review DONE tasks (what you did yesterday)
6. Review PENDING tasks (what you'll do today)
7. Click "Copy to Clipboard"
8. Paste in team meeting

### Quick Task Entry

1. Click "➕ Add Task"
2. Type task title
3. Press Enter or click "Save"
4. Task appears in list

### Weekly Planning

1. Sort by Priority (click Priority header)
2. Review High priority tasks
3. Sort by Deadline (click Deadline header)
4. Review upcoming deadlines
5. Mark completed tasks as done
6. Add new tasks as needed

## Keyboard Navigation (Current)

- **Tab**: Navigate between fields in popups
- **Enter**: Submit forms (when focused on buttons)
- **Esc**: Close popups (standard window behavior)
- **Right-click**: Open context menu

## Screen Space Optimization

### Minimum Resolution

- 800x600 pixels (app sized to 800x550)

### Recommended Resolution

- 1024x768 or higher for comfortable use

### Column Widths

- Status: 60px (icon only)
- Priority: 80px (short text)
- Title: 250px (main content)
- Deadline: 100px (date)
- Tags: 150px (multiple tags)

Total width: ~640px + scrollbar + padding = 800px

## Accessibility Features (Current)

- ✅ Clear visual hierarchy
- ✅ Large clickable areas
- ✅ Color + text indicators (not just color)
- ✅ Confirmation dialogs for destructive actions
- ✅ Error messages with clear instructions

## Future UI Enhancements

### Planned

- [ ] Dark mode toggle
- [ ] Keyboard shortcuts overlay
- [ ] Inline editing (double-click)
- [ ] Drag-and-drop reordering
- [ ] Task notes/description panel
- [ ] Quick filters toolbar
- [ ] System tray integration
- [ ] Mini-mode (compact view)

### Under Consideration

- [ ] Custom themes
- [ ] Font size adjustment
- [ ] Custom color schemes per priority
- [ ] Timeline view
- [ ] Kanban board view
- [ ] Calendar integration

---

This visual guide complements the README.md and provides a clear picture
of the user interface and interaction patterns.
