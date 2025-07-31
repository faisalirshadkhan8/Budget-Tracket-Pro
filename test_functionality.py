#!/usr/bin/env python3
"""
Test specific functionality that might be failing in the modern GUI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker

def test_budget_tracker_methods():
    """Test all BudgetTracker methods used by GUI"""
    print("🧪 Testing BudgetTracker Methods")
    print("=" * 40)
    
    tracker = BudgetTracker()
    
    # Test 1: Basic transaction operations
    print("Test 1: Basic operations...")
    try:
        tracker.add_transaction(1000, "Test Income", "Income", "USD")
        tracker.add_transaction(500, "Test Expense", "Expense", "USD")
        print("✅ add_transaction works")
    except Exception as e:
        print(f"❌ add_transaction failed: {e}")
    
    # Test 2: Get transactions
    try:
        transactions = tracker.get_transactions()
        print(f"✅ get_transactions works: {len(transactions)} transactions")
    except Exception as e:
        print(f"❌ get_transactions failed: {e}")
    
    # Test 3: Get summary
    try:
        summary = tracker.get_summary()
        print(f"✅ get_summary works: Balance ${summary['net_balance']:.2f}")
    except Exception as e:
        print(f"❌ get_summary failed: {e}")
    
    # Test 4: Get categories (both versions)
    try:
        categories_all = tracker.get_categories()
        print(f"✅ get_categories() works: {categories_all}")
    except Exception as e:
        print(f"❌ get_categories() failed: {e}")
    
    try:
        categories_income = tracker.get_categories("Income")
        print(f"✅ get_categories('Income') works: {categories_income}")
    except Exception as e:
        print(f"❌ get_categories('Income') failed: {e}")
    
    try:
        categories_expense = tracker.get_categories("Expense")
        print(f"✅ get_categories('Expense') works: {categories_expense}")
    except Exception as e:
        print(f"❌ get_categories('Expense') failed: {e}")
    
    # Test 5: Check if get_categories_by_type exists
    try:
        if hasattr(tracker, 'get_categories_by_type'):
            categories_by_type = tracker.get_categories_by_type("Expense")
            print(f"✅ get_categories_by_type works: {categories_by_type}")
        else:
            print("ℹ️ get_categories_by_type method does not exist")
    except Exception as e:
        print(f"❌ get_categories_by_type failed: {e}")
    
    # Test 6: CSV operations
    try:
        success = tracker.save_to_csv("test_save.csv")
        print(f"✅ save_to_csv works: {success}")
        if os.path.exists("test_save.csv"):
            os.remove("test_save.csv")
    except Exception as e:
        print(f"❌ save_to_csv failed: {e}")
    
    # Test 7: Currency operations
    try:
        symbol = tracker.get_currency_symbol("USD")
        print(f"✅ get_currency_symbol works: {symbol}")
    except Exception as e:
        print(f"❌ get_currency_symbol failed: {e}")
    
    try:
        usd_amount = tracker.convert_to_usd(100, "EUR")
        print(f"✅ convert_to_usd works: €100 = ${usd_amount:.2f}")
    except Exception as e:
        print(f"❌ convert_to_usd failed: {e}")

def test_gui_missing_methods():
    """Test for methods that GUI might be expecting but are missing"""
    print("\n🔍 Testing for Missing GUI Methods")
    print("=" * 40)
    
    tracker = BudgetTracker()
    
    # Methods that modern GUI might be calling
    expected_methods = [
        'add_transaction',
        'get_transactions', 
        'get_summary',
        'get_categories',
        'save_to_csv',
        'load_from_csv',
        'get_currency_symbol',
        'convert_to_usd',
        'get_categories_by_type',  # This might be missing
        'sort_column',             # This might be missing
        'update_transaction_list', # This might be missing
        'open_category_manager',   # This might be missing
        'open_budget_manager',     # This might be missing
        'export_report',           # This might be missing
    ]
    
    for method_name in expected_methods:
        if hasattr(tracker, method_name):
            print(f"✅ {method_name} exists")
        else:
            print(f"❌ {method_name} MISSING")

if __name__ == "__main__":
    test_budget_tracker_methods()
    test_gui_missing_methods()
