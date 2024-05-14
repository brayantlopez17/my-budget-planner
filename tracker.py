import datetime

import pandas as pd
import uuid
from budget_calculator import BudgetFlex


class Entry:
    def __init__(self, **obj):
        self.date = obj['date']
        self.item = obj['item']
        self.amount = obj['amount']
        self.category = obj['category']
        self.uuid = obj['UUID']


class Ledger:
    def __init__(self):
        self.year = datetime.date.today().year
        self.entries = []

        self._df = pd.DataFrame

    def add_entry(self, entry: Entry):
        self.entries.append(entry)

    def read_csv(self, filepath: str):
        self._df = pd.read_csv(filepath)
        self._df.dropna(how="all", inplace=True)
        self._df.dropna(axis=1, how="all", inplace=True)
        self._df['UUID'] = [str(uuid.uuid4()) for _ in range(len(self._df))]
        self._convert_datatypes()

    def _convert_datatypes(self):
        self._df['Date'] = self._df['Date'] + f' {self.year}'
        self._df['Date'] = pd.to_datetime(self._df['Date'], format='%b %d %Y')
        self._df['Amount'] = self._df['Amount'].replace('[\$,]', '', regex=True).astype(float)
        self._df['Category'] = self._df['Category'].astype('category')

    def to_json(self):
        return self._df.to_json(orient="records")

    def categories(self):
        return list(set(self._df['Category']))

    def category_spent(self):
        categories_ls = self.categories()
        spent_dic = {}
        for category in categories_ls:
            spent_dic[category] = round(self._df[self._df['Category'] == category]['Amount'].sum(), 2)
        return spent_dic

    @property
    def df(self):
        return self._df



if __name__ == "__main__":
    ledger = Ledger()
    ledger.read_csv("data/expense_tracker.csv")
    print(ledger.category_spent())


