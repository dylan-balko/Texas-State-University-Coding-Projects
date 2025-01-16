import threading
import time
from datamanager import DataManager

class Inventory:
    def __init__(self):
        self.data_manager = DataManager()
        self.checking = threading.Event()  # Use Event for thread-safe checking flag
        self.checking.set()  # Set the flag to start monitoring
        self.monitor_thread = threading.Thread(target=self.monitor_stock_background)
        self.monitor_thread.start()  # Start the background stock checker

    def monitor_stock_background(self):
        """Continuously monitor stock levels in the background, checking every second."""
        try:
            while self.checking.is_set():  # Run as long as the flag is set
                self.monitor_stock()
                # Check every second to allow quick exit on stop
                for _ in range(100):  # Total 100 seconds with 1-second checks
                    if not self.checking.is_set():
                        return  # Exit if monitoring has been stopped
                    time.sleep(1)
        except Exception as e:
            print(f"Exception in monitoring thread: {e}")

    def monitor_stock(self):
        """Monitor stock levels and trigger restocks if necessary."""
        print("Monitoring stock levels...")
        inventory_items = self.data_manager.get_inventory()
        for item in inventory_items:
            product, stock, min_threshold, *_ = item  # Adjust tuple unpacking for compatibility
            if stock < min_threshold:
                self.trigger_restock(product)

    def trigger_restock(self, product_name):
        """Trigger a restock process for the specified product."""
        print(f"Triggering restock for {product_name}...")

    def view_stock_levels(self):
        """View current stock levels of all products."""
        print("Current Stock Levels:")
        inventory_items = self.data_manager.get_inventory()
        for item in inventory_items:
            product, stock, min_threshold, *_ = item
            print(f"Product: {product}, Stock: {stock}, Min Threshold: {min_threshold}")

    def restock_product(self):
        """Restock a specific product by entering the product name and amount, with error handling."""
        try:
            product_name = input("Enter the product name to restock: ")
            quantity = int(input("Enter the quantity to add: "))
            self.data_manager.update_stock(product_name, quantity)
            print(f"Restocked {quantity} units of {product_name}.")
        except ValueError:
            print("Invalid quantity. Please enter a valid integer.")

    def process_deliveries(self):
        """Process deliveries by adding stock from deliveries, with error handling."""
        try:
            product_name = input("Enter the product name for the delivery: ")
            quantity = int(input("Enter the quantity delivered: "))
            self.data_manager.update_stock(product_name, quantity)
            print(f"Processed delivery of {quantity} units of {product_name}.")
        except ValueError:
            print("Invalid quantity. Please enter a valid integer.")

    def process_delivery_report(self, file_path):
        """Parse a CSV delivery report and update stock levels based on the quantities delivered."""
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                
                # Ensure CSV has the expected columns
                if 'product' not in reader.fieldnames or 'quantity' not in reader.fieldnames:
                    print("CSV file format error: 'product' and 'quantity' columns required.")
                    return

                # Process each delivery entry
                for row in reader:
                    product = row['product']
                    quantity = int(row['quantity'])
                    
                    # Update the stock for each product in the database
                    self.data_manager.update_stock(product, quantity)
                    print(f"Updated stock for {product} with an additional {quantity} units.")
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except ValueError:
            print("Invalid quantity format in CSV file.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")

    def stop_monitoring(self):
        """Stop the background monitoring thread safely."""
        self.checking.clear()  # Clear the flag to stop monitoring
        self.monitor_thread.join()  # Ensure the thread exits cleanly
        print("Stopped background stock monitoring.")

    def calculate_restock_frequency(self, product_name):
        """Calculate a simple restock frequency for a product. Placeholder for demonstration."""
        # Placeholder logic; in a real scenario, this could be based on actual restock logs.
        restock_log = {
            "Laptop": 2,
            "Smartphone": 3,
            "Headphones": 1,
            "Keyboard": 4,
            "Monitor": 5,
            "USB Cable": 2
        }
        return restock_log.get(product_name, 0)  # Return the restock count or 0 if not found

    def generate_turnover_report(self):
        """Generate a report showing turnover based on current stock and restocking activity."""
        inventory_items = self.data_manager.get_inventory()
        print("Inventory Turnover Report:")
        
        for item in inventory_items:
            product, stock, min_threshold, *_ = item
            # Example placeholder logic; ideally, you'd track sales or usage frequency in a separate log
            restock_frequency = self.calculate_restock_frequency(product)
            print(f"Product: {product}, Stock: {stock}, Min Threshold: {min_threshold}, Restocks this month: {restock_frequency}")

    def menu(self):
        """Display the inventory department menu."""
        while True:
            print("\nInventory Department Menu")
            print("1. View Stock Levels")
            print("2. Restock Products")
            print("3. Process Deliveries")
            print("4. Process Supplier Delivery Report")  # New option for processing supplier report
            print("5. Generate Turnover Report")
            print("6. Back to Main Menu")
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.view_stock_levels()
            elif choice == '2':
                self.restock_product()
            elif choice == '3':
                self.process_deliveries()
            elif choice == '4':
                file_path = input("Enter the path to the delivery report CSV file: ").strip()
                self.process_delivery_report(file_path)  # Process the delivery report
            elif choice == '5':
                self.generate_turnover_report()
            elif choice == '6':
                break
            else:
                print("Invalid choice.")

