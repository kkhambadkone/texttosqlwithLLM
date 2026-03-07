SQL_PROMPT = """
You are a function that converts natural language into SQL.

RULES (MUST FOLLOW ALL):
- Output ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include backticks
- JSON must start with '{{' and end with '}}'
- The JSON must have exactly one key: "sql"
- The value of "sql" must be a single SELECT statement
- NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER
- Use only ANSI SQL

User request:
{user_text}

➡ there are two tables employees with columns employeeid, name, departmentid, salary and departments with columns departmentid, name Don’t show all the employees for each department but only the highest paid employee for each department output should have employeeid, name, department and salary
Generated SQL:
 SELECT e.employeeid, e.name, d.name AS department, e.salary FROM employees e JOIN departments d ON e.departmentid = d.departmentid WHERE (e.departmentid, e.salary) IN (SELECT departmentid, MAX(salary) FROM employees GROUP BY departmentid)
['employeeid', 'name', 'department', 'salary']
(7, 'Grace Wilson', 'Human Resources', 77000.0)
(8, 'Henry Moore', 'Finance', 69000.0)
(9, 'Ivy Taylor', 'Engineering', 83000.0)
(10, 'Jack Anderson', 'Sales', 74000.0)
"""

def get_llm_text_stream(url, payload):
    import requests, json

    full_text = ""
    response = requests.post(url, json=payload, stream=True)
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        full_text += chunk.get("response", "")
        if chunk.get("done"):
            break

    return full_text.strip()

import json

def extract_json_or_none(text):
    start = text.find("{")
    if start == -1:
        return None

    stack = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            stack += 1
        elif text[i] == "}":
            stack -= 1
            if stack == 0:
                try:
                    return json.loads(text[start:i+1])
                except json.JSONDecodeError:
                    return None
    return None

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_sql_with_retry(user_text):
    payload = {
        "model": "llama3",
        "prompt": SQL_PROMPT.format(user_text=user_text),
        "temperature": 0
    }

    raw = get_llm_text_stream(OLLAMA_URL, payload)
    parsed = extract_json_or_none(raw)

    if parsed and "sql" in parsed:
        return parsed["sql"]

    # 🔁 Retry once with correction
    retry_prompt = f"""
Your previous output was invalid.

Return ONLY valid JSON in this format:
{{ "sql": "<SELECT statement>" }}

Rules:
- SELECT only
- No explanations
- No markdown

User request:
{user_text}
"""

    payload["prompt"] = retry_prompt
    raw = get_llm_text_stream(OLLAMA_URL, payload)
    parsed = extract_json_or_none(raw)

    if not parsed or "sql" not in parsed:
        raise ValueError("LLM failed to generate valid SQL")

    return parsed["sql"]

def is_safe_sql(sql):
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    return sql.strip().lower().startswith("select") and not any(
        f in sql.lower() for f in forbidden
    )

import sqlite3

def run_sql_query(db_path, sql):
    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL detected")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [d[0] for d in cur.description]
    conn.close()

    return columns, rows

if __name__ == "__main__":
    print("Enter a description of the search you want (type 'exit' to quit):")
    while True:
        user_text = input("➡ ").strip()
        if user_text.lower() in ("exit", "quit"):
            break

        sql = generate_sql_with_retry(user_text)
        print("Generated SQL:\n", sql)
        cols, rows = run_sql_query("example.db", sql)

        print(cols)
        for r in rows:
            print(r)

