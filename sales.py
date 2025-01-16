from datetime import datetime
from datamanager import DataManager
import threading

class Sales:
    def __init__(self):
        self.data_manager = DataManager()

    def create_order(self):
        """Create a new order and update inventory accordingly."""
        customer = input("Customer Name: ")
        product = input("Product Name: ")
        quantity = int(input("Quantity: "))
        payment_type = input("Payment Type (credit/cash/invoice): ")

        # Retrieve product price from inventory
        price_per_item = self.data_manager.get_product_price(product)
        if price_per_item is None:
            print(f"Error: Product '{product}' does not exist in inventory.")
            return

        # Calculate total cost before discounts
        total_amount = quantity * price_per_item

        # Prepare order data for discount application
        order_data = {
            "customer": customer,
            "product": product,
            "quantity": quantity,
            "payment_type": payment_type,
            "product_price": price_per_item
        }

        # Apply discounts through DataManager
        discounted_amount = self.data_manager.apply_discounts(order_data)

        # Check inventory availability
        stock = self.data_manager.check_stock(product)
        if stock >= quantity:
            # Update order with final discounted amount and save
            order_data["discounted_amount"] = discounted_amount
            self.data_manager.save_order(order_data)  # save_order should handle stock update
            print("Order recorded successfully.")
        else:
            print(f"Not enough stock available for {product} (requested: {quantity}, available: {stock}).")

    def generate_report(self, timeframe='daily'):
        """Generate a report of sales by specified timeframe."""
        orders = self.data_manager.load_orders()
        report_data = {}

        for order in orders:
            order_date = order[6]  # Assuming 'date' is the 7th column
            discounted_amount = float(order[5])  # Access the correct index for discounted amount

            # Determine the key based on the timeframe
            if timeframe == 'daily':
                key = order_date
            elif timeframe == 'weekly':
                key = datetime.strptime(order_date, '%Y-%m-%d').strftime("%Y-%U")  # Year-Week number
            elif timeframe == 'monthly':
                key = datetime.strptime(order_date, '%Y-%m-%d').strftime("%Y-%m")  # Year-Month
            elif timeframe == 'yearly':
                key = datetime.strptime(order_date, '%Y-%m-%d').strftime("%Y")  # Year
            else:
                print("Invalid timeframe. Please select daily, weekly, monthly, or yearly.")
                return

            report_data[key] = report_data.get(key, 0) + discounted_amount

        print(f"{timeframe.capitalize()} Sales Report:")
        for date, total in report_data.items():
            print(f"Date: {date}, Total Sales: ${total:.2f}")

    def check_product_availability(self):
        """Check the availability of a specific product."""
        product_name = input("Enter the product name to check availability: ")
        stock = self.data_manager.check_stock(product_name)
        if stock > 0:
            print(f"{product_name} is available with {stock} units in stock.")
        else:
            print(f"{product_name} is currently out of stock.")

    def menu(self):
        """Display the sales department menu."""
        while True:
            print("\nSales Department Menu")
            print("1. Create Order")
            print("2. View Sales Reports")
            print("3. Check Product Availability")
            print("4. Back to Main Menu")
            choice = input("Enter choice: ")
            if choice == '1':
                self.create_order()
            elif choice == '2':
                timeframe = input("Enter timeframe (daily/weekly/monthly/yearly): ").strip().lower()
                self.generate_report(timeframe)
            elif choice == '3':
                self.check_product_availability()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
