# widgets.py - Custom widgets
import tkinter as tk
from utils import lighten_color


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


def create_modern_button(parent, text, command, bg_color, fg_color="white", colors=None):
    """Create a modern button with hover effects"""
    btn = tk.Button(parent, text=text, command=command,
                   bg=bg_color, fg=fg_color,
                   font=('Segoe UI', 10, 'bold'),
                   padx=16, pady=8, relief=tk.FLAT,
                   cursor="hand2", bd=0,
                   activebackground=bg_color, activeforeground=fg_color)
    
    # Hover effects
    def on_enter(e):
        btn.configure(bg=lighten_color(bg_color))
    def on_leave(e):
        btn.configure(bg=bg_color)
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    return btn
