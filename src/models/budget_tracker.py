"""
Budget Tracker Model - Phase 3: Transaction History & Data Persistence
Handles transaction management, storage in memory, and file persistence
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class BudgetTracker:
    def __init__(self):
        """Initialize the budget tracker with empty transaction list"""
        self.transactions: List[Dict[str, Any]] = []
        
        # Default categories for Income and Expense
        self.income_categories = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other Income"]
        self.expense_categories = ["Food", "Transportation", "Entertainment", "Bills", "Shopping", "Healthcare", "Education", "Other Expense"]
        
        # Budget Alert System - Phase 4 Feature 3
        self.budget_limits = {}  # {category: limit_amount}
        self.monthly_budget_limit = None
        self.weekly_budget_limit = None
        
        # Exchange rates relative to USD (1 USD = X units of currency)
        self.exchange_rates = {
            "USD": 1,
            "EUR": 0.91,
            "GBP": 0.79,
            "JPY": 149.50,
            "CAD": 1.36,
            "AUD": 1.52,
            "CHF": 0.87,
            "CNY": 7.24,
            "INR": 83.12,
            "BRL": 5.03,
            "PKR": 278
        }
        
        # Load custom categories if they exist
        self.load_categories()
        
        # Load budget settings if they exist
        self.load_budget_settings()
    
    def add_transaction(self, amount: float, category: str, transaction_type: str, currency: str = "USD", transaction_date: str = None) -> bool:
        """
        Add a new transaction to the tracker
        
        Args:
            amount: The transaction amount (positive number)
            category: Category of the transaction
            transaction_type: Either 'Income' or 'Expense'
            currency: Currency code (e.g., 'USD', 'EUR', 'GBP')
            transaction_date: Custom date (ISO format) or None for current date
            
        Returns:
            True if transaction was added successfully, False otherwise
        """
        try:
            # Validate inputs
            if amount <= 0:
                return False
            if not category or not category.strip():
                return False
            if transaction_type not in ['Income', 'Expense']:
                return False
            
            # Use provided date or current date
            if transaction_date is None:
                transaction_date = datetime.now().isoformat()
            
            transaction = {
                'amount': amount,
                'category': category.strip(),
                'type': transaction_type,
                'currency': currency,
                'date': transaction_date,
                'id': len(self.transactions) + 1
            }
            
            self.transactions.append(transaction)
            return True
        except Exception:
            return False
    
    def convert_to_usd(self, amount: float, currency: str) -> float:
        """
        Convert amount from given currency to USD
        
        Args:
            amount: Amount in the original currency
            currency: Currency code (e.g., 'USD', 'EUR', 'PKR')
            
        Returns:
            Amount converted to USD
        """
        if currency not in self.exchange_rates:
            # Default to USD if currency not found
            return amount
        
        # Convert to USD using: amount_in_usd = abs(amount) / exchange_rates[currency]
        return abs(amount) / self.exchange_rates[currency]
    
    def get_transactions(self) -> List[Dict[str, Any]]:
        """
        Get all transactions
        
        Returns:
            List of all transactions
        """
        return self.transactions.copy()
    
    def get_summary(self) -> Dict[str, float]:
        """
        Calculate and return financial summary (all amounts converted to USD)
        
        Returns:
            Dictionary containing total_income, total_expenses, and net_balance in USD
        """
        total_income_usd = 0.0
        total_expenses_usd = 0.0
        
        for transaction in self.transactions:
            # Convert amount to USD
            amount_usd = self.convert_to_usd(transaction['amount'], transaction.get('currency', 'USD'))
            
            if transaction['type'] == 'Income':
                total_income_usd += amount_usd
            elif transaction['type'] == 'Expense':
                # For expenses, treat as positive amounts in USD (we'll show as positive in summary)
                total_expenses_usd += amount_usd
        
        net_balance_usd = total_income_usd - total_expenses_usd
        
        return {
            'total_income': total_income_usd,
            'total_expenses': total_expenses_usd,
            'net_balance': net_balance_usd
        }
    
    def get_transactions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get transactions filtered by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of transactions in the specified category
        """
        return [t for t in self.transactions if t['category'].lower() == category.lower()]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:
        """
        Get transactions filtered by type
        
        Args:
            transaction_type: 'Income' or 'Expense'
            
        Returns:
            List of transactions of the specified type
        """
        return [t for t in self.transactions if t['type'] == transaction_type]
    
    def remove_transaction(self, transaction_id: int) -> bool:
        """
        Remove a transaction by ID
        
        Args:
            transaction_id: ID of the transaction to remove
            
        Returns:
            True if transaction was removed, False if not found
        """
        for i, transaction in enumerate(self.transactions):
            if transaction['id'] == transaction_id:
                self.transactions.pop(i)
                return True
        return False
    
    def clear_all_transactions(self) -> None:
        """Clear all transactions"""
        self.transactions.clear()
    
    def get_transaction_count(self) -> int:
        """Get total number of transactions"""
        return len(self.transactions)
    
    def get_categories(self) -> List[str]:
        """
        Get list of unique categories used in transactions
        
        Returns:
            List of unique category names
        """
        categories = set()
        for transaction in self.transactions:
            categories.add(transaction['category'])
        return sorted(list(categories))
    
    def get_currency_symbol(self, currency_code: str) -> str:
        """
        Get currency symbol from currency code
        
        Args:
            currency_code: Currency code like 'USD', 'EUR', etc.
            
        Returns:
            Currency symbol
        """
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CHF': '₣',
            'CNY': '¥',
            'INR': '₹',
            'BRL': 'R$',
            'PKR': '₨'
        }
        return currency_symbols.get(currency_code, '$')
    
    def get_primary_currency(self) -> str:
        """
        Get the most commonly used currency in transactions
        
        Returns:
            Currency code of the most used currency
        """
        if not self.transactions:
            return 'USD'
        
        currency_counts = {}
        for transaction in self.transactions:
            currency = transaction.get('currency', 'USD')
            currency_counts[currency] = currency_counts.get(currency, 0) + 1
        
        return max(currency_counts, key=currency_counts.get)
    
    def save_to_csv(self, filename: str) -> bool:
        """
        Save all transactions to a CSV file
        
        Args:
            filename: Path to the CSV file to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'amount', 'currency', 'category', 'type', 'usd_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in self.transactions:
                    # Calculate USD equivalent for export
                    usd_value = self.convert_to_usd(transaction['amount'], transaction.get('currency', 'USD'))
                    
                    writer.writerow({
                        'date': transaction['date'],
                        'amount': transaction['amount'],
                        'currency': transaction.get('currency', 'USD'),
                        'category': transaction['category'],
                        'type': transaction['type'],
                        'usd_value': round(usd_value, 2)
                    })
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False
    
    def save_to_json(self, filename: str) -> bool:
        """
        Save all transactions to a JSON file
        
        Args:
            filename: Path to the JSON file to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'transactions': [],
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_transactions': len(self.transactions),
                    'currencies_used': list(set(t.get('currency', 'USD') for t in self.transactions))
                }
            }
            
            for transaction in self.transactions:
                # Add USD equivalent to each transaction
                usd_value = self.convert_to_usd(transaction['amount'], transaction.get('currency', 'USD'))
                
                transaction_data = transaction.copy()
                transaction_data['usd_value'] = round(usd_value, 2)
                data['transactions'].append(transaction_data)
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def load_from_csv(self, filename: str) -> bool:
        """
        Load transactions from a CSV file
        
        Args:
            filename: Path to the CSV file to load
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not Path(filename).exists():
                return False
            
            loaded_transactions = []
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Validate required fields
                    required_fields = ['date', 'amount', 'category', 'type']
                    if not all(field in row for field in required_fields):
                        continue
                    
                    transaction = {
                        'date': row['date'],
                        'amount': float(row['amount']),
                        'currency': row.get('currency', 'USD'),
                        'category': row['category'],
                        'type': row['type'],
                        'id': len(loaded_transactions) + 1
                    }
                    loaded_transactions.append(transaction)
            
            # Replace current transactions
            self.transactions = loaded_transactions
            return True
        except Exception as e:
            print(f"Error loading from CSV: {e}")
            return False
    
    def load_from_json(self, filename: str) -> bool:
        """
        Load transactions from a JSON file
        
        Args:
            filename: Path to the JSON file to load
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not Path(filename).exists():
                return False
            
            with open(filename, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
            
            # Handle both simple list format and structured format
            if isinstance(data, list):
                transactions_data = data
            elif isinstance(data, dict) and 'transactions' in data:
                transactions_data = data['transactions']
            else:
                return False
            
            loaded_transactions = []
            for transaction_data in transactions_data:
                # Validate required fields
                required_fields = ['date', 'amount', 'category', 'type']
                if not all(field in transaction_data for field in required_fields):
                    continue
                
                transaction = {
                    'date': transaction_data['date'],
                    'amount': float(transaction_data['amount']),
                    'currency': transaction_data.get('currency', 'USD'),
                    'category': transaction_data['category'],
                    'type': transaction_data['type'],
                    'id': len(loaded_transactions) + 1
                }
                loaded_transactions.append(transaction)
            
            # Replace current transactions
            self.transactions = loaded_transactions
            return True
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            return False
    
    # Phase 4 Feature 2: Custom Categories Management
    def get_categories(self, transaction_type: str = None) -> List[str]:
        """
        Get available categories for a specific transaction type
        
        Args:
            transaction_type: 'Income', 'Expense', or None for all categories
            
        Returns:
            List of category names
        """
        if transaction_type == "Income":
            return self.income_categories.copy()
        elif transaction_type == "Expense":
            return self.expense_categories.copy()
        else:
            return self.income_categories + self.expense_categories
    
    def add_category(self, category_name: str, transaction_type: str) -> bool:
        """
        Add a new custom category
        
        Args:
            category_name: Name of the new category
            transaction_type: 'Income' or 'Expense'
            
        Returns:
            True if category was added, False if it already exists
        """
        category_name = category_name.strip()
        if not category_name:
            return False
        
        if transaction_type == "Income":
            if category_name not in self.income_categories:
                self.income_categories.append(category_name)
                self.save_categories()
                return True
        elif transaction_type == "Expense":
            if category_name not in self.expense_categories:
                self.expense_categories.append(category_name)
                self.save_categories()
                return True
        
        return False  # Category already exists
    
    def remove_category(self, category_name: str, transaction_type: str) -> bool:
        """
        Remove a custom category
        
        Args:
            category_name: Name of the category to remove
            transaction_type: 'Income' or 'Expense'
            
        Returns:
            True if category was removed, False if it doesn't exist or has transactions
        """
        # Check if category is being used in transactions
        if self.is_category_in_use(category_name):
            return False  # Cannot remove category that's in use
        
        if transaction_type == "Income" and category_name in self.income_categories:
            self.income_categories.remove(category_name)
            self.save_categories()
            return True
        elif transaction_type == "Expense" and category_name in self.expense_categories:
            self.expense_categories.remove(category_name)
            self.save_categories()
            return True
        
        return False
    
    def is_category_in_use(self, category_name: str) -> bool:
        """Check if a category is being used in any transactions"""
        return any(transaction['category'] == category_name for transaction in self.transactions)
    
    def save_categories(self) -> bool:
        """Save custom categories to a JSON file"""
        try:
            categories_data = {
                'income_categories': self.income_categories,
                'expense_categories': self.expense_categories
            }
            
            with open('categories.json', 'w') as file:
                json.dump(categories_data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving categories: {e}")
            return False
    
    def load_categories(self) -> bool:
        """Load custom categories from JSON file"""
        try:
            categories_file = Path('categories.json')
            if not categories_file.exists():
                return False
            
            with open('categories.json', 'r') as file:
                categories_data = json.load(file)
            
            # Load categories if they exist in the file
            if 'income_categories' in categories_data:
                self.income_categories = categories_data['income_categories']
            if 'expense_categories' in categories_data:
                self.expense_categories = categories_data['expense_categories']
            
            return True
        except Exception as e:
            print(f"Error loading categories: {e}")
            return False
    
    # Phase 4 Feature 3: Budget Alerts System
    def set_monthly_budget(self, limit: float) -> None:
        """Set monthly spending limit"""
        self.monthly_budget_limit = limit
        self.save_budget_settings()
    
    def set_weekly_budget(self, limit: float) -> None:
        """Set weekly spending limit"""
        self.weekly_budget_limit = limit
        self.save_budget_settings()
    
    def set_category_budget(self, category: str, limit: float) -> None:
        """Set budget limit for a specific category"""
        self.budget_limits[category] = limit
        self.save_budget_settings()
    
    def remove_category_budget(self, category: str) -> bool:
        """Remove budget limit for a category"""
        if category in self.budget_limits:
            del self.budget_limits[category]
            self.save_budget_settings()
            return True
        return False
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status and alerts"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        
        # Get current month expenses
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_expenses = self._get_expenses_in_period(current_month_start, now)
        
        # Get current week expenses (Monday to Sunday)
        days_since_monday = now.weekday()
        current_week_start = now - timedelta(days=days_since_monday)
        current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        weekly_expenses = self._get_expenses_in_period(current_week_start, now)
        
        # Get category expenses for current month
        category_expenses = self._get_category_expenses_current_month()
        
        alerts = []
        
        # Check monthly budget
        if self.monthly_budget_limit:
            monthly_percentage = (monthly_expenses / self.monthly_budget_limit) * 100
            if monthly_expenses >= self.monthly_budget_limit:
                alerts.append({
                    'type': 'monthly_exceeded',
                    'message': f"Monthly budget exceeded! Spent ${monthly_expenses:.2f} of ${self.monthly_budget_limit:.2f}",
                    'severity': 'critical'
                })
            elif monthly_percentage >= 80:
                alerts.append({
                    'type': 'monthly_warning',
                    'message': f"Monthly budget warning: {monthly_percentage:.1f}% used (${monthly_expenses:.2f} of ${self.monthly_budget_limit:.2f})",
                    'severity': 'warning'
                })
        
        # Check weekly budget
        if self.weekly_budget_limit:
            weekly_percentage = (weekly_expenses / self.weekly_budget_limit) * 100
            if weekly_expenses >= self.weekly_budget_limit:
                alerts.append({
                    'type': 'weekly_exceeded',
                    'message': f"Weekly budget exceeded! Spent ${weekly_expenses:.2f} of ${self.weekly_budget_limit:.2f}",
                    'severity': 'critical'
                })
            elif weekly_percentage >= 80:
                alerts.append({
                    'type': 'weekly_warning',
                    'message': f"Weekly budget warning: {weekly_percentage:.1f}% used (${weekly_expenses:.2f} of ${self.weekly_budget_limit:.2f})",
                    'severity': 'warning'
                })
        
        # Check category budgets
        for category, limit in self.budget_limits.items():
            spent = category_expenses.get(category, 0)
            if spent > 0:
                percentage = (spent / limit) * 100
                if spent >= limit:
                    alerts.append({
                        'type': 'category_exceeded',
                        'message': f"Category '{category}' budget exceeded! Spent ${spent:.2f} of ${limit:.2f}",
                        'severity': 'critical'
                    })
                elif percentage >= 80:
                    alerts.append({
                        'type': 'category_warning',
                        'message': f"Category '{category}' warning: {percentage:.1f}% used (${spent:.2f} of ${limit:.2f})",
                        'severity': 'warning'
                    })
        
        return {
            'monthly_spent': monthly_expenses,
            'monthly_limit': self.monthly_budget_limit,
            'weekly_spent': weekly_expenses,
            'weekly_limit': self.weekly_budget_limit,
            'category_expenses': category_expenses,
            'category_limits': self.budget_limits.copy(),
            'alerts': alerts
        }
    
    def _get_expenses_in_period(self, start_date: datetime, end_date: datetime) -> float:
        """Get total expenses in USD for a specific period"""
        total = 0
        for transaction in self.transactions:
            if transaction['type'] == 'Expense':
                transaction_date = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
                if start_date <= transaction_date <= end_date:
                    # Convert to USD for budget comparison
                    usd_amount = self.convert_to_usd(transaction['amount'], transaction.get('currency', 'USD'))
                    total += usd_amount
        return total
    
    def _get_category_expenses_current_month(self) -> Dict[str, float]:
        """Get expenses by category for current month in USD"""
        from datetime import datetime
        
        now = datetime.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        category_totals = {}
        for transaction in self.transactions:
            if transaction['type'] == 'Expense':
                transaction_date = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
                if transaction_date >= current_month_start:
                    category = transaction['category']
                    # Convert to USD for budget comparison
                    usd_amount = self.convert_to_usd(transaction['amount'], transaction.get('currency', 'USD'))
                    category_totals[category] = category_totals.get(category, 0) + usd_amount
        
        return category_totals
    
    def save_budget_settings(self) -> bool:
        """Save budget settings to a JSON file"""
        try:
            budget_data = {
                'monthly_budget_limit': self.monthly_budget_limit,
                'weekly_budget_limit': self.weekly_budget_limit,
                'category_limits': self.budget_limits
            }
            
            with open('budget_settings.json', 'w') as file:
                json.dump(budget_data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving budget settings: {e}")
            return False
    
    def load_budget_settings(self) -> bool:
        """Load budget settings from JSON file"""
        try:
            budget_file = Path('budget_settings.json')
            if not budget_file.exists():
                return False
            
            with open('budget_settings.json', 'r') as file:
                budget_data = json.load(file)
            
            self.monthly_budget_limit = budget_data.get('monthly_budget_limit')
            self.weekly_budget_limit = budget_data.get('weekly_budget_limit')
            self.budget_limits = budget_data.get('category_limits', {})
            
            return True
        except Exception as e:
            print(f"Error loading budget settings: {e}")
            return False
