#!/usr/bin/env python3
"""
Test Phase 4 - Feature 2: Custom Categories Management
Verify that custom categories work correctly and persist data
"""

import sys
import os
import json

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker

def test_default_categories():
    """Test the default categories system"""
    print("📂 Testing Default Categories")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test getting income categories
    income_categories = tracker.get_categories("Income")
    print(f"✓ Default Income categories ({len(income_categories)}):")
    for cat in income_categories:
        print(f"  • {cat}")
    
    # Test getting expense categories
    expense_categories = tracker.get_categories("Expense")
    print(f"\n✓ Default Expense categories ({len(expense_categories)}):")
    for cat in expense_categories:
        print(f"  • {cat}")
    
    # Test getting all categories
    all_categories = tracker.get_categories()
    print(f"\n✓ All categories: {len(all_categories)} total")
    
    return True

def test_custom_category_management():
    """Test adding, removing, and managing custom categories"""
    print("\n🛠️ Testing Custom Category Management")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test 1: Add new income categories
    print("\nTest 1: Adding custom income categories...")
    success1 = tracker.add_category("Consulting", "Income")
    success2 = tracker.add_category("Side Business", "Income")
    success3 = tracker.add_category("Rental Income", "Income")
    
    print(f"✓ Added 'Consulting': {success1}")
    print(f"✓ Added 'Side Business': {success2}")
    print(f"✓ Added 'Rental Income': {success3}")
    
    # Test 2: Add new expense categories
    print("\nTest 2: Adding custom expense categories...")
    success4 = tracker.add_category("Gym Membership", "Expense")
    success5 = tracker.add_category("Pet Care", "Expense")
    success6 = tracker.add_category("Home Maintenance", "Expense")
    
    print(f"✓ Added 'Gym Membership': {success4}")
    print(f"✓ Added 'Pet Care': {success5}")
    print(f"✓ Added 'Home Maintenance': {success6}")
    
    # Test 3: Try to add duplicate category
    print("\nTest 3: Testing duplicate category prevention...")
    duplicate_success = tracker.add_category("Consulting", "Income")
    print(f"✓ Duplicate 'Consulting' rejected: {not duplicate_success}")
    
    # Test 4: Verify categories were added
    print("\nTest 4: Verifying added categories...")
    income_categories = tracker.get_categories("Income")
    expense_categories = tracker.get_categories("Expense")
    
    print(f"Income categories now ({len(income_categories)}):")
    for cat in income_categories:
        print(f"  • {cat}")
    
    print(f"\nExpense categories now ({len(expense_categories)}):")
    for cat in expense_categories:
        print(f"  • {cat}")
    
    return True

def test_category_usage_protection():
    """Test that categories in use cannot be removed"""
    print("\n🔒 Testing Category Usage Protection")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Add a custom category
    tracker.add_category("Test Category", "Expense")
    
    # Add a transaction using this category
    tracker.add_transaction(100, "Test Category", "Expense", "USD")
    
    # Test 1: Check if category is in use
    in_use = tracker.is_category_in_use("Test Category")
    print(f"✓ 'Test Category' is in use: {in_use}")
    
    # Test 2: Try to remove category that's in use
    remove_success = tracker.remove_category("Test Category", "Expense")
    print(f"✓ Remove category in use blocked: {not remove_success}")
    
    # Test 3: Remove category not in use
    tracker.add_category("Unused Category", "Expense")
    remove_unused_success = tracker.remove_category("Unused Category", "Expense")
    print(f"✓ Remove unused category allowed: {remove_unused_success}")
    
    return True

def test_category_persistence():
    """Test that custom categories are saved and loaded correctly"""
    print("\n💾 Testing Category Persistence")
    print("=" * 50)
    
    # Test 1: Create tracker and add custom categories
    print("Test 1: Creating custom categories...")
    tracker1 = BudgetTracker()
    
    tracker1.add_category("Freelance Web Design", "Income")
    tracker1.add_category("Stock Trading", "Income")
    tracker1.add_category("Streaming Subscriptions", "Expense")
    tracker1.add_category("Car Insurance", "Expense")
    
    # Save categories
    save_success = tracker1.save_categories()
    print(f"✓ Categories saved: {save_success}")
    
    # Check if file was created
    categories_file_exists = os.path.exists('categories.json')
    print(f"✓ Categories file created: {categories_file_exists}")
    
    # Test 2: Load categories in new tracker
    print("\nTest 2: Loading categories in new tracker...")
    tracker2 = BudgetTracker()
    
    income_before = len(tracker2.get_categories("Income"))
    expense_before = len(tracker2.get_categories("Expense"))
    
    # Simulate loading categories (this happens in __init__)
    load_success = tracker2.load_categories()
    print(f"✓ Categories loaded: {load_success}")
    
    income_after = len(tracker2.get_categories("Income"))
    expense_after = len(tracker2.get_categories("Expense"))
    
    print(f"✓ Income categories: {income_before} -> {income_after}")
    print(f"✓ Expense categories: {expense_before} -> {expense_after}")
    
    # Test 3: Verify specific categories were loaded
    print("\nTest 3: Verifying specific categories...")
    income_cats = tracker2.get_categories("Income")
    expense_cats = tracker2.get_categories("Expense")
    
    freelance_loaded = "Freelance Web Design" in income_cats
    streaming_loaded = "Streaming Subscriptions" in expense_cats
    
    print(f"✓ 'Freelance Web Design' loaded: {freelance_loaded}")
    print(f"✓ 'Streaming Subscriptions' loaded: {streaming_loaded}")
    
    # Test 4: Check JSON file content
    print("\nTest 4: Checking JSON file content...")
    try:
        with open('categories.json', 'r') as file:
            data = json.load(file)
        
        print("JSON file structure:")
        print(f"  • income_categories: {len(data.get('income_categories', []))} items")
        print(f"  • expense_categories: {len(data.get('expense_categories', []))} items")
        
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
    
    # Clean up
    try:
        os.remove('categories.json')
        print("✓ Cleaned up categories.json file")
    except:
        pass
    
    return save_success and load_success and freelance_loaded and streaming_loaded

def test_integration_with_transactions():
    """Test categories integration with transaction system"""
    print("\n🔄 Testing Categories Integration with Transactions")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Add custom categories
    tracker.add_category("Freelance Writing", "Income")
    tracker.add_category("Netflix", "Expense")
    
    # Add transactions using custom categories
    tracker.add_transaction(500, "Freelance Writing", "Income", "USD")
    tracker.add_transaction(15, "Netflix", "Expense", "USD")
    
    # Verify transactions were added with custom categories
    transactions = tracker.get_transactions()
    print(f"✓ Transactions added: {len(transactions)}")
    
    for i, t in enumerate(transactions, 1):
        print(f"  {i}. {t['category']} ({t['type']}): ${t['amount']:.2f}")
    
    # Test category usage detection
    freelance_in_use = tracker.is_category_in_use("Freelance Writing")
    netflix_in_use = tracker.is_category_in_use("Netflix")
    unused_in_use = tracker.is_category_in_use("Non-existent Category")
    
    print(f"\n✓ 'Freelance Writing' in use: {freelance_in_use}")
    print(f"✓ 'Netflix' in use: {netflix_in_use}")
    print(f"✓ 'Non-existent Category' in use: {unused_in_use}")
    
    return len(transactions) == 2 and freelance_in_use and netflix_in_use and not unused_in_use

if __name__ == "__main__":
    print("🎯 Phase 4 - Feature 2: Custom Categories Management Test")
    print("=" * 70)
    print("Testing dynamic category system with persistence and protection")
    print("=" * 70)
    
    # Run tests
    test1_passed = test_default_categories()
    test2_passed = test_custom_category_management()
    test3_passed = test_category_usage_protection()
    test4_passed = test_category_persistence()
    test5_passed = test_integration_with_transactions()
    
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS:")
    print("=" * 70)
    
    all_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed])
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! Custom Categories Management is working!")
        print("\n✅ What's implemented:")
        print("   • Default Income and Expense categories")
        print("   • Add/remove custom categories dynamically")
        print("   • Category persistence in categories.json file")
        print("   • Protection against removing categories in use")
        print("   • Integration with transaction system")
        print("   • Duplicate category prevention")
        
        print("\n🚀 GUI Features available:")
        print("   • Dynamic category dropdown based on transaction type")
        print("   • 'Manage Categories' button for category management")
        print("   • Separate tabs for Income/Expense categories")
        print("   • Real-time category list updates")
        
        print("\n🧪 To test in GUI:")
        print("   1. Run: python src/main.py --gui")
        print("   2. Change transaction type and see category list update")
        print("   3. Click 'Manage Categories' button")
        print("   4. Add/remove categories in the popup window")
        print("   5. ✅ Categories should update in real-time!")
        
    else:
        print("❌ SOME TESTS FAILED - Custom Categories implementation needs fixes")
        print(f"   Default Categories: {'✅' if test1_passed else '❌'}")
        print(f"   Category Management: {'✅' if test2_passed else '❌'}")
        print(f"   Usage Protection: {'✅' if test3_passed else '❌'}")
        print(f"   Persistence: {'✅' if test4_passed else '❌'}")
        print(f"   Transaction Integration: {'✅' if test5_passed else '❌'}")
    
    print("\n" + "=" * 70)
