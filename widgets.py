# widgets.py - Custom widgets
import tkinter as tk
from utils import lighten_color


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
