import streamlit as st
import pandas as pd

from sqlalchemy import text

from auth.session import is_admin

from database.reflection import (
    get_all_tables,
    get_schema_text
)

from ai.sql_generator import generate_sql
from ai.sql_validator import validate_sql
from ai.openrouter_client import ask_llm


# --------------------------------------------------
# Clean AI-generated SQL
# --------------------------------------------------

def clean_sql(sql_query):
    """
    Remove Markdown code fences and extra whitespace
    from AI-generated SQL.
    """

    if not sql_query:
        return sql_query

    sql_query = sql_query.strip()

    # Remove opening Markdown code fence

    if sql_query.startswith("```sql"):

        sql_query = sql_query[
            len("```sql"):
        ]

    elif sql_query.startswith("```SQL"):

        sql_query = sql_query[
            len("```SQL"):
        ]

    elif sql_query.startswith("```"):

        sql_query = sql_query[
            len("```"):
        ]

    # Remove closing Markdown code fence

    if sql_query.endswith("```"):

        sql_query = sql_query[:-3]

    return sql_query.strip()


# --------------------------------------------------
# Determine SQL query type
# --------------------------------------------------

def get_sql_type(sql_query):
    """
    Determine the basic SQL statement type.
    """

    if not sql_query:
        return ""

    sql = sql_query.strip().lower()

    # Remove leading comments if present

    while sql.startswith("--"):

        newline_position = sql.find("\n")

        if newline_position == -1:

            return ""

        sql = sql[
            newline_position + 1:
        ].strip()

    # Handle WITH queries

    if sql.startswith("with"):

        if "select" in sql:

            return "select"

    first_word = sql.split()[0]

    return first_word


# --------------------------------------------------
# Clear pending AI query
# --------------------------------------------------

def clear_pending_query():

    st.session_state.pop(
        "ai_sql",
        None
    )

    st.session_state.pop(
        "ai_question",
        None
    )

    st.session_state.pop(
        "ai_table",
        None
    )


# --------------------------------------------------
# AI Data Analyst Page
# --------------------------------------------------

def render_ai_chat_page():

    st.title(
        "AI Data Analyst"
    )

    # --------------------------------------------------
    # Check active database connection
    # --------------------------------------------------

    engine = st.session_state.get(
        "active_engine"
    )

    if engine is None:

        st.warning(
            "Please connect to a database first."
        )

        return

    # --------------------------------------------------
    # Get tables from currently connected database
    # --------------------------------------------------

    tables = get_all_tables()

    if not tables:

        st.warning(
            "No tables found in the connected database."
        )

        return

    # --------------------------------------------------
    # Show current database
    # --------------------------------------------------

    active_database = st.session_state.get(
        "active_database"
    )

    if active_database:

        st.info(
            f"AI is connected to: {active_database}"
        )

    else:

        st.info(
            "AI is connected to the currently selected database."
        )

    # --------------------------------------------------
    # Select table
    # --------------------------------------------------

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    # --------------------------------------------------
    # Ask question
    # --------------------------------------------------

    question = st.chat_input(
        "Ask a question about your data..."
    )

    # --------------------------------------------------
    # Generate SQL
    # --------------------------------------------------

    if question:

        schema = get_schema_text(
            selected_table
        )

        try:

            sql_query = generate_sql(
                schema,
                question
            )

            # Clean Markdown formatting
            # returned by the AI.

            sql_query = clean_sql(
                sql_query
            )

            if not sql_query:

                st.error(
                    "AI did not generate a SQL query."
                )

                return

            # Store generated information
            # in session state.

            st.session_state.ai_question = (
                question
            )

            st.session_state.ai_sql = (
                sql_query
            )

            st.session_state.ai_table = (
                selected_table
            )

        except Exception as e:

            st.error(
                f"Failed to generate SQL: {e}"
            )

            return

    # --------------------------------------------------
    # Retrieve pending AI query
    # --------------------------------------------------

    sql_query = st.session_state.get(
        "ai_sql"
    )

    pending_question = st.session_state.get(
        "ai_question"
    )

    pending_table = st.session_state.get(
        "ai_table"
    )

    if not sql_query:

        return

    # --------------------------------------------------
    # Display generated SQL
    # --------------------------------------------------

    st.subheader(
        "Generated SQL"
    )

    st.code(
        sql_query,
        language="sql"
    )

    # --------------------------------------------------
    # Determine SQL type
    # --------------------------------------------------

    sql_type = get_sql_type(
        sql_query
    )

    # --------------------------------------------------
    # SQL Permission Check
    # --------------------------------------------------

    if is_admin():

        # Admin users can execute
        # read and write SQL.

        st.warning(
            "Admin mode: AI-generated SQL may modify "
            "the database. Review the query carefully "
            "before executing."
        )

        is_valid = True

    else:

        # Non-admin users can execute
        # only read-only SELECT queries.

        try:

            is_valid = validate_sql(
                sql_query
            )

        except Exception as e:

            st.error(
                f"SQL validation failed: {e}"
            )

            return

        if not is_valid:

            st.error(
                "Unsafe query blocked. "
                "Only read-only SELECT queries "
                "are allowed for non-admin users."
            )

            clear_pending_query()

            return

    # --------------------------------------------------
    # Execute / Cancel buttons
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        execute = st.button(
            "Execute",
            type="primary",
            use_container_width=True
        )

    with col2:

        cancel = st.button(
            "Cancel",
            use_container_width=True
        )

    # --------------------------------------------------
    # Cancel
    # --------------------------------------------------

    if cancel:

        clear_pending_query()

        st.rerun()

    # --------------------------------------------------
    # Execute query
    # --------------------------------------------------

    if execute:

        try:

            # ==================================================
            # SELECT
            # ==================================================

            if sql_type == "select":

                df = pd.read_sql(
                    text(sql_query),
                    engine
                )

                st.subheader(
                    "Query Result"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # --------------------------------------------------
                # AI Explanation
                # --------------------------------------------------

                explanation_prompt = f"""
You are a database data analyst.

User Question:
{pending_question}

SQL Query:
{sql_query}

Query Result:
{df.head(20).to_string(index=False)}

Explain the answer in simple English.

Do not invent information that is not present
in the query result.
"""

                try:

                    answer = ask_llm(
                        explanation_prompt
                    )

                    st.subheader(
                        "AI Explanation"
                    )

                    st.write(
                        answer
                    )

                except Exception as e:

                    st.warning(
                        "Query executed successfully, "
                        f"but AI explanation failed: {e}"
                    )

            # ==================================================
            # INSERT / UPDATE / DELETE / DDL
            # ==================================================

            else:

                # Extra safety check

                if not is_admin():

                    st.error(
                        "Only administrators can execute "
                        "write or DDL queries."
                    )

                    return

                # Execute inside a transaction.
                #
                # engine.begin() automatically commits
                # if successful and rolls back if an
                # exception occurs.

                with engine.begin() as connection:

                    result = connection.execute(
                        text(sql_query)
                    )

                st.success(
                    "Query executed successfully."
                )

                # --------------------------------------------------
                # Show affected rows
                # --------------------------------------------------

                if result.rowcount is not None:

                    st.info(
                        f"Rows affected: {result.rowcount}"
                    )

            # --------------------------------------------------
            # Clear pending query
            # --------------------------------------------------

            clear_pending_query()

        except Exception as e:

            st.error(
                f"Query execution failed: {e}"
            )