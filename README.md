# Text-to-SQL Example using Llama3 and SQLite

![Text to SQL Workflow](text_to_sql_workflow.png)

## Overview

This project demonstrates a **Text → LLM → SQL → SQLite** workflow where
a natural language query is converted into a SQL query using an LLM and
executed against a SQLite database.

The LLM used in this example is **Llama3**, running locally using
**Ollama**.

Workflow:

1.  User asks a question in natural language.
2.  Llama3 converts the question into SQL.
3.  The SQL query is executed on a SQLite database.
4.  Results are returned to the user.

Example:

Natural Language: "Who are the employees in the Sales department?"

Generated SQL:

``` sql
SELECT * FROM employees WHERE departmentid = 102;
```

------------------------------------------------------------------------

# Architecture

Text Input → Llama3 (LLM) → SQL Query Generation → SQLite Database →
Results

------------------------------------------------------------------------

# Database Schema

## Employees Table

  Column         Type      Description
  -------------- --------- ----------------------------
  employeeid     INTEGER   Unique employee identifier
  name           TEXT      Employee name
  departmentid   INTEGER   Department identifier
  salary         REAL      Employee salary

``` sql
CREATE TABLE employees (
    employeeid INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    departmentid INTEGER,
    salary REAL
);
```

### Sample Data

``` sql
INSERT INTO employees VALUES
(1,'Alice Johnson',101,75000),
(2,'Bob Smith',102,68000),
(3,'Carol White',101,82000),
(4,'David Brown',103,72000),
(5,'Emma Davis',104,66000),
(6,'Frank Miller',102,71000),
(7,'Grace Wilson',103,77000),
(8,'Henry Moore',104,69000),
(9,'Ivy Taylor',101,83000),
(10,'Jack Anderson',102,74000);
```

------------------------------------------------------------------------

## Departments Table

  Column         Type      Description
  -------------- --------- -----------------------
  departmentid   INTEGER   Department identifier
  name           TEXT      Department name

``` sql
CREATE TABLE departments (
    departmentid INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
```

### Sample Data

``` sql
INSERT INTO departments VALUES
(101,'Engineering'),
(102,'Sales'),
(103,'Human Resources'),
(104,'Finance');
```

------------------------------------------------------------------------

# Example SQL Queries

### Employees with Department Name

``` sql
SELECT e.employeeid, e.name, d.name AS department, e.salary
FROM employees e
JOIN departments d
ON e.departmentid = d.departmentid;
```

### Average Salary per Department

``` sql
SELECT d.name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d
ON e.departmentid = d.departmentid
GROUP BY d.name;
```

------------------------------------------------------------------------

# Install SQLite

macOS usually includes SQLite, but you can install the latest version
using Homebrew.

``` bash
brew install sqlite
```

Verify:

``` bash
sqlite3 --version
```

Create database:

``` bash
sqlite3 company.db
```

------------------------------------------------------------------------

# Install Llama3

Install Ollama first.

Mac / Linux:

``` bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation:

``` bash
ollama --version
```

Pull the Llama3 model:

``` bash
ollama pull llama3
```

List the models:

ollama list

Run the model in interactive mode:

``` bash
ollama run llama3
```

Run the process in the background to accept API requests (for this example):

nohup ollama serve > ollama.out 2>&1 &

------------------------------------------------------------------------

# Example Natural Language Queries:

   Question                        SQL
   ------------------------------- -------------------------------------------------
   Show all employees              SELECT \* FROM employees
   Employees in Sales              SELECT \* FROM employees WHERE departmentid=102
   Average salary per department   GROUP BY department
   ------------------------------------------------------------------------

# Run the python script 

  python llmquery.py

##  At the prompt enter this text
  "there are two tables employees with columns employeeid, name, departmentid, salary and departments with columns departmentid, name Don’t show all the employees for each department but only the highest paid employee for each department output should have employeeid, name, department and salary"

##  It should output the following:
### Generated SQL:
 SELECT e.employeeid, e.name, d.name AS department, e.salary FROM employees e JOIN departments d ON e.departmentid = d.departmentid WHERE (e.departmentid, e.salary) IN (SELECT departmentid, MAX(salary) FROM employees GROUP BY departmentid)

### Output:
    ['employeeid', 'name', 'department', 'salary']
    (7, 'Grace Wilson', 'Human Resources', 77000.0)
    (8, 'Henry Moore', 'Finance', 69000.0)
    (9, 'Ivy Taylor', 'Engineering', 83000.0)
    (10, 'Jack Anderson', 'Sales', 74000.0)

------------------------------------------------------------------------

# Project Use Cases

This project demonstrates:

• LLM powered SQL generation\
• Natural language database querying\
• Local LLM usage with Ollama\
• Lightweight analytics using SQLite

------------------------------------------------------------------------

# Future Improvements

• Add schema auto-discovery\
• Add query validation\
• Add vector search for semantic schema retrieval\
• Build a chatbot interface for database queries
