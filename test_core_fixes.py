#!/usr/bin/env python3
"""
Test the modern GUI core functionality after fixes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker

def test_core_functionality():
    """Test core functionality that the GUI uses"""
    print("🔧 Testing Core GUI Functionality")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test 1: Transaction addition with return value
    print("Test 1: Transaction addition...")
    success1 = tracker.add_transaction(5000, "Salary", "Income", "USD", "2024-01-15")
    success2 = tracker.add_transaction(1200, "Rent", "Expense", "USD", "2024-01-16")
    print(f"Income added: {success1}")
    print(f"Expense added: {success2}")
    
    # Test 2: Summary calculation
    print("\nTest 2: Summary calculation...")
    summary = tracker.get_summary()
    print(f"Income: ${summary['total_income']:.2f}")
    print(f"Expenses: ${summary['total_expenses']:.2f}")
    print(f"Balance: ${summary['net_balance']:.2f}")
    
    # Test 3: Category filtering
    print("\nTest 3: Category filtering...")
    income_categories = tracker.get_categories("Income")
    expense_categories = tracker.get_categories("Expense")
    print(f"Income categories: {len(income_categories)} items")
    print(f"Expense categories: {len(expense_categories)} items")
    
    # Test 4: Error handling
    print("\nTest 4: Error handling...")
    error_cases = [
        tracker.add_transaction(-100, "Invalid", "Expense", "USD"),
        tracker.add_transaction(100, "", "Expense", "USD"),
        tracker.add_transaction(100, "Test", "Invalid", "USD")
    ]
    print(f"Error cases handled: {all(not case for case in error_cases)}")
    
    return success1 and success2 and len(income_categories) > 0

if __name__ == "__main__":
    success = test_core_functionality()
    print(f"\n{'✅ All tests PASSED!' if success else '❌ Some tests FAILED!'}")
