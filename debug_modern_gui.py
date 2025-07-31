"""
Debug Modern GUI to see which components are being created
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry

class DebugModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Debug Modern GUI")
        self.root.geometry("1200x800")
        
        # Create basic layout similar to modern GUI
        self.setup_basic_layout()
        
        # Debug panel creation
        self.debug_create_left_panel()
    
    def setup_basic_layout(self):
        """Setup basic layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, text="Budget Tracker Pro - Debug Mode")
        title_label.pack(side='left')
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Configure grid for two panels
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel
        self.left_panel = ttk.Frame(content_frame)
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        
        # Right panel
        self.right_panel = ttk.Frame(content_frame)
        self.right_panel.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        
        print("Basic layout created")
    
    def debug_create_left_panel(self):
        """Debug version of left panel creation"""
        print("Creating left panel components...")
        
        # 1. Summary cards
        print("1. Creating summary cards...")
        self.debug_create_summary_cards()
        
        # 2. Transaction input
        print("2. Creating transaction input...")
        self.debug_create_transaction_input()
        
        # 3. Recent transactions
        print("3. Creating recent transactions...")
        self.debug_create_recent_transactions()
        
        # 4. Quick actions
        print("4. Creating quick actions...")
        self.debug_create_quick_actions()
        
        print("Left panel creation complete!")
    
    def debug_create_summary_cards(self):
        """Debug summary cards"""
        cards_frame = ttk.Frame(self.left_panel)
        cards_frame.pack(fill='x', pady=(0, 16))
        
        # Income card
        income_card = ttk.LabelFrame(cards_frame, text="Total Income")
        income_card.pack(fill='x', pady=(0, 8))
        
        income_label = ttk.Label(income_card, text="$0.00")
        income_label.pack(padx=16, pady=8)
        
        # Expenses card
        expenses_card = ttk.LabelFrame(cards_frame, text="Total Expenses")
        expenses_card.pack(fill='x', pady=(0, 8))
        
        expenses_label = ttk.Label(expenses_card, text="$0.00")
        expenses_label.pack(padx=16, pady=8)
        
        # Balance card
        balance_card = ttk.LabelFrame(cards_frame, text="Net Balance")
        balance_card.pack(fill='x')
        
        balance_label = ttk.Label(balance_card, text="$0.00")
        balance_label.pack(padx=16, pady=8)
        
        print("   Summary cards created successfully")
    
    def debug_create_transaction_input(self):
        """Debug transaction input"""
        input_card = ttk.LabelFrame(self.left_panel, text="Add New Transaction")
        input_card.pack(fill='x', pady=(0, 16))
        
        # Form content
        form_content = ttk.Frame(input_card)
        form_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Configure grid
        form_content.columnconfigure(1, weight=1)
        
        # Date input
        ttk.Label(form_content, text="Date:").grid(
            row=0, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        try:
            self.date_entry = DateEntry(form_content, width=16, background='darkblue',
                                       foreground='white', borderwidth=1, 
                                       date_pattern='yyyy-mm-dd')
            self.date_entry.grid(row=0, column=1, sticky='ew', pady=(0, 8))
            print("   DateEntry created successfully")
        except Exception as e:
            print(f"   DateEntry error: {e}")
            # Fallback to regular entry
            self.date_entry = ttk.Entry(form_content)
            self.date_entry.grid(row=0, column=1, sticky='ew', pady=(0, 8))
        
        # Amount input
        ttk.Label(form_content, text="Amount:").grid(
            row=1, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(form_content, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=1, sticky='ew', pady=(0, 8))
        
        # Category input
        ttk.Label(form_content, text="Category:").grid(
            row=2, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_content, textvariable=self.category_var)
        self.category_combo['values'] = ['Food', 'Transport', 'Entertainment']
        self.category_combo.grid(row=2, column=1, sticky='ew', pady=(0, 8))
        
        # Type selection
        ttk.Label(form_content, text="Type:").grid(
            row=3, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.type_var = tk.StringVar(value="Expense")
        type_combo = ttk.Combobox(form_content, textvariable=self.type_var,
                                values=['Income', 'Expense'], state='readonly')
        type_combo.grid(row=3, column=1, sticky='ew', pady=(0, 8))
        
        # Action buttons
        button_frame = ttk.Frame(form_content)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(8, 0), sticky='ew')
        
        add_btn = ttk.Button(button_frame, text="Add Transaction")
        add_btn.pack(side='right')
        
        print("   Transaction input created successfully")
    
    def debug_create_recent_transactions(self):
        """Debug recent transactions"""
        transactions_card = ttk.LabelFrame(self.left_panel, text="Recent Transactions")
        transactions_card.pack(fill='both', expand=True, pady=(0, 16))
        
        # Simple list content
        list_content = ttk.Frame(transactions_card)
        list_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Simple listbox for now
        listbox = tk.Listbox(list_content, height=6)
        listbox.pack(fill='both', expand=True)
        
        # Add some sample items
        for i in range(5):
            listbox.insert(tk.END, f"Sample Transaction {i+1}")
        
        print("   Recent transactions created successfully")
    
    def debug_create_quick_actions(self):
        """Debug quick actions"""
        actions_card = ttk.LabelFrame(self.left_panel, text="Quick Actions")
        actions_card.pack(fill='x')
        
        # Actions content
        actions_content = ttk.Frame(actions_card)
        actions_content.pack(fill='x', padx=16, pady=16)
        
        # Simple buttons
        save_btn = ttk.Button(actions_content, text="Save CSV")
        save_btn.pack(side='left', padx=(0, 8))
        
        load_btn = ttk.Button(actions_content, text="Load CSV")
        load_btn.pack(side='left', padx=(0, 8))
        
        budget_btn = ttk.Button(actions_content, text="Set Budgets")
        budget_btn.pack(side='left', padx=(0, 8))
        
        print("   Quick actions created successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = DebugModernGUI(root)
    root.mainloop()
