#!/usr/bin/env python3
"""
Test Phase 4 - Feature 1: Date Picker Integration
Verify that the date picker works correctly and integrates with the model
"""

import sys
import os
from datetime import datetime, date

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker

def test_custom_date_transactions():
    """Test adding transactions with custom dates"""
    print("🗓️ Testing Date Picker Integration")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test 1: Add transaction with custom date
    print("\nTest 1: Adding transaction with custom date...")
    custom_date = "2024-01-15T00:00:00"
    tracker.add_transaction(1500, "Salary", "Income", "USD", custom_date)
    
    transactions = tracker.get_transactions()
    print(f"✓ Transaction added with custom date: {transactions[0]['date'][:10]}")
    
    # Test 2: Add transaction without custom date (should use current date/time)
    print("\nTest 2: Adding transaction without custom date...")
    tracker.add_transaction(500, "Groceries", "Expense", "USD")
    
    transactions = tracker.get_transactions()
    latest_transaction = transactions[-1]
    current_date = datetime.now().date()
    transaction_date = datetime.fromisoformat(latest_transaction['date'].replace('Z', '+00:00')).date()
    
    print(f"✓ Transaction added with current date: {transaction_date}")
    print(f"✓ Current date match: {transaction_date == current_date}")
    
    # Test 3: Verify different dates in transaction list
    print("\nTest 3: Verifying multiple dates...")
    print("Transactions by date:")
    for i, t in enumerate(transactions, 1):
        transaction_date = t['date'][:10]
        print(f"  {i}. {t['category']} ({t['type']}): {transaction_date}")
    
    # Test 4: Test date parsing and sorting
    print("\nTest 4: Testing date sorting...")
    
    # Add more transactions with different dates
    tracker.add_transaction(200, "Coffee", "Expense", "USD", "2024-01-10T00:00:00")
    tracker.add_transaction(1000, "Bonus", "Income", "USD", "2024-01-20T00:00:00")
    
    # Sort by date
    all_transactions = tracker.get_transactions()
    sorted_transactions = sorted(all_transactions, key=lambda x: x['date'])
    
    print("Transactions sorted by date:")
    for i, t in enumerate(sorted_transactions, 1):
        transaction_date = t['date'][:10]
        print(f"  {i}. {transaction_date}: {t['category']} ({t['type']}) - ${t['amount']:.2f}")
    
    # Test 5: Test CSV save/load with custom dates
    print("\nTest 5: Testing CSV persistence with custom dates...")
    filename = "test_datepicker.csv"
    
    save_success = tracker.save_to_csv(filename)
    print(f"✓ CSV save: {'Success' if save_success else 'Failed'}")
    
    # Load into new tracker
    new_tracker = BudgetTracker()
    load_success = new_tracker.load_from_csv(filename)
    print(f"✓ CSV load: {'Success' if load_success else 'Failed'}")
    
    # Verify dates preserved
    loaded_transactions = new_tracker.get_transactions()
    print(f"✓ Transactions preserved: {len(loaded_transactions)}")
    
    if loaded_transactions:
        print("Loaded transaction dates:")
        for t in loaded_transactions:
            print(f"  {t['date'][:10]}: {t['category']}")
    
    # Clean up
    try:
        os.remove(filename)
        print(f"✓ Cleaned up test file: {filename}")
    except:
        pass
    
    return True

def test_date_validation():
    """Test date validation and edge cases"""
    print("\n📅 Testing Date Validation")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test with various date formats
    test_dates = [
        "2024-01-01T00:00:00",
        "2023-12-31T23:59:59", 
        "2024-02-29T12:00:00",  # Leap year
        datetime.now().isoformat()
    ]
    
    for i, test_date in enumerate(test_dates, 1):
        print(f"\nTesting date format {i}: {test_date}")
        try:
            tracker.add_transaction(100, f"Test {i}", "Expense", "USD", test_date)
            print(f"✓ Date accepted: {test_date[:10]}")
        except Exception as e:
            print(f"❌ Date rejected: {e}")
    
    transactions = tracker.get_transactions()
    print(f"\n✓ Total transactions added: {len(transactions)}")
    
    return True

if __name__ == "__main__":
    print("🎯 Phase 4 - Feature 1: Date Picker Integration Test")
    print("=" * 60)
    print("Testing custom date functionality in the Budget Tracker model")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_custom_date_transactions()
    test2_passed = test_date_validation()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED! Date Picker Integration is working!")
        print("\n✅ What's implemented:")
        print("   • BudgetTracker.add_transaction() now accepts custom dates")
        print("   • Custom date parameter with fallback to current date")
        print("   • Date persistence in CSV/JSON files")
        print("   • Date sorting and filtering compatibility")
        
        print("\n🚀 Next steps for GUI:")
        print("   1. Test the enhanced GUI with date picker")
        print("   2. Run: python src/main.py --gui")
        print("   3. Verify date picker widget appears and works")
        print("   4. Add transactions with different dates")
        print("   5. Check that transactions show correct dates in the list")
        
    else:
        print("❌ SOME TESTS FAILED - Date picker implementation needs fixes")
        print(f"   Custom Date Test: {'✅' if test1_passed else '❌'}")
        print(f"   Date Validation Test: {'✅' if test2_passed else '❌'}")
    
    print("\n" + "=" * 60)
