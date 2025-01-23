import mysql.connector
from mysql.connector import Error

class EmployeeManagementSystem:
    def __init__(self, host, user, password, database):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Successfully connected to the database")
        except Error as e:
            print(f"Error: '{e}'")

    def add_employee(self, name, department, role, date_of_joining, salary):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO employees (name, department, role, date_of_joining, salary) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (name, department, role, date_of_joining, salary)
            cursor.execute(query, values)
            self.connection.commit()
            print("Employee added successfully")
        except Error as e:
            print(f"Error: '{e}'")

    def view_employee(self, employee_id=None):
        try:
            cursor = self.connection.cursor()
            if employee_id:
                query = "SELECT * FROM employees WHERE id = %s"
                cursor.execute(query, (employee_id,))
            else:
                query = "SELECT * FROM employees"
                cursor.execute(query)
            
            employees = cursor.fetchall()
            for employee in employees:
                print(f"ID: {employee[0]}, Name: {employee[1]}, Department: {employee[2]}, "
                      f"Role: {employee[3]}, Date of Joining: {employee[4]}, Salary: {employee[5]}")
        except Error as e:
            print(f"Error: '{e}'")

    def update_employee(self, employee_id, name, department, role, date_of_joining, salary):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE employees 
                       SET name = %s, department = %s, role = %s, date_of_joining = %s, salary = %s 
                       WHERE id = %s"""
            values = (name, department, role, date_of_joining, salary, employee_id)
            cursor.execute(query, values)
            self.connection.commit()
            print("Employee information updated successfully")
        except Error as e:
            print(f"Error: '{e}'")

    def delete_employee(self, employee_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM employees WHERE id = %s"
            cursor.execute(query, (employee_id,))
            self.connection.commit()
            print("Employee deleted successfully")
        except Error as e:
            print(f"Error: '{e}'")

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

def main():
    ems = EmployeeManagementSystem("localhost", "your_username", "your_password", "employee_db")

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. View Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter employee name: ")
            department = input("Enter department: ")
            role = input("Enter role: ")
            date_of_joining = input("Enter date of joining (YYYY-MM-DD): ")
            salary = float(input("Enter salary: "))
            ems.add_employee(name, department, role, date_of_joining, salary)

        elif choice == '2':
            ems.view_employee()

        elif choice == '3':
            employee_id = int(input("Enter employee ID: "))
            ems.view_employee(employee_id)

        elif choice == '4':
            employee_id = int(input("Enter employee ID to update: "))
            name = input("Enter new name: ")
            department = input("Enter new department: ")
            role = input("Enter new role: ")
            date_of_joining = input("Enter new date of joining (YYYY-MM-DD): ")
            salary = float(input("Enter new salary: "))
            ems.update_employee(employee_id, name, department, role, date_of_joining, salary)

        elif choice == '5':
            employee_id = int(input("Enter employee ID to delete: "))
            ems.delete_employee(employee_id)

        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()