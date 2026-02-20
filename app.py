# app.py - Main application class
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

from theme import get_colors, configure_treeview_style, configure_scrollbar_style
from widgets import TreeviewTooltip, create_modern_button
from dialogs import TaskPopup, ReportPopup
from task_manager import load_tasks, save_tasks, add_task, delete_task, mark_task_done, edit_task


class LiteTodoApp:
    """Main Task Manager application"""
    
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
        self.colors = get_colors(self.dark_mode)
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        self.style = ttk.Style()
        configure_treeview_style(self.style, self.colors)
        configure_scrollbar_style(self.style, self.colors)

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
        
        add_btn = create_modern_button(btn_frame, "➕  Add Task", 
                                       self.add_task_popup, self.colors['accent1'])
        add_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        report_btn = create_modern_button(btn_frame, "📊  Report",
                                          self.generate_report_popup, self.colors['accent2'])
        report_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        refresh_btn = create_modern_button(btn_frame, "🔄  Refresh",
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
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
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
