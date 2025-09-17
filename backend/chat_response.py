import google.generativeai as genai
from utils.schema import SCHEMA_DESCRIPTION

def generate_chat_response(user_query, sql_results):
    prompt = f"""
    You are an expert HR assistant AI. You have access to the following database schema for candidate information:
    {SCHEMA_DESCRIPTION}
    Below is the user query:
    "{user_query}"
    And here are the query results in raw form:
    {sql_results}
    Generate a clear, concise, and helpful response to the user based on the results and the query. Only include relevant information.
    If results are in some number or list or comma separated, just show the elements each below each other like some bullet numbering.
    If results is empty i.e. there are no matching records, politely inform the user that no results were found.
    """
    response = genai.GenerativeModel('gemini-2.5-flash').generate_content(prompt)
    return response.text.strip()
