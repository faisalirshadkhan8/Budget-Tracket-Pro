"""
Modern Budget Tracker GUI Application - Production Ready Design
A professional, modern interface suitable for live deployment
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


class ModernBudgetTrackerGUI:
    """Modern, professional Budget Tracker GUI with production-ready design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker Pro")
        
        # Set up window
        self.setup_window()
        
        # Initialize the budget tracker
        self.budget_tracker = BudgetTracker()
        
        # Theme management
        self.current_theme = "light"
        self.load_theme_preference()
        
        # Color schemes
        self.setup_color_schemes()
        
        # Configure modern styles
        self.setup_modern_styles()
        
        # Create the modern interface
        self.create_modern_interface()
        
        # Load initial data
        self.refresh_all_data()
    
    def setup_window(self):
        """Configure the main window with modern settings"""
        # Set minimum size and center window
        self.root.minsize(1400, 900)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1400
        window_height = 900
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure window
        self.root.configure(bg='#f8fafc')
        
        # Make window resizable
        self.root.resizable(True, True)
    
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
            },
            'dark': {
                'primary': '#3b82f6',      # Bright blue
                'secondary': '#94a3b8',    # Light slate
                'success': '#34d399',      # Light green
                'warning': '#fbbf24',      # Light amber
                'danger': '#f87171',       # Light red
                'background': '#1e293b',   # Dark blue-gray
                'surface': '#0f172a',      # Very dark
                'border': '#334155',       # Dark border
                'text_primary': '#f1f5f9', # Light text
                'text_secondary': '#cbd5e1', # Light gray text
                'accent': '#60a5fa',       # Light blue
            }
        }
    
    def get_color(self, color_name):
        """Get color from current theme"""
        return self.colors[self.current_theme][color_name]
    
    def setup_modern_styles(self):
        """Configure modern ttk styles"""
        self.style = ttk.Style()
        
        # Apply theme
        self.apply_modern_theme()
    
    def apply_modern_theme(self):
        """Apply modern theme styling"""
        if self.current_theme == "light":
            self.apply_light_modern_theme()
        else:
            self.apply_dark_modern_theme()
    
    def apply_light_modern_theme(self):
        """Apply modern light theme with simplified styling"""
        self.style.theme_use('clam')
        
        # Root window
        self.root.configure(bg='#f8fafc')
        
        # Modern button styles - simplified
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           padding=(12, 6))
        
        # Secondary button style
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           padding=(10, 5))
        
        # Success button style
        self.style.configure('Success.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           padding=(10, 5))
        
        # Danger button style
        self.style.configure('Danger.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           padding=(10, 5))
        
        # Modern label styles - simplified
        self.style.configure('Heading.TLabel',
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 14, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12, 'normal'))
        
        self.style.configure('Body.TLabel',
                           font=('Segoe UI', 10, 'normal'))
        
        # Value labels with colors - simplified
        self.style.configure('Success.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground='#10b981')
        
        self.style.configure('Danger.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground='#ef4444')
        
        self.style.configure('Primary.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground='#2563eb')
        
        # Modern treeview styles - simplified for visibility
        self.style.configure('Modern.Treeview',
                           font=('Segoe UI', 9, 'normal'),
                           background='white',
                           foreground='black',
                           fieldbackground='white',
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 9, 'bold'),
                           background='#f8fafc',
                           foreground='black',
                           relief='flat',
                           borderwidth=1)
        
        # LabelFrame styles
        self.style.configure('Modern.TLabelFrame',
                           background=self.get_color('background'),
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.TLabelFrame.Label',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'))
    
    def apply_dark_modern_theme(self):
        """Apply modern dark theme"""
        self.style.theme_use('alt')
        
        # Root window
        self.root.configure(bg=self.get_color('surface'))
        
        # Modern button styles for dark theme
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           borderwidth=1,
                           relief='flat',
                           background=self.get_color('primary'),
                           foreground='white',
                           padding=(16, 8))
        
        self.style.map('Modern.TButton',
                      background=[('active', '#1d4ed8'),
                                ('pressed', '#1e40af')])
        
        # Secondary button style
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           borderwidth=1,
                           relief='flat',
                           background=self.get_color('secondary'),
                           foreground='white',
                           padding=(12, 6))
        
        # Success button style
        self.style.configure('Success.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           borderwidth=1,
                           relief='flat',
                           background=self.get_color('success'),
                           foreground='black',
                           padding=(12, 6))
        
        # Danger button style
        self.style.configure('Danger.TButton',
                           font=('Segoe UI', 9, 'normal'),
                           borderwidth=1,
                           relief='flat',
                           background=self.get_color('danger'),
                           foreground='white',
                           padding=(12, 6))
        
        # Frame styles
        self.style.configure('Card.TFrame',
                           background=self.get_color('background'),
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Surface.TFrame',
                           background=self.get_color('surface'),
                           borderwidth=0)
        
        # Label styles for dark theme
        self.style.configure('Heading.TLabel',
                           font=('Segoe UI', 18, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'))
        
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'))
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12, 'normal'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_secondary'))
        
        self.style.configure('Body.TLabel',
                           font=('Segoe UI', 10, 'normal'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'))
        
        # Value labels with colors
        self.style.configure('Success.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('success'))
        
        self.style.configure('Danger.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('danger'))
        
        # Entry and Combobox styles
        self.style.configure('Modern.TEntry',
                           font=('Segoe UI', 10, 'normal'),
                           borderwidth=1,
                           relief='solid',
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'),
                           insertcolor=self.get_color('primary'),
                           padding=(8, 6))
        
        self.style.configure('Modern.TCombobox',
                           font=('Segoe UI', 10, 'normal'),
                           borderwidth=1,
                           relief='solid',
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'),
                           padding=(8, 6))
        
        # Treeview styles
        self.style.configure('Modern.Treeview',
                           font=('Segoe UI', 9, 'normal'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'),
                           fieldbackground=self.get_color('background'),
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 9, 'bold'),
                           background=self.get_color('surface'),
                           foreground=self.get_color('text_primary'),
                           relief='flat',
                           borderwidth=1)
        
        # LabelFrame styles
        self.style.configure('Modern.TLabelFrame',
                           background=self.get_color('background'),
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.TLabelFrame.Label',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.get_color('background'),
                           foreground=self.get_color('text_primary'))
    
    def create_modern_interface(self):
        """Create the modern interface layout"""
        # Main container
        self.main_container = ttk.Frame(self.root, style='Surface.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Create header
        self.create_modern_header()
        
        # Create main content area
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()
    
    def create_modern_header(self):
        """Create modern header with branding and controls"""
        header_frame = ttk.Frame(self.main_container, style='Card.TFrame')
        header_frame.pack(fill='x', padx=16, pady=(16, 0))
        
        # Header content
        header_content = ttk.Frame(header_frame, style='Card.TFrame')
        header_content.pack(fill='x', padx=24, pady=16)
        
        # Left side - App branding
        left_frame = ttk.Frame(header_content, style='Card.TFrame')
        left_frame.pack(side='left', fill='y')
        
        # App title and subtitle
        app_title = ttk.Label(left_frame, text="Budget Tracker Pro", style='Heading.TLabel')
        app_title.pack(anchor='w')
        
        subtitle = ttk.Label(left_frame, text="Professional Financial Management", style='Subtitle.TLabel')
        subtitle.pack(anchor='w')
        
        # Right side - Controls
        right_frame = ttk.Frame(header_content, style='Card.TFrame')
        right_frame.pack(side='right', fill='y')
        
        # Theme toggle button
        theme_text = "🌙 Dark" if self.current_theme == "light" else "☀️ Light"
        self.theme_toggle_btn = ttk.Button(right_frame, text=theme_text, 
                                          command=self.toggle_theme,
                                          style='Secondary.TButton')
        self.theme_toggle_btn.pack(side='right', padx=(8, 0))
        
        # Current date/time
        current_time = datetime.now().strftime("%B %d, %Y")
        time_label = ttk.Label(right_frame, text=current_time, style='Body.TLabel')
        time_label.pack(side='right', padx=(0, 16))
    
    def create_content_area(self):
        """Create main content area with modern layout"""
        content_frame = ttk.Frame(self.main_container, style='Surface.TFrame')
        content_frame.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Configure grid
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - Controls and Summary
        self.left_panel = ttk.Frame(content_frame, style='Surface.TFrame')
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        
        # Right panel - Analytics
        self.right_panel = ttk.Frame(content_frame, style='Surface.TFrame')
        self.right_panel.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        
        # Create left panel content
        self.create_left_panel()
        
        # Create right panel content
        self.create_right_panel()
    
    def create_left_panel(self):
        """Create left panel with transaction input and summary"""
        # Quick stats cards
        self.create_summary_cards()
        
        # Transaction input section
        self.create_modern_transaction_input()
        
        # Recent transactions
        self.create_recent_transactions()
        
        # Quick actions
        self.create_quick_actions()
    
    def create_summary_cards(self):
        """Create modern summary cards"""
        cards_frame = ttk.Frame(self.left_panel)
        cards_frame.pack(fill='x', pady=(0, 16))
        
        # Income card
        income_card = self.create_stat_card(cards_frame, "Total Income", "$0.00", "success")
        income_card.pack(fill='x', pady=(0, 8))
        
        # Expenses card
        expenses_card = self.create_stat_card(cards_frame, "Total Expenses", "$0.00", "danger")
        expenses_card.pack(fill='x', pady=(0, 8))
        
        # Balance card
        balance_card = self.create_stat_card(cards_frame, "Net Balance", "$0.00", "primary")
        balance_card.pack(fill='x')
    
    def create_stat_card(self, parent, title, value, color_type):
        """Create a modern stat card"""
        card = ttk.LabelFrame(parent, text=title)
        
        # Card content
        content = ttk.Frame(card)
        content.pack(fill='both', expand=True, padx=16, pady=12)
        
        # Value
        style_name = f'{color_type.title()}.TLabel'
        value_label = ttk.Label(content, text=value, style=style_name)
        value_label.pack(anchor='w')
        
        # Store reference for updates
        if title == "Total Income":
            self.income_value_label = value_label
        elif title == "Total Expenses":
            self.expenses_value_label = value_label
        elif title == "Net Balance":
            self.balance_value_label = value_label
        
        return card
    
    def create_modern_transaction_input(self):
        """Create modern transaction input form"""
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
        
        # Currency selection
        ttk.Label(form_content, text="Currency:", style='Body.TLabel').grid(
            row=4, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.currency_var = tk.StringVar(value="USD ($)")
        currency_combo = ttk.Combobox(form_content, textvariable=self.currency_var,
                                    values=['USD ($)', 'EUR (€)', 'GBP (£)', 'JPY (¥)', 
                                           'CAD (C$)', 'AUD (A$)', 'CHF (₣)', 'CNY (¥)', 
                                           'INR (₹)', 'BRL (R$)', 'PKR (₨)'],
                                    state='readonly')
        currency_combo.grid(row=4, column=1, sticky='ew', pady=(0, 8))
        
        # Action buttons
        button_frame = ttk.Frame(form_content)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(8, 0), sticky='ew')
        
        add_btn = ttk.Button(button_frame, text="Add Transaction", 
                           command=self.add_transaction, style='Modern.TButton')
        add_btn.pack(side='right')
        
        manage_categories_btn = ttk.Button(button_frame, text="Manage Categories", 
                                         command=self.open_category_manager, 
                                         style='Secondary.TButton')
        manage_categories_btn.pack(side='right', padx=(0, 8))
        
        # Initialize categories
        self.update_category_list("Expense")
    
    def create_recent_transactions(self):
        """Create recent transactions list"""
        transactions_card = ttk.LabelFrame(self.left_panel, text="Recent Transactions")
        transactions_card.pack(fill='both', expand=True, pady=(0, 16))
        
        # Transaction list content
        list_content = ttk.Frame(transactions_card)
        list_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Filter controls
        filter_frame = ttk.Frame(list_content)
        filter_frame.pack(fill='x', pady=(0, 8))
        
        ttk.Label(filter_frame, text="Filter:", style='Body.TLabel').pack(side='left')
        
        self.filter_var = tk.StringVar(value="All")
        filter_all = ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, 
                                   value="All", command=self.update_transaction_list)
        filter_all.pack(side='left', padx=(8, 4))
        
        filter_income = ttk.Radiobutton(filter_frame, text="Income", variable=self.filter_var, 
                                      value="Income", command=self.update_transaction_list)
        filter_income.pack(side='left', padx=4)
        
        filter_expense = ttk.Radiobutton(filter_frame, text="Expenses", variable=self.filter_var, 
                                       value="Expense", command=self.update_transaction_list)
        filter_expense.pack(side='left', padx=4)
        
        # Transaction table
        columns = ('Date', 'Type', 'Category', 'Amount', 'Currency')
        self.tree = ttk.Treeview(list_content, columns=columns, show='headings',
                               height=8, style='Modern.Treeview')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            
        self.tree.column('Date', width=80)
        self.tree.column('Type', width=60)
        self.tree.column('Category', width=100)
        self.tree.column('Amount', width=80)
        self.tree.column('Currency', width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_content, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initialize sorting
        self.sort_reverse = False
        self.last_sort_column = None
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_card = ttk.LabelFrame(self.left_panel, text="Quick Actions")
        actions_card.pack(fill='x')
        
        # Actions content
        actions_content = ttk.Frame(actions_card)
        actions_content.pack(fill='x', padx=16, pady=16)
        
        # Configure grid
        actions_content.columnconfigure((0, 1), weight=1)
        
        # Data management buttons
        save_csv_btn = ttk.Button(actions_content, text="Save CSV", 
                                command=self.save_to_csv, style='Secondary.TButton')
        save_csv_btn.grid(row=0, column=0, sticky='ew', padx=(0, 4), pady=(0, 4))
        
        load_csv_btn = ttk.Button(actions_content, text="Load CSV", 
                                command=self.load_from_csv, style='Secondary.TButton')
        load_csv_btn.grid(row=0, column=1, sticky='ew', padx=(4, 0), pady=(0, 4))
        
        budget_btn = ttk.Button(actions_content, text="Set Budgets", 
                              command=self.open_budget_manager, style='Secondary.TButton')
        budget_btn.grid(row=1, column=0, sticky='ew', padx=(0, 4))
        
        export_btn = ttk.Button(actions_content, text="Export Report", 
                              command=self.export_report, style='Success.TButton')
        export_btn.grid(row=1, column=1, sticky='ew', padx=(4, 0))
    
    def create_right_panel(self):
        """Create right panel with analytics and charts"""
        # Charts section
        charts_card = ttk.LabelFrame(self.right_panel, text="Financial Analytics")
        charts_card.pack(fill='both', expand=True)
        
        # Charts content
        charts_content = ttk.Frame(charts_card)
        charts_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Create notebook for charts
        self.charts_notebook = ttk.Notebook(charts_content)
        self.charts_notebook.pack(fill='both', expand=True)
        
        # Chart tabs
        self.create_modern_charts()
        
        # Budget alerts section
        self.create_budget_alerts_section()
    
    def create_modern_charts(self):
        """Create modern styled charts"""
        # Pie Chart Tab
        self.pie_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.pie_frame, text="Expenses Breakdown")
        
        # Bar Chart Tab
        self.bar_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.bar_frame, text="Income vs Expenses")
        
        # Trend Chart Tab
        self.trend_frame = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.trend_frame, text="Balance Trend")
        
        # Setup charts with modern styling
        self.setup_modern_pie_chart()
        self.setup_modern_bar_chart()
        self.setup_modern_trend_chart()
    
    def setup_modern_pie_chart(self):
        """Setup modern pie chart"""
        # Create figure with modern styling
        self.pie_fig = Figure(figsize=(8, 6), dpi=100, facecolor=self.get_color('background'))
        self.pie_ax = self.pie_fig.add_subplot(111, facecolor=self.get_color('background'))
        
        # Create canvas
        self.pie_canvas = FigureCanvasTkAgg(self.pie_fig, self.pie_frame)
        self.pie_canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)
        
        self.update_pie_chart()
    
    def setup_modern_bar_chart(self):
        """Setup modern bar chart"""
        self.bar_fig = Figure(figsize=(8, 6), dpi=100, facecolor=self.get_color('background'))
        self.bar_ax = self.bar_fig.add_subplot(111, facecolor=self.get_color('background'))
        
        self.bar_canvas = FigureCanvasTkAgg(self.bar_fig, self.bar_frame)
        self.bar_canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)
        
        self.update_bar_chart()
    
    def setup_modern_trend_chart(self):
        """Setup modern trend chart"""
        self.trend_fig = Figure(figsize=(8, 6), dpi=100, facecolor=self.get_color('background'))
        self.trend_ax = self.trend_fig.add_subplot(111, facecolor=self.get_color('background'))
        
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, self.trend_frame)
        self.trend_canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)
        
        self.update_trend_chart()
    
    def create_budget_alerts_section(self):
        """Create modern budget alerts section"""
        alerts_card = ttk.LabelFrame(self.right_panel, text="Budget Alerts")
        alerts_card.pack(fill='x', pady=(16, 0))
        
        # Alerts content
        self.alerts_content = ttk.Frame(alerts_card)
        self.alerts_content.pack(fill='x', padx=16, pady=16)
        
        # Initial empty state
        self.no_alerts_label = ttk.Label(self.alerts_content, 
                                       text="No budget alerts at this time", 
                                       style='Subtitle.TLabel')
        self.no_alerts_label.pack()
    
    def create_status_bar(self):
        """Create modern status bar"""
        status_frame = ttk.Frame(self.main_container, style='Surface.TFrame')
        status_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        # Status content
        status_content = ttk.Frame(status_frame, style='Card.TFrame')
        status_content.pack(fill='x', padx=0, pady=8)
        
        # Status text
        self.status_text = ttk.Label(status_content, text="Ready", style='Body.TLabel')
        self.status_text.pack(side='left', padx=16)
        
        # Transaction count
        self.transaction_count_label = ttk.Label(status_content, text="0 transactions", 
                                               style='Body.TLabel')
        self.transaction_count_label.pack(side='right', padx=16)
    
    # Core functionality methods (adapted from original GUI)
    
    def add_transaction(self):
        """Add a new transaction with modern validation"""
        # Get values
        amount_str = self.amount_var.get().strip()
        category = self.category_var.get().strip()
        transaction_type = self.type_var.get()
        currency_full = self.currency_var.get()
        
        # Get date and convert to string
        try:
            selected_date = self.date_entry.get_date()
            date_str = selected_date.strftime("%Y-%m-%d")
        except Exception:
            # Fallback to string format
            date_str = self.date_entry.get()
        
        # Extract currency code
        currency = currency_full.split(' ')[0] if currency_full else "USD"
        
        # Validate inputs
        if not amount_str:
            messagebox.showerror("Input Error", "Please enter an amount")
            return
        
        if not category:
            messagebox.showerror("Input Error", "Please enter a category")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive amount")
            return
        
        # Add transaction
        success = self.budget_tracker.add_transaction(
            amount, category, transaction_type, currency, date_str
        )
        
        if success:
            # Clear form
            self.amount_var.set("")
            self.category_var.set("")
            
            # Refresh all data
            self.refresh_all_data()
            
            # Update status
            self.status_text.config(text=f"Added {transaction_type.lower()}: {category} - ${amount:.2f}")
        else:
            messagebox.showerror("Error", "Failed to add transaction")
    
    def refresh_all_data(self):
        """Refresh all GUI components with current data"""
        self.update_summary_cards()
        self.update_transaction_list()
        self.update_all_charts()
        self.update_transaction_count()
        self.update_budget_alerts()
    
    def update_summary_cards(self):
        """Update summary cards with current data"""
        summary = self.budget_tracker.get_summary()
        
        # Update card values
        self.income_value_label.config(text=f"${summary['total_income']:.2f}")
        self.expenses_value_label.config(text=f"${summary['total_expenses']:.2f}")
        
        balance = summary['net_balance']
        self.balance_value_label.config(text=f"${balance:.2f}")
        
        # Update balance color
        if balance > 0:
            style_name = 'Success.TLabel'
        elif balance < 0:
            style_name = 'Danger.TLabel'
        else:
            style_name = 'Body.TLabel'
        
        self.balance_value_label.config(style=style_name)
    
    def update_transaction_list(self):
        """Update transaction list with current filter"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered transactions
        transactions = self.get_filtered_transactions()
        
        # Sort if needed
        if self.last_sort_column:
            transactions = self.sort_transactions(transactions)
        
        # Populate tree
        for transaction in transactions:
            values = (
                transaction['date'][:10],  # Date only
                transaction['type'],
                transaction['category'],
                f"${transaction['amount']:.2f}",
                transaction.get('currency', 'USD')
            )
            
            # Color code based on type
            tags = ('income',) if transaction['type'] == 'Income' else ('expense',)
            self.tree.insert('', 'end', values=values, tags=tags)
        
        # Configure tag colors with explicit colors for visibility
        if self.current_theme == 'light':
            self.tree.tag_configure('income', foreground='#10b981')  # Green
            self.tree.tag_configure('expense', foreground='#ef4444')  # Red
        else:
            self.tree.tag_configure('income', foreground='#34d399')  # Light green
            self.tree.tag_configure('expense', foreground='#f87171')  # Light red
            
        # Ensure tree has proper styling for visibility
        self.tree.configure(
            style='Heading.Treeview' if hasattr(self.style, 'Heading.Treeview') else 'Treeview'
        )
    
    def update_all_charts(self):
        """Update all charts"""
        self.update_pie_chart()
        self.update_bar_chart()
        self.update_trend_chart()
    
    def update_pie_chart(self):
        """Update pie chart with modern styling"""
        self.pie_ax.clear()
        
        # Get expense data
        transactions = self.budget_tracker.get_transactions_by_type("Expense")
        
        if not transactions:
            self.pie_ax.text(0.5, 0.5, 'No expense data available', 
                           horizontalalignment='center', verticalalignment='center',
                           transform=self.pie_ax.transAxes, fontsize=12,
                           color=self.get_color('text_secondary'))
            self.pie_ax.set_title("Expenses by Category", fontsize=14, fontweight='bold',
                                color=self.get_color('text_primary'))
        else:
            # Group by category
            category_totals = {}
            for transaction in transactions:
                category = transaction['category']
                amount = self.budget_tracker.convert_to_usd(
                    transaction['amount'], transaction.get('currency', 'USD')
                )
                category_totals[category] = category_totals.get(category, 0) + amount
            
            # Create modern color palette
            colors = [self.get_color('primary'), self.get_color('secondary'), 
                     self.get_color('success'), self.get_color('warning'), 
                     self.get_color('danger'), self.get_color('accent')]
            
            # Extend colors if needed
            while len(colors) < len(category_totals):
                colors.extend(colors[:3])
            
            # Create pie chart
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            
            wedges, texts, autotexts = self.pie_ax.pie(
                amounts, labels=categories, autopct='%1.1f%%', 
                colors=colors[:len(categories)], startangle=90,
                textprops={'color': self.get_color('text_primary')}
            )
            
            # Style text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
                autotext.set_fontsize(9)
            
            self.pie_ax.set_title("Expenses by Category", fontsize=14, fontweight='bold',
                                color=self.get_color('text_primary'))
        
        # Apply theme styling
        self.pie_fig.patch.set_facecolor(self.get_color('background'))
        self.pie_ax.set_facecolor(self.get_color('background'))
        
        # Refresh canvas
        self.pie_canvas.draw()
    
    def update_bar_chart(self):
        """Update bar chart with modern styling"""
        self.bar_ax.clear()
        
        # Get summary data
        summary = self.budget_tracker.get_summary()
        
        # Data for bar chart
        categories = ['Income', 'Expenses']
        values = [summary['total_income'], summary['total_expenses']]
        colors = [self.get_color('success'), self.get_color('danger')]
        
        # Create bar chart
        bars = self.bar_ax.bar(categories, values, color=colors, alpha=0.8, width=0.6)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            self.bar_ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                           f'${value:.2f}',
                           ha='center', va='bottom', fontweight='bold',
                           color=self.get_color('text_primary'))
        
        # Styling
        self.bar_ax.set_title("Income vs Expenses", fontsize=14, fontweight='bold',
                            color=self.get_color('text_primary'))
        self.bar_ax.set_ylabel("Amount (USD)", fontsize=12, color=self.get_color('text_primary'))
        
        # Set limits
        max_value = max(max(values) * 1.1, 100)
        self.bar_ax.set_ylim(0, max_value)
        
        # Grid and styling
        self.bar_ax.grid(True, alpha=0.3, axis='y', color=self.get_color('border'))
        self.bar_ax.tick_params(colors=self.get_color('text_primary'))
        
        # Apply theme
        self.bar_fig.patch.set_facecolor(self.get_color('background'))
        self.bar_ax.set_facecolor(self.get_color('background'))
        
        self.bar_canvas.draw()
    
    def update_trend_chart(self):
        """Update trend chart with modern styling"""
        self.trend_ax.clear()
        
        transactions = self.budget_tracker.get_transactions()
        
        if not transactions:
            self.trend_ax.text(0.5, 0.5, 'No transaction data available', 
                             horizontalalignment='center', verticalalignment='center',
                             transform=self.trend_ax.transAxes, fontsize=12,
                             color=self.get_color('text_secondary'))
            self.trend_ax.set_title("Balance Trend Over Time", fontsize=14, fontweight='bold',
                                  color=self.get_color('text_primary'))
        else:
            # Sort transactions by date
            sorted_transactions = sorted(transactions, key=lambda x: x['date'])
            
            # Calculate running balance
            dates = []
            balances = []
            running_balance = 0
            
            for transaction in sorted_transactions:
                # Convert to USD
                amount_usd = self.budget_tracker.convert_to_usd(
                    transaction['amount'], transaction.get('currency', 'USD')
                )
                
                if transaction['type'] == 'Income':
                    running_balance += amount_usd
                else:
                    running_balance -= amount_usd
                
                # Convert date
                date_obj = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
                dates.append(date_obj)
                balances.append(running_balance)
            
            # Plot with modern styling
            self.trend_ax.plot(dates, balances, marker='o', linewidth=3, markersize=6,
                             color=self.get_color('primary'), markerfacecolor=self.get_color('accent'))
            
            # Color areas
            self.trend_ax.fill_between(dates, balances, alpha=0.2, color=self.get_color('primary'))
            
            # Zero line
            self.trend_ax.axhline(y=0, color=self.get_color('text_secondary'), 
                                linestyle='--', alpha=0.5)
            
            # Styling
            self.trend_ax.set_title("Balance Trend Over Time", fontsize=14, fontweight='bold',
                                  color=self.get_color('text_primary'))
            self.trend_ax.set_ylabel("Balance (USD)", fontsize=12, color=self.get_color('text_primary'))
            self.trend_ax.set_xlabel("Date", fontsize=12, color=self.get_color('text_primary'))
            
            # Grid and ticks
            self.trend_ax.grid(True, alpha=0.3, color=self.get_color('border'))
            self.trend_ax.tick_params(colors=self.get_color('text_primary'), axis='x', rotation=45)
            self.trend_ax.tick_params(colors=self.get_color('text_primary'), axis='y')
        
        # Apply theme
        self.trend_fig.patch.set_facecolor(self.get_color('background'))
        self.trend_ax.set_facecolor(self.get_color('background'))
        
        # Tight layout
        self.trend_fig.tight_layout()
        
        self.trend_canvas.draw()
    
    def update_transaction_count(self):
        """Update transaction count in status bar"""
        count = len(self.budget_tracker.get_transactions())
        self.transaction_count_label.config(text=f"{count} transactions")
    
    def update_budget_alerts(self):
        """Update budget alerts display"""
        # Clear existing alerts
        for widget in self.alerts_content.winfo_children():
            widget.destroy()
        
        # Get budget status
        budget_status = self.budget_tracker.get_budget_status()
        alerts = budget_status.get('alerts', [])
        
        if not alerts:
            self.no_alerts_label = ttk.Label(self.alerts_content, 
                                           text="No budget alerts at this time", 
                                           style='Subtitle.TLabel')
            self.no_alerts_label.pack()
        else:
            for alert in alerts:
                alert_frame = ttk.Frame(self.alerts_content, style='Card.TFrame')
                alert_frame.pack(fill='x', pady=2)
                
                # Alert icon and message
                icon = "🚨" if alert['severity'] == 'critical' else "⚠️"
                alert_text = f"{icon} {alert['message']}"
                
                alert_label = ttk.Label(alert_frame, text=alert_text, style='Body.TLabel')
                alert_label.pack(anchor='w', padx=8, pady=4)
    
    # Utility methods
    
    def get_filtered_transactions(self):
        """Get filtered transactions based on current filter"""
        transactions = self.budget_tracker.get_transactions()
        
        filter_type = self.filter_var.get()
        if filter_type == "All":
            return transactions
        else:
            return [t for t in transactions if t['type'] == filter_type]
    
    def sort_transactions(self, transactions):
        """Sort transactions by specified column"""
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
            return ''
        
        return sorted(transactions, key=get_sort_key, reverse=self.sort_reverse)
    
    def sort_column(self, column):
        """Sort by column and update display"""
        if self.last_sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.last_sort_column = column
        self.update_transaction_list()
    
    def update_category_list(self, transaction_type):
        """Update category combobox for transaction type"""
        try:
            categories = self.budget_tracker.get_categories(transaction_type)
            self.category_combo['values'] = tuple(categories)
            self.category_var.set("")
        except Exception as e:
            print(f"Error updating categories: {e}")
            # Fallback to default categories
            if transaction_type == "Income":
                default_categories = ['Salary', 'Freelance', 'Business', 'Investment', 'Other Income']
            else:
                default_categories = ['Food', 'Transportation', 'Entertainment', 'Bills', 'Shopping', 'Other Expense']
            self.category_combo['values'] = tuple(default_categories)
    
    def on_type_changed(self, event=None):
        """Handle transaction type change"""
        selected_type = self.type_var.get()
        self.update_category_list(selected_type)
    
    # Theme management
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_toggle_btn.config(text="☀️ Light")
        else:
            self.current_theme = "light"
            self.theme_toggle_btn.config(text="🌙 Dark")
        
        # Apply new theme
        self.apply_modern_theme()
        
        # Update charts
        self.update_all_charts()
        
        # Save theme preference
        self.save_theme_preference()
        
        # Show notification
        self.status_text.config(text=f"Switched to {self.current_theme} theme")
    
    def save_theme_preference(self):
        """Save theme preference to file"""
        try:
            import json
            with open('theme_settings.json', 'w') as f:
                json.dump({'theme': self.current_theme}, f)
        except:
            pass  # Ignore errors
    
    def load_theme_preference(self):
        """Load theme preference from file"""
        try:
            import json
            with open('theme_settings.json', 'r') as f:
                settings = json.load(f)
                self.current_theme = settings.get('theme', 'light')
        except:
            self.current_theme = 'light'  # Default to light theme
    
    # File operations (adapted from original)
    
    def save_to_csv(self):
        """Save transactions to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Transactions as CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.save_to_csv(filename)
                if success:
                    self.status_text.config(text=f"Saved to {filename}")
                    messagebox.showinfo("Success", f"Transactions saved to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to save CSV file")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def load_from_csv(self):
        """Load transactions from CSV"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Transactions from CSV",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                success = self.budget_tracker.load_from_csv(filename)
                
                if success:
                    self.refresh_all_data()
                    self.status_text.config(text=f"Loaded from {filename}")
                    messagebox.showinfo("Success", f"Transactions loaded from {filename}")
                else:
                    messagebox.showerror("Error", "Failed to load CSV file")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def open_category_manager(self):
        """Open category management window"""
        try:
            # Import from original GUI app
            from gui_app import CategoryManagerWindow
            CategoryManagerWindow(self.root, self.budget_tracker, self.update_category_list)
        except ImportError:
            messagebox.showinfo("Category Manager", "Category management feature will be available in the next update!")
    
    def open_budget_manager(self):
        """Open budget management window"""
        try:
            # Import from original GUI app
            from gui_app import BudgetManagerWindow
            BudgetManagerWindow(self.root, self.budget_tracker, self.update_budget_alerts)
        except ImportError:
            messagebox.showinfo("Budget Manager", "Budget management feature will be available in the next update!")
    
    def export_report(self):
        """Export detailed report (placeholder for Phase 5)"""
        messagebox.showinfo("Export Report", "Export functionality will be available in Phase 5!")


def main():
    """Run the Modern Budget Tracker GUI"""
    root = tk.Tk()
    app = ModernBudgetTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
