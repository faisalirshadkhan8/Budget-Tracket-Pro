"""
Test just the transaction input form to debug visibility issues
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class TestTransactionForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Transaction Form")
        self.root.geometry("600x400")
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Test the transaction input form
        self.create_test_transaction_input(main_frame)
    
    def create_test_transaction_input(self, parent):
        """Create transaction input form for testing"""
        input_card = ttk.LabelFrame(parent, text="Add New Transaction")
        input_card.pack(fill='x', pady=(0, 16))
        
        # Form content
        form_content = ttk.Frame(input_card)
        form_content.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Configure grid
        form_content.columnconfigure(1, weight=1)
        
        # Date input
        ttk.Label(form_content, text="Date:").grid(
            row=0, column=0, sticky='w', pady=(0, 8), padx=(0, 8))
        
        self.date_entry = DateEntry(form_content, width=16, background='darkblue',
                                   foreground='white', borderwidth=1, 
                                   date_pattern='yyyy-mm-dd')
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
        self.category_combo['values'] = ['Food', 'Transport', 'Entertainment', 'Bills']
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
        
        print("Transaction form created successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TestTransactionForm(root)
    root.mainloop()
