import streamlit as st
import pandas as pd

from database.reflection import (
    get_all_tables,
    get_columns,
    get_primary_key
)


def render_tables_page():

    st.title("🗄️ Database Tables")

    # -----------------------------------------
    # CHECK DATABASE CONNECTION
    # -----------------------------------------

    if not st.session_state.get("database_connected"):

        st.warning(
            "⚠️ No database is currently connected."
        )

        st.info(
            "Go to 'Connect Database' and connect a database first."
        )

        return

    # -----------------------------------------
    # ACTIVE DATABASE
    # -----------------------------------------

    db = st.session_state.get(
        "active_database",
        {}
    )

    database_name = db.get(
        "database",
        "Unknown"
    )

    connection_name = db.get(
        "name",
        database_name
    )

    st.success(
        f"🟢 Connected Database: {connection_name}"
    )

    st.caption(
        f"Database: {database_name} | "
        f"Type: {db.get('type', 'Unknown')} | "
        f"Host: {db.get('host', 'Unknown')} | "
        f"Port: {db.get('port', 'Unknown')}"
    )

    st.divider()

    # -----------------------------------------
    # GET TABLES
    # -----------------------------------------

    tables = get_all_tables()

    if not tables:

        st.warning(
            "⚠️ No tables found in this database."
        )

        return

    st.subheader("📋 Available Tables")

    # Show table count
    st.write(
        f"Found **{len(tables)}** table(s)"
    )

    # -----------------------------------------
    # SELECT TABLE
    # -----------------------------------------

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    st.divider()

    # -----------------------------------------
    # TABLE INFORMATION
    # -----------------------------------------

    st.subheader(
        f"📊 Table: {selected_table}"
    )

    columns = get_columns(
        selected_table
    )

    if columns:

        st.dataframe(
            pd.DataFrame(columns),
            width="stretch",
            hide_index=True
        )

    else:

        st.warning(
            "No column information found."
        )

    # -----------------------------------------
    # PRIMARY KEY
    # -----------------------------------------

    pk = get_primary_key(
        selected_table
    )

    if pk:

        st.success(
            f"🔑 Primary Key: {pk}"
        )

    else:

        st.warning(
            "⚠️ No primary key found."
        )