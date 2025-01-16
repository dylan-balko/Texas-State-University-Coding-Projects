from datetime import datetime

class Transaction:
	#Instructor
	def __init__(self, transaction_id=None, amount=None, date=None, description=None):
		self._transaction_id = transaction_id
		self._amount = amount
		self._date = date
		self._description = description

	#Accessor for transaction_id
	def get_transaction_id(self):
		return self._transaction_id

	#Accessor for amount
	def get_amount(self):
		return self._amount

	#Accessor for date
	def get_date(self):
		return self._date

	#Accessor for description
	def get_description(self):
		return self._description

	#Mutator for transaction_id
	def set_transaction_id(self, transaction_id):
		self._transaction_id = transaction_id

	#Mutator for amount
	def set_amount(self, amount):
		self._amount = amount

	#Mutator for date
	def set_date(self, date):
		self._date = date

	#Mutator for description
	def set_description(self, description):
		self._description = description

	def display_details(self):
		print(f"Transaction id: {self._transaction_id}")
		print(f"Amount: {self._amount}")
		print(f"Date: {self._date}")
		print(f"Description: {self._description}")


class ExtendedTransaction(Transaction):
	#Instructor
	def __init__(self, transaction_id=None, amount=None, date=None, description=None, business_type=None, location=None):
		super().__init__(transaction_id, amount, date, description)
		self._business_type = business_type
		self._location = location

	#Accessor for business_type
	def get_business_type(self):
		return self._business_type

	#Accessor for location
	def get_location(self):
		return self._location

	#Mutator for business_type
	def set_business_type(self, business_type):
		self._business_type = business_type

	#Mutator for location
	def set_location(self, location):
		self._location = location

	#Recursive method to calculate fees for every $500
	def calculate_fee(self,amount):
		if amount < 1000:
			return 0
		else:
			return 50 + self.calculate_fee(amount - 500)
		

	#Method to display a summary of the transaction
	def display_details(self):
		super().display_details()
##		print(f"Transaction id: {self._transaction_id}")
##		print(f"Amount: {self._amount}")
##		print(f"Date: {self._date}")
##		print(f"Description: {self._description}")
		print(f"Business Type: {self._business_type}")
		print(f"Location: {self._location}")
		







	


