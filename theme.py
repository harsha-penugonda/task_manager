# theme.py - Theme and color configuration
from tkinter import ttk


# Light mode colors
LIGHT_COLORS = {
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

# Dark mode colors
DARK_COLORS = {
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

# Dialog colors for light mode
DIALOG_LIGHT_COLORS = {
    'bg': '#f8fafc',
    'bg_secondary': '#ffffff',
    'fg': '#1e293b',
    'fg_secondary': '#64748b',
    'entry_bg': '#ffffff',
    'entry_fg': '#1e293b',
    'border': '#e2e8f0',
    'accent': '#3b82f6',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b'
}

# Dialog colors for dark mode
DIALOG_DARK_COLORS = {
    'bg': '#1a1a2e',
    'bg_secondary': '#16213e',
    'fg': '#eaeaea',
    'fg_secondary': '#a0a0a0',
    'entry_bg': '#16213e',
    'entry_fg': '#ffffff',
    'border': '#0f3460',
    'accent': '#3b82f6',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b'
}


def get_colors(dark_mode=False):
    """Get color scheme based on dark mode setting"""
    return DARK_COLORS if dark_mode else LIGHT_COLORS


def get_dialog_colors(dark_mode=False):
    """Get dialog color scheme based on dark mode setting"""
    return DIALOG_DARK_COLORS if dark_mode else DIALOG_LIGHT_COLORS


def configure_treeview_style(style, colors):
    """Configure ttk Treeview styles"""
    style.theme_use('clam')
    
    style.configure('Treeview',
        background=colors['card_bg'],
        foreground=colors['fg'],
        fieldbackground=colors['card_bg'],
        rowheight=36,
        font=('Segoe UI', 10))
    
    style.configure('Treeview.Heading',
        background=colors['bg_secondary'],
        foreground=colors['fg'],
        font=('Segoe UI Semibold', 10),
        padding=(10, 8))
    
    style.map('Treeview',
        background=[('selected', colors['accent2'])],
        foreground=[('selected', '#ffffff')])
    
    style.map('Treeview.Heading',
        background=[('active', colors['button_hover'])])


def configure_scrollbar_style(style, colors):
    """Configure ttk Scrollbar styles"""
    style.configure('Vertical.TScrollbar',
        background=colors['bg_secondary'],
        troughcolor=colors['bg'],
        arrowcolor=colors['fg_secondary'])
