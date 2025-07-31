class Budget:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, description):
        self.expenses.append({'amount': amount, 'description': description})

    def remove_expense(self, description):
        self.expenses = [expense for expense in self.expenses if expense['description'] != description]

    def get_balance(self):
        return sum(expense['amount'] for expense in self.expenses)