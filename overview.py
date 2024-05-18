from monthlyBudget import Budget
from tracker import Ledger
import json


class MonthSummary:

    def __init__(self, request:json):
        self.budget = Budget(request)
        self.ledger = Ledger()



