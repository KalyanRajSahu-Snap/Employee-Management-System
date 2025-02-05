# Employee Management System (EMS)

This project is a Python-based **Employee Management System (EMS)** that interacts with a MySQL database. It provides functionalities to add, view, update, and delete employee records through a simple command-line interface.

---

## Features

### 1. **Employee Data Management**
- Handles all database operations for employee data.
- Supports adding, viewing, updating, and deleting employee records.

### 2. **Database Interactions**
- Uses `mysql.connector` to connect to a MySQL database.
- Executes SQL queries (INSERT, SELECT, UPDATE, DELETE) for interacting with employee data.
- Includes error handling for database connection and data manipulation exceptions.

### 3. **User Interface**
- A simple Command-Line Interface (CLI) is provided in the `main()` function for user interaction.
- Users can choose various options to manage employee data.

### 4. **Code Structure**
- Organized using a class (`EmployeeManagementSystem`) and functions for maintainability.
- Follows Python best practices, including proper indentation, meaningful variable names, and robust error handling.

---

## Installation

Follow these steps to set up the Employee Management System:

### Prerequisites
1. Install **MySQL** and ensure it is running on your system.
2. Install **Python** (version 3.6 or higher).
3. Install the `mysql-connector-python` library:
   ```bash
   pip install mysql-connector-python
   ```

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KalyanRajSahu-Snap/Employee-Management-System.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd employee-management-system
   ```

3. **Set Up the Database**
   Open your MySQL client and execute the following commands to create the database and table:
   ```sql
   CREATE DATABASE employee_db;
   USE employee_db;
   CREATE TABLE employees (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       department VARCHAR(100),
       role VARCHAR(100),
       date_of_joining DATE,
       salary DECIMAL(10, 2)
   );
   ```

4. **Update the Database Credentials**
   In the `main()` function of `ems.py`, locate the following line:
   ```python
   ems = EmployeeManagementSystem("localhost", "your_username", "your_password", "employee_db")
   ```
   Replace `"your_username"` and `"your_password"` with your MySQL username and password.

5. **Run the Script**
   Execute the script to launch the Employee Management System:
   ```bash
   python ems.py
   ```

---

## Usage

1. Upon running the script, you will be presented with a menu:
   - Add a new employee.
   - View all employee records.
   - Update an existing employee's information.
   - Delete an employee record.
   - Exit the system.

2. Follow the prompts to manage employee records interactively.

---

## Future Enhancements
- Implement a graphical user interface (GUI) for ease of use.
- Add search functionality to filter employees by various criteria.
- Enhance error handling and validations.

---
