# dialogs.py - Dialog popups for Task Manager
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

try:
    from tkcalendar import DateEntry
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False

from theme import get_dialog_colors
from task_manager import Task


class TaskPopup:
    """Dialog for adding/editing tasks"""
    
    def __init__(self, master, title, task=None, dark_mode=False):
        self.task = None
        self.dark_mode = dark_mode
        self.top = tk.Toplevel(master)
        self.top.withdraw()  # Hide window during setup to prevent flickering
        self.top.title(title)
        
        # Get colors based on mode
        self.colors = get_dialog_colors(dark_mode)
        
        # Configure popup window
        self.top.configure(bg=self.colors['bg'])
        self.top.geometry("520x580")
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


class MarkDonePopup:
    """Dialog for marking task as done with optional remarks"""
    
    def __init__(self, master, task_title, dark_mode=False):
        self.confirmed = False
        self.remarks = None
        self.task_title = task_title
        
        self.top = tk.Toplevel(master)
        self.top.withdraw()
        self.top.title("Mark Task Done")
        
        # Get colors based on mode
        self.colors = get_dialog_colors(dark_mode)
        
        # Configure popup window
        self.top.configure(bg=self.colors['bg'])
        self.top.geometry("450x420")
        self.top.resizable(False, False)
        
        # Modern header
        header = tk.Frame(self.top, bg=self.colors['success'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="✅  Mark Task Done",
                bg=self.colors['success'], fg='white',
                font=('Segoe UI', 14, 'bold')).pack(expand=True)
        
        # Main content area
        main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Task title display
        tk.Label(main_container, text="Task:",
                bg=self.colors['bg'], fg=self.colors['fg_secondary'],
                font=('Segoe UI', 10)).pack(anchor='w')
        
        tk.Label(main_container, text=task_title,
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 12, 'bold'), wraplength=380).pack(anchor='w', pady=(2, 15))
        
        # Remarks Section
        tk.Label(main_container, text="📝 Remarks (optional)",
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        remarks_border = tk.Frame(main_container, bg=self.colors['border'], padx=1, pady=1)
        remarks_border.pack(fill=tk.X)
        
        self.remarks_text = tk.Text(remarks_border, font=('Segoe UI', 11),
                                    bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                                    insertbackground=self.colors['fg'],
                                    relief=tk.FLAT, height=4, wrap=tk.WORD)
        self.remarks_text.pack(fill=tk.X, padx=8, pady=8)
        
        # Action Buttons - separate frame at bottom
        btn_container = tk.Frame(self.top, bg=self.colors['bg'], padx=25, pady=20)
        btn_container.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Confirm button
        confirm_btn = tk.Button(btn_container, text="✓  Mark Done", command=self.confirm,
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.colors['success'], fg='white',
                               bd=0, relief=tk.FLAT, padx=25, pady=12, cursor="hand2")
        confirm_btn.pack(side=tk.LEFT)
        
        # Cancel button
        cancel_btn = tk.Button(btn_container, text="Cancel", command=self.cancel,
                              font=('Segoe UI', 11),
                              bg=self.colors['bg_secondary'], fg=self.colors['fg'],
                              bd=1, relief=tk.SOLID, padx=25, pady=12, cursor="hand2")
        cancel_btn.pack(side=tk.RIGHT)
        
        # Center the popup
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f"{width}x{height}+{x}+{y}")
        
        self.top.transient(master)
        self.top.grab_set()
        self.top.deiconify()
        self.remarks_text.focus_set()
    
    def confirm(self):
        self.confirmed = True
        remarks = self.remarks_text.get("1.0", tk.END).strip()
        self.remarks = remarks if remarks else None
        self.top.destroy()
    
    def cancel(self):
        self.confirmed = False
        self.top.destroy()


class ReportPopup:
    """Dialog for generating standup reports"""
    
    def __init__(self, master, tasks, dark_mode=False):
        self.tasks = tasks
        self.top = tk.Toplevel(master)
        self.top.withdraw()  # Hide window during setup to prevent flickering
        self.top.title("Standup Report")
        self.top.geometry("650x650")
        
        # Get colors based on mode
        self.colors = get_dialog_colors(dark_mode)
        
        self.top.configure(bg=self.colors['bg'])
        self.top.transient(master)
        self.top.grab_set()
        
        # Modern header
        header = tk.Frame(self.top, bg=self.colors['accent'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📊  Standup Report Generator",
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 16, 'bold')).pack(expand=True)
        
        # Main content
        main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Date Range Section
        date_section = tk.Frame(main_container, bg=self.colors['bg_secondary'], padx=15, pady=15)
        date_section.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(date_section, text="📅 Date Range (optional)",
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
        gen_btn = tk.Button(date_inputs, text="↻  Generate",
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
        
        copy_btn = tk.Button(button_frame, text="📋  Copy to Clipboard",
                            command=self.copy_to_clipboard,
                            bg=self.colors['success'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            cursor="hand2", relief=tk.FLAT, bd=0,
                            padx=20, pady=10)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(button_frame, text="💾  Export to File",
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
        in_progress_tasks = []
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
            elif task.status == "In Progress":
                in_progress_tasks.append(task)
            else:
                if not start_date and not end_date:
                    pending_tasks.append(task)
                else:
                    pending_tasks.append(task)

        self.report_text = self._format_report(done_tasks, in_progress_tasks, pending_tasks, start_date_str, end_date_str)

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.report_text)
        self.text_area.config(state=tk.DISABLED)

    def _format_report(self, done_tasks, in_progress_tasks, pending_tasks, start_date, end_date):
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
                if task.remarks:
                    done_section += f"   └─ Remarks: {task.remarks}\n"
        else:
            done_section += "No completed tasks\n"

        in_progress_section = "\n🔄 IN PROGRESS:\n" + "─" * 60 + "\n"
        if in_progress_tasks:
            for i, task in enumerate(in_progress_tasks, 1):
                in_progress_section += f"{i}. {task.title}"
                if task.deadline:
                    in_progress_section += f" (deadline: {task.deadline})"
                if task.priority != "Medium":
                    in_progress_section += f" [Priority: {task.priority}]"
                if task.tags:
                    in_progress_section += f" [{', '.join(task.tags)}]"
                in_progress_section += "\n"
        else:
            in_progress_section += "No tasks in progress\n"

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

        return header + done_section + in_progress_section + pending_section

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
