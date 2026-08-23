import streamlit as st

from database.connection_manager import (
    create_database_engine,
    test_connection,
    close_connection,
)

from database.reflection import (
    refresh_metadata,
    get_all_tables,
)


def render_database_connection():

    st.title("🔌 Connect Database")
    st.write("Connect the DB Admin Portal to another database.")

    # -----------------------------
    # DATABASE TYPE
    # -----------------------------
    db_type = st.selectbox(
        "Database Type",
        ["MySQL", "PostgreSQL", "SQLite"]
    )

    connection_name = st.text_input(
        "Connection Name",
        placeholder="e.g. College Database"
    )

    # -----------------------------
    # CONNECTION DETAILS
    # -----------------------------
    if db_type == "SQLite":

        database = st.text_input(
            "Database File",
            placeholder="C:/databases/college.db"
        )

        host = None
        port = None
        username = None
        password = None

    else:

        default_port = 330 if db_type == "MySQL" else 5432

        host = st.text_input("Host", value="localhost")

        port = st.number_input(
            "Port",
            min_value=1,
            max_value=65535,
            value=default_port,
        )

        username = st.text_input(
            "Username",
            value="root"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        database = st.text_input("Database Name")

    # -----------------------------
    # BUTTONS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        test_button = st.button(
            "🔍 Test Connection",
            width="stretch"
        )

    with col2:
        connect_button = st.button(
            "🔗 Connect",
            width="stretch"
        )

    # -----------------------------
    # TEST CONNECTION
    # -----------------------------
    if test_button:

        try:
            engine = create_database_engine(
                db_type=db_type,
                host=host,
                port=port,
                username=username,
                password=password,
                database=database,
            )

            success, message = test_connection(engine)

            if success:
                st.success("✅ Connection Successful")
            else:
                st.error(message)

            close_connection(engine)

        except Exception as e:
            st.error(f"Connection failed: {e}")

    # -----------------------------
    # CONNECT DATABASE
    # -----------------------------
    if connect_button:

        try:
            engine = create_database_engine(
                db_type=db_type,
                host=host,
                port=port,
                username=username,
                password=password,
                database=database,
            )

            success, message = test_connection(engine)

            if not success:
                st.error(message)
                close_connection(engine)
                return

            # Reflect schema
            refresh_metadata(engine)

            # Get tables
            tables = get_all_tables()

            # Save everything in session state
            st.session_state["active_engine"] = engine

            st.session_state["active_database"] = {
                "name": connection_name if connection_name else database,
                "type": db_type,
                "host": host,
                "port": port,
                "database": database,
                "username": username,
            }

            st.session_state["database_connected"] = True
            st.session_state["detected_tables"] = tables

            st.success(f"✅ Connected to {connection_name if connection_name else database}")

        except Exception as e:
            st.error(f"Connection failed: {e}")

    # -----------------------------
    # SHOW CONNECTED DATABASE
    # -----------------------------
    if st.session_state.get("database_connected"):

        db = st.session_state.get("active_database", {})
        tables = st.session_state.get("detected_tables", [])

        st.divider()

        st.subheader("🟢 Active Database")

        st.write(f"**Connection Name:** {db.get('name')}")
        st.write(f"**Database Type:** {db.get('type')}")
        st.write(f"**Host:** {db.get('host')}")
        st.write(f"**Port:** {db.get('port')}")
        st.write(f"**Database:** {db.get('database')}")

        st.divider()

        st.subheader("📋 Detected Tables")

        if tables:
            for table in tables:
                st.success(table)
        else:
            st.warning("No tables found in the selected database.")