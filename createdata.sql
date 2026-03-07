CREATE TABLE employees (
    employeeid INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    departmentid INTEGER,
    salary REAL
);

INSERT INTO employees (employeeid, name, departmentid, salary) VALUES
(1, 'Alice Johnson', 101, 75000),
(2, 'Bob Smith', 102, 68000),
(3, 'Carol White', 101, 82000),
(4, 'David Brown', 103, 72000),
(5, 'Emma Davis', 104, 66000),
(6, 'Frank Miller', 102, 71000),
(7, 'Grace Wilson', 103, 77000),
(8, 'Henry Moore', 104, 69000),
(9, 'Ivy Taylor', 101, 83000),
(10, 'Jack Anderson', 102, 74000);

CREATE TABLE departments (
    departmentid INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO departments (departmentid, name) VALUES
(101, 'Engineering'),
(102, 'Sales'),
(103, 'Human Resources'),
(104, 'Finance');


