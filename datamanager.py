import sqlite3
import csv
import threading
from datetime import datetime
import requests

class DataManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Set up the SQLite database and create required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    address TEXT,
                    ssn TEXT,
                    phone TEXT,
                    email TEXT,
                    employment_type TEXT,
                    job_title TEXT,
                    department TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    federal_w4 TEXT,
                    state_tax_form TEXT,
                    hourly_rate REAL,
                    annual_salary REAL,
                    overtime_rate REAL,
                    commission REAL,
                    pay_frequency TEXT
                    local_id TEXT,  -- Local identification number for international employees
                    work_permit_status TEXT,  -- Visa or work permit information
                    currency_preference TEXT  -- Preferred currency for payroll
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    product TEXT PRIMARY KEY, 
                    stock INTEGER, 
                    min_threshold INTEGER, 
                    price REAL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY, 
                    customer TEXT, 
                    product TEXT, 
                    quantity INTEGER, 
                    payment_type TEXT, 
                    discounted_amount REAL, 
                    date TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY, 
                    amount REAL, 
                    status TEXT
                )
            ''')
             # Create the time_logs table for clock-in/out, overtime, and time-off records
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS time_logs (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    date TEXT,
                    clock_in TEXT,
                    clock_out TEXT,
                    hours_worked REAL,
                    overtime_hours REAL,
                    time_off_requested REAL,
                    time_off_approved REAL,
                    status TEXT,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deductions (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    federal_tax_rate REAL,
                    fica_tax_rate REAL,
                    state_tax_rate REAL,
                    health_insurance REAL,
                    retirement_contribution REAL,
                    other_deductions REAL,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')
            # Table for payroll schedules
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payroll_schedule (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    pay_frequency TEXT,
                    next_pay_date TEXT,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')

            # Table for bank details (required for direct deposits)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bank_details (
                    employee_id INTEGER PRIMARY KEY,
                    bank_name TEXT,
                    account_number TEXT,
                    routing_number TEXT,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')

            # Table for payroll history records
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payroll_history (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    pay_date TEXT,
                    gross_pay REAL,
                    deductions REAL,
                    net_pay REAL,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')

            # Table for deductions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deductions (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    federal_tax_rate REAL,
                    fica_tax_rate REAL,
                    state_tax_rate REAL,
                    health_insurance REAL,
                    retirement_contribution REAL,
                    other_deductions REAL,
                    FOREIGN KEY(employee_id) REFERENCES employees(id)
                )
            ''')
             # Table for state-specific tax information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS state_tax (
                    state TEXT PRIMARY KEY,
                    income_tax_rate REAL,
                    sui_rate REAL,  -- State Unemployment Insurance rate
                    local_tax_rate REAL DEFAULT 0.0  -- Optional local tax rate
                )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS state_overtime_rules (
                state TEXT PRIMARY KEY,
                daily_overtime_threshold INTEGER DEFAULT 8,
                doubletime_threshold INTEGER DEFAULT 12,
                weekly_overtime_threshold INTEGER DEFAULT 40,
                overtime_rate REAL DEFAULT 1.5,
                doubletime_rate REAL DEFAULT 2.0
            )
        ''')

            # Table to track leave balances for each employee
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS leave_balances (
                employee_id INTEGER PRIMARY KEY,
                sick_leave REAL DEFAULT 0,
                family_leave REAL DEFAULT 0,
                other_leave REAL DEFAULT 0,
                FOREIGN KEY(employee_id) REFERENCES employees(id)
            )
        ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_reciprocity (
                home_state TEXT,
                work_state TEXT,
                UNIQUE(home_state, work_state)
            )
        ''')
            # Table to store country-specific tax information
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS country_tax (
                country_code TEXT PRIMARY KEY,
                income_tax_rate REAL,
                social_contribution_rate REAL,
                expatriate_tax_rate REAL DEFAULT 0.0  -- Additional rate for expatriates
            )
        ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS time_off_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    reason TEXT,
                    status TEXT DEFAULT 'Pending',
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS state_minimum_wages (
                    state TEXT PRIMARY KEY,
                    minimum_wage REAL
                )
            ''')
            conn.commit()

    def add_employee(self, employee_data):
        """Add a new employee to the database with error handling."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO employees (
                    full_name, address, ssn, phone, email, employment_type, 
                    job_title, department, start_date, end_date, 
                    federal_w4, state_tax_form,local_id, work_permit_status, currency_preference
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
            ''', (
                employee_data["full_name"],
                employee_data["address"],
                employee_data["ssn"],
                employee_data["phone"],
                employee_data["email"],
                employee_data["employment_type"],
                employee_data["job_title"],
                employee_data["department"],
                employee_data["start_date"],
                employee_data.get("end_date"),        # Optional field
                employee_data.get("federal_w4"),      # Optional field
                employee_data.get("state_tax_form"),   # Optional field
                employee_data.get("local_id"),
                employee_data.get("work_permit_status"),
                employee_data.get("currency_preference")
            ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding employee: {e}")

    def get_employee_by_id(self, employee_id):
        """Retrieve employee data by ID from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
            row = cursor.fetchone()
            if row:
                # Assuming columns are in the correct order; match them to the Employee fields
                return {
                    "id": row[0],
                    "full_name": row[1],
                    "address": row[2],
                    "ssn": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "employment_type": row[6],
                    "job_title": row[7],
                    "department": row[8],
                    "start_date": row[9],
                    "end_date": row[10],
                    "federal_w4": row[11],
                    "state_tax_form": row[12],
                    "hourly_rate": row[13],
                    "annual_salary": row[14],
                    "overtime_rate": row[15],
                    "commission": row[16],
                    "pay_frequency": row[17]
                }
            return None

    def get_all_employees(self):
        """Retrieve all employee records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            return cursor.fetchall()

    def add_inventory_item(self, product, stock, min_threshold, price):
        """Add a new inventory item or update stock if it exists, with error handling."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO inventory (product, stock, min_threshold, price) VALUES (?, ?, ?, ?)",
                    (product, stock, min_threshold, price)
                )
                conn.commit()
        except sqlite3.IntegrityError:
            self.update_stock(product, stock)

    def get_inventory(self):
        """Retrieve all inventory records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT product, stock, min_threshold, price FROM inventory")
            return [(row[0], int(row[1]), int(row[2]), float(row[3])) for row in cursor.fetchall()]

    def get_time_logs_for_employee(self, employee_id, start_date=None, end_date=None):
        """Retrieve time logs for an employee, optionally within a specified date range."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute('''
                    SELECT date, clock_in, clock_out, hours_worked, overtime_hours, time_off_requested, time_off_approved, status
                    FROM time_logs
                    WHERE employee_id = ? AND date BETWEEN ? AND ?
                ''', (employee_id, start_date, end_date))
            else:
                cursor.execute('''
                    SELECT date, clock_in, clock_out, hours_worked, overtime_hours, time_off_requested, time_off_approved, status
                    FROM time_logs
                    WHERE employee_id = ?
                ''', (employee_id,))
            
            return [{"date": row[0], "clock_in": row[1], "clock_out": row[2], "hours_worked": row[3],
                     "overtime_hours": row[4], "time_off_requested": row[5], "time_off_approved": row[6],
                     "status": row[7]} for row in cursor.fetchall()]

    def add_time_log(self, employee_id, date, clock_in=None, clock_out=None, hours_worked=0, overtime_hours=0):
        """Insert a new time log for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO time_logs (employee_id, date, clock_in, clock_out, hours_worked, overtime_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (employee_id, date, clock_in, clock_out, hours_worked, overtime_hours))
            conn.commit()

    def get_time_log_by_date(self, employee_id, date):
        """Retrieve the time log for a specific employee on a specific date."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM time_logs WHERE employee_id = ? AND date = ?", (employee_id, date))
            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            return None

    def update_clock_out(self, employee_id, date, clock_out, hours_worked, overtime_hours):
        """Update the clock-out time and hours worked for a specific time log."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE time_logs 
                SET clock_out = ?, hours_worked = ?, overtime_hours = ? 
                WHERE employee_id = ? AND date = ?
            ''', (clock_out, hours_worked, overtime_hours, employee_id, date))
            conn.commit()
            
    def update_stock(self, product, quantity):
        """Update the stock level for a given product."""
        quantity = int(quantity)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET stock = stock + ? WHERE product = ?", (quantity, product))
            conn.commit()
        print(f"Stock for {product} updated by {quantity}.")

    def check_stock(self, product):
        """Check the stock level for a specific product."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM inventory WHERE product = ?", (product,))
            stock = cursor.fetchone()
            return stock[0] if stock else 0

    def get_product_price(self, product):
        """Retrieve product price from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM inventory WHERE product = ?", (product,))
            result = cursor.fetchone()
            return result[0] if result else None

    def save_order(self, order_data):
        """Save a new order to the database with discount application and real-time stock check."""
        # Ensure product price is available in order_data
        if "product_price" not in order_data:
            order_data["product_price"] = self.get_product_price(order_data["product"])
            if order_data["product_price"] is None:
                print("Error: Product price not found.")
                return

        # Apply discounts based on order criteria
        order_data["discounted_amount"] = self.apply_discounts(order_data)
        
        def save():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO orders (customer, product, quantity, payment_type, discounted_amount, date) VALUES (?, ?, ?, ?, ?, ?)",
                    (order_data["customer"], order_data["product"], order_data["quantity"], 
                     order_data["payment_type"], order_data["discounted_amount"], 
                     datetime.now().strftime('%Y-%m-%d'))
                )
                conn.commit()
            # Update stock after saving order
            self.update_stock(order_data["product"], -order_data["quantity"])
        
        threading.Thread(target=save).start()

    def apply_discounts(self, order_data):
        """Apply discounts based on order criteria (e.g., amount thresholds, promotions, and date-sensitive discounts)."""
        discount = 0
        today = datetime.now().date()
        product_price = order_data["product_price"]  # Use the actual product price

        # Basic discounts
        if order_data["quantity"] > 5:
            discount = 0.10  # 10% discount for bulk orders
        if order_data["customer"] == "returning":
            discount += 0.05  # Additional 5% for returning customers

        # Date-sensitive discounts
        black_friday = datetime(today.year, 11, 24).date()
        holiday_season_start = datetime(today.year, 12, 20).date()
        holiday_season_end = datetime(today.year, 12, 31).date()

        if today == black_friday:
            discount += 0.20
        elif holiday_season_start <= today <= holiday_season_end:
            discount += 0.15

        # Calculate the discounted amount based on actual product price
        total_cost = order_data["quantity"] * product_price
        discounted_amount = total_cost * (1 - discount)

        return discounted_amount

    def sync_inventory_from_csv(self, file_path):
        """Load inventory data from a CSV file into the database with error handling."""
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = row['product']
                    stock = int(row['stock'])
                    min_threshold = int(row['min_threshold'])
                    price = float(row['price'])
                    self.add_inventory_item(product, stock, min_threshold, price)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")

    def save_inventory_to_csv(self, file_path):
        """Save current inventory data from the database to a CSV file."""
        inventory = self.get_inventory()
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['product', 'stock', 'min_threshold', 'price'])
                for item in inventory:
                    writer.writerow(item)
        except IOError as e:
            print(f"Error writing to CSV file: {e}")

    def sync_orders_from_csv(self, file_path):
        """Load order data from a CSV file into the database with error handling."""
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customer = row['customer']
                    product = row['product']
                    quantity = int(row['quantity'])
                    payment_type = row['payment_type']
                    discounted_amount = float(row['discounted_amount'])
                    order_data = {
                        "customer": customer,
                        "product": product,
                        "quantity": quantity,
                        "payment_type": payment_type,
                        "discounted_amount": discounted_amount,
                        "product_price": self.get_product_price(product)
                    }
                    if order_data["product_price"] is not None:
                        self.save_order(order_data)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")

    def save_orders_to_csv(self, file_path):
        """Save current order data from the database to a CSV file."""
        orders = self.load_orders()
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'customer', 'product', 'quantity', 'payment_type', 'discounted_amount', 'date'])
                for order in orders:
                    writer.writerow(order)
        except IOError as e:
            print(f"Error writing to CSV file: {e}")

    def load_orders(self):
        """Retrieve all order records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            return cursor.fetchall()

    def load_payments(self):
        """Retrieve all payment records from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments")
            return cursor.fetchall()

    def add_time_log(self, employee_id, date, clock_in=None, clock_out=None, hours_worked=0, overtime_hours=0):
        """Insert a new time log for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO time_logs (employee_id, date, clock_in, clock_out, hours_worked, overtime_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (employee_id, date, clock_in, clock_out, hours_worked, overtime_hours))
            conn.commit()

    def update_clock_out(self, employee_id, date, clock_out, hours_worked, overtime_hours):
        """Update the clock-out time and hours worked for a specific time log."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE time_logs 
                SET clock_out = ?, hours_worked = ?, overtime_hours = ? 
                WHERE employee_id = ? AND date = ?
            ''', (clock_out, hours_worked, overtime_hours, employee_id, date))
            conn.commit()

    def request_time_off(self, employee_id, start_date, end_date, reason):
        """Record a time-off request for the employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO time_off_requests (employee_id, start_date, end_date, reason, status)
                VALUES (?, ?, ?, ?, 'Pending')
            ''', (employee_id, start_date, end_date, reason))
            conn.commit()

    def approve_time_off(self, time_log_id, hours_approved):
        """Approve a time-off request by updating the status and approved hours."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE time_logs 
                SET time_off_approved = ?, status = 'Approved' 
                WHERE id = ?
            ''', (hours_approved, time_log_id))
            conn.commit()

    def set_deductions(self, employee_id, federal_tax_rate, fica_tax_rate, state_tax_rate,
                       health_insurance, retirement_contribution, other_deductions):
        """Set or update deductions for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # First, try to update an existing record
            cursor.execute('''
                UPDATE deductions
                SET federal_tax_rate = ?, fica_tax_rate = ?, state_tax_rate = ?,
                    health_insurance = ?, retirement_contribution = ?, other_deductions = ?
                WHERE employee_id = ?
            ''', (federal_tax_rate, fica_tax_rate, state_tax_rate,
                  health_insurance, retirement_contribution, other_deductions, employee_id))

            # Check if the update affected any rows
            if cursor.rowcount == 0:
                # If no rows were updated, insert a new record
                cursor.execute('''
                    INSERT INTO deductions (employee_id, federal_tax_rate, fica_tax_rate, state_tax_rate,
                                            health_insurance, retirement_contribution, other_deductions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (employee_id, federal_tax_rate, fica_tax_rate, state_tax_rate,
                      health_insurance, retirement_contribution, other_deductions))

            conn.commit()

    def get_deductions(self, employee_id):
        """Retrieve deductions for a specific employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deductions WHERE employee_id = ?", (employee_id,))
            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            return None

    def add_bank_details(self, employee_id, bank_name, account_number, routing_number):
        """Add or update bank details for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bank_details (employee_id, bank_name, account_number, routing_number)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(employee_id) DO UPDATE SET
                    bank_name = excluded.bank_name,
                    account_number = excluded.account_number,
                    routing_number = excluded.routing_number
            ''', (employee_id, bank_name, account_number, routing_number))
            conn.commit()

    def record_payroll(self, employee_id, pay_date, gross_pay, deductions, net_pay):
        """Record a payroll transaction in payroll history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO payroll_history (employee_id, pay_date, gross_pay, deductions, net_pay)
                VALUES (?, ?, ?, ?, ?)
            ''', (employee_id, pay_date, gross_pay, deductions, net_pay))
            conn.commit()

    def get_employee_id_by_ssn(self, ssn):
        """Retrieve the employee ID based on the SSN."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM employees WHERE ssn = ?", (ssn,))
            result = cursor.fetchone()
            return result[0] if result else None

    def update_compensation(self, employee_id, hourly_rate=None, annual_salary=None, pay_frequency=None):
        """Update compensation details for an employee based on the employment type."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if hourly_rate is not None:
                cursor.execute("UPDATE employees SET hourly_rate = ? WHERE id = ?", (hourly_rate, employee_id))
            if annual_salary is not None:
                cursor.execute("UPDATE employees SET annual_salary = ? WHERE id = ?", (annual_salary, employee_id))
            if pay_frequency is not None:
                cursor.execute("UPDATE employees SET pay_frequency = ? WHERE id = ?", (pay_frequency, employee_id))
            conn.commit()

    def set_payroll_schedule(self, employee_id, pay_frequency, next_pay_date):
        """Set or update the payroll schedule for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Attempt to update an existing record
            cursor.execute('''
                UPDATE payroll_schedule
                SET pay_frequency = ?, next_pay_date = ?
                WHERE employee_id = ?
            ''', (pay_frequency, next_pay_date, employee_id))

            # If no rows were updated, insert a new record
            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT INTO payroll_schedule (employee_id, pay_frequency, next_pay_date)
                    VALUES (?, ?, ?)
                ''', (employee_id, pay_frequency, next_pay_date))

            conn.commit()

    def get_payroll_history(self, employee_id):
        """Retrieve payroll history for a specific employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pay_date, gross_pay, deductions, net_pay
                FROM payroll_history
                WHERE employee_id = ?
                ORDER BY pay_date DESC
            ''', (employee_id,))
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def set_state_tax(self, state, income_tax_rate, sui_rate, local_tax_rate=0.0):
        """Set or update tax rates for a specific state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO state_tax (state, income_tax_rate, sui_rate, local_tax_rate)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(state) DO UPDATE SET
                    income_tax_rate = excluded.income_tax_rate,
                    sui_rate = excluded.sui_rate,
                    local_tax_rate = excluded.local_tax_rate
            ''', (state, income_tax_rate, sui_rate, local_tax_rate))
            conn.commit()

    def get_state_tax_rates(self, state):
        """Retrieve state and local tax rates for a given state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT income_tax_rate, sui_rate, local_tax_rate
                FROM state_tax
                WHERE state = ?
            ''', (state,))
            row = cursor.fetchone()
            if row:
                return {
                    "income_tax_rate": row[0],
                    "sui_rate": row[1],
                    "local_tax_rate": row[2]
                }
            else:
                return {"income_tax_rate": 0.0, "sui_rate": 0.0, "local_tax_rate": 0.0}

    def get_federal_tax_rate(self):
        """Return the current federal income tax rate."""
        # Example: Replace with actual logic or a database call
        return 0.1  # 10%

    def get_fica_tax_rate(self):
        """Return the current FICA tax rate."""
        # Example: Replace with actual logic or a database call
        return 0.062  # 6.2% for Social Security

    def get_employee_deductions(self, employee_id):
        """Retrieve voluntary deductions for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT health_insurance, retirement_contribution, other_deductions
                FROM deductions
                WHERE employee_id = ?
            ''', (employee_id,))
            row = cursor.fetchone()
            return {
                "health_insurance": row[0] if row else 0.0,
                "retirement_contribution": row[1] if row else 0.0,
                "other_deductions": row[2] if row else 0.0
            }

    def get_overtime_rules(self, state):
        """Retrieve overtime rules for a specific state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT daily_overtime_threshold, doubletime_threshold, weekly_overtime_threshold,
                       overtime_rate, doubletime_rate
                FROM state_overtime_rules
                WHERE state = ?
            ''', (state,))
            row = cursor.fetchone()
            if row:
                return {
                    "daily_overtime_threshold": row[0],
                    "doubletime_threshold": row[1],
                    "weekly_overtime_threshold": row[2],
                    "overtime_rate": row[3],
                    "doubletime_rate": row[4]
                }
            else:
                # Default to standard weekly overtime if no state-specific rule exists
                return {
                    "daily_overtime_threshold": 8,
                    "doubletime_threshold": 12,
                    "weekly_overtime_threshold": 40,
                    "overtime_rate": 1.5,
                    "doubletime_rate": 2.0
                }

    def accrue_leave(self, employee_id, hours_worked):
        """Accrue leave for an employee based on state policy and hours worked."""
        employee_data = self.get_employee_by_id(employee_id)
        state = employee_data.get("state")
        leave_policy = self.get_leave_policy(state)

        # Calculate accrued leave
        sick_leave_accrued = hours_worked * leave_policy['sick_leave_rate']
        family_leave_accrued = hours_worked * leave_policy['family_leave_rate']

        # Update the employee's leave balances
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE leave_balances
                SET sick_leave = sick_leave + ?, family_leave = family_leave + ?
                WHERE employee_id = ?
            ''', (sick_leave_accrued, family_leave_accrued, employee_id))
            conn.commit()

    def get_leave_policy(self, state):
        """Retrieve leave accrual rates for a specific state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sick_leave_rate, family_leave_rate
                FROM state_leave_policies
                WHERE state = ?
            ''', (state,))
            row = cursor.fetchone()
            return {
                "sick_leave_rate": row[0] if row else 0.0,
                "family_leave_rate": row[1] if row else 0.0
            }

    def is_reciprocal_state(self, home_state, work_state):
        """Check if a reciprocity agreement exists between home and work states."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM tax_reciprocity
                WHERE home_state = ? AND work_state = ?
            ''', (home_state, work_state))
            return cursor.fetchone() is not None

    def set_country_tax(self, country_code, income_tax_rate, social_contribution_rate, expatriate_tax_rate=0.0):
        """Set or update tax information for a specific country."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO country_tax (country_code, income_tax_rate, social_contribution_rate, expatriate_tax_rate)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(country_code) DO UPDATE SET
                    income_tax_rate = excluded.income_tax_rate,
                    social_contribution_rate = excluded.social_contribution_rate,
                    expatriate_tax_rate = excluded.expatriate_tax_rate
            ''', (country_code, income_tax_rate, social_contribution_rate, expatriate_tax_rate))
            conn.commit()

    def get_country_tax_rates(self, country_code):
        """Retrieve tax rates for a specific country."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT income_tax_rate, social_contribution_rate, expatriate_tax_rate
                FROM country_tax
                WHERE country_code = ?
            ''', (country_code,))
            row = cursor.fetchone()
            return {
                "income_tax_rate": row[0] if row else 0.0,
                "social_contribution_rate": row[1] if row else 0.0,
                "expatriate_tax_rate": row[2] if row else 0.0
            }

    def fetch_and_update_exchange_rates(self, base_currency="USD"):
        """Fetch the latest exchange rates from an external API and update the database."""
        api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            rates = response.json().get("rates", {})
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for currency_code, rate in rates.items():
                    cursor.execute('''
                        INSERT INTO currency_rates (currency_code, exchange_rate, last_updated)
                        VALUES (?, ?, datetime('now'))
                        ON CONFLICT(currency_code) DO UPDATE SET
                            exchange_rate = excluded.exchange_rate,
                            last_updated = datetime('now')
                    ''', (currency_code, rate))
                conn.commit()
            print("Exchange rates successfully updated.")
        
        except requests.RequestException as e:
            print(f"Error fetching exchange rates: {e}")

    def update_tax_forms(self, employee_id, federal_form_path, state_form_path):
        """Update the federal and state tax form paths for an employee."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE employees
                SET federal_w4 = ?, state_tax_form = ?
                WHERE id = ?
            ''', (federal_form_path, state_form_path, employee_id))
            conn.commit()
        print(f"Tax forms updated for Employee ID {employee_id}.")

    def add_or_update_minimum_wage(self, state, minimum_wage):
        """Add or update the minimum wage for a given state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO state_minimum_wages (state, minimum_wage)
                VALUES (?, ?)
                ON CONFLICT(state) DO UPDATE SET minimum_wage = excluded.minimum_wage
            ''', (state, minimum_wage))
            conn.commit()

    def get_minimum_wage(self, state):
        """Retrieve the minimum wage for a given state."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT minimum_wage FROM state_minimum_wages WHERE state = ?', (state,))
            result = cursor.fetchone()
            return result[0] if result else None
