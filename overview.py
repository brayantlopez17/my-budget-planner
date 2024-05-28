from monthlyBudget import Budget
from tracker import Ledger
import json


class MonthSummary:

    def __init__(self, request_intro: json, request_tracker:json):
        self.budget = Budget(request_intro)
        self.ledger = Ledger(request_tracker)







