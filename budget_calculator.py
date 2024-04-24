import configparser
import json
import random
import matplotlib.pyplot as plt
import plotly.express as px


class BudgetFlex:

    def __init__(self):
        self.paradigm = "savage savings"
        self.file = open("config.json")
        self.config = json.load(self.file)

        self.income = float(self.config['income'])
        self.fixed_expenses = self._calculate_total_fixed_expenses()
        self.month_miscellaneous = self._calculate_total_monthly_miscellaneous()

        self.leftover = self.income - self.fixed_expenses - self.month_miscellaneous
        self.min_flex_expenses = self._calculate_min_flex_expenses()
        self.max_flex_expenses = self._calculate_max_flex_expenses()

    # def change_paradigm(self, new_paradigm):
    #     self.paradigm = new_paradigm
    def _calculate_total_fixed_expenses(self):
        # The fixed expenses consist of monthly predicted expenses
        fixed = 0.0
        for item in self.config['fixed expenses']:
            fixed += float(self.config['fixed expenses'][item])
        return fixed

    def _calculate_total_monthly_miscellaneous(self):
        # Monthly miscellaneous are one month time
        cost = 0.0
        for item in self.config['monthly miscellaneous']:
            cost += float(self.config['monthly miscellaneous'][item])
        return cost

    def _calculate_min_flex_expenses(self):
        expense = 0.0
        for item in self.config['flexible expenses']:
            expense += min(self.config['flexible expenses'][item])
        return expense

    def _calculate_max_flex_expenses(self):
        expense = 0.0
        for item in self.config['flexible expenses']:
            expense += max(self.config['flexible expenses'][item])
        return expense

    def warn_user(self):
        if self.leftover < 0:
            return "You are spending more than your income"

    def print_fixed_categories(self):
        print("FIXED EXPENSES\n---------------")
        for item in self.config['fixed expenses']:
            print(f"{item}: {self.config['fixed expenses'][item]}")

    def print_category(self, category):
        if category in ['income', 'fixed expenses', 'monthly miscellaneous', 'flex expenses', 'savings']:
            if category == 'income':
                print(f"income: {self.income}")
            elif category == 'fixed expenses':
                print(f"fixed expenses: {self.fixed_expenses}")
            elif category == 'monthly miscellaneous':
                print(f"monthly miscellaneous: {self.month_miscellaneous}")
            elif category == 'flex expenses':
                print(f"min flex expenses: {self.min_flex_expenses}")
        else:
            print("Invalid category")

    def test_allocate_flex_categories(self, flex_expenses):
        if self.leftover < flex_expenses:
            return "Can't allocate funds with the given expenses"
        new_allocation = {}
        for items in self.config['flexible expenses']:
            new_allocation[items] = float(random.randrange(self.config['flexible expenses'][items][0],
                                                     self.config['flexible expenses'][items][1]))
        return new_allocation

    def calculate_savings(self):
        #testing receiving the min flex expenses
        new_allocation = self.test_allocate_flex_categories(self.min_flex_expenses)
        spent = 0.0
        for items in new_allocation:
            spent += new_allocation[items]
        savings = self.leftover - spent
        new_allocation['savings'] = savings
        return new_allocation

    def pie_plot_flex_expenses(self):
        new_allocation = self.calculate_savings()
        labels = new_allocation.keys()
        sizes = new_allocation.values()
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.show()

    def bar_plot_flex_expenses(self):
        new_allocation = self.calculate_savings()
        fig = px.bar(x=list(new_allocation.keys()), y=list(new_allocation.values()))
        fig.show()





if __name__ == "__main__":
    budget = BudgetFlex()
    fixed_exp = budget.fixed_expenses
    month = budget.month_miscellaneous
    print(budget.calculate_savings())

