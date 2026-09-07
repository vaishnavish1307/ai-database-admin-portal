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

    st.write(
        "Connect the DB Admin Portal to another database."
    )

    # --------------------------------------------------
    # DATABASE TYPE
    # --------------------------------------------------

    db_type = st.selectbox(
        "Database Type",
        [
            "MySQL",
            "PostgreSQL",
            "SQLite",
            "Snowflake",
        ],
    )

    connection_name = st.text_input(
        "Connection Name",
        placeholder="e.g. College Database",
    )

    # ==================================================
    # MYSQL / POSTGRESQL
    # ==================================================

    if db_type in ["MySQL", "PostgreSQL"]:

        if db_type == "MySQL":
            default_port = 3306
        else:
            default_port = 5432

        host = st.text_input(
            "Host",
            value="localhost",
        )

        port = st.number_input(
            "Port",
            min_value=1,
            max_value=65535,
            value=default_port,
        )

        username = st.text_input(
            "Username",
            value="root",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        database = st.text_input(
            "Database Name",
        )

        account = None
        warehouse = None
        schema = None
        role = None

    # ==================================================
    # SQLITE
    # ==================================================

    elif db_type == "SQLite":

        database = st.text_input(
            "Database File",
            placeholder="C:/databases/college.db",
        )

        host = None
        port = None
        username = None
        password = None

        account = None
        warehouse = None
        schema = None
        role = None

    # ==================================================
    # SNOWFLAKE
    # ==================================================

    else:

        st.subheader("❄️ Snowflake Connection")

        account = st.text_input(
            "Snowflake Account",
            placeholder="xy12345.ap-south-1",
        )

        username = st.text_input(
            "Username",
            placeholder="Your Snowflake username",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        warehouse = st.text_input(
            "Warehouse",
            placeholder="COMPUTE_WH",
        )

        database = st.text_input(
            "Database",
            placeholder="MY_DATABASE",
        )

        schema = st.text_input(
            "Schema",
            value="PUBLIC",
        )

        role = st.text_input(
            "Role",
            placeholder="ACCOUNTADMIN",
        )

        host = None
        port = None

    # ==================================================
    # BUTTONS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        test_button = st.button(
            "🔍 Test Connection",
            use_container_width=True,
        )

    with col2:

        connect_button = st.button(
            "🔗 Connect",
            use_container_width=True,
        )

    # ==================================================
    # TEST CONNECTION
    # ==================================================

    if test_button:

        try:

            engine = create_database_engine(
                db_type=db_type,
                host=host,
                port=port,
                username=username,
                password=password,
                database=database,
                account=account,
                warehouse=warehouse,
                schema=schema,
                role=role,
            )

            success, message = test_connection(
                engine
            )

            if success:

                st.success(
                    "✅ Connection successful"
                )

            else:

                st.error(
                    f"❌ {message}"
                )

            close_connection(engine)

        except Exception as e:

            st.error(
                f"❌ Connection failed: {str(e)}"
            )

    # ==================================================
    # CONNECT
    # ==================================================

    if connect_button:

        try:

            engine = create_database_engine(
                db_type=db_type,
                host=host,
                port=port,
                username=username,
                password=password,
                database=database,
                account=account,
                warehouse=warehouse,
                schema=schema,
                role=role,
            )

            success, message = test_connection(
                engine
            )

            if not success:

                st.error(
                    f"❌ {message}"
                )

                close_connection(engine)

                return

            # ------------------------------------------
            # REFLECT SELECTED DATABASE
            # ------------------------------------------

            refresh_metadata(engine)

            tables = get_all_tables()

            # ------------------------------------------
            # SAVE CONNECTION
            # ------------------------------------------

            st.session_state["active_engine"] = engine

            st.session_state["active_database"] = {
                "name": connection_name or database,
                "type": db_type,
                "host": host,
                "port": port,
                "database": database,
                "username": username,
                "account": account,
                "warehouse": warehouse,
                "schema": schema,
                "role": role,
            }

            st.session_state[
                "database_connected"
            ] = True

            # ------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------

            st.success(
                f"✅ Connected to "
                f"{connection_name or database}"
            )

            st.info(
                f"Detected tables: {tables}"
            )

        except Exception as e:

            st.error(
                f"❌ Connection failed: {str(e)}"
            )