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
            self.create_table()
        except Error as e:
            messagebox.showerror("Database Connection Error", str(e))

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email_address VARCHAR(100),
                phone_number VARCHAR(20),
                current_address TEXT,
                department VARCHAR(50),
                job_title VARCHAR(100),
                employee_status VARCHAR(20),
                base_salary DECIMAL(10, 2),
                bonuses DECIMAL(10, 2),
                benefits_package TEXT,
                date_of_joining DATE,
                reporting_manager_id INT,
                FOREIGN KEY (reporting_manager_id) REFERENCES employees(id)
            )
            """
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            messagebox.showerror("Error", str(e))

    def add_employee(self, data):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO employees (
                name, email_address, phone_number, current_address,
                department, job_title, employee_status, base_salary,
                bonuses, benefits_package, date_of_joining, reporting_manager_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (
                data['name'], data['email'], data['phone'], data['address'],
                data['department'], data['job_title'], data['status'], data['base_salary'],
                data['bonuses'], data['benefits'], data['date_of_joining'], data['manager_id']
            )
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

    def update_employee(self, employee_id, data):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE employees SET 
                name = %s, email_address = %s, phone_number = %s, current_address = %s,
                department = %s, job_title = %s, employee_status = %s, base_salary = %s,
                bonuses = %s, benefits_package = %s, date_of_joining = %s, reporting_manager_id = %s
                WHERE id = %s"""
            values = (
                data['name'], data['email'], data['phone'], data['address'],
                data['department'], data['job_title'], data['status'], data['base_salary'],
                data['bonuses'], data['benefits'], data['date_of_joining'], data['manager_id'],
                employee_id
            )
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

    def get_all_managers(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT id, name FROM employees"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", str(e))
            return []

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

class EmployeeManagementUI:
    def __init__(self, master):
        self.master = master
        master.title("Employee Management System")
        master.geometry("1200x700")

        # Create EMS instance
        self.ems = EmployeeManagementSystem("localhost", "your_username", "your_password", "employee_db")

        # Create Treeview
        columns = ("ID", "Name", "Email", "Phone", "Department", "Job Title", 
                  "Status", "Base Salary", "Date of Joining", "Manager ID")
        self.tree = ttk.Treeview(master, columns=columns, show="headings", height=20)
        
        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust width as needed

        # Add scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

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
        for item in self.tree.get_children():
            self.tree.delete(item)
        employees = self.ems.view_employee()
        for emp in employees:
            # Display selected columns in tree view
            display_values = (emp[0], emp[1], emp[2], emp[3], emp[5], emp[6], 
                            emp[7], emp[8], emp[11], emp[12])
            self.tree.insert("", "end", values=display_values)

    def create_employee_form(self, window, data=None):
        # Form fields
        entries = {}
        
        # Personal Information
        tk.Label(window, text="Personal Information", font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Label(window, text="Name:").pack()
        entries['name'] = tk.Entry(window)
        entries['name'].pack()
        if data: entries['name'].insert(0, data.get('name', ''))

        tk.Label(window, text="Email:").pack()
        entries['email'] = tk.Entry(window)
        entries['email'].pack()
        if data: entries['email'].insert(0, data.get('email', ''))

        tk.Label(window, text="Phone:").pack()
        entries['phone'] = tk.Entry(window)
        entries['phone'].pack()
        if data: entries['phone'].insert(0, data.get('phone', ''))

        tk.Label(window, text="Address:").pack()
        entries['address'] = tk.Text(window, height=3, width=30)
        entries['address'].pack()
        if data: entries['address'].insert('1.0', data.get('address', ''))

        # Professional Information
        tk.Label(window, text="Professional Information", font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Label(window, text="Department:").pack()
        entries['department'] = tk.Entry(window)
        entries['department'].pack()
        if data: entries['department'].insert(0, data.get('department', ''))

        tk.Label(window, text="Job Title:").pack()
        entries['job_title'] = tk.Entry(window)
        entries['job_title'].pack()
        if data: entries['job_title'].insert(0, data.get('job_title', ''))

        tk.Label(window, text="Employee Status:").pack()
        status_var = tk.StringVar(value=data.get('status', 'Full-time') if data else 'Full-time')
        entries['status'] = ttk.Combobox(window, textvariable=status_var, 
                                       values=('Full-time', 'Part-time', 'Contractor'))
        entries['status'].pack()

        # Financial Information
        tk.Label(window, text="Financial Information", font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Label(window, text="Base Salary:").pack()
        entries['base_salary'] = tk.Entry(window)
        entries['base_salary'].pack()
        if data: entries['base_salary'].insert(0, data.get('base_salary', ''))

        tk.Label(window, text="Bonuses:").pack()
        entries['bonuses'] = tk.Entry(window)
        entries['bonuses'].pack()
        if data: entries['bonuses'].insert(0, data.get('bonuses', ''))

        tk.Label(window, text="Benefits Package:").pack()
        entries['benefits'] = tk.Text(window, height=3, width=30)
        entries['benefits'].pack()
        if data: entries['benefits'].insert('1.0', data.get('benefits', ''))

        # Other Information
        tk.Label(window, text="Other Information", font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Label(window, text="Date of Joining:").pack()
        entries['date_of_joining'] = DateEntry(window, width=12, background='darkblue', 
                                             foreground='white', borderwidth=2)
        entries['date_of_joining'].pack()
        if data and data.get('date_of_joining'):
            try:
                date_obj = datetime.strptime(str(data['date_of_joining']), "%Y-%m-%d").date()
                entries['date_of_joining'].set_date(date_obj)
            except ValueError:
                pass

        tk.Label(window, text="Reporting Manager:").pack()
        managers = self.ems.get_all_managers()
        manager_choices = ['None'] + [f"{m[0]} - {m[1]}" for m in managers]
        entries['manager_id'] = ttk.Combobox(window, values=manager_choices)
        entries['manager_id'].pack()
        if data and data.get('manager_id'):
            entries['manager_id'].set(f"{data['manager_id']}")
        else:
            entries['manager_id'].set('None')

        return entries

    def add_employee_window(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Employee")
        add_window.geometry("500x800")

        # Create scrollable frame
        canvas = tk.Canvas(add_window)
        scrollbar = ttk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        entries = self.create_employee_form(scrollable_frame)

        def save_employee():
            try:
                # Gather data from form
                data = {
                    'name': entries['name'].get(),
                    'email': entries['email'].get(),
                    'phone': entries['phone'].get(),
                    'address': entries['address'].get('1.0', tk.END).strip(),
                    'department': entries['department'].get(),
                    'job_title': entries['job_title'].get(),
                    'status': entries['status'].get(),
                    'base_salary': float(entries['base_salary'].get()),
                    'bonuses': float(entries['bonuses'].get()),
                    'benefits': entries['benefits'].get('1.0', tk.END).strip(),
                    'date_of_joining': entries['date_of_joining'].get_date().strftime("%Y-%m-%d"),
                    'manager_id': entries['manager_id'].get().split(' - ')[0] if entries['manager_id'].get() != 'None' else None
                }

                if self.ems.add_employee(data):
                    messagebox.showinfo("Success", "Employee added successfully")
                    add_window.destroy()
                    self.refresh_employees()

            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numeric values for salary and bonuses")

        tk.Button(scrollable_frame, text="Save", command=save_employee).pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_employee_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to update")
            return

        employee = self.tree.item(selected_item[0])['values']
        emp_data = {
            'name': employee[1],
            'email': employee[2],
            'phone': employee[3],
            'department': employee[4],
            'job_title': employee[5],
            'status': employee[6],
            'base_salary': employee[7],
            'date_of_joining': employee[8],
            'manager_id': employee[9]
        }

        update_window = tk.Toplevel(self.master)
        update_window.title("Update Employee")
        update_window.geometry("500x800")

        # Create scrollable frame
        canvas = tk.Canvas(update_window)
        scrollbar = ttk.Scrollbar(update_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        entries = self.create_employee_form(scrollable_frame, emp_data)

        def save_update():
            try:
                data = {
                    'name': entries['name'].get(),
                    'email': entries['email'].get(),
                    'phone': entries['phone'].get(),
                    'address': entries['address'].get('1.0', tk.END).strip(),
                    'department': entries['department'].get(),
                    'job_title': entries['job_title'].get(),
                    'status': entries['status'].get(),
                    'base_salary': float(entries['base_salary'].get()),
                    'bonuses': float(entries['bonuses'].get()),
                    'benefits': entries['benefits'].get('1.0', tk.END).strip(),
                    'date_of_joining': entries['date_of_joining'].get_date().strftime("%Y-%m-%d"),
                    'manager_id': entries['manager_id'].get().split(' - ')[0] if entries['manager_id'].get() != 'None' else None
                }

                if self.ems.update_employee(employee[0], data):
                    messagebox.showinfo("Success", "Employee updated successfully")
                    update_window.destroy()
                    self.refresh_employees()

            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numeric values for salary and bonuses")

        tk.Button(scrollable_frame, text="Save", command=save_update).pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            employee_id = self.tree.item(selected_item[0])['values'][0]
            
            if self.ems.delete_employee(employee_id):
                messagebox.showinfo("Success", "Employee deleted successfully")
                self.refresh_employees()

def main():
    root = tk.Tk()
    app = EmployeeManagementUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()