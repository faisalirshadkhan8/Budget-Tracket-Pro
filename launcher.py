"""
Budget Tracker Launcher - Choose between Original and Modern GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class GUILauncher:
    """Launcher window to choose between GUI versions"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker - Choose Interface")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create interface
        self.create_interface()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Create the launcher interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Budget Tracker Pro", 
                               font=('Segoe UI', 24, 'bold'))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Choose your interface style", 
                                  font=('Segoe UI', 12, 'normal'))
        subtitle_label.pack(pady=(0, 30))
        
        # Interface options frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='both', expand=True)
        
        # Configure grid
        options_frame.columnconfigure((0, 1), weight=1)
        options_frame.rowconfigure(0, weight=1)
        
        # Original GUI option
        original_frame = ttk.LabelFrame(options_frame, text="Original Interface", padding="20")
        original_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        original_icon = ttk.Label(original_frame, text="📊", font=('Segoe UI', 48))
        original_icon.pack()
        
        original_title = ttk.Label(original_frame, text="Classic Design", 
                                  font=('Segoe UI', 14, 'bold'))
        original_title.pack(pady=(10, 5))
        
        original_desc = ttk.Label(original_frame, 
                                 text="• Functional interface\n• All features available\n• Traditional layout\n• Familiar design patterns",
                                 font=('Segoe UI', 10),
                                 justify='left')
        original_desc.pack(pady=(0, 15))
        
        original_btn = ttk.Button(original_frame, text="🚀 Launch Classic", 
                                 command=self.launch_original,
                                 style='Classic.TButton')
        original_btn.pack()
        
        # Bind hover events for original button
        self.bind_hover_effects(original_btn, 'Classic.TButton')
        
        # Modern GUI option
        modern_frame = ttk.LabelFrame(options_frame, text="Modern Interface ⭐ RECOMMENDED", padding="20")
        modern_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        modern_icon = ttk.Label(modern_frame, text="✨", font=('Segoe UI', 48))
        modern_icon.pack()
        
        modern_title = ttk.Label(modern_frame, text="Production Ready", 
                                font=('Segoe UI', 14, 'bold'))
        modern_title.pack(pady=(10, 5))
        
        modern_desc = ttk.Label(modern_frame, 
                               text="• Professional design\n• Modern dashboard layout\n• Enhanced visual appeal\n• Production-ready styling",
                               font=('Segoe UI', 10),
                               justify='left')
        modern_desc.pack(pady=(0, 15))
        
        modern_btn = ttk.Button(modern_frame, text="✨ Launch Modern", 
                               command=self.launch_modern,
                               style='Modern.TButton')
        modern_btn.pack()
        
        # Bind hover effects for modern button
        self.bind_hover_effects(modern_btn, 'Modern.TButton')
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill='x', pady=(20, 0))
        
        footer_text = ttk.Label(footer_frame, 
                               text="Both interfaces have the same features. Choose based on your preferred design style.",
                               font=('Segoe UI', 9),
                               foreground='gray')
        footer_text.pack()
        
        # Setup styles
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles with hover effects"""
        style = ttk.Style()
        
        # Classic button style
        style.configure('Classic.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10),
                       background='#4a90e2',
                       foreground='white',
                       borderwidth=1,
                       relief='raised')
        
        style.map('Classic.TButton',
                 background=[('active', '#357abd'),
                           ('pressed', '#2a5a8a')])
        
        # Modern button style
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10),
                       background='#28a745',
                       foreground='white',
                       borderwidth=1,
                       relief='raised')
        
        style.map('Modern.TButton',
                 background=[('active', '#218838'),
                           ('pressed', '#1e7e34')])
    
    def bind_hover_effects(self, button, style_name):
        """Bind hover effects to buttons"""
        def on_enter(event):
            button.state(['active'])
        
        def on_leave(event):
            button.state(['!active'])
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def bind_frame_hover(self, frame):
        """Add visual feedback to frames"""
        original_relief = frame.cget('relief')
        original_borderwidth = frame.cget('borderwidth')
        
        def on_enter(event):
            frame.config(relief='raised', borderwidth=2)
        
        def on_leave(event):
            frame.config(relief=original_relief, borderwidth=original_borderwidth)
        
        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        
        # Also bind to child widgets
        for child in frame.winfo_children():
            child.bind('<Enter>', on_enter)
            child.bind('<Leave>', on_leave)
    
    def launch_original(self):
        """Launch original GUI"""
        try:
            self.root.destroy()
            
            # Import and launch original GUI
            from gui_app import BudgetTrackerGUI
            
            root = tk.Tk()
            app = BudgetTrackerGUI(root)
            root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch original GUI: {str(e)}")
    
    def launch_modern(self):
        """Launch modern GUI"""
        try:
            self.root.destroy()
            
            # Import and launch modern GUI
            from modern_gui_app import ModernBudgetTrackerGUI
            
            root = tk.Tk()
            app = ModernBudgetTrackerGUI(root)
            root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch modern GUI: {str(e)}")


def main():
    """Run the GUI launcher"""
    root = tk.Tk()
    launcher = GUILauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
