import datetime
import json
import pandas as pd
import uuid


class Entry:
    def __init__(self, **obj):
        self.date = obj['date']
        self.item = obj['item']
        self.amount = obj['amount']
        self.category = obj['category']
        self.uuid = obj['UUID']


class Ledger:
    def __init__(self, request: json):
        json_obj = json.load(request)
        self.date = datetime.date.today()
        self.year = self.date.year
        self.entries = []

        self._df = pd.DataFrame(json_obj)

    def add_entry(self, entry: Entry):
        self.entries.append(entry)

    def read_csv(self, filepath: str):
        self._df = pd.read_csv(filepath)
        self._df.dropna(how="all", inplace=True)
        self._df.dropna(axis=1, how="all", inplace=True)
        self._df['UUID'] = [str(uuid.uuid4()) for _ in range(len(self._df))]
        self._convert_datatypes()

    def read_json(self, json_obj):
        self._df = pd.DataFrame(json_obj)
        self._df.dropna(how="all", inplace=True)
        self._df.dropna(axis=1, how="all", inplace=True)
        if 'UUID' not in self._df.columns:
            self._df['UUID'] = [str(uuid.uuid4()) for _ in range(len(self._df))]
        self._convert_datatypes()

    def _convert_datatypes(self):
        self._df['Date'] = self._df['Date'] + f' {self.year}'
        self._df['Date'] = pd.to_datetime(self._df['Date'], format='%b %d %Y')
        self._df['Amount'] = self._df['Amount'].replace('[\$,]', '', regex=True).astype(float)
        self._df['Category'] = self._df['Category'].astype('category')

    # def to_json(self):
    #     return self._df.to_json(orient="records")

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

    def to_json(self):
        self._df.to_json(f"{self.date}_tracker.json", orient="records")



if __name__ == "__main__":
    json_file = "data/2024-05-17_tracker.json"
    file = open(json_file)
    ledger = Ledger(file)
    ledger.read_csv("data/expense_tracker.csv")
    print(ledger.category_spent())


