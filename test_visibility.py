#!/usr/bin/env python3
"""
Test the transaction list visibility issue in modern GUI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import tkinter as tk
from modern_gui_app import ModernBudgetTrackerGUI

def test_transaction_visibility():
    """Test if transactions show up in the list"""
    
    print("🧪 Testing Transaction List Visibility")
    print("=" * 50)
    
    # Create GUI
    root = tk.Tk()
    app = ModernBudgetTrackerGUI(root)
    
    # Add some test transactions
    print("Adding test transactions...")
    success1 = app.budget_tracker.add_transaction(25000, "Monthly Salary", "Income", "USD")
    success2 = app.budget_tracker.add_transaction(1200, "Rent", "Expense", "USD")
    success3 = app.budget_tracker.add_transaction(300, "Groceries", "Expense", "USD")
    
    print(f"Transaction 1 added: {success1}")
    print(f"Transaction 2 added: {success2}")
    print(f"Transaction 3 added: {success3}")
    
    # Refresh the display
    print("Refreshing display...")
    app.refresh_all_data()
    
    # Check if transactions are in the tree
    total_transactions = len(app.budget_tracker.get_transactions())
    tree_items = len(app.tree.get_children())
    
    print(f"Total transactions in tracker: {total_transactions}")
    print(f"Items in tree widget: {tree_items}")
    
    # List the actual transactions
    transactions = app.budget_tracker.get_transactions()
    print("\nTransactions in tracker:")
    for i, t in enumerate(transactions, 1):
        print(f"  {i}. {t['type']}: {t['category']} - ${t['amount']:.2f}")
    
    # List the tree items
    tree_children = app.tree.get_children()
    if tree_children:
        print("\nTree items found:")
        for item in tree_children:
            values = app.tree.item(item)['values']
            print(f"  {values}")
    else:
        print("\n❌ No items found in tree widget")
    
    # Check tree configuration
    print(f"\nTree configuration:")
    print(f"  Style: {app.tree.cget('style')}")
    print(f"  Columns: {app.tree.cget('columns')}")
    print(f"  Height: {app.tree.cget('height')}")
    
    # Check if update_transaction_list method exists and works
    try:
        app.update_transaction_list()
        print("✅ update_transaction_list() executed successfully")
    except Exception as e:
        print(f"❌ update_transaction_list() failed: {e}")
    
    # Check filter state
    print(f"Filter state: {app.filter_var.get()}")
    
    print("\n🖥️ Opening GUI window...")
    print("Check if transactions appear in the 'Recent Transactions' section")
    print("Close the window to end the test")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    test_transaction_visibility()
