import configparser
import json
import random
import matplotlib.pyplot as plt
import plotly.express as px


class Budget:

    def __init__(self, request: json):
        """
        This class host the data from the first form. It assigns the values for the different
        expenses and does general calculations.

        It receives a JSON object to start it.
        :param request: json object
        """
        self.paradigm = "savage savings"
        self.config = json.load(request)

        # Categories
        self.income = float(self.config['income'])
        self.flex_expenses = self.config['flexible expenses']
        self.fixed_expenses = self.config['fixed expenses']

        self.flex_expenses_keys = list(self.flex_expenses.keys())
        self.fixed_expenses_keys = list(self.fixed_expenses.keys())

        # Calculations
        self.total_fixed_expenses = self._calculate_total_fixed_expenses()
        self.total_leftover = self.income - self.total_fixed_expenses
        self.min_flex_expenses = self._calculate_min_flex_expenses()
        self.max_flex_expenses = self._calculate_max_flex_expenses()

        self.projected_savings = (self.total_leftover - self.min_flex_expenses, self.total_leftover - self.max_flex_expenses)

    # def change_paradigm(self, new_paradigm):
    #     self.paradigm = new_paradigm

    def _calculate_total_fixed_expenses(self):
        """
        Sum of all the fixed expenses items
        :return: fixed expenses amount
        """
        fixed = 0.0
        for item in self.config['fixed expenses']:
            fixed += float(self.config['fixed expenses'][item])
        return fixed

    # def _calculate_total_monthly_miscellaneous(self):
    #     # Monthly miscellaneous are one month time
    #     cost = 0.0
    #     for item in self.config['monthly miscellaneous']:
    #         cost += float(self.config['monthly miscellaneous'][item])
    #     return cost

    def _calculate_min_flex_expenses(self):
        """
        Calculates the minimum value that can be gotten from the flex expenses
        :return: minimum amount from the flex expenses
        """
        expense = 0.0
        for item in self.config['flexible expenses']:
            expense += min(self.config['flexible expenses'][item])
        return expense

    def _calculate_max_flex_expenses(self):
        """
        Calculates the maximum value that can be gotten from the flex expenses
        :return: maximum amount from the flex expenses
        """
        expense = 0.0
        for item in self.config['flexible expenses']:
            expense += max(self.config['flexible expenses'][item])
        return expense

    def warn_user(self):
        """
        In case the fixed expenses are more than the income, warn user
        :return:
        """
        if self.total_leftover < 0:
            return "You are spending more than your income"

    def print_fixed_categories(self):
        """
        Prints the fixed categories and their amounts
        :return: None
        """
        print("FIXED EXPENSES\n---------------")
        for item in self.config['fixed expenses']:
            print(f"{item}: {self.config['fixed expenses'][item]}")

    # def print_category(self, category):
    #     if category in ['income', 'fixed expenses', 'monthly miscellaneous', 'flex expenses', 'savings']:
    #         if category == 'income':
    #             print(f"income: {self.income}")
    #         elif category == 'fixed expenses':
    #             print(f"fixed expenses: {self.total_fixed_expenses}")
    #         # elif category == 'monthly miscellaneous':
    #         #     print(f"monthly miscellaneous: {self.month_miscellaneous}")
    #         elif category == 'flex expenses':
    #             print(f"min flex expenses: {self.min_flex_expenses}")
    #     else:
    #         print("Invalid category")

    def test_allocate_flex_categories(self, flex_expenses):
        """
        Just for testing purposes
        :param flex_expenses:
        :return:
        """
        if self.total_leftover < flex_expenses:
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
        savings = self.total_leftover - spent
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

    def print_summary(self):
        print(f"Total income: ${self.income}")
        print(f"Total fixed expenses: ${self.total_fixed_expenses}")
        print(f"Total leftover: ${self.total_leftover}")
        print(f"Projected -> Min savings: ${self.projected_savings[1]} Max savings: ${self.projected_savings[0]}")


if __name__ == "__main__":
    json_file = open("data/apr24_budget.json")
    budget = Budget(json_file)
    print(max(budget.flex_expenses['Groceries']))
    budget.print_summary()

