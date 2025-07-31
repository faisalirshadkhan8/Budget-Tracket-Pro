"""
Budget Tracker GUI Application - Phase 4: Advanced Features
Features: Transaction Management, Charts, Data Persistence, Date Picker, Custom Categories, Budget Alerts
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkcalendar import DateEntry
from models.budget_tracker import BudgetTracker


class BudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker - Phase 2: Charts & Visualizations")
        
        # Make the window cover the whole screen
        self.root.state('zoomed')  # For Windows - maximizes the window
        # Alternative for cross-platform:
        # self.root.attributes('-fullscreen', True)  # True fullscreen
        # Or get screen dimensions and set accordingly:
        # width = self.root.winfo_screenwidth()
        # height = self.root.winfo_screenheight()
        # self.root.geometry(f"{width}x{height}+0+0")
        
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the budget tracker
        self.budget_tracker = BudgetTracker()
        
        # Theme management - Phase 4 Feature 4
        self.current_theme = "light"
        self.load_theme_preference()
        
        # Configure style
        self.setup_styles()
        
        # Create main container with scrollable canvas
        self.setup_main_container()
        
        # Create widgets
        self.create_widgets()
        self.create_charts_section()
        
        # Initial updates
        self.update_summary()
        self.update_transaction_list()  # Add this missing call
        self.update_charts()
        self.update_budget_alerts()  # Initialize budget alerts
    
    def setup_styles(self):
        """Configure ttk styles for consistent appearance with theme support"""
        self.style = ttk.Style()
        
        # Apply theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme settings"""
        if self.current_theme == "light":
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
    
    def apply_light_theme(self):
        """Apply light theme styling"""
        self.style.theme_use('clam')
        
        # Light theme colors
        bg_color = '#ffffff'
        fg_color = '#000000'
        select_bg = '#e3f2fd'
        border_color = '#cccccc'
        
        # Configure window background
        self.root.configure(bg='#f0f0f0')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                           foreground=fg_color, background='#f0f0f0')
        self.style.configure('Summary.TLabel', font=('Arial', 12, 'bold'), 
                           foreground=fg_color, background=bg_color)
        self.style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Chart.TLabel', font=('Arial', 14, 'bold'), 
                           foreground=fg_color, background=bg_color)
        
        # Configure frame and other widget styles
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelFrame', background='#f0f0f0', foreground=fg_color)
        self.style.configure('TLabelFrame.Label', background='#f0f0f0', foreground=fg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('TButton', background=bg_color, foreground=fg_color)
        self.style.configure('TEntry', background=bg_color, foreground=fg_color)
        self.style.configure('TCombobox', background=bg_color, foreground=fg_color)
        
        # Update canvas background
        if hasattr(self, 'canvas'):
            self.canvas.configure(bg='#f0f0f0')
    
    def apply_dark_theme(self):
        """Apply dark theme styling"""
        self.style.theme_use('alt')
        
        # Dark theme colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        select_bg = '#404040'
        border_color = '#555555'
        
        # Configure window background
        self.root.configure(bg='#1e1e1e')
        
        # Configure custom styles for dark theme
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                           foreground=fg_color, background='#1e1e1e')
        self.style.configure('Summary.TLabel', font=('Arial', 12, 'bold'), 
                           foreground=fg_color, background=bg_color)
        self.style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Chart.TLabel', font=('Arial', 14, 'bold'), 
                           foreground=fg_color, background=bg_color)
        
        # Configure frame and widget styles for dark theme
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TLabelFrame', background='#1e1e1e', foreground=fg_color)
        self.style.configure('TLabelFrame.Label', background='#1e1e1e', foreground=fg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('TButton', background=bg_color, foreground=fg_color,
                           borderwidth=1, relief='raised')
        self.style.configure('TEntry', background=bg_color, foreground=fg_color,
                           insertcolor=fg_color, borderwidth=1)
        self.style.configure('TCombobox', background=bg_color, foreground=fg_color,
                           borderwidth=1)
        
        # Treeview dark theme
        self.style.configure('Treeview', background=bg_color, foreground=fg_color,
                           fieldbackground=bg_color)
        self.style.configure('Treeview.Heading', background='#404040', foreground=fg_color)
        
        # Update canvas background
        if hasattr(self, 'canvas'):
            self.canvas.configure(bg='#1e1e1e')
    
    def setup_main_container(self):
        """Set up the main scrollable container"""
        # Create main canvas and scrollbar
        canvas_bg = '#f0f0f0' if self.current_theme == 'light' else '#1e1e1e'
        self.canvas = tk.Canvas(self.root, bg=canvas_bg)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")
        
        # Create main frame within scrollable area
        self.main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        
        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        
        # Title and theme switcher
        title_frame = ttk.Frame(self.main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(title_frame, text="Budget Tracker - Phase 4", style='Title.TLabel')
        title_label.grid(row=0, column=1)
        
        # Theme switcher button - Phase 4 Feature 4
        theme_text = "☀️ Light Mode" if self.current_theme == "dark" else "🌙 Dark Mode"
        self.theme_button = ttk.Button(title_frame, text=theme_text, 
                                      command=self.toggle_theme, width=12)
        self.theme_button.grid(row=0, column=2, sticky=tk.E)
        
        # Create left and right columns
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Configure column weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)  # Charts take more space
        self.main_frame.rowconfigure(1, weight=1)
        
        # Create sections in left frame
        self.create_input_section()
        self.create_summary_section()
        self.create_budget_alerts_section()  # Phase 4 Feature 3
        self.create_transaction_list()
    
    def create_input_section(self):
        """Create the transaction input section with date picker"""
        
        # Input frame
        input_frame = ttk.LabelFrame(self.left_frame, text="Add New Transaction", padding="15")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=0)  # For manage categories button
        
        # Date picker - Phase 4 Feature
        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(input_frame, width=18, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Amount input
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=20)
        self.amount_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Category input with dynamic categories
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, width=18)
        
        # Initialize with default categories for Expense
        self.update_category_list("Expense")
        
        self.category_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Category management button
        self.manage_categories_btn = ttk.Button(input_frame, text="Manage Categories", 
                                              command=self.open_category_manager)
        self.manage_categories_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Transaction type
        ttk.Label(input_frame, text="Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="Expense")
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, width=18)
        self.type_combo['values'] = ('Income', 'Expense')
        self.type_combo['state'] = 'readonly'
        self.type_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Bind type change to update categories
        self.type_combo.bind('<<ComboboxSelected>>', self.on_type_changed)
        
        # Currency selection
        ttk.Label(input_frame, text="Currency:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.currency_var = tk.StringVar(value="USD")
        self.currency_combo = ttk.Combobox(input_frame, textvariable=self.currency_var, width=18)
        self.currency_combo['values'] = ('USD ($)', 'EUR (€)', 'GBP (£)', 'JPY (¥)', 'CAD (C$)', 'AUD (A$)', 'CHF (₣)', 'CNY (¥)', 'INR (₹)', 'BRL (R$)', 'PKR (₨)')
        self.currency_combo['state'] = 'readonly'
        self.currency_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Add button
        self.add_button = ttk.Button(input_frame, text="Add Transaction", 
                                   command=self.add_transaction, style='Action.TButton')
        self.add_button.grid(row=5, column=0, columnspan=2, pady=(15, 5))
        
        # Bind Enter key to add transaction
        self.amount_entry.bind('<Return>', lambda e: self.add_transaction())
        self.category_combo.bind('<Return>', lambda e: self.add_transaction())
        
        # Set default currency
        self.currency_var.set("USD ($)")
    
    def create_summary_section(self):
        """Create the financial summary section"""
        
        summary_frame = ttk.LabelFrame(self.left_frame, text="Financial Summary", padding="15")
        summary_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        summary_frame.columnconfigure(1, weight=1)
        
        # Total Income
        ttk.Label(summary_frame, text="Total Income:", style='Summary.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.income_label = ttk.Label(summary_frame, text="$0.00", foreground='green', font=('Arial', 12, 'bold'))
        self.income_label.grid(row=0, column=1, sticky=tk.E, pady=5)
        
        # Total Expenses
        ttk.Label(summary_frame, text="Total Expenses:", style='Summary.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.expenses_label = ttk.Label(summary_frame, text="$0.00", foreground='red', font=('Arial', 12, 'bold'))
        self.expenses_label.grid(row=1, column=1, sticky=tk.E, pady=5)
        
        # Net Balance
        ttk.Label(summary_frame, text="Net Balance:", style='Summary.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.balance_label = ttk.Label(summary_frame, text="$0.00", font=('Arial', 14, 'bold'))
        self.balance_label.grid(row=2, column=1, sticky=tk.E, pady=5)
    
    def create_budget_alerts_section(self):
        """Create the budget alerts section - Phase 4 Feature 3"""
        
        alerts_frame = ttk.LabelFrame(self.left_frame, text="Budget Alerts", padding="15")
        alerts_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        alerts_frame.columnconfigure(0, weight=1)
        
        # Budget management button
        budget_button_frame = ttk.Frame(alerts_frame)
        budget_button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.manage_budget_btn = ttk.Button(budget_button_frame, text="Set Budget Limits", 
                                          command=self.open_budget_manager)
        self.manage_budget_btn.pack(side=tk.LEFT)
        
        # Alerts display area
        self.alerts_frame = ttk.Frame(alerts_frame)
        self.alerts_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Initial alert display
        self.alert_labels = []
        self.update_budget_alerts()
    
    def create_transaction_list(self):
        """Create the enhanced transaction list section with Phase 3 features"""
        
        list_frame = ttk.LabelFrame(self.left_frame, text="Transaction History", padding="15")
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)  # Changed to row 1 for filter controls
        
        # Add filter controls
        self.create_filter_controls(list_frame)
        
        # Create Treeview for transaction list with enhanced columns
        columns = ('Date', 'Type', 'Category', 'Amount', 'Currency', 'USD Value')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Configure column headings and widths
        self.tree.heading('Date', text='Date', command=lambda: self.sort_column('Date'))
        self.tree.heading('Type', text='Type', command=lambda: self.sort_column('Type'))
        self.tree.heading('Category', text='Category', command=lambda: self.sort_column('Category'))
        self.tree.heading('Amount', text='Amount', command=lambda: self.sort_column('Amount'))
        self.tree.heading('Currency', text='Currency', command=lambda: self.sort_column('Currency'))
        self.tree.heading('USD Value', text='USD Value', command=lambda: self.sort_column('USD Value'))
        
        self.tree.column('Date', width=100)
        self.tree.column('Type', width=80)
        self.tree.column('Category', width=120)
        self.tree.column('Amount', width=100)
        self.tree.column('Currency', width=70)
        self.tree.column('USD Value', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Grid the treeview and scrollbar (row 1 now due to filter controls)
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Add data persistence controls
        self.create_persistence_controls(list_frame)
        
        # Configure main frame row weight
        self.left_frame.rowconfigure(3, weight=1)
        
        # Initialize sorting variables
        self.sort_reverse = False
        self.last_sort_column = None
    
    def create_filter_controls(self, parent_frame):
        """Create filter controls for transaction list"""
        filter_frame = ttk.Frame(parent_frame)
        filter_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="All")
        self.filter_all_btn = ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, 
                                            value="All", command=self.update_transaction_list)
        self.filter_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.filter_income_btn = ttk.Radiobutton(filter_frame, text="Income", variable=self.filter_var, 
                                               value="Income", command=self.update_transaction_list)
        self.filter_income_btn.pack(side=tk.LEFT, padx=5)
        
        self.filter_expense_btn = ttk.Radiobutton(filter_frame, text="Expenses", variable=self.filter_var, 
                                                value="Expense", command=self.update_transaction_list)
        self.filter_expense_btn.pack(side=tk.LEFT, padx=5)
    
    def create_persistence_controls(self, parent_frame):
        """Create save/load controls for data persistence"""
        persistence_frame = ttk.Frame(parent_frame)
        persistence_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Save buttons
        ttk.Label(persistence_frame, text="Data:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_csv_btn = ttk.Button(persistence_frame, text="Save CSV", 
                                     command=self.save_to_csv)
        self.save_csv_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_json_btn = ttk.Button(persistence_frame, text="Save JSON", 
                                      command=self.save_to_json)
        self.save_json_btn.pack(side=tk.LEFT, padx=2)
        
        # Load buttons
        self.load_csv_btn = ttk.Button(persistence_frame, text="Load CSV", 
                                     command=self.load_from_csv)
        self.load_csv_btn.pack(side=tk.LEFT, padx=2)
        
        self.load_json_btn = ttk.Button(persistence_frame, text="Load JSON", 
                                      command=self.load_from_json)
        self.load_json_btn.pack(side=tk.LEFT, padx=2)
    
    def sort_column(self, column):
        """Sort the transaction list by the specified column"""
        # Toggle sort direction if clicking the same column
        if self.last_sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.last_sort_column = column
        self.update_transaction_list()
    
    def get_filtered_transactions(self):
        """Get transactions based on current filter"""
        transactions = self.budget_tracker.get_transactions()
        
        # Safety check for filter_var initialization
        try:
            filter_type = self.filter_var.get()
        except AttributeError:
            # If filter_var is not yet initialized, return all transactions
            return transactions
        
        if filter_type == "All":
            return transactions
        else:
            return [t for t in transactions if t['type'] == filter_type]
    
    def sort_transactions(self, transactions):
        """Sort transactions based on current sort column and direction"""
        if not self.last_sort_column or not transactions:
            return transactions
        
        def get_sort_key(transaction):
            if self.last_sort_column == 'Date':
                return transaction['date']
            elif self.last_sort_column == 'Type':
                return transaction['type']
            elif self.last_sort_column == 'Category':
                return transaction['category']
            elif self.last_sort_column == 'Amount':
                return transaction['amount']
            elif self.last_sort_column == 'Currency':
                return transaction.get('currency', 'USD')
            elif self.last_sort_column == 'USD Value':
                return self.budget_tracker.convert_to_usd(transaction['amount'], 
                                                        transaction.get('currency', 'USD'))
            return ''
        
        return sorted(transactions, key=get_sort_key, reverse=self.sort_reverse)
    
    def add_transaction(self):
        """Add a new transaction with input validation and custom date"""
        
        # Get input values
        amount_str = self.amount_var.get().strip()
        category = self.category_var.get().strip()
        transaction_type = self.type_var.get()
        currency_full = self.currency_var.get()
        selected_date = self.date_entry.get_date()
        
        # Extract currency code from the selection (e.g., "USD ($)" -> "USD")
        currency = currency_full.split(' ')[0] if currency_full else "USD"
        
        # Validate inputs
        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount")
            self.amount_entry.focus()
            return
        
        if not category:
            messagebox.showerror("Error", "Please enter a category")
            self.category_combo.focus()
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for amount")
            self.amount_entry.focus()
            self.amount_entry.select_range(0, tk.END)
            return
        
        # Convert date to ISO format
        transaction_date = datetime.combine(selected_date, datetime.min.time()).isoformat()
        
        # Add transaction to budget tracker with custom date
        self.budget_tracker.add_transaction(amount, category, transaction_type, currency, transaction_date)
        
        # Clear input fields
        self.clear_inputs()
        
        # Update display
        self.update_summary()
        self.update_transaction_list()
        self.update_charts()  # Update charts when new transaction is added
        self.update_budget_alerts()  # Update budget alerts after new transaction
        
        # Show success message
        currency_symbol = self.budget_tracker.get_currency_symbol(currency)
        messagebox.showinfo("Success", f"{transaction_type} of {currency_symbol}{amount:.2f} added successfully!")
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.amount_var.set("")
        self.category_var.set("")
        self.type_var.set("Expense")
        self.currency_var.set("USD ($)")
        self.date_entry.set_date(date.today())  # Reset to today's date
        self.amount_entry.focus()
    
    def update_summary(self):
        """Update the financial summary display with USD-converted amounts"""
        summary = self.budget_tracker.get_summary()
        
        # All amounts are now in USD from the summary calculation
        self.income_label.config(text=f"${summary['total_income']:.2f}")
        self.expenses_label.config(text=f"${summary['total_expenses']:.2f}")
        
        balance = summary['net_balance']
        self.balance_label.config(text=f"${balance:.2f} (in USD)")
        
        # Update balance color based on positive/negative
        if balance > 0:
            self.balance_label.config(foreground='green')
        elif balance < 0:
            self.balance_label.config(foreground='red')
        else:
            self.balance_label.config(foreground='black')
    
    def update_transaction_list(self):
        """Update the transaction list display with filtering and sorting"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered and sorted transactions
        filtered_transactions = self.get_filtered_transactions()
        sorted_transactions = self.sort_transactions(filtered_transactions)
        
        # Add transactions to the tree
        for transaction in sorted_transactions:
            date_str = transaction['date'][:10]  # Format: YYYY-MM-DD
            currency = transaction.get('currency', 'USD')
            currency_symbol = self.budget_tracker.get_currency_symbol(currency)
            amount_str = f"{currency_symbol}{transaction['amount']:.2f}"
            
            # Calculate USD equivalent
            usd_value = self.budget_tracker.convert_to_usd(transaction['amount'], currency)
            usd_str = f"${usd_value:.2f}"
            
            values = (
                date_str, 
                transaction['type'], 
                transaction['category'], 
                amount_str,
                currency,
                usd_str
            )
            
            # Add item with different tags for income/expense
            tag = 'income' if transaction['type'] == 'Income' else 'expense'
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure tag colors
        self.tree.tag_configure('income', foreground='green')
        self.tree.tag_configure('expense', foreground='red')
    
    def save_to_csv(self):
        """Save transactions to CSV file with file dialog"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Transactions as CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.save_to_csv(filename)
                if success:
                    messagebox.showinfo("Success", f"Transactions saved successfully to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to save transactions to CSV file")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def save_to_json(self):
        """Save transactions to JSON file with file dialog"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Transactions as JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.save_to_json(filename)
                if success:
                    messagebox.showinfo("Success", f"Transactions saved successfully to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to save transactions to JSON file")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def load_from_csv(self):
        """Load transactions from CSV file with file dialog"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Transactions from CSV",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.load_from_csv(filename)
                
                if success:
                    # Refresh all displays
                    self.update_summary()
                    self.update_transaction_list()
                    self.update_charts()
                    messagebox.showinfo("Success", f"Transactions loaded successfully from {filename}")
                else:
                    messagebox.showerror("Error", "Failed to load transactions from CSV file. Please check the file format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def load_from_json(self):
        """Load transactions from JSON file with file dialog"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Transactions from JSON",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.load_from_json(filename)
                if success:
                    # Refresh all displays
                    self.update_summary()
                    self.update_transaction_list()
                    self.update_charts()
                    messagebox.showinfo("Success", f"Transactions loaded successfully from {filename}")
                else:
                    messagebox.showerror("Error", "Failed to load transactions from JSON file. Please check the file format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def create_charts_section(self):
        """Create the charts and visualizations section"""
        
        # Charts container frame
        charts_frame = ttk.LabelFrame(self.right_frame, text="Charts & Visualizations", padding="15")
        charts_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.rowconfigure(0, weight=1)
        
        # Create notebook for multiple charts
        self.charts_notebook = ttk.Notebook(charts_frame)
        self.charts_notebook.pack(fill="both", expand=True)
        
        # Pie Chart Tab
        self.pie_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.pie_frame, text="Expenses by Category")
        
        # Bar Chart Tab
        self.bar_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.bar_frame, text="Income vs Expenses")
        
        # Line Chart Tab (for future balance over time)
        self.line_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.line_frame, text="Balance Trend")
        
        # Initialize matplotlib figures
        self.setup_pie_chart()
        self.setup_bar_chart()
        self.setup_line_chart()
    
    def setup_pie_chart(self):
        """Set up the pie chart for expenses by category"""
        
        # Create matplotlib figure
        self.pie_fig = Figure(figsize=(6, 5), dpi=80)
        self.pie_ax = self.pie_fig.add_subplot(111)
        
        # Create canvas
        self.pie_canvas = FigureCanvasTkAgg(self.pie_fig, self.pie_frame)
        self.pie_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial empty chart
        self.update_pie_chart()
    
    def setup_bar_chart(self):
        """Set up the bar chart for income vs expenses"""
        
        # Create matplotlib figure
        self.bar_fig = Figure(figsize=(6, 5), dpi=80)
        self.bar_ax = self.bar_fig.add_subplot(111)
        
        # Create canvas
        self.bar_canvas = FigureCanvasTkAgg(self.bar_fig, self.bar_frame)
        self.bar_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial empty chart
        self.update_bar_chart()
    
    def setup_line_chart(self):
        """Set up the line chart for balance over time"""
        
        # Create matplotlib figure
        self.line_fig = Figure(figsize=(6, 5), dpi=80)
        self.line_ax = self.line_fig.add_subplot(111)
        
        # Create canvas
        self.line_canvas = FigureCanvasTkAgg(self.line_fig, self.line_frame)
        self.line_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial empty chart
        self.update_line_chart()
    
    def update_pie_chart(self):
        """Update the pie chart with current expense data"""
        
        self.pie_ax.clear()
        
        # Get expense transactions
        transactions = self.budget_tracker.get_transactions_by_type("Expense")
        
        if not transactions:
            self.pie_ax.text(0.5, 0.5, 'No expense data available', 
                           horizontalalignment='center', verticalalignment='center',
                           transform=self.pie_ax.transAxes, fontsize=12)
            self.pie_ax.set_title("Expenses by Category")
        else:
            # Group expenses by category
            category_totals = {}
            for transaction in transactions:
                category = transaction['category']
                amount = transaction['amount']
                category_totals[category] = category_totals.get(category, 0) + amount
            
            # Create pie chart
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            
            # Define colors
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            
            # Create pie chart
            wedges, texts, autotexts = self.pie_ax.pie(amounts, labels=categories, 
                                                     autopct='%1.1f%%', colors=colors,
                                                     startangle=90)
            
            # Improve text appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
            
            self.pie_ax.set_title("Expenses by Category", fontsize=14, fontweight='bold')
        
        # Refresh canvas
        self.pie_canvas.draw()
    
    def update_bar_chart(self):
        """Update the bar chart with income vs expenses comparison"""
        
        self.bar_ax.clear()
        
        # Get summary data
        summary = self.budget_tracker.get_summary()
        
        # Data for bar chart
        categories = ['Income', 'Expenses']
        values = [summary['total_income'], summary['total_expenses']]
        colors = ['#2ecc71', '#e74c3c']  # Green for income, red for expenses
        
        # Create bar chart
        bars = self.bar_ax.bar(categories, values, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            self.bar_ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                           f'${value:.2f}',
                           ha='center', va='bottom', fontweight='bold')
        
        # Formatting
        self.bar_ax.set_title("Income vs Expenses", fontsize=14, fontweight='bold')
        self.bar_ax.set_ylabel("Amount", fontsize=12)
        
        # Set y-axis to start from 0
        self.bar_ax.set_ylim(0, max(max(values) * 1.1, 100))
        
        # Add grid for better readability
        self.bar_ax.grid(True, alpha=0.3, axis='y')
        
        # Refresh canvas
        self.bar_canvas.draw()
    
    def update_line_chart(self):
        """Update the line chart with balance over time"""
        
        self.line_ax.clear()
        
        transactions = self.budget_tracker.get_transactions()
        
        if not transactions:
            self.line_ax.text(0.5, 0.5, 'No transaction data available', 
                            horizontalalignment='center', verticalalignment='center',
                            transform=self.line_ax.transAxes, fontsize=12)
            self.line_ax.set_title("Balance Over Time")
        else:
            # Sort transactions by date
            sorted_transactions = sorted(transactions, key=lambda x: x['date'])
            
            # Calculate running balance
            dates = []
            balances = []
            running_balance = 0
            
            for transaction in sorted_transactions:
                if transaction['type'] == 'Income':
                    running_balance += transaction['amount']
                else:
                    running_balance -= transaction['amount']
                
                # Convert date string to datetime for better plotting
                date_obj = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
                dates.append(date_obj)
                balances.append(running_balance)
            
            # Plot line chart
            self.line_ax.plot(dates, balances, marker='o', linewidth=2, markersize=4)
            
            # Color the line based on positive/negative balance
            for i in range(len(balances)):
                color = 'green' if balances[i] >= 0 else 'red'
                if i > 0:
                    self.line_ax.plot(dates[i-1:i+1], balances[i-1:i+1], color=color, linewidth=2)
            
            # Formatting
            self.line_ax.set_title("Balance Over Time", fontsize=14, fontweight='bold')
            self.line_ax.set_ylabel("Balance", fontsize=12)
            self.line_ax.set_xlabel("Date", fontsize=12)
            
            # Format x-axis dates
            self.line_ax.tick_params(axis='x', rotation=45)
            
            # Add horizontal line at y=0
            self.line_ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            
            # Add grid
            self.line_ax.grid(True, alpha=0.3)
            
            # Tight layout to prevent label cutoff
            self.line_fig.tight_layout()
        
        # Refresh canvas
        self.line_canvas.draw()
    
    def update_charts(self):
        """Update all charts"""
        self.update_pie_chart()
        self.update_bar_chart()
        self.update_line_chart()
    
    # Phase 4 Feature 2: Custom Categories Management
    def update_category_list(self, transaction_type: str):
        """Update the category combobox based on transaction type"""
        categories = self.budget_tracker.get_categories(transaction_type)
        self.category_combo['values'] = tuple(categories)
        # Clear current selection
        self.category_var.set("")
    
    def on_type_changed(self, event=None):
        """Handle transaction type change"""
        selected_type = self.type_var.get()
        self.update_category_list(selected_type)
    
    def open_category_manager(self):
        """Open the category management window"""
        CategoryManagerWindow(self.root, self.budget_tracker, self.update_category_list)
    
    # Phase 4 Feature 3: Budget Alerts Management
    def update_budget_alerts(self):
        """Update budget alerts display"""
        # Clear existing alert labels
        for label in self.alert_labels:
            label.destroy()
        self.alert_labels.clear()
        
        # Get current budget status
        budget_status = self.budget_tracker.get_budget_status()
        alerts = budget_status['alerts']
        
        if not alerts:
            # Show "No alerts" message
            no_alerts_label = ttk.Label(self.alerts_frame, text="✅ No budget alerts", 
                                       foreground='green', font=('Arial', 10))
            no_alerts_label.pack(anchor=tk.W)
            self.alert_labels.append(no_alerts_label)
        else:
            # Show each alert
            for alert in alerts:
                if alert['severity'] == 'critical':
                    icon = "🚨"
                    color = 'red'
                else:
                    icon = "⚠️"
                    color = 'orange'
                
                alert_text = f"{icon} {alert['message']}"
                alert_label = ttk.Label(self.alerts_frame, text=alert_text, 
                                       foreground=color, font=('Arial', 9))
                alert_label.pack(anchor=tk.W, pady=2)
                self.alert_labels.append(alert_label)
    
    def open_budget_manager(self):
        """Open the budget management window"""
        BudgetManagerWindow(self.root, self.budget_tracker, self.update_budget_alerts)
    
    # Phase 4 Feature 4: Theme Switcher
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_button.config(text="☀️ Light Mode")
        else:
            self.current_theme = "light"
            self.theme_button.config(text="🌙 Dark Mode")
        
        # Apply new theme
        self.apply_theme()
        
        # Save theme preference
        self.save_theme_preference()
        
        # Update chart backgrounds
        self.update_chart_themes()
        
        # Show notification
        messagebox.showinfo("Theme Changed", f"Switched to {self.current_theme} theme!")
    
    def save_theme_preference(self):
        """Save theme preference to file"""
        try:
            import json
            theme_settings = {'theme': self.current_theme}
            with open('theme_settings.json', 'w') as file:
                json.dump(theme_settings, file)
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def load_theme_preference(self):
        """Load theme preference from file"""
        try:
            import json
            from pathlib import Path
            
            theme_file = Path('theme_settings.json')
            if theme_file.exists():
                with open('theme_settings.json', 'r') as file:
                    theme_settings = json.load(file)
                self.current_theme = theme_settings.get('theme', 'light')
        except Exception as e:
            print(f"Error loading theme preference: {e}")
            self.current_theme = 'light'
    
    def update_chart_themes(self):
        """Update chart background colors to match theme"""
        if self.current_theme == "dark":
            bg_color = '#2b2b2b'
            text_color = 'white'
        else:
            bg_color = 'white'
            text_color = 'black'
        
        # Update pie chart
        if hasattr(self, 'pie_fig'):
            self.pie_fig.patch.set_facecolor(bg_color)
            self.pie_ax.set_facecolor(bg_color)
            self.pie_ax.tick_params(colors=text_color)
            self.pie_ax.title.set_color(text_color)
            self.pie_canvas.draw()
        
        # Update bar chart
        if hasattr(self, 'bar_fig'):
            self.bar_fig.patch.set_facecolor(bg_color)
            self.bar_ax.set_facecolor(bg_color)
            self.bar_ax.tick_params(colors=text_color)
            self.bar_ax.xaxis.label.set_color(text_color)
            self.bar_ax.yaxis.label.set_color(text_color)
            self.bar_ax.title.set_color(text_color)
            self.bar_canvas.draw()
        
        # Update line chart
        if hasattr(self, 'line_fig'):
            self.line_fig.patch.set_facecolor(bg_color)
            self.line_ax.set_facecolor(bg_color)
            self.line_ax.tick_params(colors=text_color)
            self.line_ax.xaxis.label.set_color(text_color)
            self.line_ax.yaxis.label.set_color(text_color)
            self.line_ax.title.set_color(text_color)
            self.line_canvas.draw()


class CategoryManagerWindow:
    """Category Management Window for adding/removing custom categories"""
    
    def __init__(self, parent, budget_tracker, update_callback):
        self.parent = parent
        self.budget_tracker = budget_tracker
        self.update_callback = update_callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Manage Categories")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.refresh_lists()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create the category manager interface"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Category Management", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for Income/Expense tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Income categories tab
        self.income_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.income_frame, text="Income Categories")
        self.create_category_tab(self.income_frame, "Income")
        
        # Expense categories tab
        self.expense_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.expense_frame, text="Expense Categories")
        self.create_category_tab(self.expense_frame, "Expense")
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.close_window)
        close_button.pack(pady=10)
    
    def create_category_tab(self, parent, category_type):
        """Create a category management tab"""
        # Create frames
        top_frame = ttk.Frame(parent, padding="10")
        top_frame.pack(fill="x", pady=(0, 10))
        
        list_frame = ttk.Frame(parent, padding="10")
        list_frame.pack(fill="both", expand=True)
        
        # Add new category section
        ttk.Label(top_frame, text=f"Add New {category_type} Category:").pack(anchor="w", pady=(0, 5))
        
        add_frame = ttk.Frame(top_frame)
        add_frame.pack(fill="x", pady=(0, 10))
        
        # Entry for new category
        entry_var = tk.StringVar()
        if category_type == "Income":
            self.income_entry_var = entry_var
        else:
            self.expense_entry_var = entry_var
        
        entry = ttk.Entry(add_frame, textvariable=entry_var, width=30)
        entry.pack(side="left", padx=(0, 10))
        
        add_button = ttk.Button(add_frame, text="Add Category", 
                               command=lambda: self.add_category(category_type))
        add_button.pack(side="left")
        
        # Bind Enter key
        entry.bind('<Return>', lambda e: self.add_category(category_type))
        
        # Current categories list
        ttk.Label(list_frame, text=f"Current {category_type} Categories:").pack(anchor="w", pady=(0, 5))
        
        # Create listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store references
        if category_type == "Income":
            self.income_listbox = listbox
        else:
            self.expense_listbox = listbox
        
        # Remove button
        remove_button = ttk.Button(list_frame, text="Remove Selected Category", 
                                  command=lambda: self.remove_category(category_type))
        remove_button.pack(pady=(10, 0))
    
    def add_category(self, category_type):
        """Add a new category"""
        if category_type == "Income":
            category_name = self.income_entry_var.get().strip()
            self.income_entry_var.set("")
        else:
            category_name = self.expense_entry_var.get().strip()
            self.expense_entry_var.set("")
        
        if not category_name:
            messagebox.showerror("Error", "Please enter a category name")
            return
        
        success = self.budget_tracker.add_category(category_name, category_type)
        
        if success:
            self.refresh_lists()
            self.update_callback(category_type)  # Update main GUI
            messagebox.showinfo("Success", f"Category '{category_name}' added successfully!")
        else:
            messagebox.showerror("Error", f"Category '{category_name}' already exists")
    
    def remove_category(self, category_type):
        """Remove selected category"""
        if category_type == "Income":
            listbox = self.income_listbox
        else:
            listbox = self.expense_listbox
        
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a category to remove")
            return
        
        category_name = listbox.get(selection[0])
        
        # Check if category is in use
        if self.budget_tracker.is_category_in_use(category_name):
            messagebox.showerror("Error", 
                               f"Cannot remove '{category_name}' because it's being used in transactions")
            return
        
        # Confirm removal
        result = messagebox.askyesno("Confirm", 
                                   f"Are you sure you want to remove '{category_name}'?")
        if result:
            success = self.budget_tracker.remove_category(category_name, category_type)
            if success:
                self.refresh_lists()
                self.update_callback(category_type)  # Update main GUI
                messagebox.showinfo("Success", f"Category '{category_name}' removed successfully!")
            else:
                messagebox.showerror("Error", f"Failed to remove category '{category_name}'")
    
    def refresh_lists(self):
        """Refresh the category lists"""
        # Clear listboxes
        self.income_listbox.delete(0, tk.END)
        self.expense_listbox.delete(0, tk.END)
        
        # Populate income categories
        income_categories = self.budget_tracker.get_categories("Income")
        for category in income_categories:
            self.income_listbox.insert(tk.END, category)
        
        # Populate expense categories
        expense_categories = self.budget_tracker.get_categories("Expense")
        for category in expense_categories:
            self.expense_listbox.insert(tk.END, category)
    
    def close_window(self):
        """Close the category manager window"""
        self.window.destroy()


class BudgetManagerWindow:
    """Budget Management Window for setting spending limits and alerts"""
    
    def __init__(self, parent, budget_tracker, update_callback):
        self.parent = parent
        self.budget_tracker = budget_tracker
        self.update_callback = update_callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Budget Management")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_current_settings()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create the budget manager interface"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Budget Management", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different budget types
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Monthly budget tab
        self.monthly_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monthly_frame, text="Monthly Budget")
        self.create_period_budget_tab(self.monthly_frame, "Monthly")
        
        # Weekly budget tab
        self.weekly_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.weekly_frame, text="Weekly Budget")
        self.create_period_budget_tab(self.weekly_frame, "Weekly")
        
        # Category budgets tab
        self.category_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.category_frame, text="Category Budgets")
        self.create_category_budget_tab(self.category_frame)
        
        # Current status tab
        self.status_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.status_frame, text="Current Status")
        self.create_status_tab(self.status_frame)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        save_button = ttk.Button(button_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        close_button = ttk.Button(button_frame, text="Close", command=self.close_window)
        close_button.pack(side=tk.LEFT)
    
    def create_period_budget_tab(self, parent, period_type):
        """Create monthly or weekly budget tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text=f"Set {period_type} Budget Limit", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Current limit display
        current_frame = ttk.Frame(frame)
        current_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(current_frame, text=f"Current {period_type} Limit:").pack(side=tk.LEFT)
        
        if period_type == "Monthly":
            self.current_monthly_label = ttk.Label(current_frame, text="Not set", 
                                                  font=('Arial', 10, 'bold'))
            self.current_monthly_label.pack(side=tk.RIGHT)
        else:
            self.current_weekly_label = ttk.Label(current_frame, text="Not set", 
                                                 font=('Arial', 10, 'bold'))
            self.current_weekly_label.pack(side=tk.RIGHT)
        
        # New limit input
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(input_frame, text=f"New {period_type} Limit ($):").pack(side=tk.LEFT)
        
        if period_type == "Monthly":
            self.monthly_var = tk.StringVar()
            monthly_entry = ttk.Entry(input_frame, textvariable=self.monthly_var, width=15)
            monthly_entry.pack(side=tk.RIGHT)
        else:
            self.weekly_var = tk.StringVar()
            weekly_entry = ttk.Entry(input_frame, textvariable=self.weekly_var, width=15)
            weekly_entry.pack(side=tk.RIGHT)
        
        # Remove budget button
        if period_type == "Monthly":
            remove_button = ttk.Button(frame, text="Remove Monthly Budget", 
                                     command=lambda: self.remove_period_budget("Monthly"))
        else:
            remove_button = ttk.Button(frame, text="Remove Weekly Budget", 
                                     command=lambda: self.remove_period_budget("Weekly"))
        remove_button.pack(pady=10)
        
        # Information
        info_text = f"""
💡 {period_type} Budget Information:
• Set a spending limit for this {period_type.lower()} period
• Alerts will appear when you reach 80% of the limit
• Critical alerts when you exceed the limit
• All calculations are in USD (converted automatically)
        """
        info_label = ttk.Label(frame, text=info_text, font=('Arial', 9))
        info_label.pack(pady=(20, 0), anchor=tk.W)
    
    def create_category_budget_tab(self, parent):
        """Create category budget management tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text="Category Budget Limits", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Add new category budget
        add_frame = ttk.LabelFrame(frame, text="Add Category Budget", padding="10")
        add_frame.pack(fill="x", pady=(0, 20))
        
        # Category selection
        cat_select_frame = ttk.Frame(add_frame)
        cat_select_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(cat_select_frame, text="Category:").pack(side=tk.LEFT)
        self.category_budget_var = tk.StringVar()
        self.category_budget_combo = ttk.Combobox(cat_select_frame, textvariable=self.category_budget_var, 
                                                 width=25)
        self.category_budget_combo.pack(side=tk.RIGHT)
        
        # Limit input
        limit_frame = ttk.Frame(add_frame)
        limit_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(limit_frame, text="Monthly Limit ($):").pack(side=tk.LEFT)
        self.category_limit_var = tk.StringVar()
        limit_entry = ttk.Entry(limit_frame, textvariable=self.category_limit_var, width=15)
        limit_entry.pack(side=tk.RIGHT)
        
        # Add button
        add_button = ttk.Button(add_frame, text="Add/Update Category Budget", 
                               command=self.add_category_budget)
        add_button.pack(pady=5)
        
        # Current category budgets
        list_frame = ttk.LabelFrame(frame, text="Current Category Budgets", padding="10")
        list_frame.pack(fill="both", expand=True)
        
        # Create treeview for category budgets
        columns = ('Category', 'Limit', 'Spent', 'Remaining')
        self.category_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.category_tree.heading(col, text=col)
            self.category_tree.column(col, width=120)
        
        self.category_tree.pack(fill="both", expand=True, pady=(0, 10))
        
        # Remove category budget button
        remove_cat_button = ttk.Button(list_frame, text="Remove Selected Category Budget", 
                                      command=self.remove_category_budget)
        remove_cat_button.pack()
        
        # Populate category combo
        self.update_category_combo()
    
    def create_status_tab(self, parent):
        """Create current budget status tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text="Current Budget Status", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Status display area
        self.status_display_frame = ttk.Frame(frame)
        self.status_display_frame.pack(fill="both", expand=True)
        
        # Refresh button
        refresh_button = ttk.Button(frame, text="Refresh Status", command=self.update_status_display)
        refresh_button.pack(pady=10)
        
        # Initial status display
        self.update_status_display()
    
    def load_current_settings(self):
        """Load current budget settings into the interface"""
        # Load monthly budget
        if self.budget_tracker.monthly_budget_limit:
            self.current_monthly_label.config(text=f"${self.budget_tracker.monthly_budget_limit:.2f}")
            self.monthly_var.set(str(self.budget_tracker.monthly_budget_limit))
        else:
            self.current_monthly_label.config(text="Not set")
        
        # Load weekly budget
        if self.budget_tracker.weekly_budget_limit:
            self.current_weekly_label.config(text=f"${self.budget_tracker.weekly_budget_limit:.2f}")
            self.weekly_var.set(str(self.budget_tracker.weekly_budget_limit))
        else:
            self.current_weekly_label.config(text="Not set")
        
        # Load category budgets
        self.update_category_budget_list()
    
    def update_category_combo(self):
        """Update category combobox with available expense categories"""
        categories = self.budget_tracker.get_categories("Expense")
        self.category_budget_combo['values'] = tuple(categories)
    
    def update_category_budget_list(self):
        """Update the category budget treeview"""
        # Clear existing items
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        # Get budget status
        budget_status = self.budget_tracker.get_budget_status()
        category_expenses = budget_status['category_expenses']
        category_limits = budget_status['category_limits']
        
        # Add category budgets to tree
        for category, limit in category_limits.items():
            spent = category_expenses.get(category, 0)
            remaining = max(0, limit - spent)
            
            self.category_tree.insert('', 'end', values=(
                category,
                f"${limit:.2f}",
                f"${spent:.2f}",
                f"${remaining:.2f}"
            ))
    
    def add_category_budget(self):
        """Add or update a category budget"""
        category = self.category_budget_var.get().strip()
        limit_str = self.category_limit_var.get().strip()
        
        if not category:
            messagebox.showerror("Error", "Please select a category")
            return
        
        if not limit_str:
            messagebox.showerror("Error", "Please enter a budget limit")
            return
        
        try:
            limit = float(limit_str)
            if limit <= 0:
                raise ValueError("Limit must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for the limit")
            return
        
        self.budget_tracker.set_category_budget(category, limit)
        self.update_category_budget_list()
        self.category_budget_var.set("")
        self.category_limit_var.set("")
        
        messagebox.showinfo("Success", f"Budget limit for '{category}' set to ${limit:.2f}")
    
    def remove_category_budget(self):
        """Remove selected category budget"""
        selection = self.category_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a category budget to remove")
            return
        
        item = selection[0]
        category = self.category_tree.item(item)['values'][0]
        
        result = messagebox.askyesno("Confirm", f"Remove budget limit for '{category}'?")
        if result:
            success = self.budget_tracker.remove_category_budget(category)
            if success:
                self.update_category_budget_list()
                messagebox.showinfo("Success", f"Budget limit for '{category}' removed")
            else:
                messagebox.showerror("Error", f"Failed to remove budget limit for '{category}'")
    
    def remove_period_budget(self, period_type):
        """Remove monthly or weekly budget"""
        result = messagebox.askyesno("Confirm", f"Remove {period_type.lower()} budget limit?")
        if result:
            if period_type == "Monthly":
                self.budget_tracker.monthly_budget_limit = None
                self.current_monthly_label.config(text="Not set")
                self.monthly_var.set("")
            else:
                self.budget_tracker.weekly_budget_limit = None
                self.current_weekly_label.config(text="Not set")
                self.weekly_var.set("")
            
            self.budget_tracker.save_budget_settings()
            messagebox.showinfo("Success", f"{period_type} budget limit removed")
    
    def update_status_display(self):
        """Update the budget status display"""
        # Clear existing widgets
        for widget in self.status_display_frame.winfo_children():
            widget.destroy()
        
        # Get budget status
        budget_status = self.budget_tracker.get_budget_status()
        
        # Monthly status
        if budget_status['monthly_limit']:
            monthly_frame = ttk.LabelFrame(self.status_display_frame, text="Monthly Budget", padding="10")
            monthly_frame.pack(fill="x", pady=5)
            
            spent = budget_status['monthly_spent']
            limit = budget_status['monthly_limit']
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            ttk.Label(monthly_frame, text=f"Spent: ${spent:.2f} of ${limit:.2f} ({percentage:.1f}%)").pack()
            
            if percentage >= 100:
                color = 'red'
                status = "EXCEEDED"
            elif percentage >= 80:
                color = 'orange'
                status = "WARNING"
            else:
                color = 'green'
                status = "OK"
            
            status_label = ttk.Label(monthly_frame, text=f"Status: {status}", foreground=color)
            status_label.pack()
        
        # Weekly status
        if budget_status['weekly_limit']:
            weekly_frame = ttk.LabelFrame(self.status_display_frame, text="Weekly Budget", padding="10")
            weekly_frame.pack(fill="x", pady=5)
            
            spent = budget_status['weekly_spent']
            limit = budget_status['weekly_limit']
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            ttk.Label(weekly_frame, text=f"Spent: ${spent:.2f} of ${limit:.2f} ({percentage:.1f}%)").pack()
            
            if percentage >= 100:
                color = 'red'
                status = "EXCEEDED"
            elif percentage >= 80:
                color = 'orange'
                status = "WARNING"
            else:
                color = 'green'
                status = "OK"
            
            status_label = ttk.Label(weekly_frame, text=f"Status: {status}", foreground=color)
            status_label.pack()
        
        # Category status
        if budget_status['category_limits']:
            cat_frame = ttk.LabelFrame(self.status_display_frame, text="Category Budgets", padding="10")
            cat_frame.pack(fill="both", expand=True, pady=5)
            
            for category, limit in budget_status['category_limits'].items():
                spent = budget_status['category_expenses'].get(category, 0)
                percentage = (spent / limit) * 100 if limit > 0 else 0
                
                cat_detail_frame = ttk.Frame(cat_frame)
                cat_detail_frame.pack(fill="x", pady=2)
                
                ttk.Label(cat_detail_frame, text=f"{category}:").pack(side=tk.LEFT)
                ttk.Label(cat_detail_frame, text=f"${spent:.2f}/${limit:.2f} ({percentage:.1f}%)").pack(side=tk.RIGHT)
        
        # Alerts summary
        alerts = budget_status['alerts']
        if alerts:
            alerts_frame = ttk.LabelFrame(self.status_display_frame, text="Active Alerts", padding="10")
            alerts_frame.pack(fill="x", pady=5)
            
            for alert in alerts:
                icon = "🚨" if alert['severity'] == 'critical' else "⚠️"
                alert_label = ttk.Label(alerts_frame, text=f"{icon} {alert['message']}")
                alert_label.pack(anchor=tk.W)
    
    def save_settings(self):
        """Save budget settings"""
        try:
            # Save monthly budget
            monthly_str = self.monthly_var.get().strip()
            if monthly_str:
                monthly_limit = float(monthly_str)
                if monthly_limit > 0:
                    self.budget_tracker.set_monthly_budget(monthly_limit)
                    self.current_monthly_label.config(text=f"${monthly_limit:.2f}")
            
            # Save weekly budget
            weekly_str = self.weekly_var.get().strip()
            if weekly_str:
                weekly_limit = float(weekly_str)
                if weekly_limit > 0:
                    self.budget_tracker.set_weekly_budget(weekly_limit)
                    self.current_weekly_label.config(text=f"${weekly_limit:.2f}")
            
            messagebox.showinfo("Success", "Budget settings saved successfully!")
            self.update_callback()  # Update alerts in main GUI
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for budget limits")
    
    def close_window(self):
        """Close the budget manager window"""
        self.window.destroy()


def main():
    """Run the Budget Tracker GUI application"""
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
