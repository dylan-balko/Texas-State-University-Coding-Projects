from Accounts import Base_Account, Savings_Account, Checking_Account

#customer class with basic attributes
class Customer():
    def __init__(self,customer_id = "", name = ""):
        self._customer_id = customer_id
        self._name = name
        self._accounts = []

#method to add accounts for the customer object
    def add_account(self,account):
        self._accounts.append(account)

#accessor to accounts list
    def get_accounts(self, accounts):
        return self._accounts

#recursion method to calculate an onject (customers) total assets
    def get_total_assets(self, index = 0):
        if index >= len(self._accounts):
            return 0
        else:
            return self._accounts[index].get_balance() + self.get_total_assets(index + 1)

#method with all the test casing to clear up main
def test_cases():
#creates two customers
    cust1 = Customer(12345, "Alice")
    cust2 = Customer(678910, "Bob")

#create and add accounts for Alice
    cust1_savings = Savings_Account(1234, 5000, .02)
    cust1_checking = Checking_Account(2345, 2000, 500)
    cust1.add_account(cust1_savings)
    cust1.add_account(cust1_checking)

#Pperform transactions for Alice's checking account
    print("\nAlice's Checking Account:")
    print(f"Balance: ${cust1_checking.get_balance():.2f}")
    cust1_checking.deposit(500)
    print(f"Balance after depositing $500: ${cust1_checking.get_balance():.2f}")
    cust1_checking.withdraw(3000)  
    print(f"Balance after withdrawing $3000: ${cust1_checking.get_balance():.2f}")

#perform transactions for Alice's savings account
    print("\nAlice's Savings Account:")
    print(f"Balance: ${cust1_savings.get_balance():.2f}")
    cust1_savings.deposit(500)
    print(f"Balance after depositing $500: ${cust1_savings.get_balance():.2f}")
    cust1_savings.withdraw(6000) 
    print(f"Balance after attempting to withdraw $6000: ${cust1_savings.get_balance():.2f}")
    cust1_savings.apply_interest()
    print(f"Balance after applying interest: ${cust1_savings.get_balance():.2f}")

#create and add accounts for Bob
    cust2_savings = Savings_Account(3456, 8000, .03)
    cust2_checking = Checking_Account(4567, 1000, 1000)
    cust2.add_account(cust2_savings)
    cust2.add_account(cust2_checking)

# Perform transactions for Bob's checking account
    print("\nBob's Checking Account:")
    print(f"Balance: ${cust2_checking.get_balance():.2f}")
    cust2_checking.deposit(500)
    print(f"Balance after depositing $500: ${cust2_checking.get_balance():.2f}")
    cust2_checking.withdraw(300)
    print(f"Balance after withdrawing $300: ${cust2_checking.get_balance():.2f}")

#perform transactions for Bob's savings account
    print("\nBob's Savings Account:")
    print(f"Balance: ${cust2_savings.get_balance():.2f}")
    cust2_savings.deposit(500)
    print(f"Balance after depositing $500: ${cust2_savings.get_balance():.2f}")
    cust2_savings.withdraw(6000)
    print(f"Balance after withdrawing $6000: ${cust2_savings.get_balance():.2f}")
    cust2_savings.apply_interest()
    print(f"Balance after applying interest: ${cust2_savings.get_balance():.2f}")

#print total assets for Alice and Bob
    print(f"\nAlice's total assets: ${cust1.get_total_assets():.2f}")
    print(f"Bob's total assets: ${cust2.get_total_assets():.2f}")

#main function which calls the test case method 
def main():
    test_cases()

if __name__ == "__main__":
        main()

        
        
