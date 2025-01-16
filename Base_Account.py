class Base_Account:
	def __init__(self, account_number=None, balance=None):
		self._account_number = account_number
		self._balance = balance

	def get_account_number(self):
		return self._account_number

	def get_balance(self):
		return self._balance

	def set_account_number(self, account_number):
		self._account_number = account_number

	def set_balance(self, balance):
		self._balance = balance

