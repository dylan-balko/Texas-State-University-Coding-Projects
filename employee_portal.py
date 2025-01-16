# employee_portal.py

from datamanager import DataManager
from datetime import datetime

class EmployeePortal:
    def __init__(self, employee_id):
        self.data_manager = DataManager()
        self.employee_id = employee_id  # Set the employee ID


    def clock_in(self, employee_id):
        """Record clock-in time for an employee."""
        date = datetime.now().date().isoformat()
        clock_in_time = datetime.now().isoformat(timespec='minutes')
        self.data_manager.add_time_log(employee_id, date, clock_in=clock_in_time)
        print(f"Employee {employee_id} clocked in at {clock_in_time} on {date}.")

    def clock_out(self, employee_id):
        """Record clock-out time, calculate hours worked and overtime."""
        date = datetime.now().date().isoformat()
        clock_out_time = datetime.now().isoformat(timespec='minutes')

        # Retrieve clock-in time to calculate hours worked
        time_log = self.data_manager.get_time_log_by_date(employee_id, date)
        if time_log and time_log['clock_in']:
            clock_in_time = datetime.fromisoformat(time_log['clock_in'])
            hours_worked = (datetime.now() - clock_in_time).seconds / 3600
            overtime_hours = max(0, hours_worked - 8)
            self.data_manager.update_clock_out(employee_id, date, clock_out_time, hours_worked, overtime_hours)
            print(f"Employee {employee_id} clocked out at {clock_out_time}. Hours worked: {hours_worked:.2f}, Overtime: {overtime_hours:.2f}.")
        else:
            print("Clock-in record not found for today.")

    def view_pay_stubs(self):
        """Allow the employee to view their pay stubs."""
        pay_history = self.data_manager.get_payroll_history(self.employee_id)
        print("Your Pay Stubs:")
        for record in pay_history:
            print(f"Date: {record['date']}, Net Pay: ${record['net_pay']:.2f}")

    def update_tax_forms(self):
        """Allow the employee to update their tax forms."""
        federal_form_path = input("Enter path for updated Federal W-4 form: ")
        state_form_path = input("Enter path for updated State Tax Form: ")
        self.data_manager.update_tax_forms(self.employee_id, federal_form_path, state_form_path)
        print("Tax forms updated successfully.")

    def request_time_off(self):
        """Allow the employee to request time off."""
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        reason = input("Enter reason for time off: ")
        self.data_manager.request_time_off(self.employee_id, start_date, end_date, reason)
        print("Time off request submitted.")
        
    def view_time_logs(self, employee_id):
        """View time logs for the employee."""
        time_logs = self.data_manager.get_time_logs_for_employee(employee_id)
        if not time_logs:
            print("No time logs found.")
            return
        print(f"Time Logs for Employee ID {employee_id}:")
        for log in time_logs:
            print(f"Date: {log['date']}, Clock In: {log['clock_in']}, Clock Out: {log['clock_out']}, "
                  f"Hours Worked: {log['hours_worked']}, Overtime Hours: {log['overtime_hours']}, "
                  f"Time Off Requested: {log['time_off_requested']}, Time Off Approved: {log['time_off_approved']}, "
                  f"Status: {log['status']}")

    def menu(self, employee_id):
        """Display the employee portal menu."""
        while True:
            print("\nEmployee Portal")
            print("1. Clock In")
            print("2. Clock Out")
            print("3. Request Time Off")
            print("4. View Time Cards")
            print("5. View Pay Stubs")
            print("6. Update Tax Forms")
            print("7. Back to Main Menu")
            choice = input("Enter choice: ")

            if choice == '1':
                self.clock_in(employee_id)
            elif choice == '2':
                self.clock_out(employee_id)
            elif choice == '3':
                self.request_time_off()
            elif choice == '4':
                self.view_time_logs(employee_id)
            elif choice == '5':
                self.view_pay_stubs()
            elif choice == '6':
                self.update_tax_forms()
            elif choice == '7':
                break
            else:
                print("Invalid choice.")
