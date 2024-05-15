from budget_calculator import MonthlyBudget
from tracker import Ledger


class MonthSummary:

    def __init__(self, filepath):
        self.budget = MonthlyBudget(filepath)
        self.ledger = Ledger()

