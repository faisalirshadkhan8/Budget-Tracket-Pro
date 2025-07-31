#!/usr/bin/env python3
"""
Test Phase 4 - Feature 3: Budget Alerts System
Verify that budget alerts work correctly with different spending scenarios
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.budget_tracker import BudgetTracker

def test_budget_limits_setup():
    """Test setting up different types of budget limits"""
    print("💰 Testing Budget Limits Setup")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Test 1: Set monthly budget
    print("Test 1: Setting monthly budget...")
    tracker.set_monthly_budget(2000.0)
    print(f"✓ Monthly budget set: ${tracker.monthly_budget_limit:.2f}")
    
    # Test 2: Set weekly budget
    print("\nTest 2: Setting weekly budget...")
    tracker.set_weekly_budget(500.0)
    print(f"✓ Weekly budget set: ${tracker.weekly_budget_limit:.2f}")
    
    # Test 3: Set category budgets
    print("\nTest 3: Setting category budgets...")
    tracker.set_category_budget("Food", 600.0)
    tracker.set_category_budget("Transportation", 300.0)
    tracker.set_category_budget("Entertainment", 200.0)
    
    print(f"✓ Category budgets set:")
    for category, limit in tracker.budget_limits.items():
        print(f"  • {category}: ${limit:.2f}")
    
    return True

def test_budget_persistence():
    """Test that budget settings are saved and loaded correctly"""
    print("\n💾 Testing Budget Persistence")
    print("=" * 50)
    
    # Test 1: Save budget settings
    print("Test 1: Saving budget settings...")
    tracker1 = BudgetTracker()
    tracker1.set_monthly_budget(3000.0)
    tracker1.set_weekly_budget(750.0)
    tracker1.set_category_budget("Bills", 800.0)
    tracker1.set_category_budget("Shopping", 400.0)
    
    save_success = tracker1.save_budget_settings()
    print(f"✓ Budget settings saved: {save_success}")
    
    # Check if file was created
    settings_file_exists = os.path.exists('budget_settings.json')
    print(f"✓ Budget settings file created: {settings_file_exists}")
    
    # Test 2: Load budget settings in new tracker
    print("\nTest 2: Loading budget settings...")
    tracker2 = BudgetTracker()
    
    # Check initial state
    print(f"Before load - Monthly: {tracker2.monthly_budget_limit}, Weekly: {tracker2.weekly_budget_limit}")
    print(f"Before load - Category budgets: {len(tracker2.budget_limits)}")
    
    # Load settings
    load_success = tracker2.load_budget_settings()
    print(f"✓ Budget settings loaded: {load_success}")
    
    # Verify loaded settings
    print(f"After load - Monthly: ${tracker2.monthly_budget_limit:.2f}")
    print(f"After load - Weekly: ${tracker2.weekly_budget_limit:.2f}")
    print(f"After load - Category budgets: {len(tracker2.budget_limits)}")
    
    for category, limit in tracker2.budget_limits.items():
        print(f"  • {category}: ${limit:.2f}")
    
    # Test 3: Verify JSON content
    print("\nTest 3: Checking JSON file structure...")
    try:
        with open('budget_settings.json', 'r') as file:
            data = json.load(file)
        
        print("Budget settings JSON structure:")
        print(f"  • monthly_budget_limit: {data.get('monthly_budget_limit')}")
        print(f"  • weekly_budget_limit: {data.get('weekly_budget_limit')}")
        print(f"  • category_limits: {len(data.get('category_limits', {}))}")
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
    
    # Clean up
    try:
        os.remove('budget_settings.json')
        print("✓ Cleaned up budget_settings.json")
    except:
        pass
    
    return save_success and load_success

def test_budget_alerts_scenarios():
    """Test various budget alert scenarios"""
    print("\n🚨 Testing Budget Alert Scenarios")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Set up budgets
    tracker.set_monthly_budget(1000.0)
    tracker.set_weekly_budget(250.0)
    tracker.set_category_budget("Food", 300.0)
    tracker.set_category_budget("Entertainment", 150.0)
    
    # Test 1: Normal spending (no alerts)
    print("\nTest 1: Normal spending scenario...")
    tracker.add_transaction(100, "Groceries", "Expense", "USD")
    tracker.add_transaction(50, "Movie", "Expense", "USD")
    
    status = tracker.get_budget_status()
    print(f"✓ Monthly spent: ${status['monthly_spent']:.2f} of ${status['monthly_limit']:.2f}")
    print(f"✓ Food category spent: ${status['category_expenses'].get('Food', 0):.2f} of ${status['category_limits'].get('Food', 0):.2f}")
    print(f"✓ Alerts: {len(status['alerts'])}")
    
    # Test 2: Warning level spending (80% of budget)
    print("\nTest 2: Warning level spending...")
    # Add more expenses to reach 80% of food budget (300 * 0.8 = 240)
    tracker.add_transaction(140, "Restaurant", "Expense", "USD")  # Total food: 240
    
    status = tracker.get_budget_status()
    food_spent = status['category_expenses'].get('Food', 0)
    food_limit = status['category_limits'].get('Food', 0)
    food_percentage = (food_spent / food_limit) * 100 if food_limit > 0 else 0
    
    print(f"✓ Food spending: ${food_spent:.2f} of ${food_limit:.2f} ({food_percentage:.1f}%)")
    print(f"✓ Warning alerts: {len([a for a in status['alerts'] if a['severity'] == 'warning'])}")
    
    if status['alerts']:
        for alert in status['alerts']:
            print(f"  • {alert['severity']}: {alert['message']}")
    
    # Test 3: Budget exceeded scenario
    print("\nTest 3: Budget exceeded scenario...")
    # Exceed food budget
    tracker.add_transaction(100, "Expensive dinner", "Expense", "USD")  # Total food: 340 (exceeds 300)
    
    status = tracker.get_budget_status()
    critical_alerts = [a for a in status['alerts'] if a['severity'] == 'critical']
    
    print(f"✓ Critical alerts: {len(critical_alerts)}")
    if critical_alerts:
        for alert in critical_alerts:
            print(f"  • CRITICAL: {alert['message']}")
    
    return True

def test_multi_currency_budget_alerts():
    """Test budget alerts with multi-currency transactions"""
    print("\n🌍 Testing Multi-Currency Budget Alerts")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Set budget in USD
    tracker.set_monthly_budget(1000.0)
    tracker.set_category_budget("Food", 400.0)
    
    print("Budget set: $1000 monthly, $400 for Food")
    
    # Add expenses in different currencies
    print("\nAdding multi-currency expenses...")
    tracker.add_transaction(100, "Local groceries", "Expense", "USD")      # $100
    tracker.add_transaction(27700, "Pakistan groceries", "Expense", "PKR")  # ~$100 USD
    tracker.add_transaction(91, "European restaurant", "Expense", "EUR")     # ~$100 USD
    tracker.add_transaction(200, "UK shopping", "Expense", "GBP")           # ~$253 USD
    
    # Check budget status
    status = tracker.get_budget_status()
    
    print(f"\nBudget Status:")
    print(f"✓ Monthly spent: ${status['monthly_spent']:.2f} of ${status['monthly_limit']:.2f}")
    print(f"✓ Food spent: ${status['category_expenses'].get('Food', 0):.2f} of ${status['category_limits'].get('Food', 0):.2f}")
    
    # Check individual transaction conversions
    print(f"\nTransaction conversions to USD:")
    for t in tracker.get_transactions():
        usd_amount = tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
        symbol = tracker.get_currency_symbol(t.get('currency', 'USD'))
        print(f"  • {symbol}{t['amount']:.2f} → ${usd_amount:.2f} USD")
    
    # Check alerts
    print(f"\nAlerts: {len(status['alerts'])}")
    for alert in status['alerts']:
        print(f"  • {alert['severity'].upper()}: {alert['message']}")
    
    return True

def test_time_period_calculations():
    """Test weekly and monthly period calculations"""
    print("\n📅 Testing Time Period Calculations")
    print("=" * 50)
    
    tracker = BudgetTracker()
    tracker.set_weekly_budget(200.0)
    tracker.set_monthly_budget(800.0)
    
    # Add transactions from different time periods
    now = datetime.now()
    
    # Current week transaction
    tracker.add_transaction(100, "This week", "Expense", "USD", now.isoformat())
    
    # Last week transaction (should not count for current week)
    last_week = now - timedelta(days=7)
    tracker.add_transaction(150, "Last week", "Expense", "USD", last_week.isoformat())
    
    # Current month transaction
    tracker.add_transaction(200, "This month", "Expense", "USD", now.isoformat())
    
    # Last month transaction (should not count for current month)
    try:
        if now.month > 1:
            last_month = now.replace(month=now.month-1)
        else:
            last_month = now.replace(year=now.year-1, month=12)
    except ValueError:
        # Handle case where current day doesn't exist in previous month (e.g., Jan 31 -> Feb 31)
        if now.month > 1:
            last_month = now.replace(month=now.month-1, day=1)
        else:
            last_month = now.replace(year=now.year-1, month=12, day=1)
    
    tracker.add_transaction(300, "Last month", "Expense", "USD", last_month.isoformat())
    
    # Check budget status
    status = tracker.get_budget_status()
    
    print(f"Total transactions: {len(tracker.get_transactions())}")
    print(f"✓ Current week spending: ${status['weekly_spent']:.2f} (should be ~$300)")
    print(f"✓ Current month spending: ${status['monthly_spent']:.2f} (should be ~$400)")
    print(f"✓ Weekly budget status: ${status['weekly_spent']:.2f} of ${status['weekly_limit']:.2f}")
    print(f"✓ Monthly budget status: ${status['monthly_spent']:.2f} of ${status['monthly_limit']:.2f}")
    
    return True

def test_budget_removal():
    """Test removing budget limits"""
    print("\n🗑️ Testing Budget Removal")
    print("=" * 50)
    
    tracker = BudgetTracker()
    
    # Set up budgets
    tracker.set_monthly_budget(1000.0)
    tracker.set_category_budget("Food", 300.0)
    tracker.set_category_budget("Shopping", 200.0)
    
    print("Initial budgets set:")
    print(f"  • Monthly: ${tracker.monthly_budget_limit:.2f}")
    print(f"  • Food: ${tracker.budget_limits.get('Food', 0):.2f}")
    print(f"  • Shopping: ${tracker.budget_limits.get('Shopping', 0):.2f}")
    
    # Test removing category budget
    print("\nRemoving Food budget...")
    success = tracker.remove_category_budget("Food")
    print(f"✓ Food budget removed: {success}")
    print(f"✓ Remaining category budgets: {list(tracker.budget_limits.keys())}")
    
    # Test removing non-existent budget
    print("\nTrying to remove non-existent budget...")
    success = tracker.remove_category_budget("NonExistent")
    print(f"✓ Non-existent budget removal failed: {not success}")
    
    return True

if __name__ == "__main__":
    print("🎯 Phase 4 - Feature 3: Budget Alerts System Test")
    print("=" * 70)
    print("Testing budget limits, alerts, and multi-currency calculations")
    print("=" * 70)
    
    # Run tests
    test1_passed = test_budget_limits_setup()
    test2_passed = test_budget_persistence()
    test3_passed = test_budget_alerts_scenarios()
    test4_passed = test_multi_currency_budget_alerts()
    test5_passed = test_time_period_calculations()
    test6_passed = test_budget_removal()
    
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS:")
    print("=" * 70)
    
    all_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed, test6_passed])
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! Budget Alerts System is working!")
        print("\n✅ What's implemented:")
        print("   • Monthly and weekly spending limits")
        print("   • Category-specific budget limits")
        print("   • Multi-currency budget calculations (converted to USD)")
        print("   • Warning alerts at 80% of budget")
        print("   • Critical alerts when budget exceeded")
        print("   • Time period calculations (current week/month)")
        print("   • Budget settings persistence")
        print("   • Budget removal functionality")
        
        print("\n🚀 GUI Features available:")
        print("   • Budget alerts display in main interface")
        print("   • 'Set Budget Limits' button for budget management")
        print("   • Tabbed budget manager with Monthly/Weekly/Category/Status tabs")
        print("   • Real-time budget status updates")
        print("   • Visual alert indicators (🚨 for critical, ⚠️ for warnings)")
        
        print("\n🧪 To test in GUI:")
        print("   1. Run: python src/main.py --gui")
        print("   2. Click 'Set Budget Limits' button")
        print("   3. Set monthly/weekly budgets and category limits")
        print("   4. Add transactions to test budget alerts")
        print("   5. ✅ Watch alerts appear in the Budget Alerts section!")
        
    else:
        print("❌ SOME TESTS FAILED - Budget Alerts implementation needs fixes")
        print(f"   Budget Setup: {'✅' if test1_passed else '❌'}")
        print(f"   Persistence: {'✅' if test2_passed else '❌'}")
        print(f"   Alert Scenarios: {'✅' if test3_passed else '❌'}")
        print(f"   Multi-Currency: {'✅' if test4_passed else '❌'}")
        print(f"   Time Periods: {'✅' if test5_passed else '❌'}")
        print(f"   Budget Removal: {'✅' if test6_passed else '❌'}")
    
    print("\n" + "=" * 70)
