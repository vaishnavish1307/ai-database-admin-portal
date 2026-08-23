from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


SUPPORTED_DATABASES = {
    "MySQL": "mysql+pymysql",
    "PostgreSQL": "postgresql+psycopg2",
    "SQLite": "sqlite",
}


def create_database_engine(
    db_type: str,
    host: str = None,
    port: int = None,
    username: str = None,
    password: str = None,
    database: str = None,
):
    """
    Create a SQLAlchemy engine for the selected database.
    """

    if db_type == "MySQL":

        url = URL.create(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            host=host,
            port=int(port),
            database=database,
        )

    elif db_type == "PostgreSQL":

        url = URL.create(
            drivername="postgresql+psycopg2",
            username=username,
            password=password,
            host=host,
            port=int(port),
            database=database,
        )

    elif db_type == "SQLite":

        url = f"sqlite:///{database}"

    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    return engine


def test_connection(engine):
    """
    Test whether the database connection works.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True, "Connection successful"

    except SQLAlchemyError as e:

        return False, str(e)


def close_connection(engine):
    """
    Dispose the SQLAlchemy engine.
    """

    if engine:
        engine.dispose()