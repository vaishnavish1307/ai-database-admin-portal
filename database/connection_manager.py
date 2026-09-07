from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


SUPPORTED_DATABASES = {
    "MySQL": "mysql+pymysql",
    "PostgreSQL": "postgresql+psycopg2",
    "SQLite": "sqlite",
    "Snowflake": "snowflake",
}


def create_database_engine(
    db_type: str,
    host: str = None,
    port: int = None,
    username: str = None,
    password: str = None,
    database: str = None,
    account: str = None,
    warehouse: str = None,
    schema: str = None,
    role: str = None,
):

    # --------------------------------------------------
    # MySQL
    # --------------------------------------------------

    if db_type == "MySQL":

        url = URL.create(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            host=host,
            port=int(port),
            database=database,
        )

    # --------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------

    elif db_type == "PostgreSQL":

        url = URL.create(
            drivername="postgresql+psycopg2",
            username=username,
            password=password,
            host=host,
            port=int(port),
            database=database,
            query={
            "sslmode": "require"
           },
        )

    # --------------------------------------------------
    # SQLite
    # --------------------------------------------------

    elif db_type == "SQLite":

        url = f"sqlite:///{database}"

    # --------------------------------------------------
    # Snowflake
    # --------------------------------------------------

    elif db_type == "Snowflake":

        if not account:
            raise ValueError("Snowflake account is required.")

        if not username:
            raise ValueError("Snowflake username is required.")

        if not password:
            raise ValueError("Snowflake password is required.")

        if not database:
            raise ValueError("Snowflake database is required.")

        if not warehouse:
            raise ValueError("Snowflake warehouse is required.")

        if not schema:
            raise ValueError("Snowflake schema is required.")

        query = {
            "warehouse": warehouse,
            "schema": schema,
        }

        if role:
            query["role"] = role

        url = URL.create(
            drivername="snowflake",
            username=username,
            password=password,
            host=account,
            database=database,
            query=query,
        )

    else:

        raise ValueError(
            f"Unsupported database type: {db_type}"
        )

    # --------------------------------------------------
    # Create SQLAlchemy engine
    # --------------------------------------------------

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    return engine


def test_connection(engine):

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return (
            True,
            "Connection successful"
        )

    except SQLAlchemyError as e:

        return (
            False,
            str(e)
        )


def close_connection(engine):

    if engine:
        engine.dispose()