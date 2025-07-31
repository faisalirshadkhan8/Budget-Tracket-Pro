"""
Budget Tracker CLI Interface - Phase 1
Command line interface for the budget tracker
"""

import argparse
import sys
import os

# Add src directory to Python path for imports
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.budget_tracker import BudgetTracker


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='Budget Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add transaction command
    add_parser = subparsers.add_parser('add', help='Add a new transaction')
    add_parser.add_argument('amount', type=float, help='Transaction amount')
    add_parser.add_argument('category', help='Transaction category')
    add_parser.add_argument('--type', choices=['Income', 'Expense'], default='Expense',
                          help='Transaction type (default: Expense)')
    add_parser.add_argument('--currency', default='USD',
                          help='Currency code (default: USD)')

    # View transactions command
    view_parser = subparsers.add_parser('view', help='View transactions')
    view_parser.add_argument('--category', help='Filter by category')
    view_parser.add_argument('--type', choices=['Income', 'Expense'], help='Filter by type')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show financial summary')

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all transactions')

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # Initialize budget tracker
    tracker = BudgetTracker()

    if args.command == 'add':
        tracker.add_transaction(args.amount, args.category, args.type, args.currency)
        currency_symbol = tracker.get_currency_symbol(args.currency)
        print(f"✓ Added {args.type.lower()}: {currency_symbol}{args.amount:.2f} in {args.category}")
        
        # Show updated summary
        summary = tracker.get_summary()
        primary_currency = tracker.get_primary_currency()
        primary_symbol = tracker.get_currency_symbol(primary_currency)
        print(f"Current balance: {primary_symbol}{summary['net_balance']:.2f}")

    elif args.command == 'view':
        transactions = tracker.get_transactions()
        
        # Apply filters
        if args.category:
            transactions = [t for t in transactions if t['category'].lower() == args.category.lower()]
        if args.type:
            transactions = [t for t in transactions if t['type'] == args.type]
        
        if not transactions:
            print("No transactions found.")
            return
        
        print(f"\n{'Date':<12} {'Type':<8} {'Category':<15} {'Amount':<10}")
        print("-" * 50)
        
        for transaction in transactions:
            date_str = transaction['date'][:10]
            currency = transaction.get('currency', 'USD')
            currency_symbol = tracker.get_currency_symbol(currency)
            amount_str = f"{currency_symbol}{transaction['amount']:.2f}"
            print(f"{date_str:<12} {transaction['type']:<8} {transaction['category']:<15} {amount_str:<10}")
        
        total = sum(t['amount'] for t in transactions)
        # Use primary currency for total
        primary_currency = tracker.get_primary_currency()
        primary_symbol = tracker.get_currency_symbol(primary_currency)
        print("-" * 50)
        print(f"Total: {primary_symbol}{total:.2f}")

    elif args.command == 'summary':
        summary = tracker.get_summary()
        primary_currency = tracker.get_primary_currency()
        currency_symbol = tracker.get_currency_symbol(primary_currency)
        
        print("\n📊 Financial Summary")
        print("=" * 25)
        print(f"Total Income:  {currency_symbol}{summary['total_income']:.2f}")
        print(f"Total Expenses: {currency_symbol}{summary['total_expenses']:.2f}")
        print(f"Net Balance:   {currency_symbol}{summary['net_balance']:.2f}")
        
        if summary['net_balance'] > 0:
            print("💰 You're in the positive!")
        elif summary['net_balance'] < 0:
            print("⚠️  You're spending more than you earn")
        else:
            print("⚖️  You're breaking even")

    elif args.command == 'clear':
        tracker.clear_all_transactions()
        print("✓ All transactions cleared")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()