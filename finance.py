import openai
import csv
from datamanager import DataManager
from datetime import datetime

class Finance:
    def __init__(self):
        self.data_manager = DataManager()
        self.api_key_loaded = False  # Track if API key is loaded to avoid reloading

    def load_api_key(self):
        """Load the OpenAI API key from a file."""
        try:
            with open("api_key.txt", "r") as file:
                openai.api_key = file.read().strip()  # Read the key and remove any extra whitespace
            self.api_key_loaded = True
        except FileNotFoundError:
            print("Error: API key file not found. Ensure 'api_key.txt' is in the correct directory.")

    def reconcile_payments(self):
        """Reconcile payments from the payments database."""
        payments = self.data_manager.load_payments()
        for payment in payments:
            print(f"Reconciling Payment ID {payment[0]} - Status: {payment[2]}")

    def generate_financial_report(self, timeframe='daily'):
        """Generate a report of total revenue by specified timeframe."""
        orders = self.data_manager.load_orders()
        report_data = {}

        for order in orders:
            order_date = order[6]  # Assuming 'date' is the 7th column
            discounted_amount = float(order[5])  # Access the correct index for discounted amount

            # Determine the key based on the timeframe
            try:
                date_obj = datetime.strptime(order_date, '%Y-%m-%d')
                if timeframe == 'daily':
                    key = order_date
                elif timeframe == 'weekly':
                    key = date_obj.strftime("%Y-%U")  # Year-Week number
                elif timeframe == 'monthly':
                    key = date_obj.strftime("%Y-%m")  # Year-Month
                elif timeframe == 'yearly':
                    key = date_obj.strftime("%Y")  # Year
                else:
                    print("Invalid timeframe. Please select daily, weekly, monthly, or yearly.")
                    return

                report_data[key] = report_data.get(key, 0) + discounted_amount
            except ValueError:
                print(f"Invalid date format in order data: {order_date}")

        print(f"{timeframe.capitalize()} Financial Report:")
        for date, total in report_data.items():
            print(f"Date: {date}, Total Revenue: ${total:.2f}")


    def export_report_to_csv(self, report_data, timeframe='daily'):
        """Export the financial report data to a CSV file."""
        filename = f"{timeframe}_financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Total Revenue"])  # CSV header
                
                for date, total in report_data.items():
                    writer.writerow([date, f"{total:.2f}"])

            print(f"Report exported successfully to {filename}")
        except IOError as e:
            print(f"Error writing to CSV file: {e}")

    def ai_financial_forecast(self, file_path):
        """Generate a financial forecast using AI based on historical revenue data read from a CSV file."""
        if not self.api_key_loaded:
            self.load_api_key()
            if not openai.api_key:
                print("Unable to load API key. Financial forecast cannot be generated.")
                return

        historical_data = self.read_historical_data(file_path)
        if not historical_data:
            print("No historical data available for forecast.")
            return

        # Prepare the prompt for OpenAI
        prompt = "Based on the following historical revenue data, provide a financial forecast for the next month:\n"
        for date, total in historical_data.items():
            prompt += f"{date}: ${total:.2f}\n"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            forecast = response['choices'][0]['message']['content']
            print("AI Financial Forecast:")
            print(forecast)
        except openai.error.OpenAIError as e:
            print(f"Error generating forecast: {e}")

    def read_historical_data(self, file_path):
        """Read historical data from CSV file."""
        historical_data = {}
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order_date = row.get('date')
                    amount = row.get('discounted_amount')
                    if order_date and amount:
                        try:
                            historical_data[order_date] = historical_data.get(order_date, 0) + float(amount)
                        except ValueError:
                            print(f"Invalid amount in CSV: {amount} for date {order_date}")
            return historical_data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except ValueError:
            print("Invalid data format in the CSV file.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
        return None

    def menu(self):
        """Display the finance department menu."""
        while True:
            print("\nFinance Department Menu")
            print("1. Reconcile Payments")
            print("2. Generate Financial Report")
            print("3. Export Financial Report to CSV")
            print("4. Back to Main Menu")
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.reconcile_payments()
            elif choice == '2':
                timeframe = input("Enter timeframe (daily/weekly/monthly/yearly): ").strip().lower()
                report_data = self.generate_financial_report(timeframe)
            elif choice == '3':
                if 'report_data' in locals():
                    self.export_report_to_csv(report_data, timeframe)
                else:
                    print("Please generate a report first.")
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
