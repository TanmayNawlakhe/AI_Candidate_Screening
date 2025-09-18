import oracledb
from utils.schema import SCHEMA_DESCRIPTION
from utils.lists import rules
from config import DB_DSN, DB_PASS, DB_USER, GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

def generate_sql_from_nl(nl_query):
    prompt = f"""
    You are an expert Oracle SQL generator. Based on the following schema description, convert the user's natural language query into a valid Oracle SQL SELECT query. If querying a JSON field (like 'skills'), use a fallback method with 'LIKE' instead of JSON functions for maximum compatibility. Use the below Schema Description mandatorily to find attributes/columns for SQL statement generation:
    {SCHEMA_DESCRIPTION}
    Mandatory Rules:
    {rules}
    User query: "{nl_query}"
    Generate only the SQL SELECT statement (do not explain).
    """
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def execute_sql(sql_query):
    sql_query = sql_query.strip()
    if sql_query.startswith('```'):
        sql_query = '\n'.join(sql_query.split('\n')[1:-1])

    if sql_query.endswith(';'):
        sql_query = sql_query[:-1]

    connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]

        rows = []
        for row in cursor.fetchall():
            processed_row = []
            for val in row:
                if isinstance(val, oracledb.LOB):   # 🔑 FIX
                    processed_row.append(val.read())  # read CLOB/BLOB as text
                else:
                    processed_row.append(val)
            rows.append(processed_row)

        return rows, columns
    except Exception as e:
        return [], [f"Error: {str(e)}"]
    finally:
        cursor.close()
        connection.close()

