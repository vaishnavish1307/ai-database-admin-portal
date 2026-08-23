from ai.openrouter_client import ask_llm


def generate_sql(schema, question):

    prompt = f"""
You are an expert MySQL database administrator.

Your task is to convert the user's natural-language request
into ONE valid MySQL SQL statement.

Database schema:
{schema}

User request:
{question}

Rules:

1. Generate ONLY the SQL query.
2. Do NOT explain the query.
3. Do NOT use Markdown code fences.
4. Do NOT write ```sql.
5. Do NOT write any text before or after the SQL query.
6. Use the exact table and column names from the schema.
7. If the user asks to retrieve information, generate SELECT.
8. If the user asks to add a record, generate INSERT.
9. If the user asks to modify an existing record, generate UPDATE.
10. If the user asks to remove a record, generate DELETE.
11. If the user asks to create a table, generate CREATE TABLE.
12. If the user asks to modify a table structure, generate ALTER TABLE.
13. If the user asks to delete a table, generate DROP TABLE.
14. If the user asks to remove all records, generate TRUNCATE.
15. For UPDATE and DELETE, ALWAYS include an appropriate WHERE clause
    when the user identifies a specific record.
16. Never invent column names that are not present in the schema.

Examples:

User:
Show the top 5 students according to marks

SQL:
SELECT *
FROM students
ORDER BY marks DESC
LIMIT 5;

User:
Change the course of student ID 1 to CSE

SQL:
UPDATE students
SET course = 'CSE'
WHERE student_id = 1;

User:
Delete student ID 5

SQL:
DELETE FROM students
WHERE student_id = 5;

User:
Add a student named Rahul with marks 90

SQL:
INSERT INTO students (name, marks)
VALUES ('Rahul', 90);

Return ONLY the SQL statement.
"""

    return ask_llm(prompt)