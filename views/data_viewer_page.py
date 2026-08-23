import streamlit as st
import pandas as pd

from auth.session import is_admin

from auth.permissions import (
    can_read_table
)

from crud.read import (
    get_table_data
)

from database.reflection import (
    get_all_tables
)


def render_data_viewer():

    st.title("📊 Data Viewer")

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
    # GET ACTIVE DATABASE
    # -----------------------------------------

    engine = st.session_state.get(
        "active_engine"
    )

    db = st.session_state.get(
        "active_database",
        {}
    )

    if engine is None:

        st.error(
            "❌ Active database connection not found."
        )

        return

    # -----------------------------------------
    # DISPLAY ACTIVE DATABASE
    # -----------------------------------------

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
            "⚠️ No tables found in this database."
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

    user_id = st.session_state.get(
        "user_id"
    )

    if not is_admin():

        if not can_read_table(
            user_id,
            selected_table
        ):

            st.error(
                "❌ You don't have READ permission."
            )

            return

    # -----------------------------------------
    # READ DATA
    # -----------------------------------------

    df = get_table_data(
        selected_table,
        engine
    )

    if df.empty:

        st.warning(
            "⚠️ No records found."
        )

        return

    # -----------------------------------------
    # TABLE INFORMATION
    # -----------------------------------------

    st.subheader(
        f"📋 {selected_table} Records"
    )

    st.write(
        f"Total Records: **{len(df)}**"
    )

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    search = st.text_input(
        "🔍 Search records"
    )

    if search:

        mask = df.astype(
            str
        ).apply(
            lambda row:
            row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )

        df = df[mask]

    # -----------------------------------------
    # PAGINATION
    # -----------------------------------------

    page_size = 10

    total_rows = len(df)

    total_pages = (
        total_rows // page_size
    ) + (
        1
        if total_rows % page_size
        else 0
    )

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=max(
            total_pages,
            1
        ),
        value=1
    )

    start = (
        page - 1
    ) * page_size

    end = start + page_size

    # -----------------------------------------
    # DISPLAY DATA
    # -----------------------------------------

    st.dataframe(
        df.iloc[start:end],
        width="stretch",
        hide_index=True
    )

    st.caption(
        f"Showing rows "
        f"{start + 1 if total_rows else 0}–"
        f"{min(end, total_rows)} "
        f"of {total_rows}"
    )