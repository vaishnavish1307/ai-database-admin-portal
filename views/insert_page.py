import streamlit as st

from sqlalchemy import (
    Integer,
    Float,
    Boolean,
    Date,
    DateTime
)

from sqlalchemy.dialects.mysql import TINYINT

from auth.session import (
    is_admin
)

from auth.permissions import (
    can_insert_table
)

from crud.create import (
    insert_record
)

from database.reflection import (
    get_all_tables,
    get_table_object
)


def render_insert_page():

    st.title(
        "➕ Insert Records"
    )

    # -----------------------------------------
    # CHECK DATABASE CONNECTION
    # -----------------------------------------

    if not st.session_state.get(
        "database_connected"
    ):

        st.warning(
            "⚠️ No database is currently connected."
        )

        st.info(
            "Go to 'Connect Database' and connect a database first."
        )

        return

    # -----------------------------------------
    # GET ACTIVE ENGINE
    # -----------------------------------------

    engine = st.session_state.get(
        "active_engine"
    )

    if engine is None:

        st.error(
            "❌ Active database connection not found."
        )

        return

    # -----------------------------------------
    # ACTIVE DATABASE
    # -----------------------------------------

    db = st.session_state.get(
        "active_database",
        {}
    )

    st.success(
        f"🟢 Connected Database: "
        f"{db.get('name', 'Database')}"
    )

    st.caption(
        f"Database: {db.get('database', 'Unknown')} | "
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
            "⚠️ No tables found."
        )

        return

    # -----------------------------------------
    # SELECT TABLE
    # -----------------------------------------

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    # -----------------------------------------
    # PERMISSION CHECK
    # -----------------------------------------

    if not is_admin():

        if not can_insert_table(
            st.session_state.user_id,
            selected_table
        ):

            st.error(
                "❌ No INSERT permission."
            )

            return

    # -----------------------------------------
    # GET TABLE
    # -----------------------------------------

    table = get_table_object(
        selected_table
    )

    if table is None:

        st.error(
            "❌ Table not found."
        )

        return

    # -----------------------------------------
    # INSERT FORM
    # -----------------------------------------

    form_data = {}

    st.subheader(
        f"Insert into {selected_table}"
    )

    for column in table.columns:

        # Skip auto-generated primary key
        if column.primary_key:
            continue

        column_type = column.type

        # Boolean / TINYINT
        if (
            column.name.lower() == "is_active"
            or isinstance(column_type, TINYINT)
            or isinstance(column_type, Boolean)
        ):

            form_data[column.name] = st.checkbox(
                column.name
            )

        # Float
        elif isinstance(
            column_type,
            Float
        ):

            form_data[column.name] = st.number_input(
                column.name,
                step=0.01
            )

        # Integer
        elif isinstance(
            column_type,
            Integer
        ):

            form_data[column.name] = st.number_input(
                column.name,
                step=1,
                value=0
            )

        # Date
        elif isinstance(
            column_type,
            Date
        ):

            form_data[column.name] = st.date_input(
                column.name
            )

        # DateTime
        elif isinstance(
            column_type,
            DateTime
        ):

            form_data[column.name] = st.date_input(
                column.name
            )

        # Email
        else:

            if "email" in column.name.lower():

                form_data[column.name] = st.text_input(
                    column.name,
                    placeholder="user@example.com"
                )

            else:

                form_data[column.name] = st.text_input(
                    column.name
                )

    # -----------------------------------------
    # INSERT BUTTON
    # -----------------------------------------

    if st.button(
        "Insert Record",
        width="stretch"
    ):

        success, message = insert_record(
            selected_table,
            form_data,
            engine
        )

        if success:

            st.success(
                f"✅ {message}"
            )

        else:

            st.error(
                f"❌ {message}"
            )