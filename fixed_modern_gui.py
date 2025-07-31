"""
Fixed Modern GUI with simplified styling for debugging
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkcalendar import DateEntry
import sys
import os
# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker


class FixedModernBudgetTrackerGUI:
    """Fixed Modern Budget Tracker GUI with simplified styling"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker Pro - Fixed")
        
        # Set up window
        self.setup_window()
        
        # Initialize the budget tracker
        self.budget_tracker = BudgetTracker()
        
        # Theme management
        self.current_theme = "light"
        self.setup_color_schemes()
        
        # Configure basic styles only
        self.setup_basic_styles()
        
        # Create the modern interface
        self.create_modern_interface()
        
        # Initialize data
        self.update_summary()
        self.update_transaction_list()
    
    def setup_window(self):
        """Setup main window"""
        # Set window size and position
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Configure for high DPI if available
        try:
            self.root.tk.call('tk', 'scaling', 1.2)
        except:
            pass
    
    def setup_color_schemes(self):
        """Define modern color schemes for light and dark themes"""
        self.colors = {
            'light': {
                'primary': '#2563eb',      # Blue
                'secondary': '#64748b',    # Slate
                'success': '#10b981',      # Green
                'warning': '#f59e0b',      # Amber
                'danger': '#ef4444',       # Red
                'background': '#ffffff',   # White
                'surface': '#f8fafc',      # Light gray
                'border': '#e2e8f0',       # Light border
                'text_primary': '#1e293b', # Dark text
                'text_secondary': '#64748b', # Gray text
                'accent': '#3b82f6',       # Light blue
            }
        }
    
    def get_color(self, color_name):
        """Get color from current theme"""
        return self.colors[self.current_theme][color_name]
    
    def setup_basic_styles(self):
        """Configure basic ttk styles without complex styling"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Basic button style
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           padding=(12, 6))
        
        # Basic label styles
        self.style.configure('Heading.TLabel',
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 14, 'bold'))
        
        self.style.configure('Body.TLabel',
                           font=('Segoe UI', 10, 'normal'))
    
    def create_modern_interface(self):
        """Create the main modern interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_modern_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Configure grid for two panels
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel (transaction input and summary)
        self.left_panel = ttk.Frame(content_frame)
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        
        # Right panel (charts and analytics)
        self.right_panel = ttk.Frame(content_frame)
        self.right_panel.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        
        # Create panel content
        self.create_left_panel()
        self.create_right_panel()
    
    def create_modern_header(self, parent):
        """Create modern header with title and controls"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Title section
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side='left', fill='x', expand=True)
        
        title_label = ttk.Label(title_frame, text="Budget Tracker Pro", 
                               style='Heading.TLabel')
        title_label.pack(side='left')
        
        subtitle_label = ttk.Label(title_frame, text="Professional Financial Management", 
                                  style='Body.TLabel')
        subtitle_label.pack(side='left', padx=(16, 0))
        
        # Controls section
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side='right')
        
        # Theme toggle button
        theme_btn = ttk.Button(controls_frame, text="🌙 Dark Mode", 
                              command=self.toggle_theme, style='Modern.TButton')
        theme_btn.pack(side='right', padx=(0, 8))
        
        # Settings button
        settings_btn = ttk.Button(controls_frame, text="⚙️ Settings", 
                                 style='Modern.TButton')
        settings_btn.pack(side='right', padx=(0, 8))
    
    def create_left_panel(self):
        """Create left panel with transaction input and summary"""
        print("Creating left panel...")
        
        # Quick stats cards
        self.create_summary_cards()
        
        # Transaction input section
        self.create_transaction_input()
        
        # Recent transactions
        self.create_recent_transactions()
        
        # Quick actions
        self.create_quick_actions()
        
        print("Left panel created successfully!")
    
    def create_summary_cards(self):
        """Create summary cards"""
        cards_frame = ttk.Frame(self.left_panel)
        cards_frame.pack(fill='x', pady=(0, 16))
        
        # Income card
        income_card = ttk.LabelFrame(cards_frame, text="Total Income")
        income_card.pack(fill='x', pady=(0, 8))
        
        self.income_value_label = ttk.Label(income_card, text="$0.00", style='Body.TLabel')
        self.income_value_label.pack(padx=16, pady=8)
        
        # Expenses card
        expenses_card = ttk.LabelFrame(cards_frame, text="Total Expenses")
        expenses_card.pack(fill='x', pady=(0, 8))
        
        self.expenses_value_label = ttk.Label(expenses_card, text="$0.00", style='Body.TLabel')
        self.expenses_value_label.pack(padx=16, pady=8)
        
        # Balance card
        balance_card = ttk.LabelFrame(cards_frame, text="Net Balance")
        balance_card.pack(fill='x')
        
        self.balance_value_label = ttk.Label(balance_card, text="$0.00", style='Body.TLabel')
        self.balance_value_label.pack(padx=16, pady=8)
        
        print("Summary cards created")
    
    def create_transaction_input(self):
        """Create transaction input form"""
        input_card = ttk.LabelFrame(self.left_panel, text="Add New Transaction")
        input_card.pack(fill='x', pady=(0, 16))
        
        # Form content
        form_content = ttk.Frame(input_card)
        form_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Configure grid
        form_content.columnconfigure(1, weight=1)
        
        # Date input
        ttk.Label(form_content, text="Date:", style='Body.TLabel').grid(
            row=0, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.date_entry = DateEntry(form_content, width=16, 
                                   date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, sticky='ew', pady=(0, 8))
        
        # Amount input
        ttk.Label(form_content, text="Amount:", style='Body.TLabel').grid(
            row=1, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(form_content, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=1, sticky='ew', pady=(0, 8))
        
        # Category input
        ttk.Label(form_content, text="Category:", style='Body.TLabel').grid(
            row=2, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_content, textvariable=self.category_var)
        self.category_combo.grid(row=2, column=1, sticky='ew', pady=(0, 8))
        
        # Type selection
        ttk.Label(form_content, text="Type:", style='Body.TLabel').grid(
            row=3, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.type_var = tk.StringVar(value="Expense")
        type_combo = ttk.Combobox(form_content, textvariable=self.type_var,
                                values=['Income', 'Expense'], state='readonly')
        type_combo.grid(row=3, column=1, sticky='ew', pady=(0, 8))
        type_combo.bind('<<ComboboxSelected>>', self.on_type_changed)
        
        # Action buttons
        button_frame = ttk.Frame(form_content)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(8, 0), sticky='ew')
        
        add_btn = ttk.Button(button_frame, text="Add Transaction", 
                           command=self.add_transaction, style='Modern.TButton')
        add_btn.pack(side='right')
        
        # Initialize categories
        self.update_category_list("Expense")
        
        print("Transaction input created")
    
    def create_recent_transactions(self):
        """Create recent transactions list"""
        transactions_card = ttk.LabelFrame(self.left_panel, text="Recent Transactions")
        transactions_card.pack(fill='both', expand=True, pady=(0, 16))
        
        # Transaction list content
        list_content = ttk.Frame(transactions_card)
        list_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Transaction table
        columns = ('Date', 'Type', 'Category', 'Amount')
        self.tree = ttk.Treeview(list_content, columns=columns, show='headings',
                               height=8)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column('Date', width=80)
        self.tree.column('Type', width=60)
        self.tree.column('Category', width=100)
        self.tree.column('Amount', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_content, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        print("Recent transactions created")
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_card = ttk.LabelFrame(self.left_panel, text="Quick Actions")
        actions_card.pack(fill='x')
        
        # Actions content
        actions_content = ttk.Frame(actions_card)
        actions_content.pack(fill='x', padx=16, pady=16)
        
        # Data management buttons
        save_csv_btn = ttk.Button(actions_content, text="Save CSV", 
                                command=self.save_to_csv, style='Modern.TButton')
        save_csv_btn.pack(side='left', padx=(0, 8))
        
        load_csv_btn = ttk.Button(actions_content, text="Load CSV", 
                                command=self.load_from_csv, style='Modern.TButton')
        load_csv_btn.pack(side='left', padx=(0, 8))
        
        print("Quick actions created")
    
    def create_right_panel(self):
        """Create right panel with analytics"""
        # Simple charts placeholder
        charts_card = ttk.LabelFrame(self.right_panel, text="Financial Analytics")
        charts_card.pack(fill='both', expand=True)
        
        # Charts content
        charts_content = ttk.Frame(charts_card)
        charts_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Placeholder for charts
        placeholder_label = ttk.Label(charts_content, text="Charts will appear here", 
                                     style='Body.TLabel')
        placeholder_label.pack(expand=True)
        
        print("Right panel created")
    
    # Simplified methods for basic functionality
    def add_transaction(self):
        """Add a new transaction"""
        try:
            date_str = self.date_entry.get()
            amount_str = self.amount_var.get().strip()
            category = self.category_var.get().strip()
            trans_type = self.type_var.get()
            
            if not amount_str or not category:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            amount = float(amount_str)
            
            # Add transaction
            self.budget_tracker.add_transaction(date_str, amount, category, trans_type)
            
            # Clear form
            self.amount_var.set("")
            self.category_var.set("")
            
            # Update displays
            self.update_summary()
            self.update_transaction_list()
            
            messagebox.showinfo("Success", "Transaction added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {str(e)}")
    
    def update_summary(self):
        """Update summary cards"""
        try:
            total_income = sum(t['amount'] for t in self.budget_tracker.transactions if t['type'] == 'Income')
            total_expenses = sum(t['amount'] for t in self.budget_tracker.transactions if t['type'] == 'Expense')
            net_balance = total_income - total_expenses
            
            self.income_value_label.config(text=f"${total_income:.2f}")
            self.expenses_value_label.config(text=f"${total_expenses:.2f}")
            self.balance_value_label.config(text=f"${net_balance:.2f}")
        except Exception as e:
            print(f"Error updating summary: {e}")
    
    def update_transaction_list(self):
        """Update transaction list"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add transactions
            for transaction in self.budget_tracker.transactions[-20:]:  # Show last 20
                self.tree.insert('', 'end', values=(
                    transaction['date'],
                    transaction['type'],
                    transaction['category'],
                    f"${transaction['amount']:.2f}"
                ))
        except Exception as e:
            print(f"Error updating transaction list: {e}")
    
    def update_category_list(self, trans_type):
        """Update category list based on transaction type"""
        try:
            categories = self.budget_tracker.get_categories_by_type(trans_type)
            self.category_combo['values'] = categories
        except Exception as e:
            print(f"Error updating categories: {e}")
    
    def on_type_changed(self, event):
        """Handle transaction type change"""
        trans_type = self.type_var.get()
        self.update_category_list(trans_type)
    
    def save_to_csv(self):
        """Save data to CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save transactions as CSV"
            )
            if file_path:
                self.budget_tracker.save_to_csv(file_path)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_from_csv(self):
        """Load data from CSV"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv")],
                title="Load transactions from CSV"
            )
            if file_path:
                self.budget_tracker.load_from_csv(file_path)
                self.update_summary()
                self.update_transaction_list()
                messagebox.showinfo("Success", f"Data loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        # For now, just show a message
        messagebox.showinfo("Theme", "Theme toggle functionality will be implemented")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FixedModernBudgetTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
