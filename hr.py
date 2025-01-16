import openai
from datamanager import DataManager
from employee import Employee
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class HR:
    def __init__(self):
        self.data_manager = DataManager()
        self.api_key_loaded = False  # Track if API key is loaded

    def load_api_key(self):
        """Load the OpenAI API key from a file."""
        if not self.api_key_loaded:
            try:
                with open("api_key.txt", "r") as file:
                    openai.api_key = file.read().strip()  # Read the key and remove any extra whitespace
                self.api_key_loaded = True
            except FileNotFoundError:
                print("Error: API key file not found. Ensure 'api_key.txt' is in the correct directory.")

    def add_employee(self):
        """Prompt and validate new employee information before adding to the system."""
        try:
            full_name = input("Employee Full Name: ")
            address = input("Address: ")
            ssn = input("SSN: ")
            phone = input("Phone Number: ")
            email = input("Email Address: ")
            employment_type = input("Employment Type (hourly/salaried): ").strip().lower()
            job_title = input("Job Title: ")
            department = input("Department: ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (optional, YYYY-MM-DD): ") or None
            federal_w4 = input("Federal W-4 Form File Path: ")
            state_tax_form = input("State-Specific Tax Form File Path (optional): ") or None
            
            # Payroll frequency setup during employee addition
            pay_frequency = input("Enter Payroll Frequency (weekly/biweekly/monthly): ").strip().lower()
            next_pay_date = input("Enter Next Pay Date (YYYY-MM-DD): ")
            local_id = input("Local ID (for international employees): ")
            work_permit_status = input("Work Permit Status (valid/expired): ")
            currency_preference = input("Currency Preference (e.g., USD, EUR): ").upper()

            # Validate date formats
            datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                datetime.strptime(end_date, "%Y-%m-%d")
            datetime.strptime(next_pay_date, "%Y-%m-%d")

            # Create the employee record in the database
            employee_data = {
                "full_name": full_name,
                "address": address,
                "ssn": ssn,
                "phone": phone,
                "email": email,
                "employment_type": employment_type,
                "job_title": job_title,
                "department": department,
                "start_date": start_date,
                "end_date": end_date,
                "federal_w4": federal_w4,
                "state_tax_form": state_tax_form,
                "local_id": local_id,
                "work_permit_status": work_permit_status,
                "currency_preference": currency_preference
            }
            self.data_manager.add_employee(employee_data)
            print(f"Employee '{full_name}' added successfully.")

            # Set payroll schedule immediately after adding employee
            employee_id = self.data_manager.get_employee_id_by_ssn(ssn)
            self.data_manager.set_payroll_schedule(employee_id, pay_frequency, next_pay_date)
            print(f"Payroll schedule set for Employee ID {employee_id}.")

        except ValueError as e:
            print(f"Error: {e}")

    def set_compensation(self):
        """Set or update compensation information for an employee."""
        try:
            employee_id = int(input("Enter Employee ID: "))
            employee_data = self.data_manager.get_employee_by_id(employee_id)

            if not employee_data:
                print("Employee not found.")
                return

            # Prompt for compensation details
            employment_type = employee_data.get("employment_type")
            if employment_type == "hourly":
                hourly_rate = float(input("Enter Hourly Rate: "))
                self.data_manager.update_compensation(employee_id, hourly_rate=hourly_rate)
                print(f"Updated hourly rate for Employee ID {employee_id}.")
            elif employment_type == "salaried":
                annual_salary = float(input("Enter Annual Salary: "))
                pay_frequency = input("Enter Pay Frequency (weekly/biweekly/monthly): ").strip().lower()
                self.data_manager.update_compensation(employee_id, annual_salary=annual_salary, pay_frequency=pay_frequency)
                print(f"Updated annual salary and pay frequency for Employee ID {employee_id}.")
            else:
                print("Unknown employment type. Cannot set compensation.")
        except ValueError:
            print("Invalid input. Please enter valid compensation details.")

    def calculate_bonus(self, role, salary):
        """Calculate bonuses based on role and salary."""
        # Bonus rates by role
        bonus_rates = {
            "Manager": 0.10,  # 10% bonus for managers
            "Sales": 0.05     # 5% bonus for sales
        }
        return salary * bonus_rates.get(role, 0)  # Default to 0 if role not in dictionary

    def generate_bonus_insight(self):
        """Generate AI insights for employee bonuses based on performance."""
        self.load_api_key()
        if not openai.api_key:
            print("Unable to load API key. Bonus insight generation cannot proceed.")
            return

        employees = self.data_manager.get_all_employees()
        if not employees:
            print("No employees found to generate bonus insights.")
            return

        for emp in employees:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user",
                        "content": f"Suggest a bonus for {emp[1]}, who is a {emp[2]} in {emp[3]} with a salary of {emp[4]}."
                    }]
                )
                # Extract the insight from the response, if available
                insight = response['choices'][0]['message']['content'] if response['choices'] else "No insight available"
                print(f"Bonus Insight for {emp[1]}: {insight}")
            except openai.error.OpenAIError as e:
                print(f"Error generating insight for {emp[1]}: {e}")
            except (IndexError, KeyError):
                print(f"Unexpected response format from OpenAI API for {emp[1]}.")

    def approve_time_off(self, time_log_id, hours_approved):
        """Approve time-off request."""
        self.data_manager.approve_time_off(time_log_id, hours_approved)
        print(f"Time-off request {time_log_id} approved for {hours_approved} hours.")


    def view_employee_time_logs(self, employee_id):
        """View all time logs for a specific employee."""
        time_logs = self.data_manager.get_time_logs_for_employee(employee_id)
        if not time_logs:
            print("No time logs found for this employee.")
            return
        print(f"Time Logs for Employee ID {employee_id}:")
        for log in time_logs:
            print(f"Date: {log['date']}, Clock In: {log['clock_in']}, Clock Out: {log['clock_out']}, "
                  f"Hours Worked: {log['hours_worked']}, Overtime Hours: {log['overtime_hours']}, "
                  f"Time Off Requested: {log['time_off_requested']}, Time Off Approved: {log['time_off_approved']}, "
                  f"Status: {log['status']}")
            
    def set_employee_deductions(self):
        """Set or update the deduction rates for an employee."""
        employee_id = int(input("Enter Employee ID: "))
        federal_tax_rate = float(input("Enter Federal Tax Rate (% as decimal, e.g., 0.10 for 10%): "))
        fica_tax_rate = 0.0765  # FICA rate is 7.65%
        state_tax_rate = float(input("Enter State Tax Rate (if applicable): ") or "0")
        health_insurance = float(input("Enter Health Insurance Deduction: ") or "0")
        retirement_contribution = float(input("Enter Retirement Contribution Deduction: ") or "0")
        other_deductions = float(input("Enter Other Deductions: ") or "0")

        self.data_manager.set_deductions(
            employee_id, federal_tax_rate, fica_tax_rate, state_tax_rate, 
            health_insurance, retirement_contribution, other_deductions
        )
        print(f"Deductions set for Employee ID {employee_id}.")

    def apply_overtime(self, employee_id, total_hours_worked, daily_hours):
        """Calculate adjusted pay with overtime based on state rules and hours worked."""
        employee_data = self.data_manager.get_employee_by_id(employee_id)
        state = employee_data.get("state")
        overtime_rules = self.data_manager.get_overtime_rules(state)
        
        # Overtime calculations
        regular_hours = 0
        overtime_hours = 0
        doubletime_hours = 0

        # Daily overtime calculation
        for hours in daily_hours:
            if hours > overtime_rules["doubletime_threshold"]:
                doubletime_hours += hours - overtime_rules["doubletime_threshold"]
                overtime_hours += overtime_rules["doubletime_threshold"] - overtime_rules["daily_overtime_threshold"]
                regular_hours += overtime_rules["daily_overtime_threshold"]
            elif hours > overtime_rules["daily_overtime_threshold"]:
                overtime_hours += hours - overtime_rules["daily_overtime_threshold"]
                regular_hours += overtime_rules["daily_overtime_threshold"]
            else:
                regular_hours += hours

        # Weekly overtime calculation
        weekly_overtime_hours = max(0, total_hours_worked - overtime_rules["weekly_overtime_threshold"])
        regular_hours = min(regular_hours, overtime_rules["weekly_overtime_threshold"])

        # Adjust overtime hours
        if weekly_overtime_hours > overtime_hours:
            overtime_hours = weekly_overtime_hours
        
        return {
            "regular_hours": regular_hours,
            "overtime_hours": overtime_hours,
            "doubletime_hours": doubletime_hours,
            "overtime_rate": overtime_rules["overtime_rate"],
            "doubletime_rate": overtime_rules["doubletime_rate"]
        }

    def calculate_net_pay(self, employee_id, gross_pay, total_hours_worked, daily_hours, leave_hours=0):
        """Calculate net pay, including state and country taxes, reciprocity, and overtime adjustments."""

        # Retrieve employee data
        employee_data = self.data_manager.get_employee_by_id(employee_id)
        home_state = employee_data.get("home_state")
        work_state = employee_data.get("work_state")
        country_code = employee_data.get("country_code")
        is_expatriate = employee_data.get("is_expatriate", False)

        # Calculate base hourly rate
        hourly_rate = gross_pay / total_hours_worked

        # Minimum wage check (using home state as default)
        minimum_wage = self.data_manager.get_minimum_wage(home_state)
        if minimum_wage and hourly_rate < minimum_wage:
            hourly_rate = minimum_wage
            print(f"Adjusted hourly rate to minimum wage for {home_state}: ${hourly_rate:.2f}")

        # Adjusted gross pay with leave and overtime
        leave_pay = leave_hours * hourly_rate
        adjusted_gross_pay = gross_pay + leave_pay

        # Apply overtime adjustments
        overtime_data = self.apply_overtime(employee_id, total_hours_worked, daily_hours)
        overtime_pay = (
            overtime_data["overtime_hours"] * hourly_rate * overtime_data["overtime_rate"] +
            overtime_data["doubletime_hours"] * hourly_rate * overtime_data["doubletime_rate"]
        )
        adjusted_gross_pay = (overtime_data["regular_hours"] * hourly_rate) + overtime_pay

        # Country-specific tax calculations
        tax_rates = self.data_manager.get_country_tax_rates(country_code)
        income_tax = adjusted_gross_pay * tax_rates.get("income_tax_rate", 0)
        social_contribution = adjusted_gross_pay * tax_rates.get("social_contribution_rate", 0)
        expatriate_tax = adjusted_gross_pay * tax_rates.get("expatriate_tax_rate", 0) if is_expatriate else 0

        # State tax with reciprocity
        if self.data_manager.is_reciprocal_state(home_state, work_state):
            state_tax_data = self.data_manager.get_state_tax_rates(home_state)
        else:
            home_state_tax_data = self.data_manager.get_state_tax_rates(home_state)
            work_state_tax_data = self.data_manager.get_state_tax_rates(work_state)
            state_tax_data = {
                "income_tax_rate": home_state_tax_data.get("income_tax_rate", 0) + work_state_tax_data.get("income_tax_rate", 0),
                "sui_rate": home_state_tax_data.get("sui_rate", 0) + work_state_tax_data.get("sui_rate", 0),
                "local_tax_rate": home_state_tax_data.get("local_tax_rate", 0) + work_state_tax_data.get("local_tax_rate", 0)
            }

        # Calculate state and local taxes
        state_tax = adjusted_gross_pay * state_tax_data.get("income_tax_rate", 0)
        sui_tax = adjusted_gross_pay * state_tax_data.get("sui_rate", 0)
        local_tax = adjusted_gross_pay * state_tax_data.get("local_tax_rate", 0)

        # Federal and FICA taxes
        federal_tax = adjusted_gross_pay * self.data_manager.get_federal_tax_rate()
        fica_tax = adjusted_gross_pay * self.data_manager.get_fica_tax_rate()

        # Voluntary deductions
        voluntary_deductions = self.data_manager.get_employee_deductions(employee_id)
        total_voluntary_deductions = sum(voluntary_deductions.values())

        # Calculate total deductions and net pay
        total_deductions = (
            federal_tax + fica_tax + state_tax + sui_tax + local_tax +
            income_tax + social_contribution + expatriate_tax + total_voluntary_deductions
        )
        net_pay = adjusted_gross_pay - total_deductions

        # Output breakdown for debugging or logging
        print(f"Adjusted Gross Pay: ${adjusted_gross_pay:.2f}")
        print(f"Federal Tax: ${federal_tax:.2f}, FICA Tax: ${fica_tax:.2f}")
        print(f"Income Tax: ${income_tax:.2f}, Social Contribution: ${social_contribution:.2f}, Expatriate Tax: ${expatriate_tax:.2f}")
        print(f"State Tax: ${state_tax:.2f}, SUI Tax: ${sui_tax:.2f}, Local Tax: ${local_tax:.2f}")
        print(f"Total Deductions: ${total_deductions:.2f}")
        print(f"Net Pay: ${net_pay:.2f}")

        return net_pay


    def log_payroll(self):
        """Process payroll for an employee based on employment type and applicable deductions."""
        try:
            employee_id = int(input("Enter Employee ID: "))
            pay_date = input("Enter Pay Date (YYYY-MM-DD): ")

            # Validate pay date format
            pay_date_obj = datetime.strptime(pay_date, "%Y-%m-%d")

            # Retrieve employee information
            employee_data = self.data_manager.get_employee_by_id(employee_id)
            if not employee_data:
                print("Employee not found.")
                return

            employment_type = employee_data.get("employment_type")
            pay_frequency = employee_data.get("pay_frequency")

            # Calculate start and end of pay period based on pay frequency
            start_date, end_date = self.calculate_pay_period(pay_date_obj, pay_frequency)

            if employment_type == "hourly":
                gross_pay = self.calculate_hourly_gross_pay(employee_id, start_date, end_date, employee_data)
            elif employment_type == "salaried":
                gross_pay = self.calculate_salaried_gross_pay(employee_data)
            else:
                print("Unknown employment type.")
                return

            if gross_pay is None:
                return  # Exit if gross pay calculation failed

            # Calculate net pay after applying deductions
            net_pay = self.calculate_net_pay(employee_id, gross_pay)
            deductions = gross_pay - net_pay
            print(f"Total Deductions: ${deductions:.2f}, Net Pay: ${net_pay:.2f}")

            # Record payroll in payroll history
            self.data_manager.record_payroll(employee_id, pay_date, gross_pay, deductions, net_pay)
            print(f"Payroll recorded for Employee ID {employee_id}.")

        except ValueError as e:
            print(f"Invalid input: {e}")

    def calculate_pay_period(self, pay_date, pay_frequency):
        """Calculate the start and end dates of the pay period based on the pay frequency."""
        if pay_frequency == "weekly":
            start_date = pay_date - timedelta(weeks=1)
            end_date = pay_date
        elif pay_frequency == "biweekly":
            start_date = pay_date - timedelta(weeks=2)
            end_date = pay_date
        elif pay_frequency == "monthly":
            start_date = pay_date - relativedelta(months=1)
            end_date = pay_date
        else:
            print("Unknown pay frequency.")
            return None, None

        print(f"Calculated Pay Period: {start_date.date()} to {end_date.date()}")
        return start_date.date(), end_date.date()

    def calculate_hourly_gross_pay(self, employee_id, start_date, end_date, employee_data):
        """Calculate gross pay for an hourly employee based on time worked and overtime."""
        hourly_rate = employee_data.get("hourly_rate")
        if hourly_rate is None:
            print("Hourly rate is missing for this employee.")
            return None

        # Calculate total hours worked and overtime hours based on time logs within the pay period
        total_hours, overtime_hours = self.calculate_hours_worked(employee_id, start_date, end_date)
        if total_hours == 0:
            print("No hours worked in this pay period.")
            return None

        # Calculate gross pay (including overtime at 1.5x rate for overtime hours)
        gross_pay = (total_hours * hourly_rate) + (overtime_hours * hourly_rate * 1.5)
        print(f"Total Hours: {total_hours}, Overtime Hours: {overtime_hours}, Gross Pay: ${gross_pay:.2f}")
        return gross_pay

    def calculate_salaried_gross_pay(self, employee_data):
        """Calculate gross pay for a salaried employee based on pay frequency."""
        annual_salary = employee_data.get("annual_salary")
        pay_frequency = employee_data.get("pay_frequency")  # Assume values like 'monthly', 'biweekly'

        if annual_salary is None or pay_frequency is None:
            print("Annual salary or pay frequency is missing for this employee.")
            return None

        # Calculate gross pay based on pay frequency
        if pay_frequency == "monthly":
            gross_pay = annual_salary / 12
        elif pay_frequency == "biweekly":
            gross_pay = annual_salary / 26
        elif pay_frequency == "weekly":
            gross_pay = annual_salary / 52
        else:
            print("Unknown pay frequency.")
            return None

        print(f"Pay Frequency: {pay_frequency.capitalize()}, Gross Pay: ${gross_pay:.2f}")
        return gross_pay

    def update_payroll_schedule(self):
        """Update the payroll schedule for an existing employee."""
        try:
            employee_id = int(input("Enter Employee ID to update payroll schedule: "))
            pay_frequency = input("Enter New Payroll Frequency (weekly/biweekly/monthly): ").strip().lower()
            next_pay_date = input("Enter Next Pay Date (YYYY-MM-DD): ")

            # Validate the date format
            datetime.strptime(next_pay_date, "%Y-%m-%d")

            self.data_manager.set_payroll_schedule(employee_id, pay_frequency, next_pay_date)
            print(f"Updated payroll schedule for Employee ID {employee_id}.")
        except ValueError:
            print("Invalid input. Please enter a valid Employee ID and date in the format YYYY-MM-DD.")

    def add_bank_details(self):
        """Add or update bank details for an employee."""
        try:
            employee_id = int(input("Enter Employee ID: "))
            bank_name = input("Enter Bank Name: ")
            account_number = input("Enter Account Number: ")
            routing_number = input("Enter Routing Number: ")

            # Save bank details to the database
            self.data_manager.add_bank_details(employee_id, bank_name, account_number, routing_number)
            print(f"Bank details added for Employee ID {employee_id}.")
        except ValueError:
            print("Invalid input. Please enter valid details.")

    def calculate_hours_worked(self, employee_id, start_date, end_date):
        """Calculate total and overtime hours worked by an employee within the specified pay period."""
        # Retrieve all time logs for the employee within the pay period
        time_logs = self.data_manager.get_time_logs_for_employee(employee_id, start_date, end_date)
        total_hours = 0
        overtime_hours = 0

        # Calculate regular and overtime hours from time logs
        for log in time_logs:
            hours_worked = log['hours_worked']
            if hours_worked > 8:
                # Standard overtime rules: over 8 hours in a day counts as overtime
                overtime_hours += hours_worked - 8
                total_hours += 8  # Only 8 hours count as regular time
            else:
                total_hours += hours_worked

        print(f"Total Hours: {total_hours}, Overtime Hours: {overtime_hours}")
        return total_hours, overtime_hours

    def view_payroll_history(self):
        """View payroll history for a specific employee."""
        try:
            employee_id = int(input("Enter Employee ID: "))
            payroll_history = self.data_manager.get_payroll_history(employee_id)

            if not payroll_history:
                print(f"No payroll history found for Employee ID {employee_id}.")
                return

            print(f"Payroll History for Employee ID {employee_id}:")
            for record in payroll_history:
                pay_date = record['pay_date']
                gross_pay = record['gross_pay']
                deductions = record['deductions']
                net_pay = record['net_pay']
                print(f"Date: {pay_date}, Gross Pay: ${gross_pay:.2f}, Deductions: ${deductions:.2f}, Net Pay: ${net_pay:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid Employee ID.")

    
    def menu(self):
        """Display the HR department menu."""
        while True:
            print("\nHR Department Menu")
            print("1. Add Employee")
            print("2. Update Payroll Schedule")
            print("3. Add Bank Details")
            print("4. Log Payroll")
            print("5. View Payroll History")
            print("6. Set Employee Deductions")
            print("7. Set Compensation")  # Added Set Compensation option
            print("8. Back to Main Menu")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.update_payroll_schedule()
            elif choice == '3':
                self.add_bank_details()
            elif choice == '4':
                self.log_payroll()
            elif choice == '5':
                self.view_payroll_history()
            elif choice == '6':
                self.set_employee_deductions()
            elif choice == '7':
                self.set_compensation()  # Call set_compensation
            elif choice == '8':
                break
            else:
                print("Invalid choice.")

