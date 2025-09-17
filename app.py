import streamlit as st
from backend.query_handler import generate_sql_from_nl, execute_sql
from backend.chat_response import generate_chat_response
from utils.lists import keywords

def load_css():
    with open("utils/styles.css", "r") as f:
        css = f.read()
    return f"<style>{css}</style>"

def is_candidate_related(nl_query):
    return any(word in nl_query.lower() for word in keywords)

def append_message(role: str, content: str, sql_query: str = None, results: list = None):
    """Add a message to the session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    message = {"role": role, "content": content}
    if sql_query:
        message["sql_query"] = sql_query
    if results:
        message["results"] = results
    
    st.session_state.messages.append(message)

def render_messages():
    if not st.session_state.get("messages", []):
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #8e8ea0;">
            <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">Welcome to AI Candidate Screening</div>
            <div>Ask me about candidates, skills, or experience!</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Render SQL query for assistant messages
            if message["role"] == "assistant" and "sql_query" in message:
                with st.expander("Generated SQL Query", expanded=False):
                    st.code(message["sql_query"], language="sql")

def render_chat():
    """Main chat interface rendering function."""
    
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <div class="chat-title">🤖 AI Candidate Screening Chatbot</div>
        <div class="chat-subtitle">Smart SQL-based Candidate Search & Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    render_messages()
    
    # Chat input
    if user_input := st.chat_input("Ask about candidates (e.g., Python developers, 3+ years experience)..."):
        append_message("user", user_input)
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        if not user_input.strip():
            st.markdown('<div class="warning-message">Please enter a query before searching.</div>', unsafe_allow_html=True)
            return
        
        if not is_candidate_related(user_input):
            error_msg = "This chatbot handles only candidate screening queries. Please ask about candidates, skills, or experience."
            append_message("assistant", error_msg)
            with st.chat_message("assistant"):
                st.markdown(error_msg)
            return
        
        # Process the query
        with st.chat_message("assistant"):
            with st.spinner("Generating SQL query from your input..."):
                try:
                    sql_query = generate_sql_from_nl(user_input)
                    
                    with st.expander("Generated SQL Query", expanded=True):
                        st.code(sql_query, language="sql")
                    
                    with st.spinner("Executing query against Oracle DB..."):
                        try:
                            results = execute_sql(sql_query)
                            
                            with st.spinner("Generating chatbot response..."):
                                chat_response = generate_chat_response(user_input, results)
                                st.markdown(chat_response)
                                
                                # Save assistant message
                                append_message("assistant", chat_response, sql_query, results)
                        
                        except Exception as e:
                            error_msg = f"Error executing SQL query: {str(e)}"
                            st.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                            append_message("assistant", error_msg)
                            
                            st.info("Please check your database connection and try again.")
                
                except Exception as e:
                    error_msg = f"Error generating SQL query: {str(e)}"
                    st.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                    append_message("assistant", error_msg)
                    
                    st.info("Please try rephrasing your question.")

def main():
    st.set_page_config(
        page_title="AI Candidate Screening Chatbot", 
        layout="wide"
    )
    
    render_chat()

if __name__ == "__main__":
    main()