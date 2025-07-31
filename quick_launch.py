"""
Quick Launch Script - Direct access to Modern GUI
"""

import tkinter as tk
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def quick_launch():
    """Quick launch with simple choice"""
    root = tk.Tk()
    root.title("Quick Launch")
    root.geometry("400x200")
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Title
    title = tk.Label(root, text="Budget Tracker Pro", font=('Arial', 16, 'bold'))
    title.pack(pady=20)
    
    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)
    
    def launch_modern():
        root.destroy()
        try:
            from modern_gui_app import ModernBudgetTrackerGUI
            new_root = tk.Tk()
            app = ModernBudgetTrackerGUI(new_root)
            new_root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
    
    def launch_classic():
        root.destroy()
        try:
            from gui_app import BudgetTrackerGUI
            new_root = tk.Tk()
            app = BudgetTrackerGUI(new_root)
            new_root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
    
    # Modern button (recommended)
    modern_btn = tk.Button(button_frame, text="🚀 Launch Modern GUI (Recommended)", 
                          command=launch_modern,
                          bg='#28a745', fg='white', font=('Arial', 12, 'bold'),
                          padx=20, pady=10, relief='raised', borderwidth=2)
    modern_btn.pack(pady=10)
    
    # Classic button
    classic_btn = tk.Button(button_frame, text="📊 Launch Classic GUI", 
                           command=launch_classic,
                           bg='#6c757d', fg='white', font=('Arial', 12),
                           padx=20, pady=10, relief='raised', borderwidth=2)
    classic_btn.pack(pady=10)
    
    # Bind hover effects
    def on_enter_modern(event):
        modern_btn.config(bg='#218838')
    
    def on_leave_modern(event):
        modern_btn.config(bg='#28a745')
    
    def on_enter_classic(event):
        classic_btn.config(bg='#5a6268')
    
    def on_leave_classic(event):
        classic_btn.config(bg='#6c757d')
    
    modern_btn.bind('<Enter>', on_enter_modern)
    modern_btn.bind('<Leave>', on_leave_modern)
    classic_btn.bind('<Enter>', on_enter_classic)
    classic_btn.bind('<Leave>', on_leave_classic)
    
    # Info text
    info = tk.Label(root, text="Choose your preferred interface style", 
                   font=('Arial', 10), fg='gray')
    info.pack(pady=(0, 10))
    
    root.mainloop()

if __name__ == "__main__":
    quick_launch()
