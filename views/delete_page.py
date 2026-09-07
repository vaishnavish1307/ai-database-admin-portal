import streamlit as st

from auth.session import (
    is_admin
)

from auth.permissions import (
    can_delete_table
)

from crud.delete import (
    delete_record
)

from database.reflection import (
    get_all_tables,
    get_primary_key
)


def render_delete_page():

    st.title(
        "Delete Records"
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
    # Display active database
    # --------------------------------------------------

    db = st.session_state.get(
        "active_database",
        {}
    )

    st.success(
        f"🟢 Connected Database: "
        f"{db.get('name', 'Database')}"
    )

    st.divider()

    # --------------------------------------------------
    # Get tables
    # --------------------------------------------------

    tables = get_all_tables()

    if not tables:

        st.warning(
            "No tables found"
        )

        return

    # --------------------------------------------------
    # Select table
    # --------------------------------------------------

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    # --------------------------------------------------
    # Permission check
    # --------------------------------------------------

    if not is_admin():

        if not can_delete_table(
            st.session_state.user_id,
            selected_table
        ):

            st.error(
                "No DELETE permission"
            )

            return

    # --------------------------------------------------
    # Primary key
    # --------------------------------------------------

    pk = get_primary_key(
        selected_table
    )

    if pk is None:

        st.error(
            "This table does not have a primary key."
        )

        return

    st.subheader(
        f"Delete from {selected_table}"
    )

    # --------------------------------------------------
    # Record ID
    # --------------------------------------------------

    record_id = st.number_input(
        f"{pk}",
        min_value=1,
        step=1
    )

    # --------------------------------------------------
    # Warning
    # --------------------------------------------------

    st.warning(
        "⚠️ This action cannot be undone."
    )

    confirm = st.checkbox(
        "I understand"
    )

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    if st.button(
        "Delete Record",
        type="primary"
    ):

        if not confirm:

            st.error(
                "Please confirm deletion."
            )

            return

        success, msg = delete_record(
            selected_table,
            record_id,
            engine
        )

        if success:

            st.success(
                msg
            )

        else:

            st.error(
                msg
            )