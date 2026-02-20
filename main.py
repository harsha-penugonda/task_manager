# main_optimized.py - Enhanced Lite Todo App
import os
# Suppress Tk deprecation warning on macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
from task_manager import Task, load_tasks, save_tasks, add_task, delete_task, mark_task_done, edit_task

class LiteTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lite Todo App")
        self.root.geometry("900x650")
        
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
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'entry_bg': '#3c3c3c',
                'entry_fg': '#ffffff',
                'accent1': '#4CAF50',
                'accent2': '#2196F3',
                'accent3': '#FF9800',
                'overdue': '#8b0000'
            }
        else:
            self.colors = {
                'bg': '#f5f5f5',
                'fg': '#000000',
                'button_bg': '#ffffff',
                'button_fg': '#000000',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'accent1': '#4CAF50',
                'accent2': '#2196F3',
                'accent3': '#FF9800',
                'overdue': '#ffcccb'
            }
        
        self.root.configure(bg=self.colors['bg'])

    def create_widgets(self):
        # Top Frame: Toolbar
        toolbar = tk.Frame(self.root, bg=self.colors['bg'], pady=5)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        btn_frame.pack(side=tk.LEFT)
        
        tk.Button(btn_frame, text="➕ Add Task", command=self.add_task_popup,
                  bg=self.colors['accent1'], fg="white", padx=10, pady=5, relief=tk.FLAT,
                  cursor="hand2").pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="📊 Report", command=self.generate_report_popup,
                  bg=self.colors['accent2'], fg="white", padx=10, pady=5, relief=tk.FLAT,
                  cursor="hand2").pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_tasks,
                  bg=self.colors['button_bg'], fg=self.colors['button_fg'], padx=10, pady=5,
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="🌙" if not self.dark_mode else "☀️", command=self.toggle_theme,
                  bg=self.colors['button_bg'], fg=self.colors['button_fg'], padx=10, pady=5,
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        # Search Frame
        search_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="🔍 Search:", bg=self.colors['bg'],
                 fg=self.colors['fg']).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_tasks())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               width=25, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                               insertbackground=self.colors['fg'])
        search_entry.pack(side=tk.LEFT)
        
        # Filter Frame
        filter_frame = tk.Frame(self.root, bg=self.colors['bg'])
        filter_frame.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(filter_frame, text="Filter:", bg=self.colors['bg'],
                 fg=self.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="All")
        for option in ["All", "Pending", "Done", "Overdue", "High Priority"]:
            tk.Radiobutton(filter_frame, text=option, variable=self.filter_var,
                          value=option, command=self.filter_tasks,
                          bg=self.colors['bg'], fg=self.colors['fg'],
                          selectcolor=self.colors['button_bg'],
                          activebackground=self.colors['bg']).pack(side=tk.LEFT, padx=5)
        
        # Task Table with Scrollbar
        table_frame = tk.Frame(self.root, bg=self.colors['bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("status", "priority", "title", "deadline", "tags")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        column_config = {
            "status": (60, "Status"),
            "priority": (80, "Priority"),
            "title": (300, "Title"),
            "deadline": (100, "Deadline"),
            "tags": (180, "Tags")
        }
        
        for col, (width, heading) in column_config.items():
            self.tree.heading(col, text=heading, command=lambda c=col: self.sort_tasks(c))
            self.tree.column(col, width=width, anchor=tk.W)
        
        # Configure row colors
        self.tree.tag_configure("overdue", background=self.colors['overdue'])
        self.tree.tag_configure("done", foreground="#888888")
        
        # Bindings
        self.tree.bind("<Button-2>" if tk.TkVersion >= 8.6 else "<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", lambda e: self.edit_task_popup())
        self.tree.bind("<Return>", lambda e: self.mark_done())
        self.tree.bind("<Delete>", lambda e: self.delete_task())
        
        # Right-click menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="✅ Mark Done", command=self.mark_done)
        self.menu.add_command(label="✏️ Edit Task", command=self.edit_task_popup)
        self.menu.add_command(label="🗑️ Delete Task", command=self.delete_task)
        self.menu.add_separator()
        self.menu.add_command(label="📋 Copy Title", command=self.copy_task_title)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, bg=self.colors['button_bg'],
                                   fg=self.colors['button_fg'], padx=10, pady=3)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
        status_text = f"Total: {total} | Pending: {pending} | Done: {done} | Overdue: {overdue}"
        
        if filtered_count < total:
            status_text += f" | Showing: {filtered_count}"
        
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
            
            tags_str = ", ".join(task.tags)
            values = (
                "✅" if task.status == "Done" else "☐",
                task.priority,
                task.title,
                task.deadline or "",
                tags_str
            )
            
            item_tags = []
            if task.is_overdue():
                item_tags.append("overdue")
            if task.status == "Done":
                item_tags.append("done")
            
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
            return
        idx = int(selected[0])
        if messagebox.askyesno("Confirm Delete", f"Delete task: {self.tasks[idx].title}?"):
            delete_task(self.tasks, idx)
            self.filter_tasks()

    def mark_done(self):
        """Mark selected task as done"""
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        mark_task_done(self.tasks, idx)
        self.filter_tasks()

    def generate_report_popup(self):
        """Show report generation dialog"""
        popup = ReportPopup(self.root, self.tasks, dark_mode=self.dark_mode)


class TaskPopup:
    def __init__(self, master, title, task=None, dark_mode=False):
        self.task = None
        self.top = tk.Toplevel(master)
        self.top.title(title)
        
        # Use very explicit colors that will always be visible
        # Light theme - high contrast
        bg_color = '#f5f5f5'  # Light gray background
        fg_color = '#000000'  # Black text
        entry_bg = '#ffffff'  # Pure white entry fields
        entry_fg = '#000000'  # Black text in entries
        label_bg = '#f5f5f5'  # Match container background
        border_color = '#1976D2'  # Blue border for visibility
        
        # Configure popup window
        self.top.configure(bg=bg_color)
        self.top.geometry("550x450")
        self.top.resizable(False, False)
        
        # Title bar
        title_bar = tk.Frame(self.top, bg='#1976D2', height=50)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text=title, bg='#1976D2', fg='white',
                font=('Helvetica', 16, 'bold')).pack(expand=True)
        
        # Create main container with padding
        main_container = tk.Frame(self.top, bg=bg_color, padx=25, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Task Title Section
        title_frame = tk.Frame(main_container, bg=bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="Task Title *", bg=label_bg, fg=fg_color, 
                font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Entry with visible border
        title_entry_frame = tk.Frame(title_frame, bg=border_color, padx=2, pady=2)
        title_entry_frame.pack(fill=tk.X)
        self.entry_title = tk.Entry(title_entry_frame, font=('Helvetica', 13), 
                                    bg=entry_bg, fg=entry_fg,
                                    insertbackground='blue',
                                    relief=tk.FLAT, bd=0)
        self.entry_title.pack(fill=tk.BOTH, ipady=8, padx=1, pady=1)
        if task:
            self.entry_title.insert(0, task.title)
        
        # Deadline Section
        deadline_frame = tk.Frame(main_container, bg=bg_color)
        deadline_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(deadline_frame, text="Deadline (YYYY-MM-DD)", bg=label_bg, fg=fg_color,
                font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        deadline_entry_frame = tk.Frame(deadline_frame, bg=border_color, padx=2, pady=2)
        deadline_entry_frame.pack(fill=tk.X)
        self.entry_deadline = tk.Entry(deadline_entry_frame, font=('Helvetica', 13),
                                       bg=entry_bg, fg=entry_fg,
                                       insertbackground='blue',
                                       relief=tk.FLAT, bd=0)
        self.entry_deadline.pack(fill=tk.BOTH, ipady=8, padx=1, pady=1)
        if task and task.deadline:
            self.entry_deadline.insert(0, task.deadline)
        
        # Priority Section
        priority_frame = tk.Frame(main_container, bg=bg_color)
        priority_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(priority_frame, text="Priority", bg=label_bg, fg=fg_color,
                font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        self.priority_var = tk.StringVar(value=task.priority if task else "Medium")
        priority_buttons = tk.Frame(priority_frame, bg=bg_color)
        priority_buttons.pack(fill=tk.X)
        
        for priority_val in ["High", "Medium", "Low"]:
            rb = tk.Radiobutton(priority_buttons, text=priority_val, 
                               variable=self.priority_var, value=priority_val,
                               bg=bg_color, fg=fg_color, 
                               font=('Helvetica', 12),
                               selectcolor='white',
                               activebackground=bg_color, 
                               activeforeground=fg_color,
                               indicatoron=1)
            rb.pack(side=tk.LEFT, padx=(0, 25))
        
        # Tags Section
        tags_frame = tk.Frame(main_container, bg=bg_color)
        tags_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(tags_frame, text="Tags (comma separated)", bg=label_bg, fg=fg_color,
                font=('Helvetica', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        tags_entry_frame = tk.Frame(tags_frame, bg=border_color, padx=2, pady=2)
        tags_entry_frame.pack(fill=tk.X)
        self.entry_tags = tk.Entry(tags_entry_frame, font=('Helvetica', 13),
                                   bg=entry_bg, fg=entry_fg,
                                   insertbackground='blue',
                                   relief=tk.FLAT, bd=0)
        self.entry_tags.pack(fill=tk.BOTH, ipady=8, padx=1, pady=1)
        if task and task.tags:
            self.entry_tags.insert(0, ", ".join(task.tags))
        
        # Buttons Section
        btn_container = tk.Frame(main_container, bg=bg_color)
        btn_container.pack(pady=(10, 0))
        
        save_btn = tk.Button(btn_container, text="✓  Save Task", command=self.save, 
                            font=('Helvetica', 12, 'bold'),
                            bg="#4CAF50", fg="white", 
                            activebackground="#45a049", activeforeground="white",
                            cursor="hand2", relief=tk.RAISED, bd=3,
                            padx=25, pady=10)
        save_btn.pack(side=tk.LEFT, padx=8)
        
        cancel_btn = tk.Button(btn_container, text="✕  Cancel", command=self.top.destroy,
                              font=('Helvetica', 12, 'bold'),
                              bg="#f44336", fg="white",
                              activebackground="#da190b", activeforeground="white",
                              cursor="hand2", relief=tk.RAISED, bd=3,
                              padx=25, pady=10)
        cancel_btn.pack(side=tk.LEFT, padx=8)
        
        # Center window and focus
        self.top.transient(master)
        self.top.grab_set()
        
        # Center the window on screen
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        
        # Safe focus setting
        self.top.after(100, lambda: self.entry_title.focus() if self.top.winfo_exists() else None)
        
        # Bindings
        self.top.bind('<Return>', lambda e: self.save())
        self.top.bind('<Escape>', lambda e: self.top.destroy())

    def save(self):
        title = self.entry_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title is required.")
            return
        
        deadline = self.entry_deadline.get().strip() or None
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid deadline format. Use YYYY-MM-DD")
                return
        
        priority = self.priority_var.get()
        tags = [t.strip() for t in self.entry_tags.get().split(",")] if self.entry_tags.get() else []
        self.task = Task(title=title, deadline=deadline, priority=priority, tags=tags)
        self.top.destroy()


class ReportPopup:
    def __init__(self, master, tasks, dark_mode=False):
        self.tasks = tasks
        self.top = tk.Toplevel(master)
        self.top.title("Standup Report")
        self.top.geometry("600x600")
        
        # Theme colors
        if dark_mode:
            bg, fg, entry_bg = '#2b2b2b', '#ffffff', '#3c3c3c'
        else:
            bg, fg, entry_bg = 'white', 'black', 'white'
        
        self.top.configure(bg=bg)
        self.top.transient(master)
        self.top.grab_set()

        # Date Range Frame
        date_frame = tk.Frame(self.top, bg=bg, pady=10)
        date_frame.pack(fill=tk.X, padx=15)

        tk.Label(date_frame, text="Start Date:", bg=bg, fg=fg,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.start_date_entry = tk.Entry(date_frame, width=12, bg=entry_bg, fg=fg,
                                         insertbackground=fg, font=('Arial', 10))
        self.start_date_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(date_frame, text="End Date:", bg=bg, fg=fg,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.end_date_entry = tk.Entry(date_frame, width=12, bg=entry_bg, fg=fg,
                                       insertbackground=fg, font=('Arial', 10))
        self.end_date_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(date_frame, text="📊 Generate", command=self.generate_report,
                 bg="#2196F3", fg="white", font=('Arial', 10, 'bold'),
                 cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # Report Text Area with Scrollbar
        text_frame = tk.Frame(self.top, bg=bg)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(text_frame, bg=entry_bg, fg=fg,
                                insertbackground=fg, font=('Arial', 10),
                                yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)

        # Buttons Frame
        button_frame = tk.Frame(self.top, bg=bg, pady=10)
        button_frame.pack(fill=tk.X, padx=15)

        tk.Button(button_frame, text="📋 Copy", command=self.copy_to_clipboard,
                 bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'),
                 cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="💾 Export", command=self.export_to_file,
                 bg="#FF9800", fg="white", font=('Arial', 10, 'bold'),
                 cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        self.generate_report()

    def generate_report(self):
        start_date_str = self.start_date_entry.get().strip()
        end_date_str = self.end_date_entry.get().strip()

        start_date = None
        end_date = None

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
