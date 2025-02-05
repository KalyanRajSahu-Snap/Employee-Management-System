import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
from datetime import datetime

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
            messagebox.showerror("Database Connection Error", str(e))

    def add_employee(self, name, department, role, date_of_joining, salary):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO employees (name, department, role, date_of_joining, salary) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (name, department, role, date_of_joining, salary)
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", str(e))
            return False

    def view_employee(self, employee_id=None):
        try:
            cursor = self.connection.cursor()
            if employee_id:
                query = "SELECT * FROM employees WHERE id = %s"
                cursor.execute(query, (employee_id,))
            else:
                query = "SELECT * FROM employees"
                cursor.execute(query)
            
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", str(e))
            return []

    def update_employee(self, employee_id, name, department, role, date_of_joining, salary):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE employees 
                       SET name = %s, department = %s, role = %s, date_of_joining = %s, salary = %s 
                       WHERE id = %s"""
            
            # Ensure date is in correct format
            if isinstance(date_of_joining, str):
                date_of_joining = datetime.strptime(date_of_joining, "%Y-%m-%d").date()
            
            values = (name, department, role, date_of_joining, salary, employee_id)
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", str(e))
            return False

    def delete_employee(self, employee_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM employees WHERE id = %s"
            cursor.execute(query, (employee_id,))
            self.connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", str(e))
            return False

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

class EmployeeManagementUI:
    def __init__(self, master):
        self.master = master
        master.title("Employee Management System")
        master.geometry("800x600")

        # Create EMS instance
        self.ems = EmployeeManagementSystem("localhost", "your_username", "your_password", "employee_db")

        # Create Treeview
        self.tree = ttk.Treeview(master, columns=("ID", "Name", "Department", "Role", "Date of Joining", "Salary"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Date of Joining", text="Date of Joining")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons Frame
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        # Buttons
        tk.Button(btn_frame, text="Add Employee", command=self.add_employee_window).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View Employees", command=self.refresh_employees).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Update Employee", command=self.update_employee_window).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee).grid(row=0, column=3, padx=5)

        # Initial load of employees
        self.refresh_employees()

    def refresh_employees(self):
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Fetch and display employees
        employees = self.ems.view_employee()
        for emp in employees:
            self.tree.insert("", "end", values=emp)

    def add_employee_window(self):
        # Create a new window for adding employee
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Employee")
        add_window.geometry("400x400")

        # Name
        tk.Label(add_window, text="Name:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        # Department
        tk.Label(add_window, text="Department:").pack()
        dept_entry = tk.Entry(add_window)
        dept_entry.pack()

        # Role
        tk.Label(add_window, text="Role:").pack()
        role_entry = tk.Entry(add_window)
        role_entry.pack()

        # Date of Joining (using DateEntry from tkcalendar)
        tk.Label(add_window, text="Date of Joining:").pack()
        date_entry = DateEntry(add_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.pack()

        # Salary
        tk.Label(add_window, text="Salary:").pack()
        salary_entry = tk.Entry(add_window)
        salary_entry.pack()

        # Save Button
        def save_employee():
            name = name_entry.get()
            department = dept_entry.get()
            role = role_entry.get()
            date_of_joining = date_entry.get_date().strftime("%Y-%m-%d")
            try:
                salary = float(salary_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid salary")
                return

            if self.ems.add_employee(name, department, role, date_of_joining, salary):
                messagebox.showinfo("Success", "Employee added successfully")
                add_window.destroy()
                self.refresh_employees()

        tk.Button(add_window, text="Save", command=save_employee).pack(pady=10)

    def update_employee_window(self):
        # Get selected employee
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to update")
            return

        # Get employee details
        employee = self.tree.item(selected_item[0])['values']
        
        # Create update window
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Employee")
        update_window.geometry("400x400")

        # Populate fields with existing data
        tk.Label(update_window, text="Name:").pack()
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, employee[1])
        name_entry.pack()

        tk.Label(update_window, text="Department:").pack()
        dept_entry = tk.Entry(update_window)
        dept_entry.insert(0, employee[2])
        dept_entry.pack()

        tk.Label(update_window, text="Role:").pack()
        role_entry = tk.Entry(update_window)
        role_entry.insert(0, employee[3])
        role_entry.pack()

        tk.Label(update_window, text="Date of Joining:").pack()
        date_entry = DateEntry(update_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        
        # Safely parse and set the date
        try:
            date_obj = datetime.strptime(str(employee[4]), "%Y-%m-%d").date()
            date_entry.set_date(date_obj)
        except (ValueError, TypeError):
            # If date parsing fails, use current date
            date_entry.set_date(datetime.now().date())
        
        date_entry.pack()

        tk.Label(update_window, text="Salary:").pack()
        salary_entry = tk.Entry(update_window)
        salary_entry.insert(0, str(employee[5]))
        salary_entry.pack()

        def save_update():
            name = name_entry.get()
            department = dept_entry.get()
            role = role_entry.get()
            date_of_joining = date_entry.get_date().strftime("%Y-%m-%d")
            try:
                salary = float(salary_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid salary")
                return

            if self.ems.update_employee(employee[0], name, department, role, date_of_joining, salary):
                messagebox.showinfo("Success", "Employee updated successfully")
                update_window.destroy()
                self.refresh_employees()

        tk.Button(update_window, text="Save", command=save_update).pack(pady=10)

    def delete_employee(self):
        # Get selected employee
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            # Get employee ID
            employee_id = self.tree.item(selected_item[0])['values'][0]
            
            # Delete employee
            if self.ems.delete_employee(employee_id):
                messagebox.showinfo("Success", "Employee deleted successfully")
                self.refresh_employees()

def main():
    root = tk.Tk()
    app = EmployeeManagementUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()