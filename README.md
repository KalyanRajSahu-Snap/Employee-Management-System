# Employee Management System

A comprehensive desktop application built with Python and Tkinter for managing employee records with MySQL database integration.

## Features

- Create, read, update, and delete employee records
- Store detailed employee information including:
  - Personal details (name, email, phone, address)
  - Professional information (department, job title, employment status)
  - Financial data (base salary, bonuses, benefits package)
  - Organizational details (reporting manager, date of joining)
- User-friendly graphical interface with:
  - Searchable and sortable employee list
  - Form-based data entry
  - Scrollable views for large datasets
  - Date picker for temporal data
- Secure MySQL database backend
- Support for hierarchical management structure

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  mysql-connector-python
  tkinter
  tkcalendar
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KalyanRajSahu-Snap/Employee-Management-System.git
   cd employee-management-system
   ```

2. Install required packages:
   ```bash
   pip install mysql-connector-python tkcalendar
   ```

3. Set up MySQL database:
   - Create a new database named `employee_db`
   - Update the database connection details in the code:
     ```python
     self.ems = EmployeeManagementSystem("localhost", "your_username", "your_password", "employee_db")
     ```

## Usage

1. Start the application:
   ```bash
   python ems.py
   ```

2. Use the interface to:
   - View all employees in a tabular format
   - Add new employees using the "Add Employee" button
   - Update existing records using the "Update Employee" button
   - Remove employees using the "Delete Employee" button

## Database Schema

The system uses the following database structure:

```sql
CREATE TABLE employees (
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
```

## Security Considerations

- Ensure proper database credentials management
- Implement user authentication if deploying in a production environment
- Regular database backups are recommended
- Consider encrypting sensitive employee data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Tkinter and MySQL Connector teams for their excellent libraries
- Inspired by the need for simple, efficient employee management solutions
