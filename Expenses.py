import csv
import datetime
import pandas as pd
from tabulate import tabulate


class Expenses:
    global df
    df = pd.read_csv('records.csv')

    def __init__(self, amount, category, date, description):
        # Instance attributes
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    # Method to only allow dates in YYYY-MM-DD format
    def validate(date):
        try:
            datetime.date.fromisoformat(date)
            return date
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    # Return expenses details in table format
    def table_result(id) -> str:
        filtered_df = df.loc[df['id'] == id]

        return print(tabulate(filtered_df[['amount', 'category',
                              'date', 'description', 'id']],
                              headers=['Amount', 'Category', 'Date',
                              'Description', 'ID'],
                              tablefmt="rounded_grid",
                              numalign="center",
                              stralign="center"))

    # Method to add a new expense into a csv file.
    @staticmethod
    def add_expense():
        # Collecting the expenses data from the user

        amount = float(input("Write the total amount of the expense: "))
        category = input('''Write the category of
                         the expense from the list below:
                      - Office Supplies
                      - Laundry and Linens
                      - Software
                      - Utilities:  ''').capitalize()
        date = input("Date of the expense (YYYY-MM-DD): ")
        description = input("Description of the expense: ")
        categories_list = ["Office Supplies", "Laundry and Linens",
                           "Software", "Utilities"]

        # Verifying if the category is in the allowed categories
        # list and validating the date added.
        if category in categories_list and Expenses.validate(date):

            x = datetime.datetime.now()
            id = category[:4] + date + x.strftime("%M")  # ID expense
            # Collecting the data to save it in a list
            data = [[amount, category, date, description, id]]
            # Append the new expenses into the csv file.
            with open('records.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            print(f"Expense added with the ID: {id}")
        else:
            return ("Be sure to write correctly the category",)
    # Search the details of a expense using the expense's ID.

    @staticmethod
    def search_expense() -> str:
        id = input("Write the id of the expense: ")
        search_expense = df[df["id"] == id]
        Expenses.table_result(id)
        return search_expense

    # Updating one expense's field
    @staticmethod
    def update_expense():
        id = input("Write the id of the expense:\n ")
        # filtered_df = df.loc[df['id'] == id]
        Expenses.table_result(id)

        # If the expense exists, we should select what field to update.
        if df.loc[df['id'] == id].index[0]:
            op = input('''\nWrite the name of the field:
                       that you want to update :
                    1.- Amount
                    2.- Category
                    3.- Date
                    4.- Description:''').lower()

        # Collecting the field to update.
        if op == 'amount':
            new_amount = float(input("Type the new amount without signs:  "))
            # Replacing the old amount with the new amount
            df.loc[df.loc[df['id'] == id].index[0], 'amount'] = new_amount
            df.to_csv('records.csv', index=False)
            print(f"The field { op } was updated successfully\n")
            Expenses.table_result(id)

        elif op == 'category':
            new_category = input('''Please specify the new category of
            the expense from the list below:
                      - Office Supplies
                      - Laundry and Linens
                      - Software
                      - Utilities:  ''')
            categories_list = ["Office Supplies", "Laundry and Linens",
                               "Software", "Utilities"]

            if new_category in categories_list:
                # Replacing the old category with the new category
                df.loc[df.loc[df['id'] == id].index[0],
                       'category'] = new_category
                df.to_csv('records.csv', index=False)
                print(f"The field { op } was updated successfully\n")
                Expenses.table_result(id)

        elif op == 'date':

            new_date = input("Date of the expense (YYYY-MM-DD): ")
            if Expenses.validate(new_date):
                # Replacing the old date with the new date
                df.loc[df.loc[df['id'] == id].index[0], 'date'] = new_date
                df.to_csv('records.csv', index=False)
                print(f"The field { op } was updated successfully\n")
                Expenses.table_result(id)

        elif op == 'description':
            # Replacing the old description with the new description
            new_description = input("Add the new description: ")
            df.loc[df.loc[df['id'] == id].index[0],
                   'description'] = new_description
            df.to_csv('records.csv', index=False)
            print(f"The field { op } was updated successfully\n")
            Expenses.table_result(id)

        else:
            return ("No option")

    @staticmethod
    def drop_expense():
        id = input("Write the expense's ID to delete: ")
        Expenses.table_result(id)
        filtered_df = df.loc[df['id'] == id].index[0]
        # Alert to delete the expense
        alert = input('''Are you sure you want to delete
                      this expense? Y/N''').lower()

        if alert == 'y':
            new = df.drop(filtered_df)
            new.to_csv('records.csv', index=False)
            print(f"The expense with the ID { id } was deleted successfully\n")
        else:
            print("No rows were deleted")

# Menu to select one option.


def options():
    op = input('''Write the number of the option you want to select :
                1.- Add expense
                2.- Search expense
                3.- Update expense
                4.- Delete expense:
                ''')
    if op == '1':
        Expenses.add_expense()

    elif op == '2':
        Expenses.search_expense()

    elif op == '3':
        Expenses.update_expense()

    elif op == '4':
        Expenses.drop_expense()

    else:
        return 'No option'


options()
