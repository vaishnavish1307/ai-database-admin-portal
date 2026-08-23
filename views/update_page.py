import streamlit as st

from sqlalchemy import (
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
    can_update_table
)

from crud.update import (
    get_record_by_id,
    update_record
)

from database.reflection import (
    get_all_tables,
    get_table_object,
    get_primary_key
)


def render_update_page():

    st.title(
        "Update Records"
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
    # Get tables from active database
    # --------------------------------------------------

    tables = get_all_tables()

    if not tables:

        st.warning(
            "No tables found"
        )

        return

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    # --------------------------------------------------
    # Permission check
    # --------------------------------------------------

    if not is_admin():

        if not can_update_table(
            st.session_state.user_id,
            selected_table
        ):

            st.error(
                "No UPDATE permission"
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

    record_id = st.number_input(
        f"{pk}",
        min_value=1,
        step=1
    )

    # --------------------------------------------------
    # Load Record
    # --------------------------------------------------

    if st.button(
        "Load Record"
    ):

        record = get_record_by_id(
            selected_table,
            record_id,
            engine
        )

        st.session_state.record = record

        st.session_state.record_table = selected_table

    # --------------------------------------------------
    # Check if record exists
    # --------------------------------------------------

    if "record" not in st.session_state:

        return

    # Make sure the loaded record belongs to
    # the currently selected table

    if st.session_state.get(
        "record_table"
    ) != selected_table:

        return

    record = st.session_state.record

    if not record:

        st.error(
            "Record not found"
        )

        return

    # --------------------------------------------------
    # Get table object
    # --------------------------------------------------

    table = get_table_object(
        selected_table
    )

    if table is None:

        st.error(
            "Table not found"
        )

        return

    updated_data = {}

    st.subheader(
        "Edit Record"
    )

    # --------------------------------------------------
    # Generate form dynamically
    # --------------------------------------------------

    for column in table.columns:

        if column.primary_key:
            continue

        column_type = column.type

        # Boolean / TINYINT
        if (
            column.name.lower() == "is_active"
            or isinstance(column_type, TINYINT)
            or isinstance(column_type, Boolean)
        ):

            updated_data[column.name] = (
                st.checkbox(
                    column.name,
                    value=bool(
                        record.get(
                            column.name,
                            0
                        )
                    )
                )
            )

        # Float
        elif isinstance(
            column_type,
            Float
        ):

            updated_data[column.name] = (
                st.number_input(
                    column.name,
                    value=float(
                        record.get(
                            column.name,
                            0
                        )
                    ),
                    step=0.01
                )
            )

        # Date
        elif isinstance(
            column_type,
            Date
        ):

            updated_data[column.name] = (
                st.date_input(
                    column.name,
                    value=record.get(
                        column.name
                    )
                )
            )

        # DateTime
        elif isinstance(
            column_type,
            DateTime
        ):

            updated_data[column.name] = (
                st.date_input(
                    column.name
                )
            )

        # Email fields
        else:

            if "email" in column.name.lower():

                updated_data[column.name] = (
                    st.text_input(
                        column.name,
                        placeholder="user@example.com",
                        value=str(
                            record.get(
                                column.name,
                                ""
                            )
                        )
                    )
                )

            else:

                updated_data[column.name] = (
                    st.text_input(
                        column.name,
                        value=str(
                            record.get(
                                column.name,
                                ""
                            )
                        )
                    )
                )

    # --------------------------------------------------
    # Update Record
    # --------------------------------------------------

    if st.button(
        "Update Record"
    ):

        success, msg = update_record(
            selected_table,
            record_id,
            updated_data,
            engine
        )

        if success:

            st.success(
                msg
            )

            # Clear old record so that the user
            # can load the updated record again

            st.session_state.pop(
                "record",
                None
            )

            st.session_state.pop(
                "record_table",
                None
            )

        else:

            st.error(
                msg
            )