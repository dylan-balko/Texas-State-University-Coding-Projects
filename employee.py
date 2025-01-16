class Employee:
    def __init__(self, *, id = None, full_name, address, ssn, phone, email, employment_type, 
                 job_title, department, start_date, end_date=None, 
                 federal_w4=None, state_tax_form=None,hourly_rate=None, 
                 annual_salary=None, overtime_rate=1.5, bonuses=None, commission=0, 
                 pay_frequency="biweekly"):

        self.full_name = full_name
        self.address = address
        self.ssn = ssn
        self.phone = phone
        self.email = email
        self.employment_type = employment_type  # hourly or salaried
        self.job_title = job_title
        self.department = department
        self.start_date = start_date
        self.end_date = end_date  # optional for terminated employees
        self.federal_w4 = federal_w4  # File path or data structure for W-4 form
        self.state_tax_form = state_tax_form  # State-specific tax form


        # Compensation attributes
        self.hourly_rate = hourly_rate  # Only for hourly employees
        self.annual_salary = annual_salary  # Only for salaried employees
        self.overtime_rate = overtime_rate  # Default is 1.5x for overtime
        self.bonuses = bonuses or []  # List to store any bonuses
        self.commission = commission  # Default is 0 if not applicable
        self.pay_frequency = pay_frequency  # Weekly, biweekly, monthly
        
    def display_info(self):
        """Return a dictionary of the employee's basic information."""
        return {
            "Name": self.full_name,
            "Address": self.address,
            "SSN": self.ssn,
            "Phone": self.phone,
            "Email": self.email,
            "Employment Type": self.employment_type,
            "Job Title": self.job_title,
            "Department": self.department,
            "Start Date": self.start_date,
            "End Date": self.end_date
        }

    def calculate_overtime_pay(self, hours):
        """Calculate overtime pay based on the hourly rate and overtime hours."""
        if self.employment_type == "hourly" and self.hourly_rate:
            return hours * self.hourly_rate * self.overtime_rate
        return 0

    def calculate_base_pay(self):
        """Calculate base pay based on employment type and pay frequency."""
        if self.employment_type == "salaried" and self.annual_salary:
            if self.pay_frequency == "biweekly":
                return self.annual_salary / 26
            elif self.pay_frequency == "weekly":
                return self.annual_salary / 52
            elif self.pay_frequency == "monthly":
                return self.annual_salary / 12
        elif self.employment_type == "hourly" and self.hourly_rate:
            weekly_hours = 40
            if self.pay_frequency == "biweekly":
                return self.hourly_rate * weekly_hours * 2
            elif self.pay_frequency == "weekly":
                return self.hourly_rate * weekly_hours
            elif self.pay_frequency == "monthly":
                return self.hourly_rate * weekly_hours * 4
        return 0
