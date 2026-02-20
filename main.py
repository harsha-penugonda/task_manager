# main.py - Task Manager Pro Entry Point
import tkinter as tk

from utils import setup_dpi_awareness, suppress_tk_warnings
from app import LiteTodoApp


def main():
    """Application entry point"""
    # Initialize environment
    setup_dpi_awareness()
    suppress_tk_warnings()
    
    # Launch application
    root = tk.Tk()
    app = LiteTodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
