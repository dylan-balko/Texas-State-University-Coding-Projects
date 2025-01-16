import sqlite3
import csv
from Transaction import Transaction, ExtendedTransaction
from datetime import datetime

class BusinessTransactionProcessor():
    def __init__(self):
        self.transactions = []

    #read transactions from a csv
    def load_transactions_from_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'business_type' in row and row['business_type'] and 'location' in row and row['location']:
                        transaction = ExtendedTransaction(
                            transaction_id = row['transaction_id'],
                            amount = float(row['amount']),
                            date = row['date'],
                            description = row['description'],
                            business_type = row['business_type'],
                            location = row['location'])

                    else:
                        transaction = Transaction(
                            transaction_id = row['transaction_id'],
                            amount = float(row['amount']),
                            date = row['date'],
                            description = row['description'])
                        
                    self.transactions.append(transaction)
            print(f"Loaded {len(self.transactions)} transactions")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    #displays the transactions and calls either the Transaction display
    #method or the Extended method depending on which class object it belongs to
    def display_transactions(self):
        if not self.transactions:
            print("No transactions loaded.")
            return
        for transaction in self.transactions:
            transaction.display_details()
            print("\n")

    #create database
    def create_db(self, db_name="transactions.db"):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    amount REAL,
                    date TEXT,
                    description TEXT,
                    business_type TEXT,
                    location TEXT
                )
            ''')
            conn.commit()
            conn.close()
            print("Database created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while adding transactions to the database: {e}")

    #adds transactiions to the database
    def add_transactions_to_db(self, db_name = "transactions.db"):
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                for transaction in self.transactions:
                    if isinstance(transaction, ExtendedTransaction):
                        cursor.execute('''
                            INSERT OR IGNORE INTO transactions (transaction_id, amount, date, description, business_type, location)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (transaction._transaction_id, transaction._amount, transaction._date,
                              transaction._description, transaction._business_type, transaction._location))
                    else:
                        cursor.execute('''
                            INSERT OR IGNORE INTO transactions (transaction_id, amount, date, description, business_type, location)
                            VALUES (?, ?, ?, ?, NULL, NULL)
                        ''', (transaction._transaction_id, transaction._amount, transaction._date,
                              transaction._description))

                conn.commit()
                conn.close()
                print("Transactions added to the database successfully.")
            except sqlite3.Error as e:
                print(f"An error occurred while adding transactions to the database: {e}")


    #allows user to find transactions over an amount threshold
    def query_transactions(self, amount_threshold):
        try:
            conn = sqlite3.connect("transactions.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM transactions WHERE amount > ?
            ''', (amount_threshold,))

            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Transaction ID: {row[0]}, Amount: {row[1]}, Date: {row[2]}, Description: {row[3]}, "
                          f"Business Type: {row[4]}, Location: {row[5]}")
            else:
                print(f"No transactions found with an amount greater than {amount_threshold}.")

            conn.close()
        except sqlite3.Error as e:
            print(f"An error occurred while querying the database: {e}")


#main function to set up method calls, class objects, and user interface
def main():
    processor = BusinessTransactionProcessor()
    while True:
        print("Transaction Menu")
        print("1: Load transactions from csv")
        print("2: Display all transactions")
        print("3: Add transactions to the database")
        print("4: Query transactions for transactions ove amount threshold")
        print("5: Exit")
        choice = input("Enter your choice:")
        if choice not in ['1','2','3','4','5']:
            print("Invalid choice")
        if choice == '1':
            filename = input("Enter filename: ")
            processor.load_transactions_from_csv(filename)
        elif choice == '2':
            processor.display_transactions()
        elif choice == '3':
            processor.create_db()
            processor.add_transactions_to_db()
        elif choice == '4':
            amount_threshold = float(input("Enter amount threshold for querying: "))
            processor.query_transactions(amount_threshold)
        elif choice == '5':
            quit()

if __name__ == "__main__":
        main()


            
            





            
