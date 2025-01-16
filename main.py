from datamanager import DataManager
from sales import Sales
from inventory import Inventory
from hr import HR
from finance import Finance
from employee_portal import EmployeePortal
import schedule


data_manager = DataManager()

def update_exchange_rates():
    data_manager.fetch_and_update_exchange_rates()

# Schedule the update to run daily
schedule.every().day.at("03:00").do(update_exchange_rates)

def add_sample_products():
    """Add sample products to the inventory for testing."""
    sample_products = [
        {"product": "Laptop", "stock": 15, "min_threshold": 10, "price": 1200.00},
        {"product": "Smartphone", "stock": 5, "min_threshold": 8, "price": 800.00},
        {"product": "Headphones", "stock": 25, "min_threshold": 5, "price": 150.00},
        {"product": "Keyboard", "stock": 2, "min_threshold": 5, "price": 75.00},
        {"product": "Monitor", "stock": 0, "min_threshold": 3, "price": 300.00},
        {"product": "USB Cable", "stock": 50, "min_threshold": 10, "price": 10.00},
    ]

    print("Adding sample products to the inventory...")
    for product in sample_products:
        try:
            data_manager.add_inventory_item(
                product['product'], 
                product['stock'], 
                product['min_threshold'], 
                product['price']
            )
            print(f"Added product to inventory: {product}")
        except Exception as e:
            print(f"Error adding product {product['product']}: {e}")

def main_menu():
    """Display the main menu for department selection."""
    hr = HR()
    finance = Finance()
    inventory = Inventory()
    sales = Sales()

    while True:
        print("\nWelcome to OptimaCorp Operations System")
        print("1. HR Department")
        print("2. Employee Portal")
        print("3. Finance Department")
        print("4. Inventory Department")
        print("5. Sales Department")
        print("6. Exit")
        choice = input("Select department (1-6): ")

        if choice == '1':
            hr.menu()
        elif choice == '2':
            employee_id = input("Enter your Employee ID to access the Employee Portal: ")
            employee_portal = EmployeePortal(employee_id)
            employee_portal.menu(employee_id)
        elif choice == '3':
            finance.menu()
        elif choice == '4':
            inventory.menu()
        elif choice == '5':
            sales.menu()
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    # Add sample products to the inventory
    add_sample_products()
    main_menu()
