import os
# Force the correct Instant Client path before any cx_Oracle call
os.environ['PATH'] = r'C:\oracle\instantclient_19_12\instantclient_23_9;' + os.environ['PATH']

import cx_Oracle
from utils.schema import SCHEMA_DESCRIPTION
from config import DB_DSN, DB_PASS, DB_USER, GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

def generate_sql_from_nl(nl_query):
    prompt = f"""
    You are an expert Oracle SQL generator. Based on the following schema description, convert the user's natural language query into a valid Oracle SQL SELECT query. If querying a JSON field (like 'skills'), use a fallback method with 'LIKE' instead of JSON functions for maximum compatibility:
    {SCHEMA_DESCRIPTION}
    Rule:
    - Lowercase all the terms and attributes and inputs and everything just lowercase them. But you dont need to lowercase the retrieved results.
    - If the user query has terms like worked on, etc. you can consider those terms which are mentioned there as skills.
    - Use Oracle syntax and functions only.
    - If the user query is vague (e.g., mentions "list of candidates", "show candidates"), generate a query selecting only the 'name' column.
    - Only include additional columns if the user explicitly asks for them (e.g., "list candidates with their skills and experience").
    - The generated SQL must be valid Oracle SQL, using SELECT and WHERE clauses as needed.
    User query: "{nl_query}"
    Generate only the SQL SELECT statement (do not explain).
    """
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def execute_sql(sql_query):
    sql_query = sql_query.strip()
    if sql_query.startswith('```'):
        sql_query = '\n'.join(sql_query.split('\n')[1:-1])

    # Remove trailing semicolon if present
    if sql_query.endswith(';'):
        sql_query = sql_query[:-1]

    connection = cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)
    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            formatted_row = []
            for val in row:
                if isinstance(val, cx_Oracle.LOB):
                    formatted_row.append(val.read())  # Read LOB as string
                else:
                    formatted_row.append(str(val))
            row_str = " | ".join(formatted_row)
            results.append(row_str)

        return results
    except Exception as e:
        return [f"Error executing SQL query: {str(e)}"]
    finally:
        cursor.close()
        connection.close()

