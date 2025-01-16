import tkinter as tk
import tkinter.messagebox
import sqlite3
import datetime
class BaseTransaction:
        #Instructor
        def __init__(self, amount=None, category=None, date=None):
                self._amount = amount
                self._category = category
                self._date = date

        #Accessor for amount
        def get_amount(self):
                return self._amount

        #Accessor for category
        def get_category(self):
                return self._category

        #Accessor for date
        def get_date(self):
                return self._date

        #Mutator for amount
        def set_amount(self, amount):
                self._amount = amount

        #Mutator for category
        def set_category(self, category):
                self._category = category

        #Mutator for date
        def set_date(self, date):
                self._date = date

        def print_summary(self):
                return f"Transaction amount: {self._amount}. Category: {self._category}. Transaction date: {self.get_date()}."
        


class Income(BaseTransaction):
        #Instructor
        def __init__(self, amount=None, category=None, source=None, date=None):
                super().__init__(amount, category, date)
                self._source = source
                
        #Accessor for source
        def get_source(self):
                return self._source

        #Mutator for source
        def set_source(self, source):
                self._source = source
                
        def print_summary(self):
                return f"Income amount: {self.get_amount()}. Source of income: {self.get_source}. Category: {self.get_category()}. Income date: {self.get_date()}"




class Expense(BaseTransaction):
        #Instructor
        def __init__(self, amount=None, category=None, source=None, date=None):
                super().__init__(amount, category, date)
                self._source = source

        #Accessor for source
        def get_source(self):
                return self._source

        #Mutator for source
        def set_source(self, source):
                self._source = source

        def print_summary(self):
                return f"Expense amount: {self.get_amount()}. Source of Expense: {self.get_source}. Category: {self.get_category()}. Income date: {date}"


#recursive calculator to calculate savings over n period of time
class SavingsCalculator:
        #instructor
        def __init__(self, incomes=None, expenses=None):
                self.incomes = incomes
                self.expenses = expenses

        def calculate_savings(self, n):
                if n == 0:
                        return 0
                if n-1 < len(self.incomes):
                        income_n = self.incomes[n-1].get_amount()

                else:
                        return 0
                if n-1 < len(self.expenses):
                        expenses_n = self.expenses[n-1].get_amount()
                else:
                        return 0

                savings = income_n - expenses_n
                return savings + self.calculate_savings(n-1)

class FinancialGUI:
        def __init__(self, root, database):
                self.root = root
                self.root.title("Financial Management Application")
                self.incomes = []
                self.expenses = []
                self.database = Database()
                self.savings_calculator = SavingsCalculator(self.incomes, self.expenses)
                # Setup the UI
                self.setup_ui()

        def setup_ui(self):
                #Create Income Button
                self.income_button = tk.Button(self.root, text="Add Income", command=self.show_income_input)
                self.income_button.pack()

                #Create Expense Button
                self.expense_button = tk.Button(self.root, text="Add Expenses",command=self.show_expense_input)
                self.expense_button.pack()

                #Create View Summary Button
                self.view_sum_button = tk.Button(self.root, text="View Summary", command=self.show_summary)
                self.view_sum_button.pack()

                #Create Frame
                self.feature_frame = tk.Frame(self.root)
                self.feature_frame.pack()

        #Clears GUI
        def clear_frame(self):
                for widget in self.feature_frame.winfo_children():
                        widget.destroy()


        def show_income_input(self):
                #Clears frame to setup the income entries
                self.clear_frame()

                #creates the label for Amount
                tk.Label(self.feature_frame, text="Amount:").grid(row=0,column=0)
                self.income_amount = tk.Entry(self.feature_frame)
                self.income_amount.grid(row=0, column=1)

                #creates the label for Category
                tk.Label(self.feature_frame, text="Category:").grid(row=1,column=0)
                self.income_category = tk.Entry(self.feature_frame)
                self.income_category.grid(row=1, column=1)

                #creates the label for Source
                tk.Label(self.feature_frame, text="Source:").grid(row=2,column=0)
                self.income_source = tk.Entry(self.feature_frame)
                self.income_source.grid(row=2, column=1)

                #creates the label for Date
                tk.Label(self.feature_frame, text="Date:").grid(row=3,column=0)
                self.income_date = tk.Entry(self.feature_frame)
                self.income_date.grid(row=3, column=1)

                #creates add income button
                tk.Button(self.feature_frame, text="Add Income:",command=self.add_income).grid(row=4,column=0)
                

        def show_expense_input(self):
                #Clears frame to setup the expense entries
                self.clear_frame()

                #Clears frame to setup the expense entries
                self.clear_frame()

                #creates the label for Amount
                tk.Label(self.feature_frame, text="Amount:").grid(row=0,column=0)
                self.expense_amount = tk.Entry(self.feature_frame)
                self.expense_amount.grid(row=0, column=1)

                #creates the label for Category
                tk.Label(self.feature_frame, text="Category:").grid(row=1,column=0)
                self.expense_category = tk.Entry(self.feature_frame)
                self.expense_category.grid(row=1, column=1)

                #creates the label for Source
                tk.Label(self.feature_frame, text="Source:").grid(row=2,column=0)
                self.expense_source = tk.Entry(self.feature_frame)
                self.expense_source.grid(row=2, column=1)

                #creates the label for Date
                tk.Label(self.feature_frame, text="Date:").grid(row=3,column=0)
                self.expense_date = tk.Entry(self.feature_frame)
                self.expense_date.grid(row=3, column=1)

                #creates add expense button
                tk.Button(self.feature_frame, text="Add Expense:",command=self.add_expense).grid(row=4,column=0)


        #Method to add income
        def add_income(self):
                amount = float(self.income_amount.get())
                category = self.income_category.get()
                source = self.income_source.get()
                date = self.income_date.get()
                if amount <= 0:
                        raise ValueError("Invalid Input")
                if not category or not source or not date:
                        raise ValueError("All fields must be filled.")
                income = Income(amount,category,source,date)
                self.incomes.append(income)
                self.database.insert_transaction('Income', category, amount,source, date)
                tkinter.messagebox.showinfo("Success", "Income added successfully!")

                
        #Method to add expense
        def add_expense(self):
                amount = float(self.expense_amount.get())
                category = self.expense_category.get()
                source = self.expense_source.get()
                date = self.expense_date.get()
                if amount <= 0:
                        raise ValueError("Invalid Input")
                if not category or not source or not date:
                        raise ValueError("All fields must be filled.")
                expense = Expense(amount,category,source,date)
                self.expenses.append(expense)
                self.database.insert_transaction('Expense', category, amount,source, date)
                tkinter.messagebox.showinfo("Success", "Expense added successfully!")


        #Method to show summaries
        def show_summary(self):
                #Clears frame to setup show the totals
                self.clear_frame()
                total_income = sum(income.get_amount() for income in self.incomes)
                total_expenses = sum(expense.get_amount() for expense in self.expenses)
                net_savings = total_income - total_expenses
                total_savings = self.savings_calculator.calculate_savings(len(self.incomes))              
                text = (f"Total Income: {total_income}\nTotal Expenses: {total_expenses}\nNet Savings: {net_savings}\nTotal Savings: {total_savings}")
                tk.Label(self.feature_frame, text=text).pack()

class Database:
        #Instructor
        def __init__(self, db_name='finance.db'):
                self._db_name = db_name
                self.create_table()

        #Creates the table in the database
        def create_table(self):
                try:
                        with sqlite3.connect(self._db_name) as conn:
                                cursor = conn.cursor()
                                cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                                        id INTEGER PRIMARY KEY,
                                        type TEXT,
                                        category TEXT,
                                        amount REAL,
                                        source TEXT,
                                        date DATE)''')
                                conn.commit()
                except sqlite3.Error as e:
                        print(f"An error has occured {e}")

        #Reads all transactions
        def read_transaction(self):
                try:
                        with sqlite3.connect(self._db_name) as conn:
                                cursor = conn.cursor()
                                cursor.execute("SELECT * FROM Transactions")
                                rows = cursor.fetchall()
                                return rows
                except sqlite3.Error as e:
                        print(f"An error has occured {e}")
                        
        #updates the transaction
        def update_transaction(self,transaction_id,transaction_type,category,amount,source, date):
                try:
                        with sqlite3.connect(self._db_name) as conn:
                                cursor = conn.cursor()
                                cursor.execute("Update Transactions SET type=?, category=?, amount=?, source=?, date=?, id=?",
                                               (transaction_type, category, amount, source, date, transaction_id))
                                conn.commit()
                except sqlite3.Error as e:
                        print(f"An error has occured {e}")

        #deletes a transaction from its id
        def delete_transaction(self,transaction_id):
                try:
                        with sqlite3.connect(self._db_name) as conn:
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM Transactions WHERE id=?", (transaction_id,))
                                conn.commit()
                except sqlite3.Error as e:
                         print(f"An error has occured {e}")

        #inserts a transaction
        def insert_transaction(self,transaction_type,category,amount,source, date):
                try:
                        with sqlite3.connect(self._db_name) as conn:
                                cursor = conn.cursor()
                                cursor.execute("INSERT INTO Transactions (type, category, amount, source, date) VALUES (?,?,?,?,?)",
                                               (transaction_type, category, amount, source, date))
                                conn.commit()
                except sqlite3.Error as e:
                        print(f"An error has occured {e}")



def main():
        database = Database()
        root = tk.Tk()
        financial_gui = FinancialGUI(root, database)
        root.mainloop()
        #User menu to allow user to query previous input/uppdate/delete it
        while True:
                print(f"\nMenu:")
                print("1. Read All Transactions")
                print("2. Delete a Transaction")
                print("3. Update a transaction")
                print("4. Quit")
                choice = input("Enter choice:")

                if choice == '1':
                        rows = database.read_transaction()
                        for row in rows:
                                print(row)
                elif choice == '2':
                        delete = input("Which transaction would you like to delete based on transaction id? ")
                        database.delete_transaction(delete)
                        print("\nTransactions after deletion")
                        rows = database.read_transaction()
                        for row in rows:
                                print(row)
                elif choice == '3':
                        update = input("Which transaction would you like to update based on id?")
                        new_type = input("New trans type: ")
                        new_category = input("New category: ")
                        new_amount = float(input("New amount: "))
                        new_source = input("New source: ")
                        new_date = input("New date MM/DD/YYYY: ")
                        database.update_transaction(update, new_type, new_category, new_amount, new_source, new_date)
                        print("\nTransactions after updating")
                        rows = database.read_transaction()
                        for row in rows:
                                print(row)
                elif choice == '4':
                        quit()

if __name__ == "__main__":
        main()









                
                

        
                
                                        
                











                        




                        
                
                






                
