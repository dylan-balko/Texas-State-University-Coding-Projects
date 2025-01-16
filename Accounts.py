#create a base account with an account number and balance
class Base_Account:
        def __init__(self, account_number = "", balance = 0.0):
                self._account_number = account_number
                self._balance = balance
                
#accessor to the account number
        def get_account_number(self):
                return self._account_number
        
#accessor to the balance
        def get_balance(self):
                return self._balance
        
#mutator for account number
        def set_account_number(self, account_number):
                self._account_number = account_number
                
# mutator for balance
        def set_balance(self, balance):
                self._balance = balance
                
#method too deposut money and add it to the objects balance
        def deposit(self, balance):
                self._balance += balance
                
#method too withdraaw money and subtract from the objects balance
        def withdraw(self, amount):
                if self._balance > amount:
                        self._balance -= amount
                else:
                        print("Insufficient Funds.")
                        
#savings account class that inherits the base characteristics
class Savings_Account(Base_Account):
        def __init__(self, account_number = "", balance = 0.0, interest_rate = 0.0):
                super().__init__(account_number, balance)
                self._interest_rate = interest_rate
                
#mutator for the interest rate
        def set_interest_rate(self, interest_rate):
                self._interest_rate = interest_rate
                
#method to calculate interest and add it to the objects balance
        def apply_interest(self):
                self._balance += self._balance * self._interest_rate
                
#checking account class that inherits the base characteristics
class Checking_Account(Base_Account):
        def __init__(self, account_number="", balance = 0.0, overdraft_lim=0):
                super().__init__(account_number, balance)
                self._overdraft_lim = overdraft_lim
                
#mutator for the overdraft limit
        def set_overdraft_lim(self, overdraft_lim):
                self._overdraft_lim = overdraft_lim
                
#method to withdraw money as long as it is not over the overdraft limit
        def withdraw(self, amount):
                if self._balance - amount >= -self._overdraft_lim:
                        self._balance -= amount
                else:
                        print("Insufficient Funds. Can't go over overdraft limit")
                

