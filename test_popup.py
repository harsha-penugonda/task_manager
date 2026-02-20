#!/usr/bin/env python3
"""Test popup to verify Entry widgets are visible"""
import tkinter as tk

def test_popup():
    root = tk.Tk()
    root.withdraw()
    
    popup = tk.Toplevel(root)
    popup.title("Test Entry Visibility")
    popup.geometry("500x400")
    popup.configure(bg='white')
    
    container = tk.Frame(popup, bg='white', padx=20, pady=20)
    container.pack(fill=tk.BOTH, expand=True)
    
    # Test 1: Basic Entry
    tk.Label(container, text="Test 1 - Basic Entry:", bg='white', fg='black',
            font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    entry1 = tk.Entry(container, font=('Helvetica', 12))
    entry1.pack(fill=tk.X, pady=(0, 15), ipady=5)
    entry1.insert(0, "Can you see this text?")
    
    # Test 2: Entry with colors
    tk.Label(container, text="Test 2 - Entry with bg/fg:", bg='white', fg='black',
            font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    entry2 = tk.Entry(container, font=('Helvetica', 12),
                     bg='white', fg='black', insertbackground='black')
    entry2.pack(fill=tk.X, pady=(0, 15), ipady=5)
    entry2.insert(0, "Can you see this one?")
    
    # Test 3: Entry with highlight
    tk.Label(container, text="Test 3 - Entry with highlight:", bg='white', fg='black',
            font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    entry3 = tk.Entry(container, font=('Helvetica', 12),
                     bg='white', fg='black', insertbackground='black',
                     highlightthickness=2, highlightbackground='#cccccc',
                     highlightcolor='#4CAF50')
    entry3.pack(fill=tk.X, pady=(0, 15), ipady=5)
    entry3.insert(0, "Can you see this highlighted one?")
    
    # Test radio buttons
    tk.Label(container, text="Test Radio Buttons:", bg='white', fg='black',
            font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(10, 5))
    var = tk.StringVar(value="Medium")
    rb_frame = tk.Frame(container, bg='white')
    rb_frame.pack(fill=tk.X)
    for val in ["High", "Medium", "Low"]:
        tk.Radiobutton(rb_frame, text=val, variable=var, value=val,
                      bg='white', fg='black', font=('Helvetica', 11)).pack(side=tk.LEFT, padx=(0, 20))
    
    # Close button
    tk.Button(container, text="Close", command=popup.destroy,
             bg='#f44336', fg='white', font=('Helvetica', 11, 'bold'),
             padx=20, pady=8).pack(pady=20)
    
    popup.mainloop()

if __name__ == '__main__':
    test_popup()
