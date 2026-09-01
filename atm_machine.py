import json
import os


class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = str(emp_id)
        self.name = name
        self.department = department
        self.salary = float(salary)
        
    def apply_raise(self, percentage):
        increase = self.salary * (percentage / 100)
        self.salary += increase  # Fixed: += instead of +

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary
        }

    def __str__(self):
        return f"ID: {self.emp_id} | Name: {self.name:<12} | Dept: {self.department:<10} | Salary: Rs. {self.salary:,.2f}"


class EmployeeManager:
    def __init__(self, filepath="employees.json"):
        self.filepath = filepath
        self.employees = []
        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as file:
                    data = json.load(file)
                    self.employees = [
                        Employee(item["emp_id"], item["name"], item["department"], item["salary"])
                        for item in data
                    ]
            except (json.JSONDecodeError, KeyError):
                self.employees = []
        else:
            self.employees = []

    # 1. Actual find_employee method
    def find_employee(self, emp_id):
        for emp in self.employees:
            if emp.emp_id == str(emp_id):
                return emp
        return None

    # 2. Actual save_to_file method
    def save_to_file(self):
        data = [emp.to_dict() for emp in self.employees]
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def add_employee(self, emp_id, name, department, salary):
        if self.find_employee(emp_id):
            print(f"\n[Error] Employee with ID '{emp_id}' already exists!")
            return False

        if salary <= 0:
            print("\n[Error] Salary must be greater than zero!")
            return False

        new_emp = Employee(emp_id, name, department, salary)
        self.employees.append(new_emp)
        self.save_to_file()
        print(f"\n[Success] Employee '{name}' added successfully!")
        return True

    def view_all(self):
        if not self.employees:
            print("\nNo employees found.")
            return

        print("\n" + "=" * 60)
        print(f"{'ALL EMPLOYEES':^60}")
        print("=" * 60)
        for emp in self.employees:
            print(emp)
        print("=" * 60)

    def search_by_department(self, department_name):
        matched = [
            emp for emp in self.employees 
            if emp.department.strip().lower() == department_name.strip().lower()
        ]

        if not matched:
            print(f"\nNo employees found in the '{department_name}' department.")
            return

        print("\n" + "=" * 60)
        print(f"EMPLOYEES IN DEPARTMENT: {department_name.upper()}")
        print("=" * 60)
        for emp in matched:
            print(emp)
        print("=" * 60)

    def total_payroll(self):
        if not self.employees:
            print("\nTotal Payroll: Rs. 0.00 (No active employees)")
            return

        total = sum(emp.salary for emp in self.employees)
        print("\n" + "-" * 40)
        print(f"Total Combined Payroll: Rs. {total:,.2f}")
        print("-" * 40)

    def give_raise(self, emp_id, percentage):
        emp = self.find_employee(emp_id)
        if not emp:
            print(f"\n[Error] Employee with ID '{emp_id}' not found!")
            return False

        if percentage <= 0:
            print("\n[Error] Raise percentage must be greater than zero!")
            return False

        old_salary = emp.salary
        emp.apply_raise(percentage)
        self.save_to_file()

        print("\n" + "-" * 45)
        print(f"Salary Raise Applied for {emp.name} (ID: {emp.emp_id})")
        print(f"Old Salary: Rs. {old_salary:,.2f}")
        print(f"New Salary: Rs. {emp.salary:,.2f} (+{percentage}%)")
        print("-" * 45)
        return True


def main():
    manager = EmployeeManager()

    while True:
        print("\n========================================")
        print("       EMPLOYEE MANAGEMENT SYSTEM       ")
        print("========================================")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search by Department")
        print("4. Total Payroll")
        print("5. Give Salary Raise")
        print("6. Exit")
        print("========================================")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            emp_id = input("Enter Employee ID: ").strip()
            name = input("Enter Employee Name: ").strip()
            department = input("Enter Department: ").strip()
            
            try:
                salary = float(input("Enter Salary: Rs. "))
                manager.add_employee(emp_id, name, department, salary)
            except ValueError:
                print("\n[Error] Invalid input! Salary must be a valid numeric value.")
        elif choice == "2":
            manager.view_all()
        elif choice == "3":
            dept = input("Enter Department Name to search: ").strip()
            manager.search_by_department(dept)
        elif choice == "4":
            manager.total_payroll()
        elif choice == "5":
            emp_id = input("Enter Employee ID to receive raise: ").strip()
            try:
                percentage = float(input("Enter Raise Percentage (e.g., 10 for 10%): "))
                manager.give_raise(emp_id, percentage)
            except ValueError:
                print("\n[Error] Invalid input! Percentage must be a valid numeric value.")
        elif choice == "6":
            print("\nThank you for using the Employee Management System. Goodbye!\n")
            break
        else:
            print("\n[Error] Invalid choice! Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()
