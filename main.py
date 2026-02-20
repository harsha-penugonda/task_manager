# main_optimized.py - Enhanced Lite Todo App
import os
# Suppress Tk deprecation warning on macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import json
try:
    from tkcalendar import DateEntry
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False
from task_manager import Task, load_tasks, save_tasks, add_task, delete_task, mark_task_done, edit_task


class TreeviewTooltip:
    """Tooltip that shows full text when hovering over treeview cells"""
    def __init__(self, tree, delay=500):
        self.tree = tree
        self.delay = delay
        self.tooltip = None
        self.after_id = None
        self.current_item = None
        self.current_col = None
        
        self.tree.bind('<Motion>', self.on_motion)
        self.tree.bind('<Leave>', self.hide_tooltip)
    
    def on_motion(self, event):
        """Handle mouse movement over treeview"""
        # Cancel any pending tooltip
        if self.after_id:
            self.tree.after_cancel(self.after_id)
            self.after_id = None
        
        # Get item and column under cursor
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        
        # If moved to different cell, hide current tooltip
        if item != self.current_item or col != self.current_col:
            self.hide_tooltip()
            self.current_item = item
            self.current_col = col
        
        # Schedule tooltip if over a valid cell
        if item and col:
            self.after_id = self.tree.after(self.delay, lambda: self.show_tooltip(event, item, col))
    
    def show_tooltip(self, event, item, col):
        """Show tooltip with full cell text"""
        if not item or not col:
            return
        
        try:
            # Get column index (col is like '#1', '#2', etc.)
            col_idx = int(col.replace('#', '')) - 1
            values = self.tree.item(item, 'values')
            
            if col_idx < 0 or col_idx >= len(values):
                return
            
            text = str(values[col_idx])
            
            # Only show tooltip if text is long enough to be truncated
            if len(text) < 15:
                return
            
            # Create tooltip window
            self.tooltip = tk.Toplevel(self.tree)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_attributes('-topmost', True)
            
            # Position tooltip near cursor
            x = event.x_root + 15
            y = event.y_root + 10
            
            # Create tooltip label with styling
            label = tk.Label(self.tooltip, text=text,
                           bg='#fffde7', fg='#1e293b',
                           font=('Segoe UI', 10),
                           relief=tk.SOLID, borderwidth=1,
                           wraplength=400, justify=tk.LEFT,
                           padx=8, pady=6)
            label.pack()
            
            # Adjust position to keep tooltip on screen
            self.tooltip.update_idletasks()
            tooltip_width = self.tooltip.winfo_width()
            tooltip_height = self.tooltip.winfo_height()
            screen_width = self.tree.winfo_screenwidth()
            screen_height = self.tree.winfo_screenheight()
            
            if x + tooltip_width > screen_width:
                x = screen_width - tooltip_width - 10
            if y + tooltip_height > screen_height:
                y = event.y_root - tooltip_height - 10
            
            self.tooltip.wm_geometry(f'+{x}+{y}')
            
        except Exception:
            self.hide_tooltip()
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip"""
        if self.after_id:
            self.tree.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class LiteTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Task Manager Pro")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Load preferences
        self.preferences = self.load_preferences()
        self.dark_mode = self.preferences.get("dark_mode", False)
        
        self.tasks = load_tasks()
        self.filtered_tasks = self.tasks.copy()
        self.sort_by = None
        self.sort_reverse = False
        
        # Setup theme
        self.setup_theme()
        self.create_widgets()
        self.setup_keyboard_shortcuts()
        self.populate_tasks()
        self.update_status_bar()

    def load_preferences(self):
        """Load user preferences from config file"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {"dark_mode": False}
    
    def save_preferences(self):
        """Save user preferences to config file"""
        try:
            with open("config.json", "w") as f:
                json.dump(self.preferences, f)
        except:
            pass

    def setup_theme(self):
        """Configure theme colors based on dark mode setting"""
        if self.dark_mode:
            self.colors = {
                'bg': '#1a1a2e',
                'bg_secondary': '#16213e',
                'fg': '#eaeaea',
                'fg_secondary': '#a0a0a0',
                'button_bg': '#0f3460',
                'button_fg': '#ffffff',
                'button_hover': '#1a4a7a',
                'entry_bg': '#16213e',
                'entry_fg': '#ffffff',
                'entry_border': '#0f3460',
                'accent1': '#00d9a5',  # Teal green
                'accent2': '#00adb5',  # Cyan
                'accent3': '#ffc947',  # Warm yellow
                'accent_red': '#ff6b6b',
                'overdue': '#4a1a1a',
                'done': '#1a4a2a',
                'card_bg': '#16213e',
                'border': '#2a2a4e'
            }
        else:
            self.colors = {
                'bg': '#f8fafc',
                'bg_secondary': '#ffffff',
                'fg': '#1e293b',
                'fg_secondary': '#64748b',
                'button_bg': '#ffffff',
                'button_fg': '#334155',
                'button_hover': '#f1f5f9',
                'entry_bg': '#ffffff',
                'entry_fg': '#1e293b',
                'entry_border': '#e2e8f0',
                'accent1': '#10b981',  # Emerald green
                'accent2': '#3b82f6',  # Blue
                'accent3': '#f59e0b',  # Amber
                'accent_red': '#ef4444',
                'overdue': '#fef2f2',
                'done': '#f0fdf4',
                'card_bg': '#ffffff',
                'border': '#e2e8f0'
            }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles for a modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Treeview styling
        self.style.configure('Treeview',
            background=self.colors['card_bg'],
            foreground=self.colors['fg'],
            fieldbackground=self.colors['card_bg'],
            rowheight=36,
            font=('Segoe UI', 10))
        
        self.style.configure('Treeview.Heading',
            background=self.colors['bg_secondary'],
            foreground=self.colors['fg'],
            font=('Segoe UI Semibold', 10),
            padding=(10, 8))
        
        self.style.map('Treeview',
            background=[('selected', self.colors['accent2'])],
            foreground=[('selected', '#ffffff')])
        
        self.style.map('Treeview.Heading',
            background=[('active', self.colors['button_hover'])])
        
        # Scrollbar styling
        self.style.configure('Vertical.TScrollbar',
            background=self.colors['bg_secondary'],
            troughcolor=self.colors['bg'],
            arrowcolor=self.colors['fg_secondary'])

    def create_modern_button(self, parent, text, command, bg_color, fg_color="white", icon=None):
        """Create a modern button with hover effects"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg=fg_color,
                       font=('Segoe UI', 10, 'bold'),
                       padx=16, pady=8, relief=tk.FLAT,
                       cursor="hand2", bd=0,
                       activebackground=bg_color, activeforeground=fg_color)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self._lighten_color(bg_color))
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_widgets(self):
        # Header Section with app branding
        header = tk.Frame(self.root, bg=self.colors['accent2'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors['accent2'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(header_content, text="✨ Task Manager Pro",
                bg=self.colors['accent2'], fg='white',
                font=('Segoe UI', 18, 'bold')).pack(side=tk.LEFT, pady=12)
        
        # Theme toggle in header
        theme_btn = tk.Button(header_content, 
                             text="🌙 Dark" if not self.dark_mode else "☀️ Light",
                             command=self.toggle_theme,
                             bg=self.colors['accent2'], fg='white',
                             font=('Segoe UI', 10),
                             bd=0, relief=tk.FLAT, cursor="hand2",
                             activebackground=self.colors['accent2'],
                             activeforeground='white')
        theme_btn.pack(side=tk.RIGHT, pady=15)
        
        # Top Frame: Toolbar
        toolbar = tk.Frame(self.root, bg=self.colors['bg'], pady=12)
        toolbar.pack(fill=tk.X, padx=20)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        btn_frame.pack(side=tk.LEFT)
        
        add_btn = self.create_modern_button(btn_frame, "➕  Add Task", 
                                           self.add_task_popup, self.colors['accent1'])
        add_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        report_btn = self.create_modern_button(btn_frame, "📊  Report",
                                              self.generate_report_popup, self.colors['accent2'])
        report_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        refresh_btn = self.create_modern_button(btn_frame, "🔄  Refresh",
                                               self.refresh_tasks, self.colors['button_bg'],
                                               self.colors['button_fg'])
        refresh_btn.pack(side=tk.LEFT)
        
        # Search Frame with modern styling
        search_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        search_frame.pack(side=tk.RIGHT)
        
        # Search container with border
        search_container = tk.Frame(search_frame, bg=self.colors['entry_border'], padx=1, pady=1)
        search_container.pack(side=tk.RIGHT)
        
        search_inner = tk.Frame(search_container, bg=self.colors['entry_bg'])
        search_inner.pack(fill=tk.BOTH)
        
        tk.Label(search_inner, text="🔍", bg=self.colors['entry_bg'],
                fg=self.colors['fg_secondary'], font=('Segoe UI', 11)).pack(side=tk.LEFT, padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_tasks())
        search_entry = tk.Entry(search_inner, textvariable=self.search_var,
                               width=28, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                               insertbackground=self.colors['fg'],
                               font=('Segoe UI', 10), bd=0, relief=tk.FLAT)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), pady=8)
        
        # Filter Frame with modern pill-style buttons
        filter_container = tk.Frame(self.root, bg=self.colors['bg'])
        filter_container.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        filter_inner = tk.Frame(filter_container, bg=self.colors['bg_secondary'], 
                               padx=5, pady=5)
        filter_inner.pack(side=tk.LEFT)
        
        tk.Label(filter_inner, text="Filter:", bg=self.colors['bg_secondary'],
                fg=self.colors['fg_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(5, 10))
        
        self.filter_var = tk.StringVar(value="All")
        self.filter_buttons = {}
        
        for option in ["All", "Pending", "Done", "Overdue", "High Priority"]:
            is_selected = option == "All"
            btn = tk.Button(filter_inner, text=option,
                          command=lambda o=option: self.set_filter(o),
                          bg=self.colors['accent2'] if is_selected else self.colors['bg_secondary'],
                          fg='white' if is_selected else self.colors['fg_secondary'],
                          font=('Segoe UI', 9),
                          bd=0, relief=tk.FLAT, padx=12, pady=4, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=2)
            self.filter_buttons[option] = btn
        
        # Task Table with modern styling
        table_container = tk.Frame(self.root, bg=self.colors['border'], padx=1, pady=1)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        table_frame = tk.Frame(table_container, bg=self.colors['card_bg'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("status", "priority", "title", "deadline", "tags")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns with better widths
        column_config = {
            "status": (70, "Status"),
            "priority": (100, "⚡ Priority"),
            "title": (350, "📝 Task"),
            "deadline": (120, "📅 Deadline"),
            "tags": (200, "🏷️ Tags")
        }
        
        for col, (width, heading) in column_config.items():
            self.tree.heading(col, text=heading, command=lambda c=col: self.sort_tasks(c))
            self.tree.column(col, width=width, anchor=tk.W)
        
        # Configure row colors for different states
        self.tree.tag_configure("overdue", background=self.colors['overdue'], foreground=self.colors['accent_red'])
        self.tree.tag_configure("done", background=self.colors['done'], foreground=self.colors['fg_secondary'])
        self.tree.tag_configure("high", foreground='#dc2626')
        self.tree.tag_configure("low", foreground=self.colors['fg_secondary'])
        
        # Action buttons below the task list
        action_frame = tk.Frame(self.root, bg=self.colors['bg'])
        action_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
        
        done_btn = tk.Button(action_frame, text="✅  Mark Done",
                            command=self.mark_done,
                            bg=self.colors['accent1'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            bd=0, relief=tk.FLAT, padx=16, pady=8, cursor="hand2")
        done_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        pending_btn = tk.Button(action_frame, text="↩️  Mark Pending",
                               command=self.mark_pending,
                               bg=self.colors['accent3'], fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               bd=0, relief=tk.FLAT, padx=16, pady=8, cursor="hand2")
        pending_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        edit_btn = tk.Button(action_frame, text="✏️  Edit",
                            command=self.edit_task_popup,
                            bg=self.colors['accent2'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            bd=0, relief=tk.FLAT, padx=16, pady=8, cursor="hand2")
        edit_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        delete_btn = tk.Button(action_frame, text="🗑️  Delete",
                              command=self.delete_task,
                              bg=self.colors['accent_red'], fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              bd=0, relief=tk.FLAT, padx=16, pady=8, cursor="hand2")
        delete_btn.pack(side=tk.LEFT)
        
        # Bindings
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click on Windows
        self.tree.bind("<Double-1>", lambda e: self.edit_task_popup())
        self.tree.bind("<Return>", lambda e: self.mark_done())
        self.tree.bind("<Delete>", lambda e: self.delete_task())
        
        # Add tooltip for showing full text on hover
        self.tree_tooltip = TreeviewTooltip(self.tree, delay=400)
        
        # Modern right-click context menu
        self.menu = tk.Menu(self.root, tearoff=0, 
                           bg=self.colors['bg_secondary'], fg=self.colors['fg'],
                           activebackground=self.colors['accent2'], activeforeground='white',
                           font=('Segoe UI', 10), bd=0, relief=tk.FLAT)
        self.menu.add_command(label="  ✅  Mark as Done  ", command=self.mark_done)
        self.menu.add_command(label="  ↩️  Mark as Pending  ", command=self.mark_pending)
        self.menu.add_command(label="  ✏️  Edit Task  ", command=self.edit_task_popup)
        self.menu.add_command(label="  🗑️  Delete Task  ", command=self.delete_task)
        self.menu.add_separator()
        self.menu.add_command(label="  📋  Copy Title  ", command=self.copy_task_title)
        
        # Modern Status Bar
        status_container = tk.Frame(self.root, bg=self.colors['border'], height=1)
        status_container.pack(fill=tk.X)
        
        self.status_bar = tk.Label(self.root, text="Ready", bd=0,
                                   anchor=tk.W, bg=self.colors['bg_secondary'],
                                   fg=self.colors['fg_secondary'], 
                                   font=('Segoe UI', 9),
                                   padx=20, pady=8)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_filter(self, option):
        """Set filter and update button styles"""
        self.filter_var.set(option)
        for opt, btn in self.filter_buttons.items():
            if opt == option:
                btn.configure(bg=self.colors['accent2'], fg='white')
            else:
                btn.configure(bg=self.colors['bg_secondary'], fg=self.colors['fg_secondary'])
        self.filter_tasks()

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        self.root.bind('<Control-n>', lambda e: self.add_task_popup())
        self.root.bind('<Control-N>', lambda e: self.add_task_popup())
        self.root.bind('<Control-r>', lambda e: self.generate_report_popup())
        self.root.bind('<Control-R>', lambda e: self.generate_report_popup())
        self.root.bind('<Control-f>', lambda e: self.search_var.get() or self.focus_search())
        self.root.bind('<Control-F>', lambda e: self.search_var.get() or self.focus_search())
        self.root.bind('<F5>', lambda e: self.refresh_tasks())
    
    def focus_search(self):
        """Focus on search entry"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for entry in child.winfo_children():
                            if isinstance(entry, tk.Entry) and entry.cget('textvariable') == str(self.search_var):
                                entry.focus_set()
                                return

    def filter_tasks(self):
        """Filter tasks based on search and filter criteria"""
        search_text = self.search_var.get().lower()
        filter_option = self.filter_var.get()
        
        self.filtered_tasks = []
        for task in self.tasks:
            # Apply search filter
            if search_text:
                if not (search_text in task.title.lower() or
                       search_text in ' '.join(task.tags).lower() or
                       search_text in task.priority.lower()):
                    continue
            
            # Apply status filter
            if filter_option == "Pending" and task.status != "Pending":
                continue
            elif filter_option == "Done" and task.status != "Done":
                continue
            elif filter_option == "Overdue" and not task.is_overdue():
                continue
            elif filter_option == "High Priority" and task.priority != "High":
                continue
            
            self.filtered_tasks.append(task)
        
        self.populate_tasks()
        self.update_status_bar()

    def refresh_tasks(self):
        """Reload tasks from file"""
        self.tasks = load_tasks()
        self.filter_tasks()
        messagebox.showinfo("Refreshed", "Tasks reloaded from file")

    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.preferences["dark_mode"] = self.dark_mode
        self.save_preferences()
        
        # Restart app for theme change
        messagebox.showinfo("Theme Changed", "Please restart the app to apply the new theme")

    def update_status_bar(self):
        """Update status bar with task statistics"""
        total = len(self.tasks)
        pending = sum(1 for t in self.tasks if t.status == "Pending")
        done = sum(1 for t in self.tasks if t.status == "Done")
        overdue = sum(1 for t in self.tasks if t.is_overdue())
        
        filtered_count = len(self.filtered_tasks)
        status_text = f"📋 Total: {total}   •   ⏳ Pending: {pending}   •   ✅ Done: {done}   •   ⚠️ Overdue: {overdue}"
        
        if filtered_count < total:
            status_text += f"   •   🔍 Showing: {filtered_count}"
        
        self.status_bar.config(text=status_text)

    def sort_tasks(self, column):
        """Sort tasks by the selected column"""
        if self.sort_by == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_by = column
            self.sort_reverse = False
        
        if column == "priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            self.tasks.sort(key=lambda t: priority_order.get(t.priority, 3), reverse=self.sort_reverse)
        elif column == "deadline":
            self.tasks.sort(key=lambda t: (t.deadline is None, t.deadline or ""), reverse=self.sort_reverse)
        elif column == "status":
            self.tasks.sort(key=lambda t: t.status, reverse=self.sort_reverse)
        elif column == "title":
            self.tasks.sort(key=lambda t: t.title.lower(), reverse=self.sort_reverse)
        elif column == "tags":
            self.tasks.sort(key=lambda t: ', '.join(t.tags).lower(), reverse=self.sort_reverse)
        
        save_tasks(self.tasks)
        self.filter_tasks()

    def populate_tasks(self):
        """Populate the task table"""
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for idx, task in enumerate(self.filtered_tasks):
            # Find original index in self.tasks
            original_idx = self.tasks.index(task)
            
            tags_str = ", ".join(task.tags) if task.tags else "—"
            
            # Format priority with icons
            priority_icons = {"High": "🔴 High", "Medium": "🟡 Medium", "Low": "🟢 Low"}
            priority_display = priority_icons.get(task.priority, task.priority)
            
            # Format deadline
            deadline_display = task.deadline if task.deadline else "—"
            
            values = (
                "✅" if task.status == "Done" else "⬜",
                priority_display,
                task.title,
                deadline_display,
                tags_str
            )
            
            item_tags = []
            if task.is_overdue():
                item_tags.append("overdue")
            elif task.status == "Done":
                item_tags.append("done")
            elif task.priority == "High":
                item_tags.append("high")
            elif task.priority == "Low":
                item_tags.append("low")
            
            self.tree.insert("", tk.END, iid=original_idx, values=values, tags=item_tags)

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.menu.post(event.x_root, event.y_root)

    def copy_task_title(self):
        """Copy selected task title to clipboard"""
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(self.tasks[idx].title)
        messagebox.showinfo("Copied", "Task title copied to clipboard!")

    def add_task_popup(self):
        """Show add task dialog"""
        popup = TaskPopup(self.root, "Add Task", dark_mode=self.dark_mode)
        self.root.wait_window(popup.top)
        if popup.task:
            add_task(self.tasks, popup.task)
            self.filter_tasks()

    def edit_task_popup(self):
        """Show edit task dialog"""
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        task = self.tasks[idx]
        popup = TaskPopup(self.root, "Edit Task", task, dark_mode=self.dark_mode)
        self.root.wait_window(popup.top)
        if popup.task:
            edit_task(self.tasks, idx, popup.task)
            self.filter_tasks()

    def delete_task(self):
        """Delete selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return
        try:
            idx = int(selected[0])
            if 0 <= idx < len(self.tasks):
                if messagebox.askyesno("Confirm Delete", f"Delete task: {self.tasks[idx].title}?"):
                    delete_task(self.tasks, idx)
                    self.filter_tasks()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Could not delete task: {e}")

    def mark_done(self):
        """Mark selected task as done"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return
        try:
            idx = int(selected[0])
            if 0 <= idx < len(self.tasks):
                mark_task_done(self.tasks, idx)
                self.filter_tasks()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Could not update task: {e}")
    
    def mark_pending(self):
        """Mark selected task as pending"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return
        try:
            idx = int(selected[0])
            if 0 <= idx < len(self.tasks):
                self.tasks[idx].status = "Pending"
                self.tasks[idx].completion_date = None
                save_tasks(self.tasks)
                self.filter_tasks()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Could not update task: {e}")

    def generate_report_popup(self):
        """Show report generation dialog"""
        popup = ReportPopup(self.root, self.tasks, dark_mode=self.dark_mode)


class TaskPopup:
    def __init__(self, master, title, task=None, dark_mode=False):
        self.task = None
        self.dark_mode = dark_mode
        self.top = tk.Toplevel(master)
        self.top.withdraw()  # Hide window during setup to prevent flickering
        self.top.title(title)
        
        # Modern theme colors based on mode
        if dark_mode:
            self.colors = {
                'bg': '#1a1a2e',
                'bg_secondary': '#16213e',
                'fg': '#eaeaea',
                'fg_secondary': '#a0a0a0',
                'entry_bg': '#16213e',
                'entry_fg': '#ffffff',
                'border': '#0f3460',
                'accent': '#3b82f6',
                'success': '#10b981',
                'danger': '#ef4444'
            }
        else:
            self.colors = {
                'bg': '#f8fafc',
                'bg_secondary': '#ffffff',
                'fg': '#1e293b',
                'fg_secondary': '#64748b',
                'entry_bg': '#ffffff',
                'entry_fg': '#1e293b',
                'border': '#e2e8f0',
                'accent': '#3b82f6',
                'success': '#10b981',
                'danger': '#ef4444'
            }
        
        # Configure popup window
        self.top.configure(bg=self.colors['bg'])
        self.top.geometry("520x520")
        self.top.resizable(False, False)
        
        # Modern header
        header = tk.Frame(self.top, bg=self.colors['accent'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_icon = "📝" if "Add" in title else "✏️"
        tk.Label(header, text=f"{header_icon}  {title}",
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 16, 'bold')).pack(expand=True)
        
        # Main content area
        main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=30, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Task Title Section
        self._create_input_section(main_container, "📌 Task Title *", "title")
        if task:
            self.entry_title.insert(0, task.title)
        
        # Deadline Section with Date Picker
        deadline_frame = tk.Frame(main_container, bg=self.colors['bg'])
        deadline_frame.pack(fill=tk.X, pady=(0, 18))
        
        tk.Label(deadline_frame, text="📅 Deadline",
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        date_container = tk.Frame(deadline_frame, bg=self.colors['bg'])
        date_container.pack(fill=tk.X)
        
        if HAS_CALENDAR:
            # Checkbox to enable/disable deadline
            self.has_deadline = tk.BooleanVar(value=bool(task and task.deadline))
            
            deadline_check = tk.Checkbutton(date_container, text="Set deadline",
                                           variable=self.has_deadline,
                                           command=self._toggle_deadline,
                                           bg=self.colors['bg'], fg=self.colors['fg'],
                                           font=('Segoe UI', 10),
                                           selectcolor=self.colors['bg_secondary'],
                                           activebackground=self.colors['bg'],
                                           cursor="hand2")
            deadline_check.pack(side=tk.LEFT, padx=(0, 10))
            
            # Use tkcalendar DateEntry
            self.date_picker = DateEntry(date_container, 
                                        width=15,
                                        background=self.colors['accent'],
                                        foreground='white',
                                        borderwidth=0,
                                        font=('Segoe UI', 11),
                                        date_pattern='yyyy-mm-dd',
                                        state='normal' if self.has_deadline.get() else 'disabled')
            self.date_picker.pack(side=tk.LEFT)
            
            if task and task.deadline:
                try:
                    d = datetime.strptime(task.deadline, "%Y-%m-%d").date()
                    self.date_picker.set_date(d)
                except:
                    pass
        else:
            # Fallback to text entry
            entry_border = tk.Frame(date_container, bg=self.colors['border'], padx=1, pady=1)
            entry_border.pack(fill=tk.X)
            self.entry_deadline = tk.Entry(entry_border, font=('Segoe UI', 12),
                                          bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                                          insertbackground=self.colors['accent'],
                                          relief=tk.FLAT, bd=0)
            self.entry_deadline.pack(fill=tk.X, ipady=10, padx=10)
            if task and task.deadline:
                self.entry_deadline.insert(0, task.deadline)
        
        # Priority Section
        priority_frame = tk.Frame(main_container, bg=self.colors['bg'])
        priority_frame.pack(fill=tk.X, pady=(0, 18))
        
        tk.Label(priority_frame, text="⚡ Priority",
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        self.priority_var = tk.StringVar(value=task.priority if task else "Medium")
        priority_btn_frame = tk.Frame(priority_frame, bg=self.colors['bg'])
        priority_btn_frame.pack(fill=tk.X)
        
        self.priority_buttons = {}
        priority_configs = [
            ("High", "🔴", "#ef4444"),
            ("Medium", "🟡", "#f59e0b"),
            ("Low", "🟢", "#10b981")
        ]
        
        for p_val, p_icon, p_color in priority_configs:
            is_selected = (self.priority_var.get() == p_val)
            btn = tk.Button(priority_btn_frame,
                          text=f"{p_icon}  {p_val}",
                          command=lambda v=p_val: self._set_priority(v),
                          bg=p_color if is_selected else self.colors['bg_secondary'],
                          fg='white' if is_selected else self.colors['fg'],
                          font=('Segoe UI', 10),
                          bd=0, relief=tk.FLAT, padx=16, pady=6, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=(0, 8))
            self.priority_buttons[p_val] = (btn, p_color)
        
        # Tags Section
        self._create_input_section(main_container, "🏷️ Tags (comma separated)", "tags")
        if task and task.tags:
            self.entry_tags.insert(0, ", ".join(task.tags))
        
        # Action Buttons - well separated
        btn_container = tk.Frame(main_container, bg=self.colors['bg'])
        btn_container.pack(fill=tk.X, pady=(25, 0))
        
        # Save button on the left
        save_btn = tk.Button(btn_container, text="✓  Save Task", command=self.save,
                            font=('Segoe UI', 11, 'bold'),
                            bg=self.colors['success'], fg='white',
                            activebackground='#059669', activeforeground='white',
                            cursor="hand2", relief=tk.FLAT, bd=0,
                            padx=30, pady=12)
        save_btn.pack(side=tk.LEFT)
        
        # Cancel button on the right
        cancel_btn = tk.Button(btn_container, text="✕  Cancel", command=self.top.destroy,
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['danger'], fg='white',
                              activebackground='#dc2626', activeforeground='white',
                              cursor="hand2", relief=tk.FLAT, bd=0,
                              padx=30, pady=12)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Center window
        self.top.transient(master)
        self.top.grab_set()
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        
        # Show window after positioning (prevents flickering)
        self.top.deiconify()
        
        self.top.after(100, lambda: self.entry_title.focus() if self.top.winfo_exists() else None)
        self.top.bind('<Return>', lambda e: self.save())
        self.top.bind('<Escape>', lambda e: self.top.destroy())
    
    def _toggle_deadline(self):
        """Enable/disable the date picker based on checkbox"""
        if HAS_CALENDAR:
            if self.has_deadline.get():
                self.date_picker.config(state='normal')
            else:
                self.date_picker.config(state='disabled')
    
    def _create_input_section(self, parent, label_text, field_name):
        """Create a modern input section with label and entry"""
        frame = tk.Frame(parent, bg=self.colors['bg'])
        frame.pack(fill=tk.X, pady=(0, 18))
        
        tk.Label(frame, text=label_text,
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        entry_border = tk.Frame(frame, bg=self.colors['border'], padx=1, pady=1)
        entry_border.pack(fill=tk.X)
        
        entry = tk.Entry(entry_border, font=('Segoe UI', 12),
                        bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                        insertbackground=self.colors['accent'],
                        relief=tk.FLAT, bd=0)
        entry.pack(fill=tk.X, ipady=10, padx=10)
        
        setattr(self, f'entry_{field_name}', entry)
    
    def _set_priority(self, value):
        """Update priority selection with visual feedback"""
        self.priority_var.set(value)
        for p_val, (btn, color) in self.priority_buttons.items():
            if p_val == value:
                btn.configure(bg=color, fg='white')
            else:
                btn.configure(bg=self.colors['bg_secondary'], fg=self.colors['fg'])

    def save(self):
        title = self.entry_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title is required.")
            return
        
        # Get deadline
        deadline = None
        if HAS_CALENDAR:
            if hasattr(self, 'has_deadline') and not self.has_deadline.get():
                deadline = None
            else:
                try:
                    deadline = self.date_picker.get_date().strftime("%Y-%m-%d")
                except:
                    deadline = None
        else:
            deadline_str = self.entry_deadline.get().strip()
            if deadline_str:
                try:
                    datetime.strptime(deadline_str, "%Y-%m-%d")
                    deadline = deadline_str
                except ValueError:
                    messagebox.showerror("Error", "Invalid deadline format. Use YYYY-MM-DD")
                    return
        
        priority = self.priority_var.get()
        tags = [t.strip() for t in self.entry_tags.get().split(",") if t.strip()]
        self.task = Task(title=title, deadline=deadline, priority=priority, tags=tags)
        self.top.destroy()


class ReportPopup:
    def __init__(self, master, tasks, dark_mode=False):
        self.tasks = tasks
        self.top = tk.Toplevel(master)
        self.top.withdraw()  # Hide window during setup to prevent flickering
        self.top.title("Standup Report")
        self.top.geometry("650x650")
        
        # Modern theme colors
        if dark_mode:
            self.colors = {
                'bg': '#1a1a2e',
                'bg_secondary': '#16213e',
                'fg': '#eaeaea',
                'fg_secondary': '#a0a0a0',
                'entry_bg': '#16213e',
                'entry_fg': '#ffffff',
                'border': '#0f3460',
                'accent': '#00adb5',
                'success': '#10b981',
                'warning': '#f59e0b'
            }
        else:
            self.colors = {
                'bg': '#f8fafc',
                'bg_secondary': '#ffffff',
                'fg': '#1e293b',
                'fg_secondary': '#64748b',
                'entry_bg': '#ffffff',
                'entry_fg': '#1e293b',
                'border': '#e2e8f0',
                'accent': '#3b82f6',
                'success': '#10b981',
                'warning': '#f59e0b'
            }
        
        self.top.configure(bg=self.colors['bg'])
        self.top.transient(master)
        self.top.grab_set()
        
        # Modern header
        header = tk.Frame(self.top, bg=self.colors['accent'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="\ud83d\udcca  Standup Report Generator",
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 16, 'bold')).pack(expand=True)
        
        # Main content
        main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Date Range Section
        date_section = tk.Frame(main_container, bg=self.colors['bg_secondary'], padx=15, pady=15)
        date_section.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(date_section, text="\ud83d\udcc5 Date Range (optional)",
                bg=self.colors['bg_secondary'], fg=self.colors['fg'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        date_inputs = tk.Frame(date_section, bg=self.colors['bg_secondary'])
        date_inputs.pack(fill=tk.X)
        
        # Start date
        tk.Label(date_inputs, text="From:", bg=self.colors['bg_secondary'],
                fg=self.colors['fg_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        if HAS_CALENDAR:
            self.start_date_picker = DateEntry(date_inputs, 
                                              width=12,
                                              background=self.colors['accent'],
                                              foreground='white',
                                              borderwidth=0,
                                              font=('Segoe UI', 10),
                                              date_pattern='yyyy-mm-dd')
            self.start_date_picker.pack(side=tk.LEFT, padx=(5, 15))
            self.start_date_picker.delete(0, tk.END)  # Clear default date
            
            tk.Label(date_inputs, text="To:", bg=self.colors['bg_secondary'],
                    fg=self.colors['fg_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
            
            self.end_date_picker = DateEntry(date_inputs, 
                                            width=12,
                                            background=self.colors['accent'],
                                            foreground='white',
                                            borderwidth=0,
                                            font=('Segoe UI', 10),
                                            date_pattern='yyyy-mm-dd')
            self.end_date_picker.pack(side=tk.LEFT, padx=(5, 15))
            self.end_date_picker.delete(0, tk.END)  # Clear default date
        else:
            start_border = tk.Frame(date_inputs, bg=self.colors['border'], padx=1, pady=1)
            start_border.pack(side=tk.LEFT, padx=(5, 15))
            self.start_date_entry = tk.Entry(start_border, width=12,
                                            bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                                            insertbackground=self.colors['accent'],
                                            font=('Segoe UI', 10), bd=0, relief=tk.FLAT)
            self.start_date_entry.pack(ipady=6, padx=8)
            
            tk.Label(date_inputs, text="To:", bg=self.colors['bg_secondary'],
                    fg=self.colors['fg_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
            
            end_border = tk.Frame(date_inputs, bg=self.colors['border'], padx=1, pady=1)
            end_border.pack(side=tk.LEFT, padx=(5, 15))
            self.end_date_entry = tk.Entry(end_border, width=12,
                                          bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                                          insertbackground=self.colors['accent'],
                                          font=('Segoe UI', 10), bd=0, relief=tk.FLAT)
            self.end_date_entry.pack(ipady=6, padx=8)
        
        # Generate button
        gen_btn = tk.Button(date_inputs, text="\u21bb  Generate",
                           command=self.generate_report,
                           bg=self.colors['accent'], fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           cursor="hand2", relief=tk.FLAT, bd=0,
                           padx=16, pady=6)
        gen_btn.pack(side=tk.LEFT, padx=5)
        
        # Report display area with modern styling
        report_container = tk.Frame(main_container, bg=self.colors['border'], padx=1, pady=1)
        report_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        report_inner = tk.Frame(report_container, bg=self.colors['bg_secondary'])
        report_inner.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(report_inner)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(report_inner,
                                bg=self.colors['bg_secondary'], fg=self.colors['fg'],
                                insertbackground=self.colors['fg'],
                                font=('Consolas', 10),
                                yscrollcommand=scrollbar.set, wrap=tk.WORD,
                                padx=15, pady=15, bd=0, relief=tk.FLAT)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)
        
        # Action buttons
        button_frame = tk.Frame(main_container, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X)
        
        copy_btn = tk.Button(button_frame, text="\ud83d\udccb  Copy to Clipboard",
                            command=self.copy_to_clipboard,
                            bg=self.colors['success'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            cursor="hand2", relief=tk.FLAT, bd=0,
                            padx=20, pady=10)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(button_frame, text="\ud83d\udcbe  Export to File",
                              command=self.export_to_file,
                              bg=self.colors['warning'], fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              cursor="hand2", relief=tk.FLAT, bd=0,
                              padx=20, pady=10)
        export_btn.pack(side=tk.LEFT)
        
        # Center window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        
        # Show window after positioning (prevents flickering)
        self.top.deiconify()
        
        self.generate_report()

    def generate_report(self):
        start_date = None
        end_date = None
        start_date_str = ""
        end_date_str = ""
        
        if HAS_CALENDAR:
            try:
                start_str = self.start_date_picker.get()
                if start_str:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                    start_date_str = start_str
            except:
                pass
            try:
                end_str = self.end_date_picker.get()
                if end_str:
                    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                    end_date_str = end_str
            except:
                pass
        else:
            start_date_str = self.start_date_entry.get().strip()
            end_date_str = self.end_date_entry.get().strip()
            try:
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

        done_tasks = []
        pending_tasks = []

        for task in self.tasks:
            if task.status == "Done":
                if task.completion_date:
                    try:
                        comp_date = datetime.strptime(task.completion_date, "%Y-%m-%d").date()
                        if (not start_date or comp_date >= start_date) and (not end_date or comp_date <= end_date):
                            done_tasks.append(task)
                    except ValueError:
                        pass
                elif not start_date and not end_date:
                    done_tasks.append(task)
            else:
                if not start_date and not end_date:
                    pending_tasks.append(task)
                else:
                    pending_tasks.append(task)

        self.report_text = self._format_report(done_tasks, pending_tasks, start_date_str, end_date_str)

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.report_text)
        self.text_area.config(state=tk.DISABLED)

    def _format_report(self, done_tasks, pending_tasks, start_date, end_date):
        header = "═" * 60 + "\n"
        header += "STANDUP REPORT\n"
        if start_date or end_date:
            period = f"Period: {start_date or 'Beginning'} to {end_date or 'Now'}\n"
        else:
            period = "Period: All Time\n"
        header += period + "═" * 60 + "\n\n"

        done_section = "✅ DONE:\n" + "─" * 60 + "\n"
        if done_tasks:
            for i, task in enumerate(done_tasks, 1):
                done_section += f"{i}. {task.title}"
                if task.completion_date:
                    done_section += f" (completed: {task.completion_date})"
                if task.tags:
                    done_section += f" [{', '.join(task.tags)}]"
                done_section += "\n"
        else:
            done_section += "No completed tasks\n"

        pending_section = "\n☐ PENDING:\n" + "─" * 60 + "\n"
        if pending_tasks:
            for i, task in enumerate(pending_tasks, 1):
                pending_section += f"{i}. {task.title}"
                if task.deadline:
                    pending_section += f" (deadline: {task.deadline})"
                if task.priority != "Medium":
                    pending_section += f" [Priority: {task.priority}]"
                if task.tags:
                    pending_section += f" [{', '.join(task.tags)}]"
                pending_section += "\n"
        else:
            pending_section += "No pending tasks\n"

        return header + done_section + pending_section

    def copy_to_clipboard(self):
        self.top.clipboard_clear()
        self.top.clipboard_append(self.report_text)
        messagebox.showinfo("Copied", "Report copied to clipboard!")

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Report"
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.report_text)
                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LiteTodoApp(root)
    root.mainloop()
